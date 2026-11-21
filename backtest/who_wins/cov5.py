import duckdb,sys
D=sys.argv[1]
c=duckdb.connect()
c.sql(f"create view tr as select * from read_parquet('{D}/trades-*.parquet')")
c.sql(f"create view tkall as select * from read_parquet('{D}/tokens.parquet')")
c.sql("create table core as select token_address, min(captured_at::timestamptz) cap, min(time_since_launch_sec) tsl from tkall group by 1")
c.sql("create table tt as select token_address, count(*) n, min(ts) f, max(ts) l from tr group by 1")
c.sql("create table j as select tt.*, core.cap, core.tsl, epoch(tt.f)-(epoch(core.cap)-core.tsl) first_off, epoch(tt.l)-epoch(core.cap) last_off from tt left join core using(token_address)")
print(c.sql("select n between 95 and 110 spike, count(*), median(first_off), quantile_cont(first_off,[.1,.25,.75,.9]), median(last_off) from j where cap is not null group by 1"))
print(c.sql("select (first_off between -60 and 120) near_start, count(*), sum(n) from j where cap is not null group by 1"))
print(c.sql("select count(*) filter(epoch(l)-epoch(f)>=3600), count(*) filter(epoch(l)-epoch(f)>=6*3600), count(*) filter(epoch(l)-epoch(f)>=86400) from j where cap is not null"))
print(c.sql("select quantile_cont(last_off,[.05,.25,.5,.75,.95]) from j where cap is not null"))
# ext tokens: span
print(c.sql("select count(*) filter(epoch(l)-epoch(f)>=3600), count(*) filter(epoch(l)-epoch(f)>=86400), count(*) from j where cap is null"))
