"""pump.fun bonding curve -> PumpSwap CPMM mechanics simulator (own implementation).
Run:  python3 -I curve_vs_amm_sim.py [section]   (sections: base a b c d e)
Params: 30 SOL / 1.073B virtual, 793.1M real tokens sellable, 1B supply, fee 1.25% (curve & PumpSwap tier0),
migration fee 0.015 SOL, pool seed = 206.9M tokens + (real SOL - 0.015). LP slice 0.02% stays in pool on AMM.
Fee convention (same as research note 01): buy: total paid = curve_cost*(1+f); sell: received = gross*(1-f).
Fees leave the reserves (protocol/creator). All SOL units, tokens in millions of tokens (floats)."""
import sys, random, math, copy

VS0, VT0, RT0, SUP = 30.0, 1073.0, 793.1, 1000.0   # tokens in M
K = VS0 * VT0
VT_END = VT0 - RT0                       # 279.9
VS_END = K / VT_END                      # 115.0
F = 0.0125
MIG = 0.015
POOL_TOK = SUP - RT0                     # 206.9
LP = 0.0002

class Mkt:
    def __init__(s, synth=True, f=F):
        s.vs, s.vt = VS0, VT0
        s.phase = 'curve'; s.synth = synth; s.f = f
        s.ps = s.pt = s.pk = 0.0
        s.fees = 0.0; s.migfee = 0.0
        s.hold = {}; s.cash = {}; s.cls = {}; s.log = []
    # --- state helpers
    def real_sol(s): return s.vs - VS0
    def price(s): return s.vs / s.vt if s.phase == 'curve' else s.ps / s.pt
    def reserve_sol(s): return s.real_sol() if s.phase == 'curve' else s.ps
    def mcap(s): return s.price() * SUP
    def prog(s): return (VT0 - s.vt) / RT0 if s.phase == 'curve' else 1.0
    # --- primitives (no ledger) ---
    def _curve_buy(s, S):
        net = S / (1 + s.f); need = K / VT_END - s.vs
        left = 0.0
        if net >= need:
            left = S - need * (1 + s.f); net = need
        vs2 = s.vs + net; vt2 = K / vs2 if left == 0 else VT_END
        n = s.vt - vt2; s.fees += net * s.f; s.vs, s.vt = vs2, vt2
        return n, S - left, left
    def _migrate(s):
        s.phase = 'pool'; s.migfee = MIG
        s.ps = s.real_sol() - MIG; s.pt = POOL_TOK; s.pk = s.ps * s.pt
    def _pool_buy(s, S):
        net = S / (1 + s.f); fee = net * s.f
        s.ps += net; # lp slice retained
        lp = net * LP; # implement: reserve takes lp slice of fee
        s.fees += fee - lp
        s.ps += lp
        pt2 = s.pk / (s.ps - lp)            # invariant on net-of-lp amount
        n = s.pt - pt2; s.pt = pt2; s.pk = s.ps * s.pt
        return n
    def _pool_sell(s, n):
        pt2 = s.pt + n; ps2 = s.pk / pt2; gross = s.ps - ps2
        fee = gross * s.f; lp = gross * LP
        s.fees += fee - lp; s.pt = pt2; s.ps = ps2 + lp; s.pk = s.ps * s.pt
        return gross - fee
    # --- public: ledger ---
    def buy(s, who, S, cls=None):
        if cls: s.cls[who] = cls
        s.hold.setdefault(who, 0.0); s.cash.setdefault(who, 0.0)
        if S <= 1e-12: return 0.0
        n = 0.0; spent = S
        if s.phase == 'curve':
            n, spent, left = s._curve_buy(S)
            if left > 0 or abs(s.vt - VT_END) < 1e-9:
                s._migrate()
                if left > 0 and s.synth: n += s._pool_buy(left); spent = S
        else:
            n = s._pool_buy(S)
        s.hold[who] += n; s.cash[who] -= spent
        s.log.append((who, 'B', spent, n, s.price()))
        return n
    def sell(s, who, n, cls=None):
        if cls: s.cls[who] = cls
        n = min(n, s.hold.get(who, 0.0))
        if n <= 1e-12: return 0.0
        if s.phase == 'curve':
            vt2 = s.vt + n; vs2 = K / vt2; gross = s.vs - vs2
            out = gross * (1 - s.f); s.fees += gross * s.f; s.vs, s.vt = vs2, vt2
        else:
            out = s._pool_sell(n)
        s.hold[who] -= n; s.cash[who] += out
        s.log.append((who, 'S', out, n, s.price()))
        return out
    def sell_all(s, who): return s.sell(who, s.hold.get(who, 0.0))
    def liq_value(s, n):                 # SOL for selling n tokens now on a copy
        c = copy.deepcopy(s); c.hold['x'] = n; c.cash['x'] = 0.0
        return c.sell('x', n)
    def spot_value(s, n): return n * s.price()

