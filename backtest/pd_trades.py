"""Step 2: trade-level phase features per event. usage: python3 -I pd_trades.py <data_dir> <work_dir>"""
import sys, numpy as np, pandas as pd, duckdb
D, W = sys.argv[1], sys.argv[2]
E = pd.read_parquet(f"{W}/events.parquet").reset_index(drop=True); E["eid"] = E.index
con = duckdb.connect()
con.register("ev", E[["eid","tok","kind","t_start","t_trig","t_peak"]])
con.sql(f"""create table T as select wallet w, token_address tok, side, amount_usd a, epoch(ts)::bigint ts from '{D}/trades-00*.parquet'""")
# first appearance of wallet anywhere (dataset-level) and distinct tokens before
con.sql("create table wf as select w, min(ts) f0 from T group by 1")
con.sql("""create table X as select ev.eid, ev.kind, ev.t_start S, ev.t_trig Tg, ev.t_peak Pk, T.w, T.side, T.a, T.ts,
   case when T.ts < ev.t_start - 3600 then 'pre2' when T.ts < ev.t_start then 'pre' when T.ts < ev.t_trig then 'pump'
        when T.ts < ev.t_trig + 3600 then 'post1' when T.ts < ev.t_trig + 7200 then 'post2' else 'x' end ph
   from ev join T on T.tok=ev.tok and T.ts >= ev.t_start - 7200 and T.ts < ev.t_trig + 7200""")
print(con.sql("select kind, ph, count(*), count(distinct eid) from X group by 1,2 order by 1,2").fetchall())
# wallet first trade in token (whole sample, any time) per event
con.sql("""create table FT as select ev.eid, T.w, min(T.ts) ft, min(case when side='buy' then T.ts end) fb from ev join T on T.tok=ev.tok group by 1,2""")
con.sql("""create table XF as select X.*, FT.ft, FT.fb, wf.f0 from X join FT using(eid,w) join wf using(w)""")
con.sql("""create table PH as select eid, kind, ph,
   count(*) n, sum(a) usd, sum(case when side='buy' then a else 0 end) buy_usd, sum(case when side='sell' then a else 0 end) sell_usd,
   count(distinct case when side='buy' then w end) nb, count(distinct case when side='sell' then w end) ns, count(distinct w) nw,
   median(a) med_a, avg(case when side='buy' then a end) mean_buy, max(a) max_a,
   avg(case when ft >= (case ph when 'pre2' then S-7200 when 'pre' then S-3600 when 'pump' then S when 'post1' then Tg else Tg+3600 end) then 1.0 else 0.0 end) new_tok_share_trades,
   sum(case when f0 >= (case ph when 'pre2' then S-7200 when 'pre' then S-3600 when 'pump' then S when 'post1' then Tg else Tg+3600 end) then a else 0 end)/sum(a) fresh_ds_usd_share
   from XF where ph<>'x' group by 1,2,3""")
con.sql("""create table WP as select eid, ph, w, sum(a) a from X where ph<>'x' group by 1,2,3""")
con.sql("""create table CONC as select eid, ph, max(a)/sum(a) top1, sum(a) filter(where r<=5)/sum(a) top5, sum((a/s)*(a/s)) hhi
   from (select *, sum(a) over(partition by eid,ph) s, row_number() over(partition by eid,ph order by a desc) r from WP) group by 1,2""")
P = con.sql("select PH.*, CONC.top1, CONC.top5, CONC.hhi from PH left join CONC using(eid,ph)").df()
P.to_parquet(f"{W}/phase_feats.parquet")
# wallet-level table per event for seller analysis
WL = con.sql("""select eid, kind, w, min(ft) ft, min(fb) fb, min(f0) f0, min(S) S, min(Tg) Tg, min(Pk) Pk,
   sum(case when side='buy' then a else 0 end) buy_all, sum(case when side='sell' then a else 0 end) sell_all,
   sum(case when side='buy' and ph in ('pre2','pre') then a else 0 end) buy_pre,
   sum(case when side='buy' and ph='pump' then a else 0 end) buy_pump,
   sum(case when side='buy' and ph in ('post1','post2') then a else 0 end) buy_post,
   sum(case when side='sell' and ph in ('pre2','pre') then a else 0 end) sell_pre,
   sum(case when side='sell' and ph='pump' then a else 0 end) sell_pump,
   sum(case when side='sell' and ph='post1' then a else 0 end) sell_post1,
   sum(case when side='sell' and ph='post2' then a else 0 end) sell_post2,
   sum(case when side='sell' and ts>=Pk-900 and ts < Pk+3600 then a else 0 end) sell_peak1h,
   count(*) n
   from XF where ph<>'x' group by 1,2,3""").df()
WL.to_parquet(f"{W}/wallet_event.parquet")
print(len(P), len(WL))
