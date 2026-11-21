"""Chronology regressions; these are synthetic checks, not trading evidence."""
from types import SimpleNamespace
import numpy as np
import pytest
from simlib import K0, P_GRAD, POOL_FEE, entry, exit_sim, pool_exit, pool_ratio, sell_value


def path(times, reserves):
    vs = np.asarray(reserves, dtype=float)
    return dict(t=np.asarray(times, dtype=float), vs=vs, vt=K0/vs,
                G=None, grad=False)


def test_entry_clock_includes_latency_even_without_an_intervening_trade():
    d = path([0, 10, 20], [30, 40, 50])
    e = entry(d, 0, 5, 1, 0, 0)
    assert e['j'] == 0
    assert e['state_t'] == 0
    assert e['tf'] == 5


def test_empty_path_has_no_fill():
    assert entry(path([], []), 0, 1, 1, 0, 0) is None


def test_ladder_cannot_replay_a_peak_before_its_first_sale_filled():
    d = path(range(10), [30, 40, 80, 30, 40, 30, 40, 40, 40, 40])
    e = entry(d, 0, 0, 1, 0, 0)
    r, kind, ntx = exit_sim(None, 0, d, e,
                           {'tps': [(1.2, .5), (4, .5)], 'tmax': 6}, 3, 0, 0, 1)
    # First sale arrives at t=4. The peak t=2 is already in the past.
    expected = sell_value(40+e['ds'], K0/40-e['dt'], e['y'], 0)-1
    assert r == pytest.approx(expected)
    assert kind == 'time'
    assert ntx == 2


def test_pool_price_is_the_last_observed_snapshot_without_clipping():
    p = SimpleNamespace(pg={1: (np.array([10., 20.]), P_GRAD*np.array([.05, 5.]))})
    assert np.isnan(pool_ratio(p, 1, 5))
    assert pool_ratio(p, 1, 15) == pytest.approx(.05)
    assert pool_ratio(p, 1, 20) == pytest.approx(5.)
    assert np.isnan(pool_ratio(p, 99, 30))


def test_delayed_stop_prices_the_actual_elapsed_time_since_migration():
    d = path([0, 1, 2], [40, 30, 30])
    d.update(grad=True, G=3)
    e = entry(d, 0, 0, 1, 0, 0)
    p = SimpleNamespace(pg_reserves={1: (np.array([0., 3., 5.]), np.array([85., 170., 340.]), np.full(3, 206.9e6))})
    r, kind, _ = exit_sim(p, 1, d, e, {'sl': .9}, 5, 0, 0, 1)
    # Signal at 1 + latency 5 reaches time 6, only 3s after migration.
    assert r == pytest.approx(pool_exit(e['y'], 2., POOL_FEE)-1)
    assert kind == 'grad_snapshot'


@pytest.mark.parametrize('lat',[1,5,30])
def test_entry_after_last_observation_is_not_a_fill(lat):
    assert entry(path([0,1],[30,40]),1,lat,1,0,0) is None


def test_timer_uses_clock_deadline_not_next_recorded_trade():
    d=path([0,10,13,20],[30,40,80,40])
    e=entry(d,0,5,1,0,0)
    r,kind,n=exit_sim(None,0,d,e,{'tmax':2},5,0,0,1)
    # Entry at5, decision at7, sell arrives12 (before high at13).
    expected=sell_value(40+e['ds'],K0/40-e['dt'],e['y'],0)-1
    assert r==pytest.approx(expected)
    assert (kind,n)==('time',1)


def test_terminal_state_is_censored_not_liquidated():
    d=path([0,1,2],[30,40,80]); e=entry(d,0,0,1,0,0)
    r,kind,n=exit_sim(None,0,d,e,{},0,0,0,1)
    assert np.isnan(r) and kind=='censored' and n==0


def test_future_graduation_does_not_make_terminal_path_known():
    d=path([0,1,2],[30,40,80]); d.update(G=100,grad=True)
    e=entry(d,0,0,1,0,0)
    r,kind,n=exit_sim(None,0,d,e,{},1,0,0,1)
    assert np.isnan(r) and kind=='censored'


