"""Frozen training-only selection and conditional PnL diagnostics.

Run only after a completed b15_replay.py manifest for all 219327 tokens.
Raw outcomes stay outside Git. This does not identify PnL of censored trades.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import duckdb
import numpy as np
import pandas as pd

POLICY = {
 'frozen_at_utc': '2026-11-21T16:26:22Z',
 'selection_latency': 1, 'minimum_fills': 300, 'minimum_resolved': 300,
 'minimum_resolved_fraction': .90,
 'score': 'largest training-only mean of resolved returns; ties by lv then rule_id',
 'training_purge': 'decision_t + maximum_horizon + 2*maximum_latency <= train_end',
 'bootstrap_unit': 'UTC decision day', 'bootstrap_replicates': 2000, 'seed': 20261121,
 'filters_frozen': ['all','creator_no_sell','buyers_ge8','top3_lt0.7',
                    'buy_ratio60_ge0.6','complete_observed_sol','combined'],
 'censor_sensitivity': 'Assign each filled-but-unresolved return -1; scenario, NOT a lower bound.'
}


def clean(x):
    if isinstance(x,dict): return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [clean(v) for v in x]
    if isinstance(x,(np.integer,)): return int(x)
    if isinstance(x,(np.floating,float)): return float(x) if np.isfinite(x) else None
    if isinstance(x,(np.bool_,)): return bool(x)
    return x


def block_ci(g):
    a=g[g.r.notna()].copy()
    if a.empty: return dict(ci95=None,n_days=0,positive_days=0)
    a['day']=np.floor(a.decision_t/86400).astype('int64')
    z=a.groupby('day').r.agg(['sum','count'])
    n=len(z); pos=int((z['sum']>0).sum())
    if n<2: return dict(ci95=None,n_days=n,positive_days=pos)
    rng=np.random.default_rng(POLICY['seed'])
    pick=rng.integers(0,n,(POLICY['bootstrap_replicates'],n))
    boot=z['sum'].to_numpy()[pick].sum(1)/z['count'].to_numpy()[pick].sum(1)
    return dict(ci95=np.quantile(boot,[.025,.975]).tolist(),n_days=n,positive_days=pos,
                caution='Conditional on observed exits; not corrected for selection or informative censoring.')


def metrics(g):
    r=g.r.dropna().astype(float); n=len(g); filled=int(g.filled.sum()); resolved=len(r)
    positive=r[r>0].sort_values(ascending=False)
    removed={}
    for k in (1,5):
        drop=positive.head(k).sum(); count=len(positive.head(k))
        removed[f'mean_without_top{k}_positive']=(r.sum()-drop)/(resolved-count) if resolved>count else None
        removed[f'top{k}_share_positive']=drop/positive.sum() if positive.sum()>0 else None
    return clean(dict(n_signals=n,n_filled=filled,n_no_fill=n-filled,n_resolved=resolved,
      n_censored=filled-resolved,coverage=resolved/filled if filled else None,
      mean_resolved=r.mean() if resolved else None,median_resolved=r.median() if resolved else None,
      wins=int((r>0).sum()),win_fraction_resolved=(r>0).mean() if resolved else None,
      missing_minus100pct_scenario=(r.sum()-(filled-resolved))/filled if filled else None,
      **removed,**block_ci(g)))


def paired(g):
    # Condition on resolved positions at every latency; never imply this is the
    # population latency effect, because support itself is outcome dependent.
    if g.empty: return dict(n_common=0)
    z=g.pivot(index=['mid','lv','rule_id'],columns='lat',values='r')
    if not {1,5,30}.issubset(z.columns): return dict(n_common=0)
    z=z[[1,5,30]].dropna()
    out=dict(n_common=len(z),means={str(k):float(z[k].mean()) for k in [1,5,30]},
             mean_delta5_minus1=float((z[5]-z[1]).mean()),
             mean_delta30_minus1=float((z[30]-z[1]).mean()),
             interpretation='Same token, level and rule; conditional common resolved support, not a population effect.')
    return clean(out)


def write_report(result, filters_out):
    dest=Path(__file__).resolve().parents[2]/'research_notes'/'Trading memecoinów backtest'/'40_trading_rules_review.md'
    existing=dest.read_text(encoding='utf-8')
    existing=existing.split('## Stan obliczeń')[0].split('## Wyniki pełnego replay')[0].rstrip()
    pct=lambda v:'brak' if v is None else f'{100*v:.2f}%'
    lines=['','## Wyniki pełnego replay','',
      f"Zweryfikowano wszystkie **219 327 tokenów** i **{result['full_replay_outcomes']:,}** wyników scenariuszy. To warianty reguł i opóźnień, nie niezależne transakcje portfela.",
      '',f"Bramkę liczebności i pokrycia przeszło **{result['n_eligible']} z {result['n_candidates']}** par poziom–wyjście na treningu."]
    if result['selected'] is None:
        lines+=['','**Nie ma reguły zakwalifikowanej przez zamrożoną bramkę pokrycia.** Najlepsza średnia wśród widocznych wyjść poniżej jest diagnostyką, nie zamiennikiem tej bramki.']
    for name,r in result['reviews'].items():
        lines+=['',f"### {name}: {r['rule']}, poziom {100*r['lv']:g}%",'',
         '| Okres i opóźnienie | Sygnały | Wejścia | Rozstrzygnięte | Nieznane | Średnia widocznych | Scenariusz braków −100% |',
         '|---|---:|---:|---:|---:|---:|---:|']
        for key,m in r['slices'].items():
            lines.append(f"| {key} | {m['n_signals']} | {m['n_filled']} | {m['n_resolved']} | {m['n_censored']} | {pct(m['mean_resolved'])} | {pct(m['missing_minus100pct_scenario'])} |")
        t=r['slices']['test_lat1'];ci=t['ci95']
        lines+=['',f"Test 1 s: {t['n_days']} dni z rozstrzygniętymi pozycjami, w tym {t['positive_days']} dodatnich. Warunkowy bootstrap dni: "+(f"[{pct(ci[0])}; {pct(ci[1])}]." if ci else 'brak przedziału przy zbyt małej liczbie dni.'),
          f"Średnia po usunięciu największego dodatniego wyniku: {pct(t['mean_without_top1_positive'])}; po pięciu: {pct(t['mean_without_top5_positive'])}."]
        pp=r['paired']['test']
        if pp['n_common']:
            lines+=[f"Na wspólnej próbie {pp['n_common']} rozstrzygniętych zdarzeń średnie dla 1/5/30 s wynoszą odpowiednio "+'/'.join(pct(pp['means'][str(k)]) for k in [1,5,30])+'. To wynik warunkowej wspólnej próby.']
    lines+=['','### Filtry wejścia','',
      'Wyniki zamrożonych filtrów są w `strategy_review_filters.csv`. Każdy ma osobno liczebność, brak cech, brak wykonania i cenzurowanie. Nie wybieramy najlepszego filtra po wyniku testu. Predykcje modelu graduacji nie są filtrem live: obecny plik ma je wyłącznie dla retrospektywnie kwalifikowanych okien etykiet.',
      '', '### Decyzja badawcza','',
      'Dodatnia średnia widocznych wyjść i jej bootstrap nie identyfikują wyniku wszystkich pozycji. Scenariusz −100% dla nierozstrzygniętych jest analizą wrażliwości, nie ścisłą dolną granicą. Retrospektywna selekcja jakości kohorty dodatkowo uniemożliwia proste potraktowanie jej jako filtra działającego przy starcie tokena.',
      '', 'Październikowy test wcześniej ustalonych reguł nie potwierdził dodatniej przewagi w modelu pokrycia całego dnia. Żadnej reguły nie kwalifikujemy tutaj do handlu realnym kapitałem. Dalszy kandydat wymaga prospektywnego paper replay z pełnym rejestrem wszystkich sygnałów, prób i zamknięć; kolejnego progu nie należy dobierać na tym samym teście.',
      '', 'Reprodukcja: `python backtest/big/b20_strategy_review.py SCRATCH --out backtest/out/big`. Manifest i checkpointy muszą potwierdzać pełną kohortę.']
    dest.write_text(existing+'\n'+'\n'.join(lines)+'\n',encoding='utf-8')


def run(scratch, out, tag):
    scratch=Path(scratch).resolve();out=Path(out);out.mkdir(parents=True,exist_ok=True)
    manifest_path=out/f'{tag}_manifest.json'
    if not manifest_path.exists(): raise RuntimeError('Full replay manifest is not present yet')
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    cfg=manifest['config'];folder=scratch/'work'/tag
    if cfg.get('limit_tokens') is not None or cfg.get('n_selected_tokens')!=219327:
        raise RuntimeError('Refusing partial or smoke replay')
    infos=[json.loads(p.read_text()) for p in (folder/'parts').glob('part-*.json')]
    if sum(x['n_tokens'] for x in infos)!=219327: raise RuntimeError('Checkpoint token count mismatch')
    files=sorted((folder/'parts').glob('part-*.parquet'))
    c=duckdb.connect();c.execute("SET memory_limit='2GB'; SET threads=4")
    c.read_parquet([str(p) for p in files]).create_view('o')
    if c.sql('select count(*) from o').fetchall()[0][0]!=manifest['outcome_rows']:
        raise RuntimeError('Outcome count mismatch')
    train_end=float(cfg['train_end_utc'])-float(cfg['horizon_seconds'])-2*max(cfg['latencies'])
    selection=c.sql(f'''select lv,rule_id,count(*) n_signals,
      count(*) filter(where filled) n_filled,count(r) n_resolved,avg(r) mean_resolved,
      sum(r) sum_resolved from o where split='train' and lat=1 and decision_t<={train_end}
      group by lv,rule_id''').df()
    selection['coverage']=selection.n_resolved/selection.n_filled.replace(0,np.nan)
    selection['eligible']=(selection.n_filled>=300)&(selection.n_resolved>=300)&(selection.coverage>=.9)
    selection['rule']=selection.rule_id.map(dict(enumerate(cfg['rules'])))
    selection=selection.sort_values(['mean_resolved','lv','rule_id'],ascending=[False,True,True])
    selection.to_csv(out/'strategy_review_training_selection.csv',index=False)
    eligible=selection[selection.eligible]
    selected=eligible.iloc[0].to_dict() if len(eligible) else None
    diag=selection[selection.n_resolved>=300]
    diagnostic=diag.iloc[0].to_dict() if len(diag) else None
    result=dict(policy=POLICY,generated_at=datetime.now(timezone.utc).isoformat(),
        replay_manifest_sha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        full_replay_outcomes=manifest['outcome_rows'],n_candidates=len(selection),
        n_eligible=len(eligible),selected=clean(selected),
        highest_train_resolved_only_diagnostic=clean(diagnostic),reviews={})
    # A failing quality gate must not silently become the deployed choice.
    choices={}
    if selected is not None: choices['coverage_gate_training_selection']=selected
    if diagnostic is not None: choices['resolved_only_diagnostic_NOT_qualified']=diagnostic
    features=scratch/'work'/'entry_features.parquet'
    c.read_parquet(str(features)).create_view('features')
    duplicates=c.sql('select count(*) from (select mid,lv from features group by mid,lv having count(*)>1)').fetchall()[0][0]
    if duplicates: raise RuntimeError('Non-unique feature keys')
    details=[];filters_out=[]
    for label,choice in choices.items():
        rid=int(choice['rule_id']);lv=float(choice['lv'])
        raw=c.sql(f'''select o.*,
          f.decision_t feature_decision_t,f.cr_sells,f.uniq_buyers,
          f.top3_buy_sol,f.buy_ratio60,f.missing_sol_share
          from o left join features f on o.mid=f.mid and o.lv=f.lv
          where o.rule_id={rid} and o.lv={lv}''').df()
        if raw.feature_decision_t.notna().any() and not np.allclose(
            raw.loc[raw.feature_decision_t.notna(),'decision_t'],
            raw.loc[raw.feature_decision_t.notna(),'feature_decision_t'],rtol=0,atol=1e-6):
            raise RuntimeError('Decision time mismatch in feature join')
        review=dict(lv=lv,rule_id=rid,rule=choice['rule'],slices={},paired={})
        for sp in ['train','test']:
            sub=raw[raw.split==sp]
            if sp=='train': sub=sub[sub.decision_t<=train_end]
            for latency in [1,5,30]:
                met=metrics(sub[sub.lat==latency]);review['slices'][f'{sp}_lat{latency}']=met
                details.append(dict(choice=label,split=sp,lat=latency,**{k:v for k,v in met.items() if not isinstance(v,(list,dict))}))
            review['paired'][sp]=paired(sub)
            # Filters frozen independently of test results, with unknown values
            # excluded from the filtered branch and retained in its denominator.
            g=sub[sub.lat==1]
            fs={'all':pd.Series(True,index=g.index),
                'creator_no_sell':g.cr_sells.eq(0),
                'buyers_ge8':g.uniq_buyers.ge(8),
                'top3_lt0.7':g.top3_buy_sol.lt(.7),
                'buy_ratio60_ge0.6':g.buy_ratio60.ge(.6),
                'complete_observed_sol':g.missing_sol_share.eq(0)}
            fs['combined']=fs['creator_no_sell']&fs['buyers_ge8']&fs['top3_lt0.7']&fs['buy_ratio60_ge0.6']&fs['complete_observed_sol']
            for name,mask in fs.items():
                met=metrics(g[mask.fillna(False)])
                met.update(choice=label,split=sp,filter=name,unfiltered_n_signals=len(g),
                  feature_join_missing=int(g.feature_decision_t.isna().sum()))
                filters_out.append({k:v for k,v in met.items() if not isinstance(v,(list,dict))})
        result['reviews'][label]=review
    result['interpretation']=[
      'Selection uses training returns only, with full-horizon purge before the training cutoff.',
      'Eligibility is a coverage gate, not proof that missing exits are missing at random.',
      'Resolved-only bootstrap intervals do not identify complete-population PnL.',
      'UTC-day bootstrap preserves within-day dependence but not dependence across days; few test days limit inference.',
      'Rules and filters were fixed before reading final test aggregates; test filters remain exploratory diagnostics, not independent discoveries.',
      'A later October ledger sample evaluates predeclared rules separately, not the best test rule chosen here.',
      'No strategy is qualified for real-capital trading by this analysis alone.'
    ]
    result['model_prediction_filter_not_applied']=(
      'The existing prediction table contains predictions only for future-label-mature, gap-free train/test cohorts, '
      'not all replay signals. Applying its non-null mask as a live filter would import retrospective observation eligibility. '
      'A prospective or all-feature-row post-fit prediction table is required before evaluating its PnL as a deployable rule.')
    oct_path=out/'october_summary.csv'
    if oct_path.exists():
        oc=pd.read_csv(oct_path)
        ledger=oc[oc.coverage_mode=='ledger_day_coverage']
        example=oc[(oc.lv==.1)&(oc.lat==1)&(oc.rule=='trail0.2_arm1.3_h600')]
        result['independent_october']=clean(dict(
          input_sha256=hashlib.sha256(oct_path.read_bytes()).hexdigest(),
          n_ledger_groups=len(ledger),n_positive_resolved_mean=int((ledger.mean_resolved>0).sum()),
          ledger_mean_range=[ledger.mean_resolved.min(),ledger.mean_resolved.max()],
          coverage_bias_example=example.to_dict('records'),
          interpretation='Two coverage models with slightly different fills, not a randomized or pure missing-position intervention. Ledger-day coverage is an explicit constant-state sensitivity, not guaranteed execution. Only one UTC day.'))
    pd.DataFrame(details).to_csv(out/'strategy_review_slices.csv',index=False)
    pd.DataFrame(filters_out).to_csv(out/'strategy_review_filters.csv',index=False)
    (out/'strategy_review.json').write_text(json.dumps(clean(result),ensure_ascii=False,indent=2),encoding='utf-8')
    write_report(result,filters_out)
    print(json.dumps(clean({k:result[k] for k in ['n_candidates','n_eligible','selected','highest_train_resolved_only_diagnostic']}),indent=2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('scratch');p.add_argument('--out',required=True)
    p.add_argument('--tag',default='replay_v2');a=p.parse_args();run(a.scratch,a.out,a.tag)
