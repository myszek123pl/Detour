import duckdb,sys
S=sys.argv[1]
c=duckdb.connect(f"{S}/work/jocry.duckdb")
c.sql(f"pragma memory_limit='10GB'; pragma threads=4; pragma temp_directory='{S}/work/tmp'; pragma max_temp_directory_size='15GB'")
c.sql("create or replace table mints as select mint, row_number() over (order by detected_at, mint)::int mid from tokens")
c.sql("""create or replace table wal as select user_wallet w, (row_number() over (order by user_wallet))::int wid from (select distinct user_wallet from trades_raw)""")
c.sql("""create or replace table tr as
select m.mid, epoch(event_time) t, r.is_buy b, r.sol_amount/1e0 sol_raw, r.token_amount tok_raw,
  w.wid, r.v_sol_bonding_curve/1e9 vs, r.v_tokens_bonding_curve/1e6 vt, r.price_sol px,
  hash(r.tx_signature) sh, r.id, r.seconds_since_launch ssl
from trades_raw r join mints m using(mint) join wal w on w.w=r.user_wallet
order by m.mid, r.event_time, r.id""")
print(c.sql("select count(*) from tr").fetchall())
c.sql("drop table trades_raw")
c.sql("checkpoint")
