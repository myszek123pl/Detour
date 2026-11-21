"""Recount the pinned corpus before any simulator is run.

Usage: python b00_audit.py SCRATCH --output audit.json
SCRATCH/datasets/jocry contains the downloaded files, not committed to Git.
No supplied issue counts or labels are treated as ground truth.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import duckdb


def run(scratch, output):
    root = Path(scratch).resolve()
    data = root / 'datasets' / 'jocry'
    tmp = root / 'work' / 'tmp'
    tmp.mkdir(parents=True, exist_ok=True)
    c = duckdb.connect()
    c.execute("SET TimeZone='UTC'")
    c.execute("SET memory_limit='4GB'")
    c.execute('SET threads=4')
    c.execute(f"SET temp_directory='{tmp.as_posix().replace(chr(39), chr(39)*2)}'")
    c.read_parquet(str(data/'trades'/'*.parquet')).create_view('raw')
    c.read_parquet(str(data/'tokens.parquet')).create_view('tokens')
    c.read_parquet(str(data/'postgard_snapshots.parquet')).create_view('pg')
    def rows(sql):
        rel = c.sql(sql)
        return [dict(zip(rel.columns, r)) for r in rel.fetchall()]
    report = dict(generated_at=datetime.now(timezone.utc).isoformat(),
                  provenance=json.loads((data/'download_manifest.json').read_text(encoding='utf-8')))
    report['trades'] = rows("""select count(*) n, count(distinct id) distinct_ids,
        count(distinct mint) mints, min(event_time) start_utc, max(event_time) end_utc,
        count(*) filter(where v_sol_bonding_curve is null or v_tokens_bonding_curve is null) missing_reserves,
        count(*) filter(where sol_amount is null or price_sol is null) missing_sol_or_price,
        count(*) filter(where token_amount*price_sol>0 and
          sol_amount/(token_amount*price_sol) not between .01 and 100) suspect_volume,
        count(*) filter(where user_wallet='BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s') provider_excluded_wallet_rows,
        count(*) filter(where user_wallet='11111111111111111111111111111111') actual_system_program_rows
        from raw""")[0]
    print('trade totals', report['trades'], flush=True)
    report['tokens'] = rows("""select count(*) n, count(distinct mint) unique_mints,
        count(*) filter(where graduated_at is not null) provider_graduated,
        count(*) filter(where is_mayhem_mode) mayhem,
        count(*) filter(where top10_pct_suspect) suspect_concentration,
        min(detected_at) first_detected, max(detected_at) last_detected from tokens""")[0]
    report['by_day'] = rows("""select cast(event_time as date) as day_utc, count(*) n,
        count(distinct mint) mints,
        count(*) filter(where v_sol_bonding_curve is not null and v_tokens_bonding_curve is not null) with_reserves,
        count(*) filter(where abs((v_sol_bonding_curve/1e9)*(v_tokens_bonding_curve/1e6)/(30*1073000000.0)-1)<.01) standard_invariant,
        count(*) filter(where sol_amount is null or price_sol is null) missing_sol_or_price
        from raw group by 1 order by 1""")
    report['by_source'] = rows("""select source,count(*) n,
        count(*) filter(where v_sol_bonding_curve is not null and v_tokens_bonding_curve is not null) with_reserves
        from raw group by 1 order by 1""")
    # State alignment: compare each source's signed trade amount with reserve
    # movement before/after that row. These are diagnostics, not chain ordering.
    report['state_alignment'] = rows("""with s as (
      select source,is_buy,sol_amount,v_sol_bonding_curve/1e9 vs,
        lag(v_sol_bonding_curve/1e9) over w prev_vs,
        lead(v_sol_bonding_curve/1e9) over w next_vs
      from raw where v_sol_bonding_curve is not null and sol_amount>0
      window w as(partition by mint,source order by event_time,id))
      select source, count(*) n,
        median(abs((vs-prev_vs)-(case when is_buy then sol_amount else -sol_amount end))/sol_amount) previous_delta_relative_error,
        median(abs((next_vs-vs)-(case when is_buy then sol_amount else -sol_amount end))/sol_amount) next_delta_relative_error
      from s group by 1""")
    report['postgrad'] = rows("""select count(*) n, count(distinct mint) mints,
        min(snapshot_time) first_snapshot, max(snapshot_time) last_snapshot,
        count(*) filter(where incomplete_data) incomplete,
        count(*) filter(where price_native>0 and liquidity_quote>0 and liquidity_base>0) with_price_and_reserves
        from pg""")[0]
    report['interpretation'] = [
        'Provider graduation timestamps are dataset annotations, not independently chain-verified events.',
        'event_time/id order is collector order; it is not a slot/transaction-index replay.',
        'The provider-excluded wallet is recorded as a data-quality exclusion; its identity is not independently established.',
        'A corpus row count does not imply every row can support execution simulation.',
    ]
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print('wrote', output, flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('scratch')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    run(args.scratch, args.output)
