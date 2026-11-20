import numpy as np
outsB=np.array([0.1,0.7,1.8,4,10,40]); psB=np.array([0.45,0.30,0.13,0.08,0.03,0.01])
fee=0.0125      # platform fee per side
base=0.000005; prio=0.0005; tip=0.001  # SOL per tx (assumptions)
fail=0.15       # share of submitted tx that land but fail (pay base+prio, no tip)
X=30.0          # virtual SOL reserve (early bonding curve) -- assumption
def fixed_per_trade():
    # each leg: expected attempts until success = 1/(1-fail); failed attempts pay base+prio
    per_leg = (base+prio+tip) + (fail/(1-fail))*(base+prio)
    return 2*per_leg
F=fixed_per_trade(); print("fixed SOL per round trip",F)
def net_mult(gross,S,X=X,sandwich=0.0):
    imp_buy=S/X               # CPMM avg price premium on buy
    tokens_frac=(1-fee)/(1+imp_buy) # value at spot after fees+impact
    # sell: proceeds value V=S*gross*tokens_frac at spot; impact ~ V/X_at_exit, approximated with reserve scaled by price gain
    V=S*gross*tokens_frac
    Xexit=X*np.sqrt(np.maximum(gross,1e-9))  # in CPMM reserve in SOL scales with sqrt(price)
    imp_sell=V/(Xexit+V)
    proceeds=V*(1-imp_sell)*(1-fee)*(1-sandwich)
    return (proceeds - F)/S
for S in [0.01,0.05,0.1,0.25,0.5,1,2,5]:
    nm=np.array([net_mult(o,S) for o in outsB]); ev=(psB*nm).sum()-1
    rt=1-net_mult(1.0,S)
    print(f"S={S} SOL: round-trip cost at flat price {rt*100:.1f}%, net EV {ev*100:.1f}% (gross 50.9%)")
# break-even: fixed costs as % of stake
for S in [0.01,0.05,0.1,0.5,1]:
    print(S, "fixed share", round(F/S*100,2),"%")
# thin-edge distribution A
outsA=np.array([0.05,0.6,1.5,4,10,50]); psA=np.array([0.50,0.30,0.12,0.06,0.015,0.005])
for S in [0.05,0.1,0.5,1]:
    nm=np.array([net_mult(o,S) for o in outsA]); print("A S",S,"net EV",round(((psA*nm).sum()-1)*100,1),"% (gross 2.5%)")
