import pandas as pd, numpy as np
def md(df, nd=3):
    df=df.reset_index() if not isinstance(df.index,pd.RangeIndex) else df
    def f(x):
        if isinstance(x,(float,np.floating)):
            if np.isnan(x): return ""
            return f"{x:.{nd}f}" if abs(x)<1000 else f"{x:,.0f}"
        return str(x)
    h="| "+" | ".join(map(str,df.columns))+" |"; s="|"+"|".join(["---"]*len(df.columns))+"|"
    return "\n".join([h,s]+["| "+" | ".join(f(v) for v in r)+" |" for r in df.itertuples(index=False)])