def test_stop_execution_after_capture_end_is_censored():
    d=path([0,1,2],[40,30,30]); e=entry(d,0,0,1,0,0)
    r,kind,n=exit_sim(None,0,d,e,{'sl':.9},5,0,0,1)
    assert np.isnan(r) and kind=='censored' and n==0


def test_partial_realized_cash_does_not_hide_unresolved_remainder():
    d=path([0,1,2],[30,40,40]); e=entry(d,0,0,1,0,0)
    r,kind,n=exit_sim(None,0,d,e,{'tps':[(1.2,.5)]},0,0,0,1)
    assert np.isnan(r) and kind=='censored' and n==1


def test_pending_partial_sale_preserves_the_trailing_peak():
    d=path(range(10),[30,40,80,40,40,30,40,40,40,40])
    e=entry(d,0,0,1,0,0)
    r,kind,n=exit_sim(None,0,d,e,{'tps':[(1.2,.5)],'trail':.4,'arm':2},3,0,0,1)
    assert np.isfinite(r) and kind=='trail' and n==2


def test_stale_curve_state_is_not_treated_as_current():
    d=path([0,100],[30,40])
    assert entry(d,0,31,1,0,0) is None
    e=entry(d,0,0,1,0,0)
    r,kind,n=exit_sim(None,0,d,e,{'tmax':31},0,0,0,1)
    assert np.isnan(r) and kind=='censored'


def test_missing_and_stale_pool_reserves_are_not_synthetic_profits():
    d=path([0,1,2],[40,30,30]); d.update(G=3,grad=True)
    e=entry(d,0,0,1,0,0)
    for p in [SimpleNamespace(pg={1:(np.array([0]),np.array([P_GRAD]))}),
              SimpleNamespace(pg_reserves={1:(np.array([0]),np.array([85]),np.array([206.9e6]))})]:
        r,kind,n=exit_sim(p,1,d,e,{'sl':.9},50,0,0,1)
        assert np.isnan(r) and kind=='censored_pool' and n==0


@pytest.mark.parametrize('bad',[0,-1,np.nan,np.inf])
def test_invalid_reserves_reject_entry(bad):
    d=path([0,1],[30,40]);d['vt'][0]=bad
    assert entry(d,0,0,1,0,0) is None


def test_invalid_future_state_cannot_be_skipped_for_later_profit():
    d=path([0,1,2,3],[30,40,80,100]);d['vt'][1]=np.nan
    e=entry(d,0,0,1,0,0)
    r,kind,n=exit_sim(None,0,d,e,{'tps':[(2,1)]},0,0,0,1)
    assert np.isnan(r) and kind=='censored'


def test_round_trip_with_unchanged_reserves_loses_only_fees_and_tips():
    d=path([0,10,20],[30,30,30]); e=entry(d,0,0,1,.01,.001)
    r,kind,n=exit_sim(None,0,d,e,{'tmax':10},0,.01,.001,1)
    expected=((1/1.01)*.99-.001-(1+.001))/(1+.001)
    assert r==pytest.approx(expected)
    assert (kind,n)==('time',1)


@pytest.mark.parametrize('lat',[np.nan,np.inf,-1])
def test_invalid_latency_is_rejected(lat):
    d=path([0,1],[30,40])
    with pytest.raises(ValueError): entry(d,0,lat,1,0,0)
    with pytest.raises(ValueError): exit_sim(None,0,d,None,{},lat,0,0,1)


def test_on_top_buy_fee_preserves_the_total_budget():
    d=path([0,10,20],[30,30,30])
    e=entry(d,0,0,1,.01,0,fee_model='on_top')
    assert e['xin']*(1+.01)==pytest.approx(1)
    assert e['cost']==1


def test_unsorted_time_path_is_not_a_valid_entry():
    assert entry(path([1,0,2],[30,40,50]),0,0,1,0,0) is None



def test_large_curve_buy_cannot_overflow_standard_graduation_reserves():
    d=path([0,10,20],[110,110,110])
    assert entry(d,0,0,10,.01,0) is None


def test_on_top_is_the_default_buy_fee_formula():
    d=path([0,10],[30,30]); e=entry(d,0,0,1,.01,0)
    assert e['xin']==pytest.approx(1/1.01)
