"""Build clean per-token path + token tables for jocry corpus (window with reliable reserves/capture).
Usage: python3 -I b03_prep.py <scratch>"""
import duckdb,sys
S=sys.argv[1]
c=duckdb.connect(f"{S}/work/jocry.duckdb")
c.sql(f"pragma memory_limit='10GB'; pragma threads=4; pragma temp_directory='{S}/work/tmp'")
SYS=c.sql("select wid from wal where w='BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s'").fetchall()[0][0]
# token table with point-in-time creator history (only earlier launches in corpus)
c.sql("""create or replace table tok as
with k as (select m.mid, t.mint, t.creator, t.detected_at, epoch(t.detected_at) L, t.is_mayhem_mode mh, t.is_cashback_enabled cb,
   t.graduated_at, epoch(t.graduated_at) G, t.seconds_to_graduation sg, t.dev_buy_pct_corrected dev_pct, t.initial_buy_sol dev_sol,
   t.initial_top10_pct_corrected top10_prov, t.top10_pct_suspect, t.initial_holder_count hc_prov, t.launch_snipe_delta_sol snipe_delta,
   t.peak_market_cap_sol
 from tokens t join mints m using(mint))
select k.*,
  count(*) over (partition by creator order by detected_at rows between unbounded preceding and 1 preceding) cr_prev_launches,
  count(graduated_at) over (partition by creator order by detected_at rows between unbounded preceding and 1 preceding) cr_prev_grads_any
from k""")
# NOTE cr_prev_grads_any counts graduations of earlier tokens (even ones graduating after this token's launch) -> recompute strictly point-in-time below
c.sql("""create or replace table crh as
select a.mid, count(b.mid) cr_prev_launch, count(b.mid) filter (where b.graduated_at < a.detected_at) cr_prev_grad_pit
from tok a left join tok b on a.creator=b.creator and b.detected_at<a.detected_at and b.detected_at>=a.detected_at - interval 30 day
where a.detected_at>=timestamp '2026-07-04 00:00' group by 1""")
c.sql(f"""create or replace table paths as
select tr.mid, t, b, sol_raw sol, vs, vt, wid, (wid={SYS}) is_sys, id
from tr join tok using(mid)
where detected_at>=timestamp '2026-07-04 12:00' and vs is not null and vt is not null
qualify row_number() over (partition by tr.mid, sh, vs, vt, b order by t, id)=1
order by tr.mid, t, id""")
print(c.sql("select count(*), count(distinct mid) from paths").fetchall())
c.sql(f"copy (select * from paths) to '{S}/work/paths_jocry.parquet' (format parquet, compression zstd)")
c.sql(f"""copy (select tok.*, crh.cr_prev_launch, crh.cr_prev_grad_pit from tok left join crh using(mid) where detected_at>=timestamp '2026-07-04 12:00') to '{S}/work/tok_jocry.parquet' (format parquet)""")
# postgrad snapshots for graduated tokens: price ratio table
c.sql(f"""copy (select m.mid, s.seconds_since_graduation ssg, s.price_native, s.liquidity_quote from read_parquet('{S}/datasets/jocry/postgard_snapshots.parquet') s join mints m using(mint) where s.price_native>0 and s.seconds_since_graduation<7200) to '{S}/work/postgrad_jocry.parquet' (format parquet)""")
