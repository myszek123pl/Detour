import duckdb
B='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/'
W=B+'w27/'; D=B+'datasets/solana-memecoin-dataset/repo/data/'
c=duckdb.connect()
c.sql(f"create view t as select * from '{W}t3.parquet'")
def agg(name,cond):
    out=[]
    for ph,pc in [('pre','ts<cap'),('post','ts>=cap and ts<cap+900')]:
        for s in ['buy','sell']:
            out.append(f"coalesce(sum(case when side='{s}' and {pc} and ({cond}) then usd end),0) {name}_{ph}_{s}")
    out.append(f"count(distinct case when ts<cap and ({cond}) then wallet end) {name}_n")
    out.append(f"count(distinct case when side='sell' and ts<cap and ({cond}) then wallet end) {name}_nsell")
    return ','.join(out)
q=f"""create table tf as select tok, any_value(cap) cap, min(ts)-any_value(cap) tmin, max(ts)-any_value(cap) tmax, count(*) ntr,
 {agg('all','true')}, {agg('ins',"wt='insider'")}, {agg('sm',"wt='smart_money'")}, {agg('cl','incl')}, {agg('early','rk<=10')}, {agg('early25','rk<=25')}
 from t group by tok"""
c.sql(q)
c.sql(f"""create table out as select tf.*, k.* exclude(token_address) from tf join '{D}tokens.parquet' k on k.token_address=tf.tok and epoch(k.captured_at)=tf.cap""")
c.sql(f"copy out to '{W}tokfeat.parquet'")
print(c.sql("select count(*), count(distinct tok) from out").fetchall())
print(c.sql("select count(*) filter(where cl_n>0), count(*) filter(where ins_n>0), count(*) filter(where early_n>0), avg(tmin), median(tmin), median(tmax) from out").fetchall())