def curve_state_at_real(r):               # curve state with r real SOL raised
    return VS0 + r, K / (VS0 + r)

# ---------------- closed forms -------------
def price_mult_to_grad(r): return (VS_END / (VS0 + r)) ** 2
def sol_for_doubling(vs): return (math.sqrt(2) - 1) * vs

def md_table(h, rows):
    out = ["| " + " | ".join(h) + " |", "|" + "---|" * len(h)]
    for r in rows: out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)

# =============== base: constants & continuity ===============
def base():
    print("### B0 Derived constants")
    m = Mkt(); m.vs, m.vt = VS_END, VT_END; m._migrate()
    print(f"- k_curve = {K:,.1f} SOL*Mtok; VT_end = {VT_END} Mtok; VS_end = {VS_END:.4f} SOL; real SOL raised = {VS_END-VS0:.4f}")
    print(f"- curve end price = {VS_END/VT_END:.6e} SOL/Mtok; mcap = {VS_END/VT_END*SUP:.2f} SOL; start mcap {VS0/VT0*SUP:.2f} SOL; mult = {(VS_END/VT_END)/(VS0/VT0):.3f}x")
    print(f"- pool seed: {m.ps:.4f} SOL + {m.pt:.1f} Mtok; pool price = {m.ps/m.pt:.6e} (vs curve end {VS_END/VT_END:.6e}, gap {(m.ps/m.pt)/(VS_END/VT_END)-1:+.4%})")
    print(f"- k_pool = {m.pk:.1f} vs k_curve = {K:.1f}  -> pool k is {m.pk/K:.1%} of curve k ({1-m.pk/K:.1%} thinner)")
    allsell_curve = VS_END - VS0
    allsell_pool = m.ps - m.pk / (m.pt + RT0)
    print(f"- sell ALL 793.1M tokens back: curve returns {allsell_curve:.2f} SOL gross (=100% of raised); pool returns {allsell_pool:.2f} SOL gross ({allsell_pool/allsell_curve:.1%}); structural haircut {allsell_curve-allsell_pool:.2f} SOL locked in pool + {MIG} migration fee")
    print()
    print("### B1 Price / depth vs progress (closed form: P = vs^2/k, mcap = P*1000)")
    rows = []
    for r in [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 85]:
        vs, vt = curve_state_at_real(r)
        imp1 = ((vs + 1/(1+F))**2/vs**2 - 1)
        rows.append([r, f"{r/85:.0%}", f"{(VT0-vt)/RT0:.1%}", f"{vs/vt:.3e}", f"{(vs/vt)/(VS0/VT0):.2f}x", f"{vs/vt*SUP:.1f}", f"{imp1:.2%}", f"{price_mult_to_grad(r):.2f}x", f"{sol_for_doubling(vs):.1f}" if price_mult_to_grad(r) >= 2 else "n/a (<2x left)"])
    print(md_table(["real SOL r", "% of 85", "% tokens sold", "price", "x start", "mcap SOL", "price impact of 1 SOL buy (excl. fee)", "price mult left to graduation (115/(30+r))^2", "net SOL needed for next 2x (0.414*vs)"], rows))
    print()
    print("### B2 Marginal depth: price impact per SOL of net buy = 2/R_eff")
    print(md_table(["venue/state", "R_eff (SOL)", "impact of +1 SOL net", "SOL net to double price", "SOL net to 10x"],
        [["curve r=0", 30, f"{(31/30)**2-1:.2%}", f"{sol_for_doubling(30):.1f}", f"{30*(math.sqrt(10)-1):.0f}"],
         ["curve r=50", 80, f"{(81/80)**2-1:.2%}", f"{sol_for_doubling(80):.1f}", f"{80*(math.sqrt(10)-1):.0f}"],
         ["curve end (vs=115)", 115, f"{(116/115)**2-1:.2%}", f"{sol_for_doubling(115):.1f}", f"{115*(math.sqrt(10)-1):.0f}"],
         ["pool just after migration", f"{m.ps:.2f}", f"{((m.ps+1)/m.ps)**2-1:.2%}", f"{sol_for_doubling(m.ps):.1f}", f"{m.ps*(math.sqrt(10)-1):.0f}"]]))

