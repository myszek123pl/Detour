import duckdb,sys
W=sys.argv[1]; D=sys.argv[2]
c=duckdb.connect(W+'/who.duckdb')
c.sql("pragma threads=4; pragma memory_limit='10GB'")
def p(title,q):
    print('###',title); print(c.sql(q).df().to_string(float_format=lambda x:f'{x:,.3f}')); print()
c.sql("""create or replace table WX as select WU.*, W2.ntr, W2.fast, W2.med_gap, W2.ngap, W2.active_span,
 case when WU.ntok>=100 or W2.ntr>=300 then '4:heavy/bot-like (>=100 tok or >=300 trades)' when WU.ntok>=20 then '3:active (20-99 tok)' when WU.ntok>=5 then '2:regular (5-19)' when WU.ntok>=2 then '1:occasional (2-4)' else '0:one-token' end cls,
 (n_snipe::double/ntok) snipe_share from WU join W2 using(w)""")
def wdim(title, expr, where='true'):
    p(title, f"""select {expr} b, count(*) wallets, sum(buy)/1e6 buyM, sum(pnl)/1e6 netM, sum(pnl)/sum(buy) roi, median(pnl) med_pnl, avg((pnl>0)::int) pct_profit,
     avg((n_exit>0)::int) any_exit, avg((pnl>0)::int) filter(n_exit>0) pp_exiters, sum(pnl) filter(pnl>0)/1e6 gwM, sum(pnl) filter(pnl<0)/1e6 glM, median(buy) med_buy, median(ntok) med_ntok
     from WX where {where} group by 1 order by 1""")
wdim("wallet activity class", "cls")
wdim("wallet activity class, exiters only (n_exit>0)", "cls", "n_exit>0")
wdim("median gap between trades", "case when ngap<5 then '0:<5 gaps' when med_gap<=1 then '1:<=1s' when med_gap<=10 then '2:1-10s' when med_gap<=120 then '3:10s-2m' when med_gap<=3600 then '4:2m-1h' else '5:>1h' end")
wdim("sniper share (entries within 2s of first logged trade)", "case when snipe_share=0 then '0:none' when snipe_share<0.2 then '1:<20%' when snipe_share<0.5 then '2:20-50%' else '3:>=50%' end", "ntok>=3")
wdim("fast-trade share (gaps<=1s)", "case when ngap<20 then '0:<20 gaps' when fast/ngap<0.1 then '1:<10%' when fast/ngap<0.5 then '2:10-50%' else '3:>=50%' end")
wdim("total wallet buy size", "case when buy<10 then '0:<$10' when buy<100 then '1:$10-100' when buy<1000 then '2:$100-1k' when buy<10000 then '3:$1k-10k' when buy<100000 then '4:$10k-100k' else '5:>$100k' end")
# winners profile
c.sql("create or replace table top as select * from WX order by pnl desc limit 7000")
c.sql("create or replace table bot as select * from WX order by pnl asc limit 7000")
p("top 7000 (1%) winners vs bottom 7000 vs all","""select 'top1%' g, count(*) n, sum(pnl)/1e6 netM, median(buy) med_buy, median(ntok) med_ntok, median(med_gap) med_gap, avg(snipe_share) snipe, avg((n_exit=ntok)::int) all_exited, avg(n_win::double/ntok) winrate from top
 union all select 'bottom1%', count(*), sum(pnl)/1e6, median(buy), median(ntok), median(med_gap), avg(snipe_share), avg((n_exit=ntok)::int), avg(n_win::double/ntok) from bot
 union all select 'all', count(*), sum(pnl)/1e6, median(buy), median(ntok), median(med_gap), avg(snipe_share), avg((n_exit=ntok)::int), avg(n_win::double/ntok) from WX""")
p("winner class mix","select cls, count(*) n, sum(pnl)/1e6 netM from top group by 1 order by 1")
p("loser class mix","select cls, count(*) n, sum(pnl)/1e6 netM from bot group by 1 order by 1")
# who funds winners: share of loss by class
p("share of gross loss / gross win by class","""select cls, sum(pnl) filter(pnl>0)/1e6 gw, sum(pnl) filter(pnl<0)/1e6 gl, count(*) n from WX group by 1 order by 1""")
# token-level: for tokens where top1% wallets made profit, who lost? net pnl by class of wallets on top-winner tokens
p("repeat winners: wallets with >=10 tokens, share profitable & ROI","""select count(*) n, avg((pnl>0)::int) pp, sum(pnl)/sum(buy) roi, median(pnl) from WX where ntok>=10""")
# funding clusters
c.sql(f"create or replace table wf as select * from read_parquet('{D}/wallet_funding.parquet')")
c.sql(f"create or replace table wl as select * from read_parquet('{D}/wallets.parquet')")
p("funding table","select count(*) edges, count(distinct wallet) wallets, count(distinct funder) funders, median(amount_sol) from wf")
c.sql("create or replace table fc as select funder, count(distinct wallet) nw from wf group by 1")
p("funder fanout","select nw, count(*) from fc group by 1 order by 1 limit 12")
c.sql("""create or replace table wcl as select wallet w, max(fc.nw) maxfan, count(distinct funder) nfund from wf join fc using(funder) group by 1""")
p("funding cluster membership vs PnL","""select case when wcl.w is null then '0:no funding data' when maxfan>=3 then '2:shared funder (>=3 wallets)' when maxfan=2 then '1:shared funder (2)' else '1b:unique funder' end b,
 count(*) wallets, sum(buy)/1e6 buyM, sum(pnl)/1e6 netM, sum(pnl)/sum(buy) roi, median(pnl) med_pnl, avg((pnl>0)::int) pp, median(ntok) med_ntok, median(buy) med_buy from WX left join wcl using(w) group by 1 order by 1""")
p("wallets.parquet type vs PnL","""select coalesce(wl.wallet_type,'unlabeled') t, count(*) wallets, sum(buy)/1e6 buyM, sum(pnl)/1e6 netM, sum(pnl)/sum(buy) roi, median(pnl) med_pnl, avg((pnl>0)::int) pp, avg((n_exit>0)::int) any_exit, median(ntok) med_ntok, median(buy) med_buy, sum(pnl) filter(pnl>0)/1e6 gwM from WX left join wl on wl.address=WX.w group by 1 order by 1""")
p("labeled wallets share among top 1%","select coalesce(wl.wallet_type,'unlabeled') t, count(*) from top left join wl on wl.address=top.w group by 1")
p("cluster size dist among top1%","select case when wcl.w is null then 'none' else 'in funding table' end, count(*) from top left join wcl using(w) group by 1")
