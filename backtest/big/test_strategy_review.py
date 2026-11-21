import numpy as np
import pandas as pd
import pytest
from b20_strategy_review import metrics, paired


def test_unknown_positions_keep_their_denominators():
    g=pd.DataFrame(dict(r=[-.2,.4,np.nan,np.nan],filled=[True,True,True,False],
                        decision_t=[0.,1.,86400.,86401.]))
    m=metrics(g)
    assert (m['n_signals'],m['n_filled'],m['n_resolved'],m['n_censored'],m['n_no_fill'])==(4,3,2,1,1)
    assert m['mean_resolved']==pytest.approx(.1)
    assert m['missing_minus100pct_scenario']==pytest.approx((.2-1)/3)


def test_latency_comparison_uses_identical_resolved_support():
    g=pd.DataFrame(dict(mid=[1,1,1,2,2,2],lv=[.1]*6,rule_id=[0]*6,
        lat=[1,5,30]*2,r=[.1,.05,-.1,10.,np.nan,10.]))
    r=paired(g)
    assert r['n_common']==1
    assert r['mean_delta30_minus1']==pytest.approx(-.2)
    assert r['means']['1']==pytest.approx(.1)
