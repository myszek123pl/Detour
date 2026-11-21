"""Describe a bounded API panel; quote changes are not executable returns.

Usage: python analyze.py --input RAW_DIRECTORY --output RESULT_DIRECTORY
"""
import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import Counter
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path


def dt(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def number(value):
    try:
        x = float(value)
        return x if math.isfinite(x) else None
    except (ValueError, TypeError):
        return None


def median(xs):
    xs = [x for x in xs if x is not None and math.isfinite(x)]
    return statistics.median(xs) if xs else None


def pools(snapshot, kind):
    found = {}
    for key, rec in snapshot['responses'].items():
        if key == kind or (kind == 'new' and key.startswith('new_')):
            for pool in rec.get('payload', {}).get('data', []):
                found.setdefault(pool['id'], pool)
    return list(found.values())


def boost_addresses(snapshot):
    found = set()
    for key in ('boost_latest', 'boost_top'):
        payload = snapshot['responses'].get(key, {}).get('payload', [])
        if isinstance(payload, list):
            found.update(x['tokenAddress'] for x in payload
                         if x.get('chainId') == 'solana' and x.get('tokenAddress'))
    return found


def pair_records(snapshot):
    found = {}
    for key, rec in snapshot['responses'].items():
        if not key.startswith('pairs_'):
            continue
        payload = rec.get('payload', [])
        if not isinstance(payload, list):
            continue
        for pair in payload:
            if pair.get('chainId') != 'solana':
                continue
            token = pair.get('baseToken', {}).get('address')
            if not token:
                continue
            row = dict(pair)
            row['observed_utc'] = rec['response_end_utc']
            found[pair['pairAddress']] = row
    return found


def cohort(snapshot):
    boosted = boost_addresses(snapshot)
    by_token = {}
    for pair in pair_records(snapshot).values():
        token = pair['baseToken']['address']
        liq = number(pair.get('liquidity', {}).get('usd'))
        if liq is None or liq <= 0:
            continue
        if token not in by_token or liq > by_token[token]['liquidity_usd']:
            created = number(pair.get('pairCreatedAt'))
            now = dt(pair['observed_utc']).timestamp()
            active = number(pair.get('boosts', {}).get('active')) or 0
            by_token[token] = dict(token=token, pair=pair['pairAddress'], dex=pair.get('dexId'),
                                   liquidity_usd=liq, age_minutes=(now - created / 1000) / 60 if created else None,
                                   price_usd=number(pair.get('priceUsd')),
                                   volume_m5_usd=number(pair.get('volume', {}).get('m5')),
                                   quote_change_m5_pct=number(pair.get('priceChange', {}).get('m5')),
                                   boost_visible=int(active > 0 or token in boosted), active_boosts=active,
                                   boost_list_member=int(token in boosted), observed_utc=pair['observed_utc'])
    return list(by_token.values())


def group_summary(rows):
    return dict(n=len(rows), median_age_minutes=median([r['age_minutes'] for r in rows]),
                median_liquidity_usd=median([r['liquidity_usd'] for r in rows]),
                median_volume_m5_usd=median([r['volume_m5_usd'] for r in rows]),
                median_quote_change_m5_pct=median([r['quote_change_m5_pct'] for r in rows]),
                forward_observed_n=sum(r.get('forward_quote_change_pct') is not None for r in rows),
                median_forward_quote_change_pct=median([r.get('forward_quote_change_pct') for r in rows]))


def trending_transitions(snapshots):
    """Only successful reads are rankings; a 429 is missing, never an empty list."""
    valid = [s for s in snapshots if s['responses'].get('trending', {}).get('status') == 200
             and isinstance(s['responses']['trending'].get('payload', {}).get('data'), list)]
    transitions = []
    for a, b in zip(valid, valid[1:]):
        al = [p['id'] for p in pools(a, 'trending')]
        bl = [p['id'] for p in pools(b, 'trending')]
        aset, bset = set(al), set(bl)
        shared = aset & bset
        da = dt(a['responses']['trending']['response_end_utc'])
        db = dt(b['responses']['trending']['response_end_utc'])
        transitions.append(dict(from_round=a['round'], to_round=b['round'], elapsed_seconds=(db - da).total_seconds(),
                                intersection=len(shared), union=len(aset | bset),
                                jaccard=len(shared) / len(aset | bset) if aset | bset else None,
                                retention=len(shared) / len(aset) if aset else None,
                                entered=len(bset - aset), exited=len(aset - bset),
                                mean_absolute_rank_change=statistics.mean(abs(al.index(p) - bl.index(p)) for p in shared) if shared else None))
    return valid, transitions


def analyze(raw_directory, result_directory, expected_date=None):
    files = sorted(Path(raw_directory).glob('snapshot_*.json'))
    if not files:
        raise ValueError('No snapshots found')
    snapshots = [json.loads(f.read_text(encoding='utf-8')) for f in files]
    start, end = dt(snapshots[0]['start_utc']), dt(snapshots[-1]['end_utc'])
    requests = [rec for s in snapshots for rec in s['responses'].values()]
    cache_ages, date_lags = [], []
    request_summary = []
    for s in snapshots:
        for key, rec in s['responses'].items():
            h = {k.lower(): v for k, v in rec.get('headers', {}).items()}
            age = number(h.get('age'))
            if age is not None:
                cache_ages.append(age)
            lag = None
            if h.get('date'):
                lag = (dt(rec['response_end_utc']) - parsedate_to_datetime(h['date'])).total_seconds()
                date_lags.append(lag)
            request_summary.append(dict(round=s['round'], endpoint=key, status=rec.get('status'),
                                        start_utc=rec['request_start_utc'], end_utc=rec['response_end_utc'],
                                        http_date=h.get('date'), http_age=age, client_minus_http_date_s=lag,
                                        body_sha256=rec.get('body_sha256'), error=rec.get('error')))

    new_lists = [pools(s, 'new') for s in snapshots]
    all_new = {p['id']: p for pp in new_lists for p in pp}
    initial_ids = {p['id'] for p in new_lists[0]}
    created_during = [p for p in all_new.values()
                      if p.get('attributes', {}).get('pool_created_at')
                      and start <= dt(p['attributes']['pool_created_at']) <= end]
    per_round = []
    for s, pp in zip(snapshots, new_lists):
        times = [dt(p['attributes']['pool_created_at']) for p in pp
                 if p.get('attributes', {}).get('pool_created_at')]
        dex = Counter(p.get('relationships', {}).get('dex', {}).get('data', {}).get('id', 'unknown') for p in pp)
        per_round.append(dict(round=s['round'], start_utc=s['start_utc'], end_utc=s['end_utc'],
                              new_distinct_pools=len(pp), oldest_creation_utc=min(times).isoformat() if times else None,
                              newest_creation_utc=max(times).isoformat() if times else None,
                              dex_counts=dict(dex), trending_n=len(pools(s, 'trending')) if s['responses'].get('trending', {}).get('status') == 200 else None,
                              boost_visible_addresses=len(boost_addresses(s))))

    valid_trends, transitions = trending_transitions(snapshots)
    first_trend = {p['id'] for p in pools(valid_trends[0], 'trending')} if valid_trends else set()
    last_trend = {p['id'] for p in pools(valid_trends[-1], 'trending')} if valid_trends else set()
    rows = cohort(snapshots[0])
    last_pairs = pair_records(snapshots[-1])
    for row in rows:
        row['forward_quote_change_pct'] = None
        row['quote_horizon_seconds'] = None
        final = last_pairs.get(row['pair'])
        if final and row['price_usd'] and row['price_usd'] > 0:
            px = number(final.get('priceUsd'))
            if px is not None and px > 0:
                row['forward_quote_change_pct'] = 100 * (px / row['price_usd'] - 1)
                row['quote_horizon_seconds'] = (dt(final['observed_utc']) - dt(row['observed_utc'])).total_seconds()
    boosted = [r for r in rows if r['boost_visible']]
    controls = [r for r in rows if not r['boost_visible']]
    # Greedy one-to-one matching without replacement: same DEX, age and
    # liquidity each within a factor of two. This does not remove selection bias.
    matches, unused = [], set(r['token'] for r in controls)
    for row in sorted(boosted, key=lambda r: r['token']):
        if row['age_minutes'] is None or row['age_minutes'] <= 0:
            continue
        candidates = []
        for c in controls:
            if c['token'] not in unused or c['dex'] != row['dex'] or not c['age_minutes'] or c['age_minutes'] <= 0:
                continue
            age_d = abs(math.log2(c['age_minutes'] / row['age_minutes']))
            liq_d = abs(math.log2(c['liquidity_usd'] / row['liquidity_usd']))
            if age_d <= 1 and liq_d <= 1:
                candidates.append((age_d + liq_d, c['token'], c))
        if candidates:
            _, _, c = min(candidates, key=lambda x: (x[0], x[1]))
            unused.remove(c['token'])
            matches.append(dict(boosted_token=row['token'], control_token=c['token'], dex=row['dex'],
                                boosted_age_minutes=row['age_minutes'], control_age_minutes=c['age_minutes'],
                                boosted_liquidity_usd=row['liquidity_usd'], control_liquidity_usd=c['liquidity_usd'],
                                boosted_forward_quote_change_pct=row['forward_quote_change_pct'],
                                control_forward_quote_change_pct=c['forward_quote_change_pct'],
                                difference_pp=(row['forward_quote_change_pct'] - c['forward_quote_change_pct'])
                                if row['forward_quote_change_pct'] is not None and c['forward_quote_change_pct'] is not None else None))
    pump = [r for r in rows if r['dex'] in ('pumpfun', 'pumpswap')]
    summary = dict(
        method_version=1, network='solana', start_utc=start.isoformat(), end_utc=end.isoformat(),
        rounds=len(snapshots), duration_seconds=(end-start).total_seconds(),
        manifest=[dict(file=f.name, size=f.stat().st_size, sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in files],
        request_status_counts=dict(Counter(str(r.get('status')) for r in requests)),
        request_error_count=sum('error' in r for r in requests),
        max_http_cache_age_seconds=max(cache_ages) if cache_ages else None,
        max_abs_client_minus_http_date_seconds=max(map(abs, date_lags)) if date_lags else None,
        expected_client_date=expected_date,
        observed_client_dates=sorted({dt(s['start_utc']).date().isoformat() for s in snapshots}),
        client_date_consistent=all(dt(s['start_utc']).date().isoformat() == expected_date for s in snapshots) if expected_date else None,
        per_round=per_round,
        new_pools=dict(initial_distinct=len(initial_ids), union_distinct=len(all_new), newly_seen_after_baseline=len(set(all_new) - initial_ids),
                       observed_created_during_collection=len(created_during),
                       observed_created_per_minute=len(created_during) / ((end-start).total_seconds()/60) if end > start else None,
                       observed_created_during_by_dex=dict(Counter(p.get('relationships', {}).get('dex', {}).get('data', {}).get('id', 'unknown') for p in created_during)),
                       interpretation='Lower bound for pools observed by these API pages; not network launch rate or pump.fun mint rate.'),
        trending=dict(valid_snapshots=len(valid_trends), missing_snapshots=len(snapshots)-len(valid_trends),
                      transitions=transitions, first_last_intersection=len(first_trend & last_trend),
                      first_last_jaccard=len(first_trend & last_trend)/len(first_trend | last_trend) if first_trend | last_trend else None,
                      first_last_retention=len(first_trend & last_trend)/len(first_trend) if first_trend else None),
        baseline_comparison=dict(discovered_token_count=len({p['baseToken']['address'] for p in pair_records(snapshots[0]).values()}),
                                 eligible_positive_liquidity_tokens=len(rows),
                                 excluded_missing_or_nonpositive_liquidity_tokens=len({p['baseToken']['address'] for p in pair_records(snapshots[0]).values()})-len(rows),
                                 boost_visible=group_summary(boosted), boost_unreported=group_summary(controls),
                                 pumpfun_or_pumpswap_pairs=len(pump),
                                 pumpfun_boost_visible=group_summary([r for r in pump if r['boost_visible']]),
                                 pumpfun_boost_unreported=group_summary([r for r in pump if not r['boost_visible']]),
                                 matched_n=len(matches), unmatched_boosted_n=len(boosted)-len(matches),
                                 matched_forward_quote_difference_median_pp=median([m['difference_pp'] for m in matches]),
                                 quote_horizon_min_seconds=min((r['quote_horizon_seconds'] for r in rows if r['quote_horizon_seconds'] is not None),default=None),
                                 quote_horizon_max_seconds=max((r['quote_horizon_seconds'] for r in rows if r['quote_horizon_seconds'] is not None),default=None)),
        limitations=['Discovery-list selection bias; no representative launch census.',
                     'Pair age is not token age; a PumpSwap DEX venue alone does not prove a pump.fun origin.',
                     'Boost-unreported means no positive active field/current list membership; past advertising is unknown.',
                     'Matched DEX/age/liquidity does not remove confounding by pre-boost momentum, funding, or visibility.',
                     'HTTP cache age and non-simultaneous request times limit sub-minute resolution.',
                     'Observed quote-price changes exclude fees, price impact, failed fills, and executable depth.',
                     'No long-term profitability or causal effect of boosts can be inferred.'])
    out = Path(result_directory)
    out.mkdir(parents=True, exist_ok=True)
    (out/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    for name, records in [('baseline_tokens.csv', rows), ('matched_pairs.csv', matches), ('request_audit.csv', request_summary)]:
        if records:
            with (out/name).open('w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(f, fieldnames=list(records[0]))
                w.writeheader()
                w.writerows(records)
    print(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--expected-date', help='Optional client date YYYY-MM-DD for clock sanity check')
    args = p.parse_args()
    analyze(args.input, args.output, args.expected_date)