# =============== (a) scenarios =================
def organic_flow(rng, n, sell_bias=0.15, med=0.8, sig=0.9, pool_ids=None):
    ev = []
    for i in range(n):
        if rng.random() < sell_bias: ev.append(('S', rng.choice([0.3, 0.5, 1.0]), None))
        else: ev.append(('B', min(12.0, rng.lognormvariate(math.log(med), sig)), None))
    return ev

def run_scenario(name, sniper_exit, dev_exit, bot_entry_r, bot_exit, seed=7, post_bias=0.55, synth=True,
                 n_snip=6, snip_sol=1.5, dev_sol=2.0, post_orders=60, verbose=False):
    """sniper_exit / dev_exit: ('r', value) sell when real SOL >= value; ('pool', k) sell after k pool orders; None = hold.
       bot_entry_r: real-SOL level (or None) at which bot buys 1 SOL; ('pool',k) = after k pool orders.
       bot_exit: ('pool', k) = after k pool orders; ('r', v); ('G',0)=first pool state (after migration)."""
    rng = random.Random(seed); m = Mkt(synth=synth)
    m.buy('dev', dev_sol, 'dev')
    for i in range(n_snip): m.buy(f'snp{i}', snip_sol, 'sniper')
    org = {}; oid = 0; pool_orders = 0
    done = {'snp': False, 'dev': False, 'botin': False, 'botout': False}
    def trig(spec, pool_orders):
        if spec is None: return False
        if spec[0] == 'r': return m.phase == 'curve' and m.real_sol() >= spec[1] or m.phase == 'pool'
        if spec[0] == 'pool': return m.phase == 'pool' and pool_orders >= spec[1]
        if spec[0] == 'G': return m.phase == 'pool'
    steps = 0
    while steps < 4000:
        steps += 1
        # triggers (checked before each organic order)
        if not done['snp'] and trig(sniper_exit, pool_orders):
            for i in range(n_snip): m.sell_all(f'snp{i}')
            done['snp'] = True
        if not done['dev'] and trig(dev_exit, pool_orders):
            m.sell_all('dev'); done['dev'] = True
        if bot_entry_r is not None and not done['botin'] and trig(bot_entry_r, pool_orders):
            m.buy('bot', 1.0, 'bot'); done['botin'] = True
        if bot_entry_r is not None and done['botin'] and not done['botout'] and trig(bot_exit, pool_orders):
            m.sell_all('bot'); done['botout'] = True
        if m.phase == 'pool' and pool_orders >= post_orders: break
        bias = 0.15 if m.phase == 'curve' else post_bias
        ev = organic_flow(rng, 1, sell_bias=bias)[0]
        if ev[0] == 'B':
            oid += 1; m.buy(f'org{oid}', ev[1], 'organic')
        else:
            holders = [w for w in m.hold if m.cls.get(w) == 'organic' and m.hold[w] > 1e-6]
            if holders:
                w = rng.choice(holders); m.sell(w, m.hold[w] * ev[1])
        if m.phase == 'pool': pool_orders += 1
    # final flush of any untriggered exits is NOT done: untriggered stay as bags.
    return m

def summarize(m, label=""):
    cls = {}
    for w in m.hold:
        c = m.cls.get(w, '?'); d = cls.setdefault(c, dict(n=0, spent=0.0, recv=0.0, tok=0.0))
        d['n'] += 1; d['tok'] += m.hold[w]
        # cash is net; reconstruct spent/recv from log
    for (who, side, sol, n, p) in m.log:
        c = m.cls.get(who, '?')
        if side == 'B': cls[c]['spent'] += sol
        else: cls[c]['recv'] += sol
    return cls

