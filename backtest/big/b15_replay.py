"""Checkpointed descriptive replay of the 32 frozen exit rules.

The quality cohort is selected retrospectively. Temporal slices are NOT an
untouched holdout. Missing execution data must remain censored, never zero.
Raw per-token outcomes stay under SCRATCH/work/TAG, outside the repository.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

import duckdb
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from simlib import VS0, Paths, entry, exit_sim, load

LEVELS = [.05, .10, .20, .30, .40, .50, .60]
LATENCIES = [1, 5, 30]
TRAIN_END = datetime(2026, 7, 8, tzinfo=timezone.utc).timestamp()
TEST_START = TRAIN_END + 12 * 3600


def rules(horizon):
    specs = {'hold': {}}
    for sl in (.5, .7, .85):
        for tp in (1.25, 1.5, 2., 3.):
            specs[f'br_sl{sl}_tp{tp}'] = dict(sl=sl, tps=[(tp, 1.)])
    for tr in (.10, .20, .30, .50):
        for arm in (1., 1.3, 2.):
            specs[f'trail{tr}_arm{arm}'] = dict(trail=tr, arm=arm)
    specs['ladderB'] = dict(sl=.5, tps=[(2., .5), (5., .25)], trail=.5, arm=2.)
    specs['ladderC'] = dict(sl=.6, tps=[(1.5, 1/3), (3., 1/3), (10., 1/3)])
    specs['ladderD'] = dict(sl=.7, tps=[(1.3, .5), (2., .5)])
    for tm in (30, 120, 600, 3600):
        specs[f'time{tm}_sl0.7'] = dict(sl=.7, tmax=tm)
    for spec in specs.values():
        spec['tmax'] = min(spec.get('tmax', horizon), horizon)
    assert len(specs) == 32
    return specs


def split_name(ts):
    return 'train' if ts < TRAIN_END else ('test' if ts >= TEST_START else 'embargo')


SCHEMA = pa.schema([
    ('mid', pa.int32()), ('decision_t', pa.float64()), ('launch_t', pa.float64()),
    ('lv', pa.float64()), ('lat', pa.int8()), ('rule_id', pa.int8()),
    ('filled', pa.bool_()), ('r', pa.float64()), ('kind', pa.string()),
    ('n_sells', pa.int8()), ('split', pa.string())])


def simulate_one(P, mid, specs, args):
    d = P.tok(mid)
    t = d['t']
    out = []
    coverage = Counter()
    if len(t) < 2:
        coverage['short_path'] += 1
        return out, coverage
    prog = (d['vs'] - VS0) / 85.
    for lv in LEVELS:
        key = f'{lv:.2f}'
        where = np.flatnonzero(prog >= lv)
        if not len(where):
            coverage[f'no_crossing_{key}'] += 1
            continue
        i = int(where[0])
        if i == 0 and prog[0] > lv + .03:
            coverage[f'left_truncated_crossing_{key}'] += 1
            continue
        coverage[f'signals_{key}'] += 1
        # All three latency cases use the same observed decision.
        ts = float(t[i])
        split = split_name(ts)
        for lat in LATENCIES:
            en = entry(d, i, lat, args.size_sol, args.fee, args.tip_sol, fee_model='on_top')
            for rid, spec in enumerate(specs.values()):
                if en is None:
                    r, kind, ntx = None, 'no_fill', 0
                else:
                    val, kind, ntx = exit_sim(P, mid, d, en, spec, lat,
                        args.fee, args.tip_sol, args.size_sol)
                    r = float(val) if np.isfinite(val) else None
                    kind = str(kind) if kind is not None else 'unknown'
                out.append((mid, ts, float(d['L']), lv, lat, rid, en is not None,
                            r, kind, ntx, split))
    return out, coverage


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def summarize(folder, output, config, coverage, elapsed):
    files = list((folder/'parts').glob('part-*.parquet'))
    if not files:
        raise RuntimeError('no replay outcomes')
    c = duckdb.connect()
    c.execute("SET memory_limit='2GB'; SET threads=4")
    c.read_parquet([str(f) for f in files]).create_view('outcomes')
    summary = c.sql('''select split,lv,lat,rule_id,count(*) n_signals,
        count(*) filter(where filled) n_filled,
        count(*) filter(where not filled) n_no_fill,
        count(r) n_resolved,
        count(*) filter(where filled and r is null) n_censored,
        avg(r) mean_resolved,median(r) median_resolved,
        count(*) filter(where r>0) n_wins,
        min(r) min_resolved,max(r) max_resolved,
        sum(r) sum_resolved,
        sum(case when r>0 then r else 0 end) sum_positive,
        max(case when r>0 then r else 0 end) largest_positive
        from outcomes group by all order by split,lv,lat,rule_id''').df()
    names = list(config['rules'])
    summary['rule'] = summary.rule_id.map(dict(enumerate(names)))
    summary['resolved_fraction_of_fills'] = summary.n_resolved / summary.n_filled.replace(0, np.nan)
    summary['win_fraction_resolved'] = summary.n_wins / summary.n_resolved.replace(0, np.nan)
    summary['missing_minus100pct_scenario'] = (summary.sum_resolved.fillna(0)-summary.n_censored) / summary.n_filled.replace(0,np.nan)
    summary['largest_winner_share_positive'] = summary.largest_positive / summary.sum_positive.replace(0, np.nan)
    output.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output/f'{config["tag"]}_summary.csv', index=False)
    daily = c.sql('''select floor(decision_t/86400)::bigint day_utc,split,lv,lat,rule_id,
        count(*) n_signals,count(*) filter(where filled) n_filled,count(r) n_resolved,
        sum(r) sum_resolved,sum(r*r) sumsq_resolved,
        count(*) filter(where r>0) n_wins
        from outcomes group by all order by day_utc,lv,lat,rule_id''').df()
    daily.to_csv(output/f'{config["tag"]}_daily.csv', index=False)
    reasons = c.sql('''select split,lat,kind,count(*) n from outcomes
        group by all order by split,lat,n desc''').df()
    reasons.to_csv(output/f'{config["tag"]}_reasons.csv', index=False)
    manifest = dict(config=config, elapsed_seconds=elapsed, coverage=dict(coverage),
        completed_chunks=len(files), outcome_rows=int(summary.n_signals.sum()),
        generated_at=datetime.now(timezone.utc).isoformat(),
        interpretation=[
            'Resolved-only averages are conditional on observed exits; censored positions can change the sign.',
            'No-fill means no supported execution in this dataset, not necessarily a rejected real transaction.',
            'The corpus was retrospectively filtered for quality, not selected by a live trading rule.',
            'Own impact holds the other flow fixed: a counterfactual approximation, not an exchange fill guarantee.',
            'The temporal test slice may have been inspected in previous research; it is not untouched holdout.',
            'Fees, position size and tips are declared scenarios, not verified historical tariffs.',
            'All rule variants have a declared maximum horizon; hold is capped, not hold forever.'])
    (output/f'{config["tag"]}_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('SUMMARY', json.dumps({k: manifest[k] for k in ['elapsed_seconds','completed_chunks','outcome_rows']}), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('scratch', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--tag', default='replay_v2')
    ap.add_argument('--size-sol', type=float, default=1.)
    ap.add_argument('--fee', type=float, default=.0125)
    ap.add_argument('--tip-sol', type=float, default=.30/70)
    ap.add_argument('--horizon', type=float, default=3600.)
    ap.add_argument('--chunk-tokens', type=int, default=500)
    ap.add_argument('--limit-tokens', type=int)
    args = ap.parse_args()
    if args.size_sol <= 0 or not 0 <= args.fee < 1 or args.tip_sol < 0:
        ap.error('invalid cost scenario')
    if args.horizon <= 0 or args.chunk_tokens <= 0:
        ap.error('horizon and chunk size must be positive')
    scratch = args.scratch.resolve()
    folder = scratch/'work'/args.tag
    (folder/'parts').mkdir(parents=True, exist_ok=True)
    specs = rules(args.horizon)
    config = dict(tag=args.tag, size_sol=args.size_sol, fee=args.fee, buy_fee_model='on_top',
        tip_sol=args.tip_sol, horizon_seconds=args.horizon, levels=LEVELS,
        latencies=LATENCIES, rules=specs, chunk_tokens=args.chunk_tokens,
        limit_tokens=args.limit_tokens, split_clock='decision_t',
        train_end_utc=TRAIN_END,test_start_utc=TEST_START,
        simlib_sha256=sha(Path(__file__).with_name('simlib.py')),
        runner_sha256=sha(__file__),
        inputs={n:sha(scratch/'work'/n) for n in ['tok_jocry2.parquet','paths_jocry.parquet','postgrad_jocry.parquet']})
    cf=folder/'config.json'
    if cf.exists() and json.loads(cf.read_text())!=config:
        raise RuntimeError('Existing run has different configuration/code/input hashes; use a new --tag')
    cf.write_text(json.dumps(config,indent=2),encoding='utf-8')
    started=time.monotonic()
    print('LOAD',datetime.now(timezone.utc).isoformat(),flush=True)
    tk,df,pg=load(scratch.as_posix(),mayhem=False)
    if args.limit_tokens:
        idx=np.linspace(0,len(tk)-1,min(args.limit_tokens,len(tk)),dtype=int)
        tk=tk.iloc[idx].copy(); df=df[df.mid.isin(tk.mid)].copy()
    P=Paths(tk,df,pg)
    del df,pg
    mids=sorted(P.rng)
    config['n_selected_tokens']=len(tk)
    # Keep the immutable resume config separate from computed run metadata.
    coverage=Counter()
    print('READY',len(mids),'tokens',len(P.t),'states','rules',len(specs),flush=True)
    for start in range(0,len(mids),args.chunk_tokens):
        chunk=start//args.chunk_tokens
        target=folder/'parts'/f'part-{chunk:05d}.parquet'
        info=target.with_suffix('.json')
        if target.exists() and info.exists():
            old=json.loads(info.read_text()); coverage.update(old['coverage'])
            continue
        rows=[]; counts=Counter()
        for mid in mids[start:start+args.chunk_tokens]:
            r,c=simulate_one(P,mid,specs,args); rows.extend(r); counts.update(c)
        table=pa.Table.from_pylist([dict(zip(SCHEMA.names,r)) for r in rows],schema=SCHEMA)
        tmp=target.with_suffix('.tmp')
        pq.write_table(table,tmp,compression='zstd');tmp.replace(target)
        info.write_text(json.dumps(dict(coverage=dict(counts),n_tokens=min(args.chunk_tokens,len(mids)-start),
            rows=len(rows))),encoding='utf-8')
        coverage.update(counts)
        print('CHECKPOINT',start+min(args.chunk_tokens,len(mids)-start),'/',len(mids),
            'rows',len(rows),'elapsed_s',round(time.monotonic()-started,1),flush=True)
    summarize(folder,args.output,config,coverage,time.monotonic()-started)


if __name__=='__main__':
    main()
