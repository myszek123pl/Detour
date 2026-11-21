import numpy as np
def block_ids(L, hours=3.0, t0=None):
    t0 = L.min() if t0 is None else t0
    return ((L - t0)//(hours*3600)).astype(int)
def boot_mean(x, blocks, nrep=1000, seed=1, stat=np.mean):
    """cluster (block) bootstrap CI for mean (or other stat) of x"""
    rng=np.random.default_rng(seed)
    x=np.asarray(x,float); blocks=np.asarray(blocks)
    ub,inv=np.unique(blocks,return_inverse=True)
    nb=len(ub)
    sums=np.bincount(inv,weights=x,minlength=nb); cnt=np.bincount(inv,minlength=nb).astype(float)
    if stat is np.mean:
        res=np.empty(nrep)
        for r in range(nrep):
            k=rng.integers(0,nb,nb)
            c=cnt[k].sum(); res[r]=sums[k].sum()/c if c>0 else np.nan
        return np.nanpercentile(res,[2.5,97.5])
    # generic: resample blocks, concat
    idx=[np.nonzero(inv==b)[0] for b in range(nb)]
    res=np.empty(nrep)
    for r in range(nrep):
        k=rng.integers(0,nb,nb)
        res[r]=stat(x[np.concatenate([idx[q] for q in k])])
    return np.nanpercentile(res,[2.5,97.5])
def fmt_ci(m, ci, pct=True, d=1):
    f=100 if pct else 1
    return f"{m*f:.{d}f} [{ci[0]*f:.{d}f}, {ci[1]*f:.{d}f}]"
