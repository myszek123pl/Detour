"""Capture timestamped, bounded public API snapshots; no trading or credentials.

Usage: python collect.py --output PATH --rounds 5 --interval 60
Raw payloads stay outside the repository. Public lists are samples, not a census.
"""
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def collect(output, rounds=5, interval=60, pages=3):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({'User-Agent': 'DetourResearch/1.0', 'Accept': 'application/json'})
    last = {}
    blocked_until = {}

    def get(url):
        host = url.split('/')[2]
        if time.monotonic() < blocked_until.get(host, 0):
            return dict(url=url, request_start_utc=utcnow(), response_end_utc=utcnow(),
                        error='Skipped while respecting Retry-After backoff from earlier HTTP 429')
        gap = 2.2 if 'geckoterminal' in host else 1.1
        time.sleep(max(0, gap - (time.monotonic() - last.get(host, -1e9))))
        rec = {'url': url, 'request_start_utc': utcnow()}
        try:
            response = session.get(url, timeout=30)
            rec.update(status=response.status_code, response_end_utc=utcnow(),
                       headers={k: v for k, v in response.headers.items()
                                if k.lower() in ('date', 'age', 'cache-control', 'last-modified',
                                                 'cf-cache-status', 'retry-after', 'x-cache')},
                       body_sha256=hashlib.sha256(response.content).hexdigest())
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After', '60')
                try:
                    seconds = float(retry_after)
                except ValueError:
                    try:
                        seconds = (parsedate_to_datetime(retry_after) - datetime.now(timezone.utc)).total_seconds()
                    except (ValueError, TypeError):
                        seconds = 60
                blocked_until[host] = time.monotonic() + max(seconds, 60)
            response.raise_for_status()
            rec['payload'] = response.json()
        except (requests.RequestException, ValueError) as exc:
            rec['error'] = str(exc)
            rec.setdefault('response_end_utc', utcnow())
        last[host] = time.monotonic()
        return rec

    for i in range(rounds):
        start = time.monotonic()
        snapshot = {'round': i, 'start_utc': utcnow(), 'network': 'solana', 'responses': {}}
        r = snapshot['responses']
        for page in range(1, pages + 1):
            r[f'new_{page}'] = get(f'https://api.geckoterminal.com/api/v2/networks/solana/new_pools?page={page}&include=base_token,dex')
        r['trending'] = get('https://api.geckoterminal.com/api/v2/networks/solana/trending_pools?page=1&duration=1h&include=base_token,dex')
        r['boost_latest'] = get('https://api.dexscreener.com/token-boosts/latest/v1')
        r['boost_top'] = get('https://api.dexscreener.com/token-boosts/top/v1')
        addresses = set()
        for key, rec in list(r.items()):
            payload = rec.get('payload', {})
            if key.startswith('new_') or key == 'trending':
                for pool in payload.get('data', []):
                    token_id = pool.get('relationships', {}).get('base_token', {}).get('data', {}).get('id', '')
                    if token_id.startswith('solana_'):
                        addresses.add(token_id[len('solana_'):])
            elif isinstance(payload, list):
                addresses.update(x['tokenAddress'] for x in payload
                                 if x.get('chainId') == 'solana' and x.get('tokenAddress'))
        # Follow all previously selected tokens so disappearance from a discovery
        # list does not itself censor their price observations.
        registry = output / 'tracked_tokens.json'
        if registry.exists():
            addresses.update(json.loads(registry.read_text(encoding='utf-8')))
        addresses = sorted(addresses)
        registry.write_text(json.dumps(addresses), encoding='utf-8')
        for j in range(0, len(addresses), 30):
            r[f'pairs_{j // 30}'] = get('https://api.dexscreener.com/tokens/v1/solana/' + ','.join(addresses[j:j + 30]))
        snapshot['end_utc'] = utcnow()
        filename = output / f'snapshot_{i:03d}.json'
        filename.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'round': i, 'start': snapshot['start_utc'], 'end': snapshot['end_utc'],
                          'tokens': len(addresses), 'requests': len(r),
                          'errors': {k: v['error'] for k, v in r.items() if 'error' in v}}), flush=True)
        if i < rounds - 1:
            time.sleep(max(0, interval - (time.monotonic() - start)))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True)
    p.add_argument('--rounds', type=int, default=5)
    p.add_argument('--interval', type=float, default=60)
    p.add_argument('--pages', type=int, default=3)
    args = p.parse_args()
    if not 1 <= args.pages <= 10 or not 1 <= args.rounds <= 30 or args.interval < 60:
        p.error('pages 1..10; rounds 1..30; interval >=60 seconds required')
    collect(args.output, args.rounds, args.interval, args.pages)