def pnl_tables(m, title):
    cl = summarize(m)
    spot = m.price(); rows = []
    tot_real = tot_mark = tot_liq = 0.0
    # liquidation: sequentially sell all remaining holders, bags order: organic first? use arbitrary fixed order (sorted by token size desc)
    c = copy.deepcopy(m)
    for w in sorted(c.hold, key=lambda x: -c.hold[x]): c.sell(w, c.hold[w])
    liq = {}
    for w in m.hold: liq.setdefault(m.cls[w], 0.0); liq[m.cls[w]] += c.cash[w]
    for k in ['dev', 'sniper', 'organic', 'bot']:
        if k not in cl: continue
        d = cl[k]; real = d['recv'] - d['spent']; mark = real + d['tok'] * spot
        rows.append([k, d['n'], f"{d['spent']:.2f}", f"{d['recv']:.2f}", f"{d['tok']:.1f}", f"{d['tok']/SUP:.2%}", f"{real:+.2f}", f"{mark:+.2f}", f"{liq[k]:+.2f}"])
        tot_real += real; tot_mark += mark; tot_liq += liq[k]
    print(f"#### {title}")
    print(f"final state: phase={m.phase}, pool/curve SOL reserve={m.reserve_sol():.2f}, price={spot:.3e}, mcap={m.mcap():.0f} SOL, fees paid={m.fees:.3f} SOL, mig fee={m.migfee}")
    print(md_table(["class", "#", "SOL in", "SOL out (realised)", "tokens held (M)", "% supply", "realised PnL", "PnL marked @spot", "PnL if all liquidate (sequential)"], rows))
    # zero-sum identity for the full liquidation
    print(f"- sum realised PnL = {tot_real:+.3f} ; sum marked@spot = {tot_mark:+.3f} ; sum liquidation = {tot_liq:+.3f}")
    lock = c.reserve_sol()
    ident = -(m.fees_after if hasattr(m, 'fees_after') else 0)
    print(f"- identity check: -(fees {c.fees:.3f} + migfee {c.migfee:.3f} + SOL left in market {lock:.3f}) = {-(c.fees+c.migfee+lock):+.3f}  vs sum liquidation {tot_liq:+.3f}")
    print()
    return cl

def sec_a():
    print("### A1 Scenario base: dev 2 SOL + 6 snipers x 1.5 SOL at creation, ~organic flow (lognormal median 0.8 SOL, 15% sells) to graduation, then 60 pool orders (55% sell bias)")
    print()
    sc = [("S1 snipers dump at r=15 SOL (curve), dev holds", ('r', 15), None),
          ("S2 snipers+dev hold to graduation and dump in first pool block", ('pool', 0), ('pool', 0)),
          ("S3 snipers dump on the curve at r=70, dev holds", ('r', 70), None),
          ("S4 nobody dumps (all hold)", None, None)]
    for nm, se, de in sc:
        m = run_scenario(nm, se, de, None, None)
        pnl_tables(m, nm)
    print("### A2 Bot (1 SOL) entry at different points x exit at different points; Scenario = S2 (snipers+dev dump on pool right after graduation) vs S1")
    entries = [2, 10, 25, 45, 65, 80]
    exits = [('G', 0), ('pool', 0), ('pool', 5), ('pool', 30), ('pool', 60)]
    exlab = ["first pool state (before dump)", "after sniper/dev dump block", "+5 pool orders", "+30 pool orders", "+60 pool orders"]
    for nm, se, de in [("S2: snipers+dev dump at pool block 0", ('pool', 0), ('pool', 0)), ("S1: snipers dumped early at r=15, dev holds", ('r', 15), None)]:
        print(f"\n#### Bot PnL (SOL, realised after exit incl. all fees), {nm}; seeds 1..40 mean [p10 .. p90]")
        rows = []
        for e in entries:
            row = [f"r={e}"]
            for ex in exits:
                if ex == ('G', 0) and e is None: continue
                vals = []
                for seed in range(1, 41):
                    mm = run_scenario(nm, se, de, ('r', e), ex, seed=seed)
                    if 'bot' in mm.hold and mm.hold['bot'] < 1e-9:
                        vals.append(mm.cash['bot'])
                    else: vals.append(None)
                v = sorted(x for x in vals if x is not None)
                if len(v) < 10: row.append("n/a"); continue
                row.append(f"{sum(v)/len(v):+.3f} [{v[len(v)//10]:+.2f} .. {v[9*len(v)//10]:+.2f}]")
            rows.append(row)
        print(md_table(["bot entry"] + exlab, rows))
    # deterministic full trade-log for a single example
    print("\n#### A3 Example fixed-seed trade log, S2 with bot in at r=45 and out +5 pool orders (seed 7)")
    m = run_scenario("log", ('pool', 0), ('pool', 0), ('r', 45), ('pool', 5), seed=7)
    cl = pnl_tables(m, "S2 + bot(r=45 -> pool+5)")

