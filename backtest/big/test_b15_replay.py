"""Mianowniki muszą zachować nieznane wyniki i brak wykonania."""
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from b15_replay import SCHEMA, rules, split_name, TRAIN_END, TEST_START, summarize


def test_frozen_grid_has_32_rules_and_an_explicit_horizon():
    specs=rules(600)
    assert len(specs)==32
    assert specs['hold']['tmax']==600
    assert specs['time30_sl0.7']['tmax']==30
    assert specs['time3600_sl0.7']['tmax']==600
    assert specs['ladderB']['tps']==[(2.,.5),(5.,.25)]


def test_temporal_slices_are_half_open():
    assert split_name(TRAIN_END-1)=='train'
    assert split_name(TRAIN_END)=='embargo'
    assert split_name(TEST_START)=='test'


def test_summary_does_not_drop_censored_or_count_no_fill_as_loss(tmp_path):
    parts=tmp_path/'parts';parts.mkdir()
    rows=[dict(mid=i,decision_t=1.,launch_t=0.,lv=.1,lat=1,rule_id=0,
               filled=f,r=r,kind=k,n_sells=0,split='train')
          for i,(f,r,k) in enumerate([(True,.2,'time'),(True,None,'censored'),(False,None,'no_fill')])]
    pq.write_table(pa.Table.from_pylist(rows,schema=SCHEMA),parts/'part-00000.parquet')
    out=tmp_path/'out'
    summarize(tmp_path,out,{'tag':'test','rules':{'hold':{}},'n_selected_tokens':3},{'signals_0.10':3},1.)
    r=pd.read_csv(out/'test_summary.csv').iloc[0]
    assert r.n_signals==3 and r.n_filled==2 and r.n_no_fill==1
    assert r.n_resolved==1 and r.n_censored==1
    assert r.mean_resolved==pytest.approx(.2)
    assert r.missing_minus100pct_scenario==pytest.approx(-.4)
    m=json.loads((out/'test_manifest.json').read_text())
    assert m['outcome_rows']==3
