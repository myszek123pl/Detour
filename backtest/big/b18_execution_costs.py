"""Measure ledger transaction fees/failures once per (slot,idx), not per leg.

These observed frequencies describe the sample. They are not estimated fill
probabilities for a new strategy or a causal effect of paying a larger tip.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import duckdb


def run(data_dir, output):
    d=Path(data_dir).resolve();c=duckdb.connect()
    c.execute("SET TimeZone='UTC'; SET threads=4; SET memory_limit='4GB'")
    c.read_parquet(str(d/'data'/'*.parquet')).create_view('trades')
    def rows(q):
        rel=c.sql(q)
        return [dict(zip(rel.columns,r)) for r in rel.fetchall()]
    receipt=json.loads((d/'receipt.json').read_text(encoding='utf-8'))
    summary=json.loads((d/'summary.json').read_text(encoding='utf-8'))
    result=dict(generated_at=datetime.now(timezone.utc).isoformat(),
      provenance=json.loads((d/'validation_download_manifest.json').read_text(encoding='utf-8')),
      receipt=receipt,provider_summary=summary)
    result['rows']=rows('''select count(*) n,count(distinct mint) mints,
      count(distinct wallet) wallets,min(ts) first_second,max(ts) last_second,
      count(*) filter(where sol_lamports is null and not failed) successful_missing_sol,
      count(*) filter(where r1 is null and not failed) successful_missing_r1
      from trades''')[0]
    result['venue_rows']=rows('''select venue,failed,count(*) n,count(distinct mint) mints
      from trades group by all order by venue,failed''')
    c.execute('''create temp table tx as select slot,idx,first(failed) failed,
      max(fee_lamports) fee,max(tip_lamports) tip,max(compute_units) cu,
      count(*) legs,count(distinct venue) venues,
      count(distinct mint) mints,count(distinct wallet) users,
      count(distinct fee_lamports) n_fee_values,
      bool_or(venue='curve') touches_curve,
      bool_or(venue='pumpswap') touches_pool,
      sum(sol_lamports) turnover_lamports
      from trades group by slot,idx''')
    result['transactions']=rows('''select failed,count(*) n,sum(legs) legs,
      sum(fee)/1e9 fee_sol,sum(tip)/1e9 tip_sol,
      quantile_cont(fee,[.5,.9,.99]) fee_lamports_quantiles,
      quantile_cont(tip,[.5,.9,.99]) tip_lamports_quantiles,
      count(*) filter(where tip>0) with_tip,
      count(*) filter(where n_fee_values>1) inconsistent_repeated_fee,
      count(*) filter(where legs>1) multi_leg_transactions,
      quantile_cont(cu,[.5,.9,.99]) compute_unit_quantiles
      from tx group by failed order by failed''')
    result['transaction_fee_turnover']=rows('''select
      case when turnover_lamports<1e8 then '<0.1SOL' when turnover_lamports<1e9 then '0.1-1SOL'
        when turnover_lamports<10e9 then '1-10SOL' else '>=10SOL' end turnover_bucket,
      count(*) n,median((fee+coalesce(tip,0))/turnover_lamports) fee_tip_over_gross_turnover,
      median((fee+coalesce(tip,0))/1e9) fee_tip_sol
      from tx where not failed and turnover_lamports>0 group by 1 order by 1''')
    result['top_failure_errors']=rows('''select error,count(*) trade_rows,
      count(distinct (slot,idx)) transactions
      from trades where failed group by error order by transactions desc limit 15''')
    result['curve_state']=rows('''select count(*) n,
      count(*) filter(where quote_mint='So11111111111111111111111111111111111111112') wsol_quoted,
      count(*) filter(where quote_mint='So11111111111111111111111111111111111111112' and
        abs((r1/1e9)*(r2/1e6)/(30*1073000000.0)-1)<.005) standard_invariant,
      count(*) filter(where r1>114.5e9) near_completion
      from trades where venue='curve' and not failed''')[0]
    result['interpretation']=[
      'Repeated transaction fees are counted once per(slot,idx). Protocol/creator/LP fees are additional and not in fee_lamports.',
      'tip_lamports on failed transactions is unknown, not proven zero.',
      'Failure frequency is conditional on exported attempts; failed multi-hop attempts without identifiable mint are excluded by the publisher.',
      'An observed failure share cannot calibrate the fill probability of our unsubmitted orders.',
      'Current official SDK quotes fixed total budgets with net input X/(1+fee), before integer rounding; June-July fee schedules remain an assumption.',
      'Fees divided by total gross transaction turnover are descriptive, not per-position round-trip costs.'
    ]
    dest=Path(output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,default=str),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['rows','transactions','curve_state']},indent=2,default=str),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data_dir');p.add_argument('--output',required=True)
    a=p.parse_args();run(a.data_dir,a.output)
