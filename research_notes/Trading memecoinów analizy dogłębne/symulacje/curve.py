"""pump.fun bonding curve math. Params from pump-public-docs PUMP_PROGRAM_README (Global account)."""
VS0=30.0; VT0=1073000000.0; RT0=793100000.0; SUPPLY=1e9
K=VS0*VT0
F=0.0125   # 0.95% protocol + 0.30% creator (fees.png), flat on curve
VT_END=VT0-RT0          # 279.9M
VS_END=K/VT_END
def state_at_token_progress(p):   # p in [0,1], token-based
    vt=VT0-RT0*p; return K/vt, vt
def price(vs,vt): return vs/vt
def mcap(vs,vt): return vs*SUPPLY/vt
def real_sol(vs): return vs-VS0
def buy_exact_in(vs,vt,S,f=F):
    net=S/(1+f)  # fee added on top of curve cost: total=cost*(1+f)
    vs2=vs+net; vt2=K/vs2
    return vt-vt2,vs2,vt2   # tokens, new state
def sell(vs,vt,n,f=F):
    vt2=vt+n; vs2=K/vt2; gross=vs-vs2
    return gross*(1-f),vs2,vt2
def impact_buy(vs,vt,S):
    n,_,_=buy_exact_in(vs,vt,S); eff=S/n; return eff/price(vs,vt)-1, n
def impact_buy_nofee(vs,vt,S):
    vs2=vs+S; n=vt-K/vs2; return (S/n)/price(vs,vt)-1
def impact_sell(vs,vt,n):
    out,_,_=sell(vs,vt,n); eff=out/n; return 1-eff/price(vs,vt), out
def breakeven(vs,vt,S):
    n,vs1,vt1=buy_exact_in(vs,vt,S)
    # find state (via others' buying) where our net sell proceeds == S
    lo,hi=vt_end=VT_END,vt1
    def proceeds(vt2):
        vs2=K/vt2; return (vs2-K/(vt2+n))*(1-F)
    if proceeds(VT_END)<S: return None
    for _ in range(200):
        mid=(lo+hi)/2
        if proceeds(mid)>=S: lo=mid
        else: hi=mid
    vt2=hi; vs2=K/vt2
    others=vs2-vs1
    return dict(mult_price=price(vs2,vt2)/price(vs1,vt1), mult_entry=price(vs2,vt2)/(S/n),
                mult_mcap_vs_start=mcap(vs2,vt2)/mcap(vs,vt), others_sol=others, mcap2=mcap(vs2,vt2),
                n=n, prog2=(VT0-vt2)/RT0)
