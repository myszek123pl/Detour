"""Fetch GeckoTerminal hourly OHLCV for universe pools (<=30 req/min -> 2.2s spacing). Resumable cache; adaptive spacing on HTTP 429."""
import pandas as pd, json, os, time, urllib.request, urllib.error
SP="/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/"
OUT=SP+"gt_hour/"; os.makedirs(OUT,exist_ok=True)
u=pd.read_csv(SP+"universe.csv"); now=int(time.time())
H={"Accept":"application/json;version=20230302","User-Agent":"research-backtest"}
t_last=0; gap=2.2; n429=0
for i,row in u.iterrows():
    fn=OUT+row.pair+".json"
    if os.path.exists(fn): continue
    bt=min(now,int(row.grad_ts)+41*86400)
    url=f"https://api.geckoterminal.com/api/v2/networks/solana/pools/{row.pair}/ohlcv/hour?aggregate=1&limit=1000&currency=usd&before_timestamp={bt}"
    for a in range(5):
        w=gap-(time.time()-t_last)
        if w>0: time.sleep(w)
        t_last=time.time()
        try:
            j=json.load(urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=30))
            json.dump({"mint":row.mint,"grad_ts":int(row.grad_ts),"bt":bt,"l":j['data']['attributes']['ohlcv_list']},open(fn,"w")); break
        except urllib.error.HTTPError as e:
            if e.code==429:
                n429+=1; gap=min(gap*1.25,8); print('429 gap',round(gap,2),flush=True); time.sleep(15); continue
            if e.code==404: json.dump({"mint":row.mint,"grad_ts":int(row.grad_ts),"bt":bt,"l":[],"err":404},open(fn,"w")); break
            time.sleep(5)
        except Exception as e: time.sleep(5)
    if i%50==0: print(i,flush=True)
print("DONE")