# =============== (b) zero-sum ===============
def sec_b():
    print("### B-1 Zero-sum identity checks (full liquidation of every holder)")
    rows = []
    for seed in range(1, 9):
        m = run_scenario("z", ('pool', 0), ('pool', 0), ('r', 45), ('pool', 5), seed=seed, post_orders=40)
        c = copy.deepcopy(m)
        for w in sorted(c.hold, key=lambda x: -c.hold[x]): c.sell(w, c.hold[w])
        tot = sum(c.cash.values()); lock = c.reserve_sol()
        rows.append([seed, f"{tot:+.4f}", f"{c.fees:.4f}", f"{c.migfee:.3f}", f"{lock:.4f}", f"{-(c.fees+c.migfee+lock):+.4f}", f"{tot+(c.fees+c.migfee+lock):+.2e}"])
    print(md_table(["seed", "sum trader PnL (all liquidated)", "fees leaked", "migration fee", "SOL left in AMM (locked LP)", "-(fees+mig+locked)", "residual"], rows))
    print()
    print("### B-2 Same for a curve-only life (no graduation): buy a bunch, all sell back -> PnL sum = -fees")
    m = Mkt()
    rng = random.Random(3)
    for i in range(30): m.buy(f'o{i}', rng.uniform(0.3, 2.0), 'organic')
    c = copy.deepcopy(m)
    for w in list(c.hold): c.sell_all(w)
    print(f"curve phase after buys: real SOL {m.real_sol():.2f}; after liquidation: real SOL {c.real_sol():.2e}; sum PnL {sum(c.cash.values()):+.4f} vs -fees {-c.fees:.4f}")
    print()
    print("### B-3 Who is left holding at graduation (token distribution under S2 base path)")
    m = run_scenario("g", None, None, None, None, post_orders=0)
    # when post_orders=0 loop breaks immediately once pool
    cl = summarize(m)
    sp = m.price()
    print(md_table(["class", "tokens (M)", "% of 1B", "cost basis SOL", "mark @pool spot", "liq value into pool", "liq/cost"],
        [[k, f"{d['tok']:.1f}", f"{d['tok']/SUP:.1%}", f"{d['spent']-d['recv']:.2f}", f"{d['tok']*sp:.2f}", f"{(m.liq_value(d['tok']) if d['tok']>0 else 0):.2f}", f"{(m.liq_value(d['tok'])/(d['spent']-d['recv'])) if d['spent']-d['recv']>0 else float('nan'):.2f}"] for k, d in cl.items()]))
    print(f"\npool tokens {m.pt:.1f} M = {m.pt/SUP:.1%} of supply (owned by locked LP); traders hold {sum(m.hold.values()):.1f} M")
    print("\n### B-4 Exit-liquidity attribution (curve): a seller is paid from the SOL previously deposited and not yet withdrawn")
    print("- Reserve identity: real_sol(t) = sum_i (net SOL deposited by i, ex fee) = sum over *current holders* of their (cost basis - realised proceeds). A sell of X tokens is funded by whoever is currently net-long in SOL terms, i.e. the later buyers (and bag holders of earlier flows).")
    print("- Therefore per-token PnL transfers only along the price path: a token bought at price p_b and sold at p_s gives (p_s - p_b)*n to the seller and the same amount is lost by the buyer chain *holding at the bottom of the chain*; fees (1.25% each side) leak to protocol/creator.")

# =============== (c) dump absorption ===============
def dump_on_curve(r, X):
    """holder with X (fraction of 1B supply) dumps at curve state with r real SOL. returns dict"""
    vs, vt = curve_state_at_real(r); n = X * SUP
    if n > RT0 - (VT0 - vt): pass
    vt2 = vt + n; vs2 = K / vt2; gross = vs - vs2; out = gross * (1 - F)
    p0, p1 = vs / vt, vs2 / vt2
    # buy volume (gross, with 1.25% on top) required to restore vs back to vs (restore price)
    restore_gross = gross * (1 + F)  # net buys needed = gross, paid = net*(1+F)
    # buy volume to restore only HALF the price drop (price p0 -> p_half) is solved numerically
    return dict(out=out, gross=gross, drop=1 - p1 / p0, restore=restore_gross, p0=p0, p1=p1,
                eff=out / n / p0 - 1)

def dump_on_pool(X, extra_r=0.0, start_ps=None, start_pt=None):
    ps = start_ps; pt = start_pt; n = X * SUP
    pt2 = pt + n; ps2 = ps * pt / pt2; gross = ps - ps2
    out = gross * (1 - F)
    p0, p1 = ps / pt, ps2 / pt2
    return dict(out=out, gross=gross, drop=1 - p1 / p0, restore=gross * (1 + F), eff=out / n / p0 - 1)

