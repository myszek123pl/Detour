"""Rebuild auditable standard-curve paths directly from the pinned corpus.

Unlike old scratchpad steps this file has no dependency on an unpublished
tok_jocry2 build. Qualifying tokens are selected by measured path coverage;
the resulting cohort is conditional and must not represent all launches.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import duckdb


def run(scratch, report_path):
    root = Path(scratch).resolve()
    data, work = root/'datasets'/'jocry', root/'work'
    work.mkdir(parents=True, exist_ok=True)
    (work/'tmp').mkdir(exist_ok=True)
    c = duckdb.connect()
    c.execute("SET TimeZone='UTC'; SET threads=4; SET memory_limit='4GB'")
    c.execute(f"SET temp_directory='{(work/'tmp').as_posix()}'")
    c.read_parquet(str(data/'trades'/'*.parquet')).create_view('raw')
    c.read_parquet(str(data/'tokens.parquet')).create_view('tokens')
    c.read_parquet(str(data/'postgard_snapshots.parquet')).create_view('pg')
    def rows(q):
        r = c.sql(q)
        return [dict(zip(r.columns, x)) for x in r.fetchall()]
    c.execute('''create temp table cov as select mint,count(*) n_raw,
      min(epoch(event_time)) first_t,max(epoch(event_time)) last_t,
      count(*) filter(where v_sol_bonding_curve>0 and v_tokens_bonding_curve>0) n_reserve,
      count(*) filter(where v_sol_bonding_curve>=30e9 and v_tokens_bonding_curve>0 and
        abs((v_sol_bonding_curve/1e9)*(v_tokens_bonding_curve/1e6)/(30*1073000000.0)-1)<.005) n_standard
      from raw group by mint''')
    c.execute('''create temp table selected as select t.*, v.* exclude(mint),
      row_number() over(order by detected_at,mint)::int mid
      from tokens t join cov v using(mint)
      where t.is_mayhem_mode=false and coalesce(t.top10_pct_suspect,false)=false
        and v.n_reserve>=.99*v.n_raw and v.n_standard>=.99*v.n_raw
        and v.first_t-epoch(t.detected_at) between 0 and 10 and v.n_raw>=2''')
    print('selected', c.sql('select count(*),sum(n_raw) from selected').fetchall(), flush=True)
    c.execute('''create temp table wallets as select w,row_number() over(order by w)::int wid
      from (select distinct r.user_wallet w from raw r join selected s using(mint)
        union select creator w from selected) where w is not null''')
    c.execute('''create temp table crh as select a.mint,
      count(b.mint) cr_prev_launch,
      count(b.mint) filter(where b.graduated_at<a.detected_at) cr_prev_grad_pit
      from selected a left join tokens b on a.creator=b.creator
        and b.detected_at<a.detected_at and b.detected_at>=a.detected_at-interval 30 day
      group by a.mint''')
    c.execute('''create temp table tk as select s.mid,s.mint,epoch(s.detected_at) L,
      epoch(s.graduated_at) G,s.is_mayhem_mode mh,s.is_cashback_enabled cb,
      s.dev_buy_pct_corrected dev_pct,s.launch_snipe_delta_sol snipe_delta,
      s.first_t,s.last_t,s.n_raw,s.n_reserve,s.n_standard,
      w.wid creator_wid,crh.cr_prev_launch,crh.cr_prev_grad_pit
      from selected s left join wallets w on w.w=s.creator left join crh using(mint)''')
    c.execute(f"copy tk to '{(work/'tok_jocry2.parquet').as_posix()}' (format parquet)")
    # Retain reserve states even when volume is missing/corrupt. Such rows
    # receive NULL sol and must not contribute to SOL-denominated features.
    c.execute(f'''copy (
      select s.mid,epoch(r.event_time) t,r.is_buy b,
        case when r.token_amount*r.price_sol>0 and
          r.sol_amount/(r.token_amount*r.price_sol) between .01 and 100 then r.sol_amount end sol,
        r.v_sol_bonding_curve/1e9 vs,r.v_tokens_bonding_curve/1e6 vt,
        coalesce(w.wid,-1) wid,
        coalesce(r.user_wallet='BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s',false) is_sys,
        r.id
      from raw r join selected s using(mint) left join wallets w on w.w=r.user_wallet
      where r.v_sol_bonding_curve>=30e9 and r.v_tokens_bonding_curve>0
        and abs((r.v_sol_bonding_curve/1e9)*(r.v_tokens_bonding_curve/1e6)/(30*1073000000.0)-1)<.005
      qualify row_number() over(partition by s.mid,r.tx_signature,r.v_sol_bonding_curve,r.v_tokens_bonding_curve,r.is_buy order by r.event_time,r.id)=1
      order by s.mid,r.event_time,r.id
      ) to '{(work/'paths_jocry.parquet').as_posix()}' (format parquet,compression zstd)''')
    c.execute(f'''copy (select s.mid,p.seconds_since_graduation ssg,
        p.price_native,p.liquidity_quote,p.liquidity_base,p.snapshot_time
      from pg p join selected s using(mint)
      where p.price_native>0 and not coalesce(p.incomplete_data,true)
        and p.seconds_since_graduation>=0
      order by s.mid,p.seconds_since_graduation)
      to '{(work/'postgrad_jocry.parquet').as_posix()}' (format parquet,compression zstd)''')
    report = dict(generated_at=datetime.now(timezone.utc).isoformat(),
      selection='non-mayhem; concentration not flagged; >=99% raw rows with positive reserves and standard invariant within0.5%; first capture0-10s; >=2 rows',
      counts=rows('''select count(*) tokens,sum(n_raw) raw_rows,
        count(*) filter(where graduated_at is not null) provider_graduated
        from selected''')[0],
      by_day=rows('''select cast(detected_at as date) day_utc,count(*) tokens,sum(n_raw) raw_rows
        from selected group by 1 order by 1'''),
      path_rows=c.sql(f"select count(*) from '{(work/'paths_jocry.parquet').as_posix()}'").fetchall()[0][0],
      caveats=['Selection uses complete-path coverage and is retrospective; this is a data-quality cohort, not a deployable token filter.',
        'State ordering is collector event_time/id, not on-chain slot/index.',
        'No execution at an unobserved terminal reserve state can establish actual realizable PnL.',
        'Own reserve impact replay holds other traders token/SOL changes fixed; a counterfactual approximation.',
        'The is_sys name is legacy: it flags a provider-excluded address whose identity has not been verified.'])
    dest=Path(report_path); dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,default=str),encoding='utf-8')
    print('prepared',report['counts'],'path_rows',report['path_rows'],flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('scratch');p.add_argument('--report',required=True)
    a=p.parse_args();run(a.scratch,a.report)
