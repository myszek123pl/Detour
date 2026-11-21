"""Build Oct-15 (pumpdata.fun sample) paths in the same schema as the jocry prep. python3 -I b10_oct.py <scratch>"""
import duckdb, sys
S=sys.argv[1]; D=f"{S}/datasets/pumpdatafun"
c=duckdb.connect(f"{S}/work/oct.duckdb")
c.sql(f"pragma memory_limit='10GB'; pragma threads=4; pragma temp_directory='{S}/work/tmp'")
W="'So11111111111111111111111111111111111111112'"
# per-second slot anchors for sub-second time
c.sql(f"""create or replace table anchors as select ts, min(slot) s0 from (select ts,slot from '{D}/data/*.parquet' union all select ts,slot from '{D}/events/*.parquet') group by 1""")
c.sql("""create or replace table anc2 as select ts, s0, coalesce(lead(s0) over (order by ts), s0+5) s1 from anchors""")
c.sql("create or replace macro tmap(sl, ts_) as (select ts+ (sl-s0)*1.0/greatest(s1-s0,1) from anc2 where anc2.ts=ts_)")
c.sql(f"""create or replace table cv as
select d.mint, d.ts, d.slot, d.idx, d.seq, (d.side='buy') b, d.sol_lamports/1e9 sol, d.token_amount/1e6 tokq, d.wallet, d.r1/1e9 vs, d.r2/1e6 vt, d.r3/1e9 real_sol, d.tip_lamports,
   d.ts + (d.slot-a.s0)*1.0/greatest(a.s1-a.s0,1) t
from '{D}/data/*.parquet' d join anc2 a using(ts)
where d.venue='curve' and not d.failed and d.quote_mint={W} and d.r1 is not null""")
c.sql(f"""create or replace table lh as
select l.mint, l.creator, l.ts, l.slot, l.idx, l.ts + (l.slot-a.s0)*1.0/greatest(a.s1-a.s0,1) L from '{D}/launches/*.parquet' l join anc2 a using(ts) where l.quote_mint={W}""")
c.sql(f"""create or replace table comp as
select e.a mint, e.ts + (e.slot-a.s0)*1.0/greatest(a.s1-a.s0,1) G from '{D}/events/*.parquet' e join anc2 a using(ts) where e.kind='complete'""")
# standard-curve flag: invariant holds in >=90% of rows
c.sql("""create or replace table stdf as select mint, avg((abs(vs*vt/(30.0*1073000000.0)-1)<0.005)::int) inv, count(*) n from cv group by 1""")
c.sql("""create or replace table tk0 as select row_number() over (order by L, mint)::int mid, lh.*, comp.G, s.inv, s.n from lh left join comp using(mint) left join stdf s using(mint) where lh.L < (select min(L) from lh)+14*3600""")
c.sql("""create or replace table wal as select wallet w,(row_number() over (order by wallet))::int wid from (select distinct wallet from cv union select distinct creator from lh)""")
# dev buy pct: creator buys within 3 slots of create
c.sql("""create or replace table devb as select tk0.mint, sum(cv.tokq)/1e9*100 dev_pct, sum(cv.sol) dev_sol from tk0 join cv on cv.mint=tk0.mint and cv.wallet=tk0.creator and cv.slot between tk0.slot and tk0.slot+3 and cv.b group by 1""")
c.sql("""create or replace table tok as
select t.mid, t.mint, t.L, t.G, false mh, w.wid creator_wid, coalesce(d.dev_pct,0) dev_pct, 0 cb, NULL::double snipe_delta, t.inv, t.n,
  (count(*) over (partition by t.creator order by t.L rows between unbounded preceding and 1 preceding)) cr_prev_launch,
  (count(*) filter (where false) over ()) cr_prev_grad_pit
from tk0 t left join devb d using(mint) left join wal w on w.w=t.creator""")
# point-in-time creator grads
c.sql("""create or replace table crg as select a.mid, count(b.mid) filter (where b.G < a.L) g from tok a left join tok b on a.creator_wid=b.creator_wid and b.L<a.L group by 1""")
c.sql("""create or replace table tokf as select tok.* exclude(cr_prev_grad_pit), coalesce(crg.g,0) cr_prev_grad_pit from tok left join crg using(mid)""")
c.sql(f"""copy (select * from tokf where inv>=0.9) to '{S}/work/oct_tok.parquet' (format parquet)""")
c.sql(f"""copy (select m.mid, cv.t, cv.b, cv.sol, cv.vs, cv.vt, w.wid, false is_sys from cv join tokf m using(mint) join wal w on w.w=cv.wallet where m.inv>=0.9 order by m.mid, cv.slot, cv.idx, cv.seq) to '{S}/work/oct_paths.parquet' (format parquet, compression zstd)""")
# post-graduation pool prices
c.sql(f"""copy (select m.mid, p.ts + (p.slot-a.s0)*1.0/greatest(a.s1-a.s0,1) - m.G ssg, (p.r2+p.r3)/1e9/(p.r1/1e6) price_native, 0.0 liquidity_quote
  from '{D}/data/*.parquet' p join anc2 a using(ts) join tokf m on m.mint=p.mint where p.venue='pumpswap' and not p.failed and p.migration_pool and m.G is not null and p.r1>0 and p.r2 is not null and p.r3 is not null and m.inv>=0.9 and p.ts+(p.slot-a.s0)*1.0/greatest(a.s1-a.s0,1) >= m.G order by 1,2) to '{S}/work/oct_postgrad.parquet' (format parquet)""")
print(c.sql("select count(*), sum((G is not null)::int), sum((inv>=0.9)::int), sum((inv is null)::int) from tokf").fetchall())
print(c.sql(f"select count(*) from '{S}/work/oct_paths.parquet'").fetchall(), c.sql(f"select count(distinct mid), count(*) from '{S}/work/oct_postgrad.parquet'").fetchall())
# failed tx stats for curve (by time since launch bucket) and error mix
c.sql(f"""create or replace table fl as select f.mint, f.ts, f.error, f.failed from '{D}/data/*.parquet' f where f.venue='curve' and (f.failed or f.quote_mint={W})""")
c.sql(f"""copy (select t.L is not null has_l, case when f.ts-t.L<5 then '0-5s' when f.ts-t.L<30 then '5-30s' when f.ts-t.L<300 then '30s-5m' when f.ts-t.L<3600 then '5m-1h' else '>1h' end age,
   failed, count(*) n from fl f left join lh t using(mint) group by all) to '{S}/work/oct_failstats.csv' (header)""")
c.sql(f"copy (select error, count(*) n from fl where failed group by 1 order by 2 desc limit 15) to '{S}/work/oct_errors.csv' (header)")