def sec_c():
    print("### C1 Dump of X% of total supply on the CURVE at real-SOL level r (holder must exist, i.e. X*1000 <= tokens sold)")
    print("Cell: price drop % / SOL proceeds net of 1.25% / buy volume (gross SOL incl. fee) needed from new buyers to push price back to the pre-dump level")
    Xs = [0.01, 0.02, 0.05, 0.10, 0.15, 0.20]
    levels = [10, 20, 40, 60, 80, 84.9]
    rows = []
    for X in Xs:
        row = [f"{X:.0%}"]
        for r in levels:
            vs, vt = curve_state_at_real(r); sold = VT0 - vt
            if X * SUP > sold: row.append("-"); continue
            d = dump_on_curve(r, X)
            row.append(f"-{d['drop']:.0%} / {d['out']:.1f} / {d['restore']:.1f}")
        rows.append(row)
    print(md_table(["X (supply)"] + [f"r={l}" for l in levels], rows))
    m = Mkt(); m.vs, m.vt = VS_END, VT_END; m._migrate()
    print("\n### C2 Same dump on the POOL right after graduation (pool: 84.985 SOL / 206.9M tok)")
    rows = []
    for X in Xs:
        d = dump_on_pool(X, start_ps=m.ps, start_pt=m.pt)
        rows.append([f"{X:.0%}", f"-{d['drop']:.0%}", f"{d['out']:.2f}", f"{d['restore']:.2f}", f"{d['eff']:.1%}"])
    print(md_table(["X (supply)", "price drop", "SOL proceeds net", "buy volume to restore price (gross)", "effective sell price vs spot"], rows))
    print("\nClosed forms: curve - drop = 1-(vt/(vt+n))^2 ; gross out = vs*n/(vt+n) ; restore volume = gross*(1+f).  pool - identical with (ps, pt).  Restore volume equals what the dumper took out, plus the 1.25% fee: buyers must re-deposit exactly the SOL withdrawn.")
    print("\n### C3 Required buy volume to ABSORB the dump *and* keep market cap flat when the dumper's tokens are re-bought (same quantity as restore); expressed vs organic flow")
    print("Typical organic inflow: pump.fun tokens that graduate raise 85 SOL over their life; e.g. an 85-SOL curve token with a 10% dump at r=40 needs:")
    d = dump_on_curve(40, 0.10); print(f"  restore volume = {d['restore']:.1f} SOL = {d['restore']/85:.0%} of the whole graduation raise; price drop {d['drop']:.0%}")
    d = dump_on_pool(0.10, start_ps=m.ps, start_pt=m.pt); print(f"  same 10% dumped on pool post-graduation: restore {d['restore']:.1f} SOL, drop {d['drop']:.0%}; pool dump proceeds {d['out']:.1f} SOL")
    print("\n### C4 Dump absorption by buying: time series. Sniper cluster (X% supply bought at start for tiny SOL) dumps at r; organic buyers needed to bring price back to the sniper's *entry* mcap level is trivial -> but to bring it back to the PRE-DUMP level requires restore volume above.")
    # sniper cost: buy X% of supply at start
    rows = []
    for X in [0.05, 0.10, 0.15, 0.20]:
        n = X * SUP; vt2 = VT0 - n; vs2 = K / vt2; cost = (vs2 - VS0) * (1 + F)
        row = [f"{X:.0%}", f"{cost:.2f}"]
        for r in [20, 40, 60]:
            vs, vt = curve_state_at_real(r)
            # snipers' tokens are inside 'sold'; dump at state after organic raise r
            d = dump_on_curve(r, X)
            row.append(f"{d['out']:.1f} SOL ({d['out']/cost:.0f}x) / needs {d['restore']:.0f} SOL organic")
        rows.append(row)
    print(md_table(["sniper X%", "entry cost SOL (incl fee)", "dump @r=20 (proceeds, multiple, restore)", "dump @r=40", "dump @r=60"], rows))
    print("\n### C5 Breakeven absorption: how much organic buy volume per sniper-dumped SOL to hold the *price* at the level it had before dump? = (1+f) SOL per 1 SOL taken out (curve) -- independent of dump size. What changes with size is how far price falls if volume is insufficient:")
    rows = []
    for r in [20, 40, 60, 80]:
        row = [f"r={r}"]
        for X in [0.05, 0.10, 0.20]:
            vs, vt = curve_state_at_real(r)
            if X * SUP > VT0 - vt: row.append("-"); continue
            # organic volume = V gross during/after the dump -> price drop remaining
            res = []
            for frac in [0.25, 0.5, 1.0]:
                d = dump_on_curve(r, X); V = d['restore'] * frac
                net = V / (1 + F); n = X * SUP
                vsx = vs + net - d['gross']  # reserve after both
                # tokens: dumper returns n, buyers take tokens: reserve (vs) path-independent in vs: vs_final = vs - gross + net
                vtx = K / vsx
                res.append(f"{(vsx/vtx)/(vs/vt)-1:+.0%}")
            row.append(" / ".join(res))
        rows.append(row)
    print(md_table(["state", "X=5% (25%/50%/100% of restore vol)", "X=10%", "X=20%"], rows))
    print("(price vs pre-dump after buyers supply 25%/50%/100% of the restore volume; since reserve vs is path-independent, price = vs_final^2/k)")

