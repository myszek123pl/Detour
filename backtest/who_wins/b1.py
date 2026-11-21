import duckdb,sys
W=sys.argv[1]; D=sys.argv[2]
c=duckdb.connect(W+'/who.duckdb')
c.sql("pragma threads=4; pragma memory_limit='10GB'")
def p(q):
    print(c.sql(q).df().to_string()); print()
# wallet behavioural features from row level
c.sql("""create or replace table wfeat as
 select w, count(*) ntr, count(distinct tk) ntok2,
  count(*) filter(gap<=1.0) fast, median(gap) med_gap, count(*) filter(gap is not null) ngap,
  count(*) filter(not isb)::double/count(*) sellshare,
  epoch(to_timestamp(max(t)))-epoch(to_timestamp(min(t))) active_span
 from (select w,tk,isb,t, t - lag(t) over (partition by w order by t) gap from tr0) group by w""")
c.sql("""create or replace table P as select wt2.*, tflag.conserve, tflag.iscore ic2, wt2.fb - wt2.tf entry_delay, (wt2.fs - wt2.fb) hold_first, (wt2.ls - wt2.fb) hold_last, (wt2.tl - wt2.tf) tspan
 from wt2 join tflag using(tk) where wt2.nb>0""")
p("select count(*), count(distinct w), count(distinct tk) from P")
p("select conserve, count(*) pairs, count(distinct w) wallets, sum(buy)/1e6 buyM, sum(sell)/1e6 sellM, sum(pnl)/1e6 pnlM from P group by 1")
# link wallet features
c.sql("create or replace table W2 as select * from wfeat")
# wallet-level in U
c.sql("""create or replace table WU as select w, count(*) ntok, sum(nb) nb, sum(ns) ns, sum(buy) buy, sum(sell) sell, sum(pnl) pnl,
  count(*) filter(ns>0) n_exit, count(*) filter(pnl>0) n_win, median(buy) med_pos,
  count(*) filter(entry_delay<=2) n_snipe, count(*) filter(brank<=10) n_top10, min(fb) t0
  from P where conserve group by w""")
p("select count(*), quantile_cont(ntok,[.5,.9,.99]), count(*) filter(pnl>0) win, sum(pnl)/1e6 from WU")