if __name__=="__main__":
    out=[]
    P=out.append
    P("### T0 derived constants")
    P(f"k = {K:.6e} (SOL*tokens); VT_end={VT_END:,.0f}; VS_end={VS_END:.4f} SOL; real SOL raised at completion={VS_END-VS0:.4f}")
    P(f"start price={price(VS0,VT0):.4e} SOL/token; start mcap={mcap(VS0,VT0):.3f} SOL; end price={price(VS_END,VT_END):.4e}; end mcap={mcap(VS_END,VT_END):.2f} SOL; price multiple start->end={price(VS_END,VT_END)/price(VS0,VT0):.2f}x")
    P("\n### T1 price/mcap vs progress (token-based progress = tokens sold / 793.1M)")
    P("| Progress % | Real SOL raised | Tokens sold (M) | Price (SOL/token) | Price x vs start | Mcap (SOL) | Mcap @ $150/SOL | Mcap @ $200/SOL |")
    P("|---|---|---|---|---|---|---|---|")
    for pc in list(range(0,101,5)):
        vs,vt=state_at_token_progress(pc/100)
        P(f"| {pc} | {real_sol(vs):.2f} | {RT0*pc/100/1e6:.1f} | {price(vs,vt):.3e} | {price(vs,vt)/price(VS0,VT0):.2f} | {mcap(vs,vt):.1f} | ${mcap(vs,vt)*150:,.0f} | ${mcap(vs,vt)*200:,.0f} |")
    P("\n### T1b SOL-based progress (real SOL / 85) vs token-based")
    P("| Real SOL raised | % of 85 SOL | % tokens sold |")
    P("|---|---|---|")
    for s in [1,5,10,20,30,40,50,60,70,80,85]:
        vs=VS0+s; vt=K/vs; P(f"| {s} | {s/85*100:.1f} | {(VT0-vt)/RT0*100:.1f} |")
    levels=[0,10,25,50,75,90,95]
    sizes=[0.1,0.25,0.5,1,2,5,10]
    P("\n### T2 BUY price impact incl. 1.25% fee (effective avg price vs current spot, %). Cell: impact% / tokens received (M)")
    P("| Buy SOL \\ Progress | "+" | ".join(f"{l}%" for l in levels)+" |"); P("|---|"+"---|"*len(levels))
    for S in sizes:
        row=[]
        for l in levels:
            vs,vt=state_at_token_progress(l/100)
            if S/(1+F)>VS_END-vs: row.append("exceeds remaining"); continue
            im,n=impact_buy(vs,vt,S); row.append(f"{im*100:.2f}% / {n/1e6:.2f}M")
        P(f"| {S} | "+" | ".join(row)+" |")
    P("\n### T2b BUY slippage excluding fee (pure curve impact %)")
    P("| Buy SOL \\ Progress | "+" | ".join(f"{l}%" for l in levels)+" |"); P("|---|"+"---|"*len(levels))
    for S in sizes:
        row=[]
        for l in levels:
            vs,vt=state_at_token_progress(l/100)
            if S>VS_END-vs: row.append("n/a"); continue
            row.append(f"{impact_buy_nofee(vs,vt,S)*100:.2f}%")
        P(f"| {S} | "+" | ".join(row)+" |")
    P("\n### T3 SELL price impact incl. 1.25% fee: sell the token amount that a SOL-size buy at that level would give. Cell: shortfall vs spot % / SOL received")
    P("| Sell (SOL-equiv of tokens at spot) \\ Progress | "+" | ".join(f"{l}%" for l in levels)+" |"); P("|---|"+"---|"*len(levels))
    for S in sizes:
        row=[]
        for l in levels:
            vs,vt=state_at_token_progress(l/100)
            n=S/price(vs,vt)
            if n>VT0-VT_END*0+0 : pass
            im,o=impact_sell(vs,vt,n); row.append(f"{im*100:.2f}% / {o:.3f}")
        P(f"| {S} | "+" | ".join(row)+" |")
    P("\n### T4 Immediate round-trip (buy S, sell all tokens right after, no other trades)")
    P("| Buy SOL \\ Progress | "+" | ".join(f"{l}%" for l in levels)+" |"); P("|---|"+"---|"*len(levels))
    for S in sizes:
        row=[]
        for l in levels:
            vs,vt=state_at_token_progress(l/100)
            if S/(1+F)>VS_END-vs: row.append("n/a"); continue
            n,vs1,vt1=buy_exact_in(vs,vt,S); o,_,_=sell(vs1,vt1,n)
            row.append(f"{(o/S-1)*100:.2f}% ({o:.4f})")
        P(f"| {S} | "+" | ".join(row)+" |")
    P("\n### T5 Break-even: SOL-price multiple (spot after others buy / spot right after my buy) needed so net sell proceeds = SOL spent. Cell: price multiple / extra SOL others must put in")
    P("| Buy SOL \\ Entry progress | "+" | ".join(f"{l}%" for l in levels)+" |"); P("|---|"+"---|"*len(levels))
    for S in sizes:
        row=[]
        for l in levels:
            vs,vt=state_at_token_progress(l/100)
            if S/(1+F)>VS_END-vs: row.append("n/a"); continue
            b=breakeven(vs,vt,S)
            row.append("unreachable pre-grad" if b is None else f"{b['mult_price']:.4f}x / {b['others_sol']:.2f}")
        P(f"| {S} | "+" | ".join(row)+" |")
    P("\n### T5b Break-even in terms of mcap multiple vs entry mcap, fee-only floor")
    P("Fee-only floor for tiny size: (1)/((1-F)/(1+F)) -> "+f"{(1+F)/(1-F):.5f}x (round-trip fee drag {((1-F)/(1+F)-1)*100:.3f}%)")
    P("\n### T6 Break-even for 1 SOL buy incl. optional fixed overhead (priority fee+tip+rent assumed 0.01 SOL round trip, UNVERIFIED assumption)")
    P("| Progress | Break-even price multiple (no overhead) | with 0.01 SOL overhead | Mcap at entry (SOL) | Mcap needed (SOL) |")
    P("|---|---|---|---|---|")
    for l in [0,10,25,50,75,90]:
        vs,vt=state_at_token_progress(l/100)
        b=breakeven(vs,vt,1.0)
        b2=breakeven(vs,vt,1.01)  # need proceeds >= 1.01 -> approx
        n,vs1,vt1=buy_exact_in(vs,vt,1.0)
        # proper: need proceeds==1.01 for buy of 1.0
        import copy
        lo,hi=VT_END,vt1
        def pr(v): return (K/v-K/(v+n))*(1-F)
        if pr(VT_END)<1.01: P(f"| {l}% | {b['mult_price']:.4f}x | unreachable | | |"); continue
        for _ in range(200):
            mid=(lo+hi)/2
            if pr(mid)>=1.01: lo=mid
            else: hi=mid
        m2=price(K/hi,hi)/price(vs1,vt1)
        P(f"| {l}% | {b['mult_price']:.4f}x | {m2:.4f}x | {mcap(vs,vt):.1f} | {mcap(K/hi,hi):.1f} |")
    P("\n### T7 Break-even vs ENTRY average price (multiple of what I paid per token, incl. fee) 1 SOL buy")
    P("| Entry progress | avg entry price / spot-before | needed spot / entry-spot-before (market-cap multiple from pre-buy mcap) |")
    P("|---|---|---|")
    for l in [0,10,25,50,75,90]:
        vs,vt=state_at_token_progress(l/100)
        b=breakeven(vs,vt,1.0)
        P(f"| {l}% | {1+impact_buy(vs,vt,1.0)[0]:.4f} | {b['mult_mcap_vs_start']:.4f}x (mcap {mcap(vs,vt):.1f} -> {b['mcap2']:.1f} SOL, ends at {b['prog2']*100:.1f}% progress) |")
    print("\n".join(out))
