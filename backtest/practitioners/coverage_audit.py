"""Audit whether the corpus can test Wood/Satsdats; does not estimate returns.

Usage: python coverage_audit.py --data-dir <jocry> --output <coverage.json>
Requires duckdb. Inputs are frozen local Parquet files, not vendor live state.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import duckdb


def audit(data_dir):
    data_dir = Path(data_dir).resolve()
    con = duckdb.connect()
    con.execute("SET TimeZone='UTC'")
    con.execute("SET memory_limit='2GB'")
    con.execute("SET threads=2")

    def load(name, filename):
        path = str(data_dir / filename).replace("'", "''")
        con.execute(f"CREATE VIEW {name} AS SELECT * FROM read_parquet('{path}')")

    def records(sql):
        cur = con.execute(sql)
        names = [d[0] for d in cur.description]
        return [dict(zip(names, row)) for row in cur.fetchall()]

    def one(sql):
        return records(sql)[0]

    load('tokens', 'tokens.parquet')
    load('snapshots', 'postgard_snapshots.parquet')
    load('outcomes', 'postgard_outcomes.parquet')
    load('migrations', 'migrations.parquet')
    result = {
        'audit': 'coverage_only_not_strategy_backtest',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'dataset': 'jocry/Pumpfun_Memecoin_Corpus',
        'duckdb_version': duckdb.__version__,
        'rules': {
            'wood_age_proxy_seconds': 48 * 3600,
            'wood_entry_freshness_seconds': 1800,
            'satsdats_market_cap_usd_inclusive': [5_000_000, 10_000_000],
            'ema_warmup_completed_hours': 9,
            'hourly_close_max_staleness_seconds': 300,
            'valid_snapshot': 'price_usd>0 AND NOT incomplete_data AND timestamp>=graduated_at',
            'important': 'detected_at is not independently verified on-chain creation time; snapshots are not executed OHLCV/trades',
        },
    }
    manifest = data_dir / 'download_manifest.json'
    if manifest.exists():
        provenance = json.loads(manifest.read_text(encoding='utf-8'))
        result['dataset_revision'] = provenance['revision']
        used_files = {'tokens.parquet', 'postgard_snapshots.parquet', 'postgard_outcomes.parquet', 'migrations.parquet'}
        result['input_sha256_from_download_manifest'] = {
            f['path']: f['sha256'] for f in provenance['files'] if f['path'] in used_files
        }
    result['tokens'] = one("""
        SELECT count(*) rows, count(DISTINCT mint) unique_mints,
          min(detected_at)::varchar first_detected_utc,
          max(detected_at)::varchar last_detected_utc,
          count(*) FILTER(WHERE graduated_at IS NOT NULL) labeled_graduated,
          count(*) FILTER(WHERE is_mayhem_mode) mayhem,
          count(*) FILTER(WHERE top10_pct_suspect) concentration_suspect
        FROM tokens
    """)
    result['snapshot_table'] = one("""
        SELECT count(*) rows, count(DISTINCT mint) unique_mints,
          min(snapshot_time)::varchar first_snapshot_utc,
          max(snapshot_time)::varchar last_snapshot_utc,
          count(*) FILTER(WHERE incomplete_data) incomplete_rows,
          count(*) FILTER(WHERE price_usd>0) positive_price_rows,
          count(*) FILTER(WHERE market_cap_usd>0) positive_market_cap_rows,
          count(*) FILTER(WHERE fdv_usd>0) positive_fdv_rows,
          count(*) FILTER(WHERE liquidity_usd>0) positive_liquidity_rows,
          max(market_cap_usd) max_reported_market_cap_usd
        FROM snapshots
    """)
    con.execute("""
        CREATE TABLE joined AS
        SELECT s.*, t.detected_at, t.graduated_at, t.is_mayhem_mode,
          epoch(s.snapshot_time) ts,
          epoch(s.snapshot_time)-epoch(t.detected_at) age_detection_s,
          (s.price_usd>0 AND NOT coalesce(s.incomplete_data, true)
             AND s.snapshot_time>=t.graduated_at) valid
        FROM snapshots s JOIN tokens t USING(mint)
    """)
    result['joined'] = one("""
        SELECT count(*) rows, count(DISTINCT mint) unique_mints,
          count(*) FILTER(WHERE valid) valid_rows,
          count(DISTINCT mint) FILTER(WHERE valid) valid_mints,
          count(*) FILTER(WHERE snapshot_time<graduated_at) rows_before_recorded_graduation,
          count(*) FILTER(WHERE age_detection_s<0) rows_before_detected,
          min(age_detection_s) min_age_detection_s,
          max(age_detection_s) max_age_detection_s
        FROM joined
    """)
    result['wood_coverage'] = one("""
        SELECT count(DISTINCT mint) FILTER(WHERE age_detection_s>=172800) any_snapshot_at_or_after_48h,
          count(DISTINCT mint) FILTER(WHERE valid AND age_detection_s>=172800) valid_price_at_or_after_48h,
          count(DISTINCT mint) FILTER(WHERE valid AND age_detection_s BETWEEN 172800 AND 174600) valid_price_first_30min_after_48h,
          count(DISTINCT mint) FILTER(WHERE valid AND age_detection_s BETWEEN 172800 AND 174600 AND liquidity_usd>0 AND volume_1h>0) priced_liquid_active_first_30min_after_48h,
          count(DISTINCT mint) FILTER(WHERE valid AND age_detection_s>=259200) valid_price_at_or_after_72h,
          count(DISTINCT mint) FILTER(WHERE valid AND age_detection_s>=777600) valid_price_at_or_after_9days
        FROM joined
    """)
    # A necessary entry+24h coverage condition, not a survival/strategy outcome.
    result['wood_coverage']['candidate_with_later_price_at_least_24h_after_first_48h_entry'] = one("""
        WITH e AS (SELECT mint,min(ts) et FROM joined
          WHERE valid AND age_detection_s BETWEEN 172800 AND 174600
            AND liquidity_usd>0 AND volume_1h>0 GROUP BY mint)
        SELECT count(DISTINCT e.mint) n FROM e JOIN joined j USING(mint)
          WHERE j.valid AND j.ts>=e.et+86400
    """)['n']
    result['satsdats_coverage'] = one("""
        SELECT count(*) FILTER(WHERE market_cap_usd BETWEEN 5000000 AND 10000000) rows_in_market_cap_band,
          count(DISTINCT mint) FILTER(WHERE market_cap_usd BETWEEN 5000000 AND 10000000) mints_in_market_cap_band,
          count(*) FILTER(WHERE valid AND market_cap_usd BETWEEN 5000000 AND 10000000) valid_rows_in_market_cap_band,
          count(DISTINCT mint) FILTER(WHERE valid AND market_cap_usd BETWEEN 5000000 AND 10000000) valid_mints_in_market_cap_band,
          count(DISTINCT mint) FILTER(WHERE valid AND market_cap_usd BETWEEN 5000000 AND 10000000 AND liquidity_usd>0 AND volume_1h>0) priced_liquid_active_mints_in_band,
          count(DISTINCT mint) FILTER(WHERE valid AND fdv_usd BETWEEN 5000000 AND 10000000) mints_with_fdv_in_band_not_a_substitute_for_market_cap
        FROM joined
    """)
    con.execute("""
        CREATE TABLE hours AS SELECT mint, floor(ts/3600)::bigint h,
          max(ts) last_ts, arg_max(price_usd,ts) close_proxy
        FROM joined WHERE valid GROUP BY mint,h
    """)
    result['hourly_snapshot_coverage'] = one("""
        SELECT count(*) observed_token_hours, count(DISTINCT mint) mints,
          count(*) FILTER(WHERE last_ts>=(h+1)*3600-300) close_proxy_fresh_within_5min_hours
        FROM hours
    """)
    # Fix candidates from the first observed cap-band event; never select using
    # a later return, a peak cap, or a post-hoc survival label.
    result['satsdats_first_entry_warmup'] = one("""
        WITH e AS (SELECT mint,min(ts) et FROM joined
            WHERE valid AND market_cap_usd BETWEEN 5000000 AND 10000000
              AND liquidity_usd>0 AND volume_1h>0 GROUP BY mint),
        w AS (SELECT e.mint,e.et,
            count(h.h) prior_observed_hours,
            count(h.h) FILTER(WHERE h.last_ts>=(h.h+1)*3600-300) prior_fresh_hours
          FROM e LEFT JOIN hours h ON e.mint=h.mint
            AND h.h BETWEEN floor(e.et/3600)-9 AND floor(e.et/3600)-1
          GROUP BY e.mint,e.et)
        SELECT count(*) first_entry_mints,
          count(*) FILTER(WHERE prior_observed_hours=9) with_9_consecutive_observed_closed_hours,
          count(*) FILTER(WHERE prior_fresh_hours=9) with_9_consecutive_fresh_closed_hour_proxies
        FROM w
    """)
    result['satsdats_first_observed_entry_dates_utc'] = records("""
        WITH e AS (SELECT mint,min(ts) et FROM joined
          WHERE valid AND market_cap_usd BETWEEN 5000000 AND 10000000
            AND liquidity_usd>0 AND volume_1h>0 GROUP BY mint)
        SELECT strftime(to_timestamp(et), '%Y-%m-%d') date_utc, count(*) mints
        FROM e GROUP BY 1 ORDER BY 1
    """)
    result['postgrad_coverage_by_age'] = records("""
        WITH a AS (SELECT mint, max(age_detection_s)/3600 age_h
            FROM joined WHERE valid GROUP BY mint)
        SELECT CASE WHEN age_h<1 THEN '<1h' WHEN age_h<9 THEN '1-9h'
          WHEN age_h<24 THEN '9-24h' WHEN age_h<48 THEN '24-48h'
          WHEN age_h<72 THEN '48-72h' ELSE '>=72h' END max_valid_age,
          count(*) mints FROM a GROUP BY 1 ORDER BY 1
    """)
    result['outcome_label_coverage'] = one("""
        SELECT count(*) rows, count(*) FILTER(WHERE still_liquid_at_24h) labeled_liquid_at_24h,
          count(*) FILTER(WHERE still_liquid_at_48h) labeled_liquid_at_48h,
          count(*) FILTER(WHERE peak_mcap_usd BETWEEN 5000000 AND 10000000) peak_cap_in_band_not_entry_signal
        FROM outcomes
    """)
    result['migration_address_coverage'] = one("""
        SELECT count(*) rows,
          count(*) FILTER(WHERE pool_address IN ('synthetic_graduation_queue','backfilled_from_pumpswap_trade')) sentinel_addresses,
          count(*) FILTER(WHERE pool_address IS NULL) missing_addresses
        FROM migrations
    """)
    result['preexisting_script_audit'] = {
        'p01_universe.py': 'frame is graduated-only, found-pair backfill; U plus high-early-cap H stratum is not a uniform launch cohort; files point to another session',
        'p02_fetch.py': 'hourly OHLCV cannot resolve 1/5/30-second execution; fetch-time now and pagination/retention can alter coverage',
        'plib.py': 'reference age is graduation timestamp, not creation; fixed 1e9 supply and price-derived liquidity; missing hours forward-filled; NOW constant',
        'run_filters.py': 'tests early 15-minute bars, not 48-hour/5-10m cohort; concentration flags require point-in-time provenance',
    }
    result['verdict'] = {
        'wood_exact_strategy_tested': False,
        'satsdats_exact_strategy_tested': False,
        'pnl_estimated': False,
        'reason': 'coverage counts do not reconstruct discretionary entry filters or executable prices; necessary price-history conditions must be checked before any return test',
    }
    con.close()
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data-dir', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    result = audit(args.data_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == '__main__':
    main()