# =============== (d) slippage at graduation ===============
def slip_buy_curve(r, S, f=F):
    vs, vt = curve_state_at_real(r); net = S / (1 + f); need = K / VT_END - vs
    if net > need: return None
    vs2 = vs + net; n = vt - K / vs2
    return (S / n) / (vs / vt) - 1, n
def slip_buy_pool(S):
    m = Mkt(); m.vs, m.vt = VS_END, VT_END; m._migrate(); p0 = m.price(); n = m._pool_buy(S); return (S / n) / p0 - 1, n
def slip_sell_curve(r, n):
    vs, vt = curve_state_at_real(r); vt2 = vt + n; vs2 = K / vt2; out = (vs - vs2) * (1 - F)
    return 1 - (out / n) / (vs / vt), out
def slip_sell_pool(n):
    m = Mkt(); m.vs, m.vt = VS_END, VT_END; m._migrate(); p0 = m.price(); out = m._pool_sell(n); return 1 - (out / n) / p0, out

def sec_d():
    sizes = [0.5, 1, 2, 5, 10, 25, 50]
    print("### D1 BUY slippage (effective price vs spot, INCLUDING the 1.25% fee; fee-free impact in brackets): last curve states vs pool just after graduation")
    rows = []
    for S in sizes:
        row = [S]
        for r in [60, 80, 84]:
            x = slip_buy_curve(r, S)
            if x is None:
                row.append("crosses grad"); continue
            nofee = slip_buy_curve(r, S, f=0.0)
            row.append(f"{x[0]:.2%} [{nofee[0]:.2%}]")
        p = slip_buy_pool(S); pn = (lambda m: (m, m._pool_buy(S)))(None)
        m2 = Mkt(); m2.vs, m2.vt = VS_END, VT_END; m2._migrate(); pf = ((S) / (m2.pt - m2.pk/(m2.ps+S)))/ m2.price() - 1
        row.append(f"{p[0]:.2%} [{pf:.2%}]")
        rows.append(row)
    print(md_table(["buy SOL", "curve r=60", "curve r=80", "curve r=84", "pool just after graduation"], rows))
    print("\n### D2 SELL slippage (shortfall of net proceeds vs spot*tokens, including 1.25% fee). Size given as SOL-equivalent at spot (tokens = S/spot)")
    rows = []
    sp_end = VS_END / VT_END
    for S in sizes + [100, 200, 400]:
        row = [S]
        for r in [60, 80, 84.9]:
            vs, vt = curve_state_at_real(r); n = S / (vs / vt)
            if n > (VT0 - vt): row.append("-"); continue
            row.append(f"{slip_sell_curve(r,n)[0]:.2%}")
        n = S / sp_end
        row.append(f"{slip_sell_pool(n)[0]:.2%}")
        rows.append(row)
    print(md_table(["sell SOL-eq", "curve r=60", "curve r=80", "curve r=84.9", "pool just after graduation"], rows))
    print("\n### D3 Ratio: sell slippage excluding fee, pool / curve(r=84.9) at the same SOL-eq size (depth cliff)")
    rows = []
    for S in [1, 5, 10, 25, 50, 100, 200]:
        n = S / sp_end
        vs, vt = curve_state_at_real(84.9)
        c = 1 - (slip_sell_curve(84.9, n)[0] * -1 + 0) if False else None
        vt2 = vt + n; gross_c = vs - K / vt2; sl_c = 1 - (gross_c / n) / (vs / vt)
        m = Mkt(); m.vs, m.vt = VS_END, VT_END; m._migrate(); g = m.ps - m.pk / (m.pt + n); sl_p = 1 - (g / n) / m.price()
        rows.append([S, f"{sl_c:.2%}", f"{sl_p:.2%}", f"{sl_p/sl_c:.2f}x"])
    print(md_table(["sell SOL-eq", "curve slip (no fee)", "pool slip (no fee)", "pool/curve"], rows))
    print("\n### D4 Sequence across the boundary: a single big BUY that straddles graduation (synthetic migration) vs the same two buys split")
    for S in [100, 120, 150]:
        m = Mkt(); m.vs, m.vt = curve_state_at_real(80)
        n = m.buy('a', S, 'x')
        print(f"- start r=80 (5 SOL left on curve): buy {S} SOL -> {n:.1f}M tokens, avg price {S/n:.3e}, post-grad pool price {m.price():.3e} (x{m.price()/(VS_END/VT_END):.2f} of curve-end price), pool SOL {m.ps:.1f}")
    print("\n### D5 Round-trip cost for 1/5/10 SOL: enter at r then exit immediately at same-state (reset) vs enter at curve end and exit into the pool (price flat)")
    rows = []
    for S in [1, 5, 10]:
        row = [S]
        for r in [0, 30, 60, 80]:
            vs, vt = curve_state_at_real(r); m = Mkt(); m.vs, m.vt = vs, vt
            n = m.buy('a', S, 'x'); out = m.sell_all('a'); row.append(f"{1-out/S:.2%}")
        m = Mkt(); m.vs, m.vt = VS_END, VT_END; m._migrate(); n = m.buy('a', S, 'x'); out = m.sell_all('a'); row.append(f"{1-out/S:.2%}")
        rows.append(row)
    print(md_table(["SOL", "curve r=0", "r=30", "r=60", "r=80", "pool (post-grad)"], rows))

