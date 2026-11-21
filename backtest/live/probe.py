import urllib.request, json, sys
def g(u):
    r=urllib.request.Request(u,headers={"Accept":"application/json","User-Agent":"research-snapshot/1.0"})
    with urllib.request.urlopen(r,timeout=25) as f: return json.load(f)
for u in ["https://api.dexscreener.com/token-profiles/latest/v1","https://api.dexscreener.com/token-boosts/latest/v1","https://api.dexscreener.com/token-boosts/top/v1","https://api.geckoterminal.com/api/v2/networks/solana/new_pools?page=1","https://api.geckoterminal.com/api/v2/networks/solana/trending_pools?include=base_token&duration=1h","https://api.geckoterminal.com/api/v2/networks/solana/pools?page=1&sort=h24_volume_usd_desc","https://api.dexscreener.com/latest/dex/search?q=SOL"]:
    try:
        d=g(u); print(u, type(d).__name__, list(d)[:5] if isinstance(d,dict) else len(d))
        x=d if isinstance(d,list) else d.get("data") or d.get("pairs")
        print(json.dumps(x[0])[:1500])
    except Exception as e: print(u,"ERR",e)
