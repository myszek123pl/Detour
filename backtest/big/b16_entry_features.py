"""Point-in-time entry features and fixed temporal tests of collector labels.

python b16_entry_features.py SCRATCH --out-dir backtest/out/big
Local per-event features stay under SCRATCH/work; only summaries enter Git.
No token-level future snapshot measurements are used as predictors.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import time

os.environ.setdefault('OMP_NUM_THREADS', '1')

import duckdb
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, brier_score_loss,
                             log_loss, roc_auc_score)
from threadpoolctl import threadpool_limits

LEVELS = [.05, .10, .20, .30, .40, .50, .60]
SPLIT = pd.Timestamp('2026-07-08T00:00:00Z').timestamp()
TEST_START = SPLIT + 12*3600
LABEL_HORIZON = 24*3600
GAPS = [(pd.Timestamp(d, tz='UTC').timestamp(),
         pd.Timestamp(d, tz='UTC').timestamp()+86400)
        for d in ['2026-07-03', '2026-07-12']]
BASE = ['lv', 'progress']
PACE = BASE + ['age', 'n_tr', 'speed', 'progress_delta60']
EXTENDED = BASE + ['age', 'first_gap', 'n_tr', 'uniq_buyers', 'buy_ratio_all',
    'buy_ratio60', 'n60', 'netflow60', 'buy_sol_ratio60', 'top1_buy_sol',
    'top3_buy_sol', 'hhi_buy_sol', 'missing_sol_share', 'cr_sells',
    'cr_sell_sol', 'cr_buy_sol', 'cr_prev_launch', 'cr_prev_grad_pit',
    'progress_delta60', 'drawdown_from_peak', 'speed', 'snipers3']


def _jsonable(v):
    if isinstance(v, dict): return {k: _jsonable(x) for k,x in v.items()}
    if isinstance(v, list): return [_jsonable(x) for x in v]
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, (np.floating, float)): return float(v) if np.isfinite(v) else None
    return v


def _features(g, r, counts):
    t = g.t.to_numpy(float)
    # Same curve truncation/crossing convention as the replay runner.
    end = len(t)
    done = np.flatnonzero(g.vs.to_numpy() >= 114.5)
    if len(done): end = int(done[0])+1
    elif np.isfinite(r.G): end = int(np.searchsorted(t, r.G, side='right'))
    if end < 2:
        counts['too_few_pregraduation_states'] += 1
        return []
    t = t[:end]
    progress = (g.vs.to_numpy(float)[:end]-30.)/85.
    b = g.b.to_numpy(bool)[:end]
    sol = g.sol.to_numpy(float)[:end]
    wid = g.wid.to_numpy(np.int64)[:end]
    good = (~g.is_sys.to_numpy(bool)[:end]) & (wid >= 0)
    out = []
    for lv in LEVELS:
        hit = np.flatnonzero(progress >= lv)
        if not len(hit): continue
        i = int(hit[0]); ti = t[i]
        if i == 0 and progress[0] > lv+.03:
            counts['overshot_first_state_events'] += 1
            continue
        if np.isfinite(r.G) and ti >= r.G:
            counts['already_provider_graduated_events'] += 1
            continue
        # All masks end at decision index. The complete path is never read
        # to construct a feature, only to locate the first crossing.
        tt, bb, ss, ww, ok = t[:i+1], b[:i+1], sol[:i+1], wid[:i+1], good[:i+1]
        buy = ok & bb
        vbuy = buy & np.isfinite(ss)
        total_b = ss[vbuy].sum()
        if total_b > 0 and np.isfinite(ss[buy]).all():
            _, ix = np.unique(ww[vbuy], return_inverse=True)
            weights = np.sort(np.bincount(ix, weights=ss[vbuy]))[::-1]/total_b
            top1, top3, hhi = weights[0], weights[:3].sum(), np.square(weights).sum()
        else: top1 = top3 = hhi = np.nan
        w60 = ok & (tt > ti-60)
        complete60 = bool(w60.any() and np.isfinite(ss[w60]).all())
        vol60 = ss[w60].sum() if complete60 else np.nan
        cr = ok & (ww == r.creator_wid)
        def sum_complete(mask):
            return float(ss[mask].sum()) if np.isfinite(ss[mask]).all() else np.nan
        k60 = int(np.searchsorted(tt, ti-60, side='right'))-1
        f = dict(mid=int(r.mid), lv=float(lv), decision_t=float(ti), L=float(r.L),
            G=float(r.G), age=float(ti-r.L), first_gap=float(t[0]-r.L),
            progress=float(progress[i]), n_tr=int(i+1),
            uniq_buyers=int(len(np.unique(ww[buy]))),
            buy_ratio_all=float(bb[ok].mean()) if ok.any() else np.nan,
            buy_ratio60=float(bb[w60].mean()) if w60.any() else np.nan,
            n60=int(w60.sum()),
            netflow60=float(np.where(bb[w60], ss[w60], -ss[w60]).sum()) if complete60 else np.nan,
            buy_sol_ratio60=float(ss[w60 & bb].sum()/vol60) if vol60>0 else np.nan,
            top1_buy_sol=float(top1), top3_buy_sol=float(top3), hhi_buy_sol=float(hhi),
            missing_sol_share=float((~np.isfinite(ss[ok])).mean()) if ok.any() else np.nan,
            cr_sells=int((cr & ~bb).sum()), cr_sell_sol=sum_complete(cr & ~bb),
            cr_buy_sol=sum_complete(cr & bb),
            cr_prev_launch=float(r.cr_prev_launch),
            cr_prev_grad_pit=float(r.cr_prev_grad_pit),
            progress_delta60=float(progress[i]-(progress[k60] if k60>=0 else 0.)),
            drawdown_from_peak=float(progress[:i+1].max()-progress[i]),
            speed=float(progress[i]/max(ti-r.L,1.)),
            snipers3=float(len(np.unique(ww[buy & (tt<=r.L+3) & (ww!=r.creator_wid)]))) if t[0]-r.L<=1 else np.nan,
            provider_grad_in_corpus=int(np.isfinite(r.G)),
            provider_grad24=int(np.isfinite(r.G) and ti < r.G <= ti+LABEL_HORIZON),
            planned_tracking_end=float(r.L+48*3600))
        out.append(f)
    counts['tokens_processed'] += 1
    return out


def build(scratch):
    work = scratch/'work'
    tk = pd.read_parquet(work/'tok_jocry2.parquet').set_index('mid', drop=False)
    counts = Counter(tokens_in_quality_cohort=len(tk))
    output = work/'entry_features.parquet'
    writer = None; buf = []; carry = None; started = time.monotonic(); last_log = started
    def flush():
        nonlocal writer, buf
        if not buf: return
        table = pa.Table.from_pandas(pd.DataFrame(buf), preserve_index=False)
        if writer is None: writer = pq.ParquetWriter(output, table.schema, compression='zstd')
        writer.write_table(table)
        counts['events_written'] += len(buf)
        buf = []
    try:
        for batch in pq.ParquetFile(work/'paths_jocry.parquet').iter_batches(batch_size=500000):
            df = batch.to_pandas()
            if carry is not None: df = pd.concat([carry, df], ignore_index=True)
            last_mid = int(df.mid.iloc[-1])
            carry = df[df.mid==last_mid].copy()
            df = df[df.mid!=last_mid]
            for mid,g in df.groupby('mid', sort=False):
                buf.extend(_features(g, tk.loc[mid], counts))
                if len(buf)>=20000: flush()
            if time.monotonic()-last_log>20:
                print('FEATURES',dict(counts),'seconds',round(time.monotonic()-started),flush=True)
                last_log = time.monotonic()
        if carry is not None:
            buf.extend(_features(carry, tk.loc[int(carry.mid.iloc[0])], counts))
        flush()
    finally:
        if writer is not None: writer.close()
    counts['seconds'] = round(time.monotonic()-started, 2)
    print('FEATURES DONE',dict(counts),flush=True)
    return output, dict(counts)


def metrics(y, p):
    out = dict(n=len(y), positives=int(np.sum(y)), rate=float(np.mean(y)),
        mean_prediction=float(np.mean(p)), brier=float(brier_score_loss(y,p)),
        log_loss=float(log_loss(y,p,labels=[0,1])))
    if len(np.unique(y))==2:
        out.update(auc=float(roc_auc_score(y,p)), ap=float(average_precision_score(y,p)))
        z = np.log(np.clip(p,1e-9,1-1e-9)/(1-np.clip(p,1e-9,1-1e-9)))[:,None]
        cal = LogisticRegression(C=1e6, max_iter=500).fit(z,y)
        out.update(calibration_intercept=float(cal.intercept_[0]), calibration_slope=float(cal.coef_[0,0]))
    return out


def evaluate(scratch, features, out_dir, counts):
    d = pd.read_parquet(features)
    raw_end = duckdb.connect().sql(f"select max(epoch(event_time)) from '{(scratch/'datasets/jocry/trades/*.parquet').as_posix()}'").fetchall()[0][0]
    horizon_end = d.decision_t+LABEL_HORIZON
    mature = (horizon_end<=raw_end) & (horizon_end<=d.planned_tracking_end)
    gap_free = pd.Series(True,index=d.index)
    for lo,hi in GAPS:
        gap_free &= ~((d.decision_t<hi) & (horizon_end>lo))
    train = (d.L<SPLIT)&(horizon_end<=SPLIT)&mature&gap_free
    test = (d.L>=TEST_START)&(d.decision_t>=TEST_START)&mature&gap_free
    d['split'] = np.where(train,'train',np.where(test,'test','excluded'))
    # Persist maturity flags for downstream PnL joins without redefining the
    # replay's own fill/censoring population.
    d['label24_mature'] = mature
    d['label24_gap_free'] = gap_free
    d.to_parquet(features,index=False,compression='zstd')
    report = dict(generated_at=datetime.now(timezone.utc).isoformat(), counts=counts,
        target='Provider-reported graduation within 24h of decision, NOT on-chain success or profitability.',
        horizon_seconds=LABEL_HORIZON, split_cutoff_utc='2026-07-08T00:00:00Z',
        test_start_utc='2026-07-08T12:00:00Z',
        exclusion_counts=dict(label_not_mature=int((~mature).sum()), label_window_intersects_gap=int((~gap_free).sum()),
            train_events=int(train.sum()),test_events=int(test.sum()),
            train_tokens=int(d.loc[train,'mid'].nunique()),test_tokens=int(d.loc[test,'mid'].nunique())),
        features=dict(baseline=BASE,curve_and_pace=PACE,extended=EXTENDED),models={},rule_associations=[],
        provenance=json.loads((scratch/'datasets/jocry/download_manifest.json').read_text(encoding='utf-8'))['revision'],
        caveats=['Retrospective path-quality cohort is not a deployable live entry filter.',
            'Negative collector labels are not independently confirmed failed tokens.',
            'Decision order is event_time/id, not on-chain slot/index.',
            'Repeated levels of the same token are correlated; splits keep tokens separate.',
            'Only a few calendar days are available in the final test after maturity and gap exclusions.',
            'Historical creator features are restricted to earlier corpus launches in a 30-day lookback; left truncation varies over the corpus.',
            'No fitted model or graduation lift is claimed as a positive net trading return.'])
    rate_table = d.groupby(['split','lv'],observed=True).agg(events=('mid','size'),tokens=('mid','nunique'),
        provider_grad24_rate=('provider_grad24','mean'),provider_any_grad_rate=('provider_grad_in_corpus','mean'),
        median_age=('age','median'),missing_sol_share_mean=('missing_sol_share','mean')).reset_index()
    rate_table.to_csv(out_dir/'entry_features_rates.csv',index=False)
    missing = d[EXTENDED].isna().mean().to_dict()
    report['missing_feature_fraction'] = missing
    pred = d[['mid','lv','decision_t','split','provider_grad24']].copy()
    tr,te=d[train],d[test]
    ytr,yte=tr.provider_grad24.to_numpy(),te.provider_grad24.to_numpy()
    # Same estimator capacity, different information sets; no tuning on test.
    with threadpool_limits(limits=1):
        for name,cols in [('curve_only',BASE),('curve_and_pace',PACE),('behavior_extended',EXTENDED)]:
            mdl=HistGradientBoostingClassifier(max_iter=120,max_depth=3,min_samples_leaf=200,
                learning_rate=.06,l2_regularization=5,random_state=20261121)
            mdl.fit(tr[cols],ytr)
            ptr=mdl.predict_proba(tr[cols])[:,1]; pte=mdl.predict_proba(te[cols])[:,1]
            result=dict(train=metrics(ytr,ptr),test=metrics(yte,pte),frozen_train_thresholds=[])
            result['test_by_level']=[]
            result['frozen_thresholds_within_level']=[]
            for lv in LEVELS:
                tr_lv=tr.lv.to_numpy()==lv; te_lv=te.lv.to_numpy()==lv
                if not te_lv.any() or not tr_lv.any(): continue
                result['test_by_level'].append(dict(lv=lv,**metrics(yte[te_lv],pte[te_lv])))
                for q in [.90,.95,.99]:
                    threshold=float(np.quantile(ptr[tr_lv],q))
                    keep=te_lv&(pte>=threshold)
                    denom=float(yte[te_lv].mean())
                    result['frozen_thresholds_within_level'].append(dict(lv=lv,train_quantile=q,
                        threshold=threshold,test_n=int(keep.sum()),
                        test_coverage_within_level=float(keep.sum()/te_lv.sum()),
                        test_label_rate=float(yte[keep].mean()) if keep.any() else np.nan,
                        test_lift=float(yte[keep].mean()/denom) if keep.any() and denom>0 else np.nan))
            for q in [.90,.95,.99]:
                threshold=float(np.quantile(ptr,q))
                keep=pte>=threshold
                result['frozen_train_thresholds'].append(dict(train_quantile=q,threshold=threshold,
                    test_n=int(keep.sum()),test_coverage=float(keep.mean()),
                    test_label_rate=float(yte[keep].mean()) if keep.any() else np.nan,
                    test_lift=float(yte[keep].mean()/yte.mean()) if keep.any() and yte.mean()>0 else np.nan))
            # Day-block bootstrap describes calendar fragility, not independent
            # token confidence intervals. Avoid pretending a 4-day test is large.
            # Group by launch day so all level-signals of one token remain
            # in the same resampled block even if decisions cross midnight.
            days=np.floor(te.L.to_numpy()/86400).astype(int)
            unique=np.unique(days); rng=np.random.default_rng(20261121)
            aucs=[];aps=[]
            for _ in range(200):
                chosen=rng.choice(unique,len(unique),replace=True)
                ix=np.concatenate([np.flatnonzero(days==day) for day in chosen])
                if len(np.unique(yte[ix]))<2: continue
                aucs.append(roc_auc_score(yte[ix],pte[ix])); aps.append(average_precision_score(yte[ix],pte[ix]))
            result['test_calendar_blocks']=len(unique)
            result['day_bootstrap_auc_95']=np.quantile(aucs,[.025,.975]).tolist() if aucs else None
            result['day_bootstrap_ap_95']=np.quantile(aps,[.025,.975]).tolist() if aps else None
            report['models'][name]=result
            pred.loc[test,f'p_{name}']=pte
            pred.loc[train,f'p_{name}']=ptr
            print('MODEL',name,json.dumps(_jsonable({'train':result['train'],
                'test':result['test'],'test_calendar_blocks':result['test_calendar_blocks'],
                'day_bootstrap_auc_95':result['day_bootstrap_auc_95']})),flush=True)
    pred.to_parquet(scratch/'work/entry_features_predictions.parquet',index=False,compression='zstd')
    rules={'all':pd.Series(True,index=d.index),'age_gt600':d.age>600,
        'creator_has_sold':d.cr_sells>=1,'buy_ratio60_ge80pct':d.buy_ratio60>=.8,
        'unique_buyers_ge10':d.uniq_buyers>=10,'top3_buy_sol_lt70pct':d.top3_buy_sol<.7,
        'creator_prior_grad_ge1':d.cr_prev_grad_pit>=1,'netflow60_positive':d.netflow60>0,
        'buy80_10buyers_no_creator_sale':(d.buy_ratio60>=.8)&(d.uniq_buyers>=10)&(d.cr_sells==0)}
    for name,mask in rules.items():
        for sp,scope in [('train',train),('test',test)]:
            g=d[mask&scope]
            report['rule_associations'].append(dict(rule=name,split=sp,n=len(g),tokens=g.mid.nunique(),
                provider_grad24_rate=g.provider_grad24.mean(),median_age=g.age.median()))
    report['by_test_day']=d[test].assign(day=pd.to_datetime(d.loc[test,'decision_t'],unit='s',utc=True).dt.strftime('%Y-%m-%d')).groupby('day').agg(n=('mid','size'),tokens=('mid','nunique'),positives=('provider_grad24','sum')).reset_index().to_dict('records')
    with (out_dir/'entry_features_summary.json').open('w',encoding='utf-8') as f:
        json.dump(_jsonable(report),f,indent=2,ensure_ascii=False,allow_nan=False)
    print('EVALUATION DONE',report['exclusion_counts'],flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('scratch',type=Path);ap.add_argument('--out-dir',type=Path,required=True)
    ap.add_argument('--reuse-features',action='store_true')
    a=ap.parse_args();a.scratch=a.scratch.resolve();a.out_dir.mkdir(parents=True,exist_ok=True)
    if a.reuse_features:
        p=a.scratch/'work/entry_features.parquet'
        prior=a.out_dir/'entry_features_summary.json'
        counts=json.loads(prior.read_text(encoding='utf-8'))['counts'] if prior.exists() else {
            'tokens_in_quality_cohort':len(pd.read_parquet(a.scratch/'work/tok_jocry2.parquet',columns=['mid'])),
            'events_written':pq.ParquetFile(p).metadata.num_rows}
        counts['reused_feature_table']=True
    else: p,counts=build(a.scratch)
    evaluate(a.scratch,p,a.out_dir,counts)
