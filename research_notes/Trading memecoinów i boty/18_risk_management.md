# Risk management and position sizing for fat-tailed, high-failure-rate assets (memecoins)

Note on sourcing: 3 web searches were run (of ~8 budget; the rest were not needed). Items tagged [STD] are standard textbook math (Kelly 1956, Thorp, Taleb, basic probability), stated without URL. Items tagged [SIM] are my own Monte Carlo on made-up distributions, illustrative only, NOT empirical. Web data on memecoin costs is thin/anecdotal.

## 1. EV with power-law returns (venture-style math)

### Takeaway
With ~99% of launches failing and a heavy right tail, per-trade EV is dominated by 1-2 rare outliers, so it is hard to estimate and easily negative after costs. A bot is only +EV if filtering raises the odds/tail above the cost drag; sample sizes of hundreds of trades are needed before EV is believable.

### Cited Findings
- Pump.fun graduation rate (reaching ~$69k mcap and migrating to a DEX) was reported around 0.26% in 2026 by DEXTools (Dune data), below 1% through much of 2025, and peaked ~2.1% (June 2024) per The Block — [DEXTools](https://www.dextools.io/news/pump-fun-graduation-collapse-solana-fees-2026), [The Block](https://www.theblock.co/post/343742/pump-fun-rapid-decline-graduating-tokens-memecoin-frenzy-fizzles-out), [Cointelegraph](https://cointelegraph.com/news/pump-fun-memecoins-are-dying-at-record-rates-less-than-1-survive)
- Solidus Labs claimed ~98-99% of Pump.fun launches are rug pulls/pump-and-dumps; Pump.fun disputed this and definitions vary — [Defiant](https://thedefiant.io/alarming-99-of-memecoin-launches-on-pumpfun-are-pump-and-dumps-or-rug-pulls-report), [Cointelegraph](https://cointelegraph.com/news/memecoins-pump-fun-99-percent-fail-launch). Graduation measures launchpad survival, not scam status.

### Standard math [STD]
- Per-trade EV (net multiple of stake): E[M] = sum p_i * m_i, edge = E[M] - 1 - c, where c = round-trip cost fraction (+ fixed costs / position size).
- Power-law tail: if P(M > x) ~ x^-alpha with alpha <= 2, variance is infinite; alpha <= 1 means infinite mean. Sample mean is dominated by the max observation; the sample median trade is a loser. Taleb: naive sample statistics underestimate tail contribution (and the lack of observed tail makes risk look lower than it is).
- Venture math: if hit probability p_h per trade with payoff X, you need p_h * X > 1 + c just to break even; P(at least one hit in n trades) = 1-(1-p_h)^n. Example: p_h = 0.2% for a 100x: n=500 trades gives 1-0.998^500 = 63%; n=100 gives 18%. So 1 in 3 portfolios of 500 trades gets no 100x at all, and the realized result varies enormously ("luck of the tail").

### Worked example [SIM, made-up distribution]
Outcome multiples/probs: 0x:70%, 0.5x:14%, 2x:10%, 10x:5.8%, 100x:0.2% -> E[M]=1.05 gross (+5% EV per trade). Median trade loses. Required hit-rate precision: changing the 100x probability from 0.2% to 0.1% cuts E[M] by 0.10 -> EV becomes -5%. I.e. the entire edge sits in an event happening 1 in 500 trades; it cannot be verified with fewer than thousands of trades.

### Inferences
- Treat the bot's historical backtest EV as an upper bound with very wide error bars; use a bootstrap/Bayesian lower bound (e.g. 20th percentile of EV) for sizing decisions.
- Winsorize or trim the top 1-2 outliers when estimating EV ("EV ex-top-outlier"); if EV ex-outlier is deeply negative, the strategy is a lottery ticket and should be sized as such (small, fixed budget).

### Gaps
- No reliable empirical distribution of realized returns for a filtered memecoin bot was found; the distribution above is hypothetical.

## 2. Kelly / fractional Kelly, risk of ruin, drawdown

### Takeaway
Full Kelly is far too aggressive with fat tails and parameter uncertainty; with discrete rug outcomes, Kelly fraction is tiny (fractions of 1% of bankroll) and goes to zero if net EV is ~0 or negative. Use 1/4 Kelly or less, and cap by a drawdown budget.

### Cited Findings
- Thorp ("Leverage and Uncertainty", arXiv): fat tails/uncertainty reduce the optimal Kelly fraction and growth; supports fractional Kelly in practice — [arXiv 1612.07194](https://arxiv.org/pdf/1612.07194)
- Risk.net abstract: fractional Kelly justified by negative skew and positive kurtosis — [Risk.net](https://www.risk.net/journal-of-investment-strategies/5330296/leverage-and-uncertainty)
- Under full Kelly with GBM assumptions, probability of a 50% drawdown is ~50% (reported in Entropy paper) — [MDPI Entropy](https://mdpi.com/1099-4300/25/2/202); fractional Kelly gives a growth/security trade-off, ~25% growth sacrificed for much better safety per Thorp commentary — [arXiv 1801.01948](https://arxiv.org/pdf/1801.01948)
- Caveat from the same literature: the tail parameters cannot be estimated accurately, so the adjustment is qualitative.

### Standard math [STD]
- Binary Kelly: f* = (b*p - q)/b, b = net odds, q = 1-p. Example: p=0.25, b=3 -> f* = (0.75-0.75)/3 = 0 (breakeven -> bet nothing).
- General discrete: maximize g(f) = sum p_i ln(1 + f*(m_i - 1)). Because there is a 0x (-100%) outcome, f must satisfy 1 - f > 0, and in practice f* is small.
- Continuous approx: f* ~ mu/sigma^2 (mean/variance of per-trade return); growth g ~ f*mu - f^2 sigma^2/2; fractional Kelly c*f* gives growth fraction c(2-c) of optimal (half Kelly: 75% of growth; quarter Kelly: 44%) with variance c^2 of full. Drawdown probability: P(ever hit fraction x of peak) ~ x^(2/c - 1) under GBM at fraction c of Kelly (full Kelly: P(drop to 50%)=50%; half Kelly: 0.5^3 = 12.5%; quarter Kelly: 0.5^7 = 0.8%).
- Parameter error: overestimating edge by 2x makes full Kelly equal to 2x-overbetting, which gives zero growth and ruin-like drawdowns; hence the practical rule: never exceed half of estimated Kelly, and use lower-bound edge estimates.
- Risk of ruin (fixed fraction f, win/loss symmetric approx): RoR ~ exp(-2*mu*B/sigma^2) for ruin level B; for heavy tails this is a lower bound, because jumps can skip barriers.

### Worked example [SIM, 20,000 paths x 300 trades, same made-up distribution, fixed fraction of current equity per trade, 6% round-trip cost (EV roughly -1.3%)]
Numerically solving Kelly for gross distribution: f* = 0.225% of bankroll per trade (EV +5%). With 3% cost EV +1.85%, f* = 0.075%. At 6% cost EV is negative, f* = 0.
Simulation at 3 sizes (with the negative-EV costed version, shown to illustrate drawdown behaviour, not profit): f=1%: median final equity 0.70, median max drawdown 52%, P(DD>50%) 56%; f=2%: median 0.39, P(DD>50%) 97%; f=5%: median 0.03; f=10%: ruin (median ~0). Conclusion: even at 1% per trade, a 70%-loser strategy produces >50% drawdowns more often than not within 300 trades, because losing streaks of 20-30 are routine (P(30 consecutive losses at 70% loss) = 0.7^30 = 2e-5 per start but streaks of 15+ occur often: 0.7^15 = 0.5% per start -> ~1.5 expected across 300 trades).
Rule-of-thumb result: sizes at 0.1-0.5% per trade (position = 0.1-0.5% of bankroll) are the Kelly-consistent range for a lottery-shaped strategy with thin edge.

### Inferences
- A bot sized on "1-5% per trade" (common retail advice) is, under a 70-80% rug/loss rate with thin edge, over-Kelly and has a high probability of 50%+ drawdown.
- Because Kelly is ~0 when net EV ~0, the bot's first job is estimating net EV with cost; sizing can be tied to a Bayesian lower bound of EV and shrinks to zero automatically.
- Use a fixed-fraction of *starting/peak-based* bankroll, or fixed-dollar units, with an overall "risk budget" separate from the portfolio.

### Gaps
- Exact fat-tail Kelly closed form is model-dependent; not found a standard formula. I used numerical maximization of expected log-growth.

## 3. Cost modeling (fees, tips, slippage, failed tx)

### Takeaway
Round-trip costs for memecoin trades are several percent (platform fee ~0.5-1% each way, plus slippage and tips), and fixed per-tx costs make very small positions structurally -EV. Costs are the single most controllable term in EV.

### Cited Findings
- Sniper/trading bot platforms commonly charge 0.5-1% per transaction, some add fixed priority/Jito costs — [RPC Fast review](https://rpcfast.com/blog/top-solana-sniper-bot) (affiliate-style source; verify current pricing)
- Developer posts cite Jito tips of ~50,000 lamports (~$0.15) at claimed 95% inclusion and other examples ~0.001 SOL; internally inconsistent anecdotes, not benchmarks — [DEV Community](https://dev.to/apollo_ag/i-sniped-a-solana-token-in-400ms-heres-the-full-tech-stack-4eg6)
- Academic study of >1.5 billion failed Solana transactions across >72 million blocks; reports up to 75% of non-vote transactions failed in periods of memecoin mania — [arXiv 2504.18055](https://arxiv.org/html/2504.18055v1)
- Bundles via Jito are atomic (all or nothing), limiting partial failure but not bundle misses — same DEV/RPC Fast sources. Failed Jito bundles typically do not charge the tip (landed bundles only) [STD/domain knowledge, verify in Jito docs].

### Cost model [STD, parameters illustrative]
Round-trip cost fraction c = (fee_in + fee_out) + (slip_in + slip_out) + (tips + priority + base fees + rent)/S, where S = position size in USD, plus failure drag: expected cost of failures = P(fail)*(wasted fee) + opportunity cost; effective entry price is worse by the delay.
Example: fee 1% each way = 2%; slippage 1% each way on thin pool = 2%; tip+priority 0.002 SOL each way at $150/SOL = $0.60 round trip.
- S = $20: fixed = 3.0% -> c = 7.0%. 
- S = $100: fixed = 0.6% -> c = 4.6%.
- S = $1,000: fixed = 0.06% -> c = 4.06%.
Break-even win-rate shift: need E[M] >= 1 + c. At c = 7% the strategy needs 7% more gross EV than at c=0. Using the example distribution above (+5% gross EV), costs above ~5% turn it negative; [SIM] numeric Kelly: at 3% cost f*=0.075%, at 6% f*=0.
- Slippage scales with size/liquidity: constant-product pool price impact ~ S/(2*L_quote) for small trades (L_quote = SOL-side reserves, ~S/L for buy of fraction). Example: pool with $20k quote-side liquidity, buy $200 -> impact ~1%; exit when pool drained/rugged -> unbounded. Exit liquidity limits max position: keep S <= 0.5-1% of pool liquidity.
- Rug exits: stop-losses are not executable if liquidity is pulled or honeypot; assume -100% for sizing, not the stop level.

### Inferences
- Minimum viable position size: choose S such that fixed costs < ~0.5% of S (here S >= ~$120). Below that, the bot is paying more in tips than it can expect to earn.
- Measure realized costs per trade (slippage vs. quote, fee, tip, failed tx) and recompute net EV continuously; cost drift is an early warning signal.

### Gaps
- Could not find authoritative, current Jito tip floor, landing-rate, or typical slippage data; sources were anecdotal. Verify against Jito docs and own logs.

## 4. Practical rules: per-trade caps, daily limits, circuit breakers, correlation

### Takeaway
Define the whole memecoin allocation as a loss-able "risk budget", cap each trade at a tiny fraction, and automate halts on loss streaks, drawdown, cost anomalies and market-wide stress. Memecoin positions are highly correlated in crashes, so diversification across tokens does not diversify risk.

### Cited Findings
- Network-level congestion/failure spikes occur during memecoin mania (up to 75% failed non-vote txs) — [arXiv 2504.18055](https://arxiv.org/html/2504.18055v1): operational risk correlates with euphoria periods when bots trade most.
- Fractional Kelly / drawdown tradeoff references above (Thorp, MacLean) support drawdown-constrained sizing — [arXiv 1801.01948](https://arxiv.org/pdf/1801.01948)

### Proposed rules (author's synthesis, standard risk practice [STD]; no single source)
1. Capital tiering: memecoin bot bankroll = money you can lose entirely (e.g. <=5-10% of liquid net worth). Treat it as a venture sleeve.
2. Per-trade size: min(0.25 x Kelly lower-bound, 0.5-1% of bankroll, 0.5-1% of pool liquidity). Default 0.25-0.5% of bankroll; maximum 1% (in-sim 1% already gives 50%+ drawdown more often than not on a 70%-loss strategy with no edge).
3. Max concurrent positions / gross exposure: e.g. <=10 positions and <=5% of bankroll open, since crash correlation ~1.
4. Daily loss limit: halt for the day at -3% to -5% of bankroll (about 8-10 full-loss trades at 0.5%); weekly -10%; trailing drawdown from peak -20/25% -> halve size, -35% -> stop and review (fractional Kelly drawdown logic).
5. Loss-streak breaker: pause after N consecutive losses where N is set from the model, e.g. P(streak) < 1% under the believed win rate (0.7^13 = 1% -> N ~ 13-15 for 70% loss rate; streak well beyond expectation suggests regime change or broken bot).
6. Cost/health breakers: halt if rolling failed-tx rate > threshold (e.g. 30%), realized slippage > 2x model, or RPC/Jito latency degrades; cap tip per trade at a % of position (e.g. <=0.5%).
7. Market-regime breaker: reduce/stop when launch volume, SOL price (e.g. -10% in 24h) or graduation rate collapse; correlated dumps hit all positions at once and exit liquidity vanishes.
8. Pre-trade filters as risk control: honeypot/mint+freeze authority checks, liquidity locked/burned, holder concentration, simulate sell before buy (cheap tx simulation).
9. Take-profit discipline for power-law: size-out initial stake at 2-3x ("moonbag" remainder); lock profits out to cold wallet periodically (ratchet), reducing bankroll at risk.
10. Hot-wallet risk: keep only the trading bankroll on hot wallet; sweep profits; daily withdrawal. Not strictly sizing but a ruin source.
11. Kill-switch and paper-trade/live-shadow period: require N>=300-500 live trades with small size before scaling; scale only on verified net EV lower bound > 0.

### Inferences
- Because the strategy return is lottery-shaped, "expected ruin" is the base case; the circuit breakers primarily limit time-to-ruin and keep the option on the tail.
- Correlation: treat memecoin positions as one position when computing portfolio risk (use a correlation of ~0.7-1.0 in stress); sum of position sizes = effective exposure.

### Gaps
- No empirical source on memecoin cross-correlation in crashes was found; the near-1 assumption is a prudent engineering assumption, not a cited result.
- Thresholds above (daily limit %, streak N) are heuristics, not backed by a source; calibrate via simulation on the bot's own trade logs.

## Reproducibility
Simulation code (numpy; fixed-fraction compounding, multiples 0/0.5/2/10/100 with probs .70/.14/.10/.058/.002; cost applied as multiplicative factor 0.94 or 0.97 on payoff) is at /tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/t.py. Results are illustrative only.
