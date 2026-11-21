import duckdb,sys
S=sys.argv[1]
c=duckdb.connect(f"{S}/work/jocry.duckdb")
c.sql("pragma memory_limit='11GB'; pragma threads=4")
c.sql(f"create or replace table trades_raw as select * from read_parquet('{S}/datasets/jocry/trades/*.parquet')")
print(c.sql("select count(*), count(distinct id), min(event_time), max(event_time) from trades_raw").fetchall())
print(c.sql("select source,count(*), sum((sol_amount is null)::int), sum((v_sol_bonding_curve is null)::int) from trades_raw group by 1").fetchall())
c.sql(f"create or replace table tokens as select * from read_parquet('{S}/datasets/jocry/tokens.parquet')")
c.sql(f"create or replace table migrations as select * from read_parquet('{S}/datasets/jocry/migrations.parquet')")