# =============== (e) implications =================
def sec_e():
    print("### E1 Entry-point scorecard (1 SOL buy at real-SOL level r; all numbers computed)")
    rows = []
    for r in [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 84]:
        vs, vt = curve_state_at_real(r)
        m = Mkt(); m.vs, m.vt = vs, vt
        cost_rt = None
        n = m.buy('b', 1.0, 'x'); entry = 1.0 / n
        out_now = m.liq_value(n)
        # price multiple needed to break even
        be = (1.0 / out_now)
        # grad pnl: hold through graduation (curve completes by organic net buys), sell first pool state
        m2 = Mkt(); m2.vs, m2.vt = vs, vt; n2 = m2.buy('b', 1.0, 'x')
        m2.buy('whale', 200.0, 'w')              # completes the curve; synthetic migration fill
        # after this buy price is above end; we want the *grad-state* exit: use pure curve-end state
        m3 = Mkt(); m3.vs, m3.vt = vs, vt; n3 = m3.buy('b', 1.0, 'x')
        # drive the curve to completion with exact tokens (no overshoot)
        rem = m3.vt - VT_END
        need_net = K / VT_END - m3.vs
        m3.buy('w', need_net * (1 + F), 'w')
        pool_out = m3.sell_all('b') if m3.phase == 'pool' else float('nan')
        # exit liquidity: aggregate haircut (everyone exits into pool)
        rows.append([r, f"{vs/vt*SUP:.0f}", f"{n:.1f}M ({n/SUP:.2%})", f"{be:.3f}x", f"{price_mult_to_grad(r):.2f}x", f"{pool_out:.3f}", f"{pool_out-1:+.1%}", f"{sol_for_doubling(vs):.1f}" if price_mult_to_grad(r) >= 2 else "-"])
    print(md_table(["entry r", "entry mcap SOL", "tokens bought", "breakeven price mult (1 SOL, exit same state)", "price mult left to grad", "SOL back if graduates & sold on first pool state (net of 2 fees)", "= PnL", "net SOL demand needed for 2x"], rows))
    print("\n### E2 Post-graduation: demand needed for multiples above graduation price")
    m = Mkt(); m.vs, m.vt = VS_END, VT_END; m._migrate()
    rows = []
    for mult in [1.5, 2, 3, 5, 10, 14.7]:
        need = m.ps * (math.sqrt(mult) - 1)
        rows.append([f"{mult}x", f"{need:.1f}", f"{need*(1+F):.1f}", f"{need/85:.2f}x of whole curve raise"])
    print(md_table(["price multiple above graduation price", "net SOL into pool", "gross incl 1.25% fee", "vs 85 SOL curve raise"], rows))
    print("\n### E3 Where is the aggregate-exit haircut: SOL obtainable if every holder sells everything, as function of progress (curve) vs after graduation")
    rows = []
    for r in [20, 40, 60, 80, 84.9]:
        rows.append([f"curve r={r}", f"{r:.1f}", "100% of net deposits (before fees)", "n/a"])
    rows.append(["after graduation (all 793.1M back into pool)", "84.985", f"{(m.ps - m.pk/(m.pt+RT0)):.1f} gross = {(m.ps - m.pk/(m.pt+RT0))/84.985:.1%}", f"locked: {m.pk/(m.pt+RT0):.1f} SOL"])
    print(md_table(["state", "reserve SOL", "recoverable if all exit", "left stuck"], rows))

if __name__ == '__main__':
    sec = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for name, fn in [('base', base), ('a', sec_a), ('b', sec_b), ('c', sec_c), ('d', sec_d), ('e', sec_e)]:
        if sec in ('all', name): fn(); print()
