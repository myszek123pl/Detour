"""Frozen four-rule validation on the independent October 15 ledger sample.

Block time has only second precision. A state/signal is assigned ts+1, the
upper end of its reported second; slot/idx/seq preserve within-second order.
No future block is used to interpolate a subsecond timestamp.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime,timezone
import hashlib,json,time
from pathlib import Path
from types import SimpleNamespace
import duckdb
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from simlib import entry,exit_sim,K0

LEVELS=[.1,.3,.5]
LATS=[1,5,30]
RULES={
    'time30_sl0.7':dict(sl=.7,tmax=30),
    'time120_sl0.7':dict(sl=.7,tmax=120),
    'br_sl0.7_tp1.25_h600':dict(sl=.7,tps=[(1.25,1.)],tmax=600),
    'trail0.2_arm1.3_h600':dict(trail=.2,arm=1.3,tmax=600),
}
WSOL='So11111111111111111111111111111111111111112'
SCHEMA=pa.schema([('mid',pa.int32()),('decision_t',pa.float64()),('lv',pa.float64()),
    ('lat',pa.int8()),('rule',pa.string()),('coverage_mode',pa.string()),
    ('filled',pa.bool_()),('r',pa.float64()),('kind',pa.string()),('n_sells',pa.int8())])


def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def prepare(data,work):
    c=duckdb.connect();c.execute("SET TimeZone='UTC';SET threads=2;SET memory_limit='2GB'")
    c.read_parquet(str(data/'data'/'*.parquet')).create_view('raw')
    c.read_parquet(str(data/'launches'/'*.parquet')).create_view('launches')
    c.read_parquet(str(data/'events'/'*.parquet')).create_view('events')
    def rows(q):
        r=c.sql(q);return [dict(zip(r.columns,x)) for x in r.fetchall()]
    counts=dict(launches=rows('select count(*) n,count(distinct mint) mints from launches')[0])
    counts['raw']=rows('select venue,failed,count(*) n from raw group by all order by venue,failed')
    counts['duplicate_trade_keys']=c.sql('''select count(*) from(
      select slot,idx,seq,failed,count(*) n from raw group by all having n>1)''').fetchall()[0][0]
    c.execute(f'''create temp table cv as select mint,ts,slot,idx,seq,side,
      r1/1e9 vs,r2/1e6 vt,sol_lamports/1e9 sol
      from raw where venue='curve' and not failed and quote_mint='{WSOL}' ''')
    counts['curve']=rows('''select count(*) rows,count(distinct mint) mints,
      count(*) filter(where vs>0 and vt>0) positive_reserves,
      count(*) filter(where abs(vs*vt/(30*1073000000.0)-1)<.005) standard_invariant
      from cv''')[0]
    c.execute('''create temp table completion as select a mint,min(ts+1) G
      from events where kind='complete' group by a''')
    c.execute('''create temp table cov as select mint,count(*) n,
      min(ts) first_ts,max(ts) last_ts,
      count(*) filter(where vs>=30 and vt>0 and abs(vs*vt/(30*1073000000.0)-1)<.005) n_valid
      from cv group by mint''')
    c.execute(f'''create temp table eligible as select
      row_number() over(order by l.slot,l.idx,l.mint)::int mid,l.mint,l.ts+1.0 L,g.G,
      v.n,v.n_valid,v.first_ts,v.last_ts
      from launches l join cov v using(mint) left join completion g using(mint)
      where l.quote_mint='{WSOL}' and l.supply=1000000000000000 and l.decimals=6
        and v.n>=2 and v.n_valid>=.99*v.n and v.first_ts-l.ts between 0 and 10''')
    counts['eligible']=rows('''select count(*) tokens,sum(n) raw_curve_rows,
      count(*) filter(where G is not null) observed_completions from eligible''')[0]
    counts['excluded_launches']=counts['launches']['n']-counts['eligible']['tokens']
    # We retain a complete token's state order until the completion event.
    # Combined curve+pool completion rows are never used as entry states;
    # they may establish G, after which pool exits remain censored here.
    c.execute('''create temp table p0 as select e.mid,c.* exclude(mint),e.L,e.G,
      max(c.ts) over(partition by e.mid order by c.slot,c.idx,c.seq
        rows between unbounded preceding and current row)+1.0 t
      from cv c join eligible e using(mint)
      where vs>=30 and vt>0 and abs(vs*vt/(30*1073000000.0)-1)<.005
        and (e.G is null or c.ts+1<=e.G)''')
    counts['clock_adjusted_rows']=c.sql('select count(*) from p0 where t<>ts+1').fetchall()[0][0]
    counts['prepared_rows']=c.sql('select count(*) from p0').fetchall()[0][0]
    c.execute(f"copy(select * from eligible order by mid) to '{(work/'tokens.parquet').as_posix()}'(format parquet)")
    c.execute(f"copy(select mid,t,vs,vt,sol,slot,idx,seq from p0 order by mid,slot,idx,seq) to '{(work/'paths.parquet').as_posix()}'(format parquet,compression zstd)")
    counts['end_exclusive_utc']=datetime(2026,10,16,tzinfo=timezone.utc).timestamp()
    (work/'preparation.json').write_text(json.dumps(counts,indent=2),encoding='utf-8')
    return counts


def summarize(work,out,config,coverage,elapsed):
    c=duckdb.connect();c.execute("SET threads=2;SET memory_limit='1GB'")
    c.read_parquet(str(work/'parts'/'part-*.parquet')).create_view('r')
    df=c.sql('''select coverage_mode,lv,lat,rule,count(*) n_signals,
      count(*) filter(where filled) n_filled,count(*) filter(where not filled) n_no_fill,
      count(r) n_resolved,count(*) filter(where filled and r is null) n_censored,
      avg(r) mean_resolved,median(r) median_resolved,
      count(*) filter(where r>0) n_wins,min(r) min_resolved,max(r) max_resolved,
      sum(r) sum_resolved,sum(case when r>0 then r else 0 end) sum_positive,
      max(case when r>0 then r else 0 end) max_positive
      from r group by all order by coverage_mode,lv,rule,lat''').df()
    df['resolved_fraction_of_fills']=df.n_resolved/df.n_filled.replace(0,np.nan)
    df['win_fraction_resolved']=df.n_wins/df.n_resolved.replace(0,np.nan)
    df['missing_minus100pct_scenario']=(df.sum_resolved.fillna(0)-df.n_censored)/df.n_filled.replace(0,np.nan)
    df['largest_winner_share_positive']=df.max_positive/df.sum_positive.replace(0,np.nan)
    df.to_csv(out/'october_summary.csv',index=False)
    paired=c.sql('''with p as(select coverage_mode,mid,lv,rule,
        max(r) filter(where lat=1) r1,max(r) filter(where lat=5) r5,max(r) filter(where lat=30) r30
      from r group by all)
      select coverage_mode,lv,rule,count(*) n_common_resolved,
        avg(r1) mean_r1,avg(r5) mean_r5,avg(r30) mean_r30,
        avg(r5-r1) mean_delta5_vs1,avg(r30-r1) mean_delta30_vs1,
        median(r1) median_r1,median(r5) median_r5,median(r30) median_r30
      from p where r1 is not null and r5 is not null and r30 is not null
      group by all order by coverage_mode,lv,rule''').df()
    paired.to_csv(out/'october_paired.csv',index=False)
    reasons=c.sql('select coverage_mode,lat,kind,count(*) n from r group by all order by coverage_mode,lat,n desc').df()
    reasons.to_csv(out/'october_reasons.csv',index=False)
    # Selection of resolved records is especially visible in these per-hour
    # counts; the day is only one independent regime, not 46k independent days.
    hourly=c.sql('''select coverage_mode,floor(decision_t/3600)::bigint hour_utc,lv,lat,rule,
      count(*) n_signals,count(*) filter(where filled) n_filled,count(r) n_resolved,
      sum(r) sum_resolved from r group by all order by coverage_mode,hour_utc,lv,lat,rule''').df()
    hourly.to_csv(out/'october_hourly.csv',index=False)
    # Descriptive uncertainty conditional on the stated coverage model.
    # Resampling cannot correct informative censoring or one-day regime risk.
    rng=np.random.default_rng(42);boot=[]
    all_hours=np.arange(int(datetime(2026,10,15,tzinfo=timezone.utc).timestamp()/3600),
                        int(datetime(2026,10,16,tzinfo=timezone.utc).timestamp()/3600))
    pick=rng.integers(0,len(all_hours),(2000,len(all_hours)))
    for key,g in hourly.groupby(['coverage_mode','lv','lat','rule']):
        gg=g.set_index('hour_utc').reindex(all_hours)
        sums=gg.sum_resolved.fillna(0).to_numpy();n=gg.n_resolved.fillna(0).to_numpy()
        den=n[pick].sum(axis=1);num=sums[pick].sum(axis=1)
        vals=num[den>0]/den[den>0]
        ci=np.quantile(vals,[.025,.975]) if len(vals) else [np.nan,np.nan]
        boot.append(dict(zip(['coverage_mode','lv','lat','rule'],key))|
          dict(resolved_mean_ci95_low=ci[0],resolved_mean_ci95_high=ci[1],
               bootstrap_replicates=2000,hour_blocks=24,nonempty_hours=int((n>0).sum())))
    import pandas as pd
    pd.DataFrame(boot).to_csv(out/'october_uncertainty.csv',index=False)
    manifest=dict(config=config,coverage=dict(coverage),elapsed_seconds=elapsed,
      generated_at=datetime.now(timezone.utc).isoformat(),
      outcome_rows=int(df.n_signals.sum()),
      caveats=[
       'One held-out ledger day, four rules fixed before reading outcome results. Not proof of stability across months.',
       'Quality selection uses full paths retrospectively and cannot be a live entry filter.',
       'trade_supported censors absence of supported later states; resolved-only means can be selection-biased.',
       'ledger_day_coverage is a separate assumption: complete reported ledger coverage implies unchanged curve state between trades until midnight, for non-graduates. It disables the stale-state limit; missing events or Mayhem would invalidate it.',
       'Graduation exits are censored_pool; pool pre-trade rows are not naively treated as post-trade states.',
       'Block time upper-second convention adds up to one second of signal delay; actual block-time uncertainty remains.',
       'Costs are declared assumptions. Observed failed attempts do not estimate our own fill probability.',
       'Additive own-impact replay holds the other flow fixed, not an exchange execution guarantee.',
       'Paired latency rows require all three outcomes resolved and are a selected common-support subset.'
       ,'Intervals are descriptive 2000-replicate UTC-hour block bootstraps (seed42), conditional on the coverage model, with no multiple-comparison correction and only one observed day.'
      ])
    (out/'october_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('SUMMARY',len(df),'groups',manifest['outcome_rows'],'rows',round(elapsed,1),'s',flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('scratch',type=Path);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--limit-tokens',type=int);p.add_argument('--tag',default='october_v2')
    p.add_argument('--size-sol',type=float,default=1.);p.add_argument('--fee',type=float,default=.0125)
    p.add_argument('--tip-sol',type=float,default=.30/70);p.add_argument('--chunk-tokens',type=int,default=500)
    a=p.parse_args();scratch=a.scratch.resolve();data=scratch/'datasets'/'pumpdatafun'
    work=scratch/'work'/a.tag;work.mkdir(parents=True,exist_ok=True);(work/'parts').mkdir(exist_ok=True)
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    config=dict(tag=a.tag,levels=LEVELS,latencies=LATS,rules=RULES,size_sol=a.size_sol,fee=a.fee,tip_sol=a.tip_sol,
      limit_tokens=a.limit_tokens,simlib_sha256=sha(Path(__file__).with_name('simlib.py')),
      runner_sha256=sha(__file__),provenance=json.loads((data/'validation_download_manifest.json').read_text()),
      clock='max_observed_block_ts_in_chain_order + 1 second; no future anchors')
    cfg=work/'config.json'
    if cfg.exists() and json.loads(cfg.read_text())!=config:raise RuntimeError('configuration changed; use a new tag')
    cfg.write_text(json.dumps(config,indent=2),encoding='utf-8')
    start=time.monotonic()
    prep=work/'preparation.json'
    counts=json.loads(prep.read_text()) if prep.exists() else prepare(data,work)
    (out/'october_preparation.json').write_text(json.dumps(counts,indent=2),encoding='utf-8')
    print('PREPARED',counts['eligible'],flush=True)
    tk=pq.read_table(work/'tokens.parquet').to_pandas()
    paths=pq.read_table(work/'paths.parquet').to_pandas()
    if a.limit_tokens:
        tk=tk.iloc[np.linspace(0,len(tk)-1,min(a.limit_tokens,len(tk)),dtype=int)]
        paths=paths[paths.mid.isin(tk.mid)].copy()
    mids=paths.mid.to_numpy();u,st=np.unique(mids,return_index=True);ends=np.r_[st[1:],len(paths)]
    metadata=tk.set_index('mid');T=paths.t.to_numpy(dtype='float64');VS=paths.vs.to_numpy(dtype='float64');VT=paths.vt.to_numpy(dtype='float64')
    ranges=list(zip(u,st,ends));del paths
    pp=SimpleNamespace(pg={},pg_reserves={});coverage=Counter()
    day_end=counts['end_exclusive_utc']
    print('READY',len(ranges),'tokens',len(T),'states',flush=True)
    for begin in range(0,len(ranges),a.chunk_tokens):
        target=work/'parts'/f'part-{begin//a.chunk_tokens:05d}.parquet';inf=target.with_suffix('.json')
        if target.exists() and inf.exists():coverage.update(json.loads(inf.read_text()));continue
        records=[];cnt=Counter()
        for mid,s,e in ranges[begin:begin+a.chunk_tokens]:
            meta=metadata.loc[mid];g=None if np.isnan(meta.G) else float(meta.G)
            t=T[s:e];vs=VS[s:e];vt=VT[s:e];prog=(vs-30)/85
            for lv in LEVELS:
                hits=np.flatnonzero(prog>=lv)
                if not len(hits):cnt[f'no_crossing_{lv}']+=1;continue
                i=int(hits[0])
                if i==0 and prog[0]>lv+.03:cnt[f'left_truncated_{lv}']+=1;continue
                cnt[f'signals_{lv}']+=1;decision=float(t[i])
                for mode in ['trade_supported','ledger_day_coverage']:
                    tt,vv,bb=t,vs,vt
                    if mode=='ledger_day_coverage' and g is None and t[-1]<day_end:
                        tt=np.r_[t,day_end];vv=np.r_[vs,vs[-1]];bb=np.r_[vt,vt[-1]]
                    d=dict(t=tt,vs=vv,vt=bb,G=g,grad=g is not None)
                    state_age=30. if mode=='trade_supported' else None
                    for lat in LATS:
                        en=entry(d,i,lat,a.size_sol,a.fee,a.tip_sol,max_state_age=state_age,fee_model='on_top')
                        for name,spec in RULES.items():
                            if en is None:r,kind,ntx=None,'no_fill',0
                            else:
                                value,kind,ntx=exit_sim(pp,int(mid),d,en,dict(spec,max_state_age=state_age),lat,a.fee,a.tip_sol,a.size_sol)
                                r=float(value) if np.isfinite(value) else None
                            records.append(dict(mid=int(mid),decision_t=decision,lv=lv,lat=lat,rule=name,
                              coverage_mode=mode,filled=en is not None,r=r,kind=kind,n_sells=ntx))
        pq.write_table(pa.Table.from_pylist(records,schema=SCHEMA),target,compression='zstd')
        inf.write_text(json.dumps(dict(cnt)),encoding='utf-8');coverage.update(cnt)
        print('CHECKPOINT',min(begin+a.chunk_tokens,len(ranges)),'/',len(ranges),'rows',len(records),'seconds',round(time.monotonic()-start,1),flush=True)
    summarize(work,out,dict(config,n_selected_tokens=len(tk)),coverage,time.monotonic()-start)


if __name__=='__main__':main()
