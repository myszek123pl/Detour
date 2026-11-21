# 22 - Who makes and who loses money in memecoins (wallet x token cash PnL)

Date: 2026-11-21. Data: ian05012/solana-memecoin-dataset (GMGN-sourced, June 2026): trades-000..003 (9,500,565 rows, 734,407 wallets, 66,990 tokens), tokens.parquet, wallets.parquet, wallet_funding.parquet. Analysis in DuckDB (`python3 -I`), scripts in the session scratchpad `.../scratchpad/w/` (cov*.py, build.py, b1-b5.py; outputs b2-b5.out). No web.

## Bottom line

1. In this sample the trade-level game is strongly negative-sum in cash terms: on 6.27M wallet x token positions (conserving tokens, see coverage), buys $1.85B, sells $1.38B, net cash -$473M. Only 10.7% of positions and 10.9% of wallets show positive cash PnL; median position -$5.6, median wallet -$8.5. A large part of the "loss" is open (unsold) positions (67% of positions never sold in the window), so these are lower bounds on losses, not realised losses.
2. Winnings are extremely concentrated. Gini of gross winnings across winning wallets 0.96 (positions 0.93); the top 1% of wallets (7,000) take $103.4M of $108.0M total gross wallet-level profit (96%); top 100 wallets $24.9M; top 0.1% (712) $65.4M. Losses are also concentrated (bottom 1% of wallets = -$384M of -$581M, i.e. a few huge holders, not the crowd).
3. Net winners are NOT "early" per se; they are large, repeat, high-activity wallets that EXIT. Among wallets that bought >$100k in total (2,053 wallets): 63% profitable, median PnL +$10.6k, but also the biggest bag-holders. Wallets that never sell in-window are all losers by construction.
4. Early rank buys that are large and held are the biggest cash "losers" (open bags); early rank buys that exit are the best trade. Small late buyers lose steadily (ROI -31% to -57% among ranks 101+).
5. Funding clusters / labelled wallets: tiny coverage (2,105 wallets in funding table = 0.3%), so cluster inference is weak; GMGN-labelled "smart_money" wallets (1,599) are the only group with positive net cash PnL (+$9.1M, ROI +10%, 68% profitable) - partly circular (label defined by realised cash PnL >=1 on GMGN's own history).

## Coverage and data validity (do this before trusting anything)

- Trades are not a full tape. README: behaviour features come from the most recent 200 trades before each snapshot; the log is a union of per-snapshot fetches. Per token: median 121 trades, p99 533, max 2,564; clear spike at 98-106 trades (about 4,600 core tokens), i.e. a ~100-trade fetch window. Median observed span per token is only 777 s (13 min); only ~5,000 of 31,000 core tokens span >=1 h and ~3,300 >=6 h. So positions are heavily right-censored: "never sold" mostly means "not yet observed to sell".
- Universe: 31,013 tokens are in tokens.parquet ("core", detection snapshots; graduated pump.fun tokens, first logged trade ~ pool start so "entry rank" means rank in the logged tape, i.e. post-graduation pool buyers, not bonding-curve buyers). 35,986 more tokens (4.0M trades, 3.1B USD) appear only in trades ("ext"; median 100 trades, 90th pct span 2.5 days) - head of tape often not guaranteed. 2,765 ext tokens have trades before June 2026 (tiny sprinkling back to 2024).
- Head completeness cannot be verified independently: launch time looks derived from the first fetched trade (first trade is consistently -3..-7 s from "launch"). Cross-check vs sequences.parquet: log trade count >=98% of sequence count for 75% of snapshots, 25% partly covered (5th pct ratio 0.33). Distinct trade wallets / GMGN holder_count median 0.6 (holders include pre-graduation curve buyers not in the log). GMGN volume_h24 is not a usable benchmark (ratio to log volume spans 0.3x-80x).
- Wallets: the log is wallet-level for any wallet in a token's tape, but wallets are only seen in the fetched tokens: 443,725 of 734,407 wallets (60%) appear in a single token; a wallet's "activity level" is therefore dataset-visible activity, a lower bound.
- CRITICAL DATA ARTIFACT: sell USD volume exceeds buy USD volume by 1.7x overall (buys $2.47B, sells $4.23B), physically impossible for a pool (sells cannot exceed buys + seed liquidity). It is concentrated in 2,354 tokens (3.5%; 1,118 core + 1,236 ext) with sells > 1.5x buys + $25k: they carry $2.85B of the $4.23B sells, with dust buys ($0.02) and sells of $18k-$800k per trade (example DQsmfJ..: buys $75k, sells $31.7M). Likely mis-priced sell legs / fake-volume tokens / glitch. If left in, wallet x token PnL shows +$2.2B profit on 329k positions from these tokens (3,569 positions >$100k profit vs 2 losers >$100k) - fake. All results below EXCLUDE them ("conserving universe": tsell <= 1.5*tbuy + $25k): 65,803 tokens, 6,272,114 positions, 711,740 wallets. Pair-level "ALL tokens" contrast: net +$1,760M, 11.9% profitable - do not use.
- Dust: 29% of positions are <$1 (1.84M; $0.3M total). Included in position counts, excluded (buy <$5) in rank analysis.
- Realised cash PnL = sell USD - buy USD per wallet x token (log has no token amounts, so no mark-to-market). Unsold = buys with no sells in-window (4.22M positions, $381M cost, 67%). Partial sells also leave remainders, so "exited" pairs' PnL is also understated if still holding some.

## PnL distribution (conserving universe)

Positions (wallet x token with >=1 buy), n = 6,272,114:
- % profitable 10.7%; % with any sell 32.6%; among sellers 32.7% profitable, median sell/buy 0.86 (p10 0.19, p90 1.63, p99 8.95).
- Position PnL quantiles: p1 -$768, p5 -$205, p10 -$105, p25 -$36, median -$5.6, p75 -$0.04, p90 +$0.04, p95 +$10.8, p99 +$278, p99.9 +$5,211.
- Gross wins $180.3M, gross losses -$653.0M, net -$472.7M. Gini of winning-position PnL 0.933, losing positions 0.910, position size 0.937.
- Young tokens (span <1h): 10.4% profitable, ROI -28%; mature tokens (span >=6h, 7,238 tokens, 856k positions): 12.2% profitable, 65.8% never sold, ROI -36%, median -$4.3. Censoring explains part of the loss, but not all (mature tokens are not better).

Wallets (all tokens in universe): median -$8.5, mean -$664, 10.9% profitable (77,417), p1 -$15.5k, p99 +$1.05k, p99.9 +$31k. Total gross wins +$108.0M, gross losses -$580.7M (ROI on buys -25.6%). Gini of wallet profits among winners 0.962, of losses among losers 0.955. Top 100 wallets = $24.9M, top 1,000 = $72.9M, top 1% = $103.5M, top 0.1% (712 wallets) = $65.4M. Wallets with >=10 tokens (102k): 8.0% profitable, ROI -17%, median -$193 - repeat activity is not generally profitable.

## Decomposition

All tables: conserving universe, cash PnL. netM = sum(sell-buy) in $M; ROI = net/buy; pp = % positions profitable; pp_sell = % profitable among positions with a sell.

### Entry timing (rank among distinct buyers by first buy time in the logged tape; buys >= $5 only)
| rank | positions | buy $M | net $M | ROI | any sell | % profit | % profit among sellers | median sell/buy | open (unsold) buy $M |
|---|---|---|---|---|---|---|---|---|---|
| 1-5 | 469k | 581 | -351 | -60% | 60% | 28.4% | 47.5% | 0.99 | 217 |
| 6-20 | 684k | 464 | +0.3 | 0% | 52% | 18.7% | 35.6% | 0.92 | 23 |
| 21-50 | 1.11M | 407 | -13 | -3% | 45% | 12.9% | 28.8% | 0.85 | 32 |
| 51-100 | 1.22M | 217 | -38 | -17% | 36% | 8.5% | 23.9% | 0.78 | 43 |
| 101-200 | 416k | 122 | -38 | -31% | 34% | 8.5% | 25.2% | 0.72 | 38 |
| 201+ | 102k | 57 | -32 | -57% | 35% | 5.4% | 15.6% | 0.60 | 26 |

Early buyers have a far higher hit rate (28% vs 5%) and the best hit rate among exiters, but the largest cash loss sits in rank 1-5 large positions (>$10k: -$316M, $1k-10k: -$33M) - mostly unsold bags. Counting open positions at cost (neutral scenario), exited positions only: rank 1-5 ROI -37% (-$133M on $364M bought; large exited early buys also lose), rank 6-20 +5.3% (+$23M), 21-50 +5.1% (+$19M), 51-100 +3.2%, 101-200 +0.4%, 201+ -21.7%. So "early" is only mildly positive for exiters and strongly negative for rank 1-5 whales. Gross wins by rank ($M): 47 / 50 / 41 / 23 / 15 / 4; losses: -398 / -50 / -54 / -61 / -53 / -36.
- Robustness: same ordering in core-only, ext-only, uncapped tokens (<95 trades), capped tokens (>=95) and mature (>=6h) subsets (rank 1-5 ROI -0.77/-0.76/-0.84/-0.75/-0.79; rank 201+ ROI -0.56/+0.07/n.a./-0.46/-0.54). Percentile-within-token view (core, >=30 buyers): top 5% -72% ROI, 5-20% -10%, 20-50% -8%, 50-80% -17%, 80-100% -19%.
- Entry delay since first logged trade (core): 0-2 s ROI -83% (net -$171M on $205M, 28% profitable), 2-10 s -11%, 10-30 s -16%, 30 s-2 min -7%, 2-10 min -5%, 10 min-1 h -15%, >1 h -34% (net -$64M).
- Token outcome check (core, early=rank<=20, label max_return_24h): almost all tokens (>97%) have max return <1.2x from detection, so outcome buckets are dominated by one class; 5x+ tokens: later buyers -75% ROI; too few early observations to conclude. Using forward labels here is only descriptive.

### Holding time (time from first buy to first sell)
| first sell after first buy | positions | net $M | ROI | % profit |
|---|---|---|---|---|
| never sold | 4.22M | -381 | -100% | 0% |
| <=10 s | 388k | +3.9 | +1.6% | 32.8% |
| 10-60 s | 452k | -6.2 | -2.5% | 35.9% |
| 1-5 min | 617k | +3.1 | +0.8% | 34.5% |
| 5-30 min | 525k | -93.6 | -18.2% | 27.0% |
| 30 min-6 h | 53k | +2.0 | +3.4% | 36.3% |
| >6 h | 11k | -0.6 | -10.6% | 45.7% |
Fast exits roughly break even in cash (about 1/3 profitable, median -$1); the 5-30 minute holders lose most ($158M gross loss). Selection note: exit time is only observable for positions that exit in-window, longer holds are under-observed. Mature-token subset is similar (5-30 min ROI -29%).

### Trade count per position
Single trade (buy only) 4.22M positions, -$381M; 2-3 trades 1.99M, ROI -20.5%, 32% profitable; 4-10 trades 60.5k positions, ROI +8.7%, 40.8% profitable, median buy $1,270 (bots/whales); 11-30 trades 622 positions, ROI +20.9%, 63.8% profitable, median buy $36k. More repeated trades in the same token => larger, more professional, positive ROI (small n, survivor-ish).

### Position size
| buy size | positions | net $M | ROI | any sell | % profit | median PnL |
|---|---|---|---|---|---|---|
| <$1 (dust) | 1.84M | -0.06 | -21% | 9% | 4.1% | -$0.03 |
| $1-10 | 960k | -2.6 | -52% | 29% | 9.5% | -$4.3 |
| $10-100 | 2.36M | -52.5 | -54% | 38% | 13.4% | -$21 |
| $100-1k | 958k | -87.9 | -34% | 60% | 16.7% | -$112 |
| $1k-10k | 120k | -40.9 | -11% | 85% | 18.1% | -$244 |
| >$10k | 37k | -288.6 | -26% | 74% | 11.3% | -$1,581 |
Small positions lose mostly by not exiting (low any-sell). Mid-large ($1k-10k) exit most and lose least in ROI; very large positions lose most in dollars but include open bags. ROI of exited positions by rank x size (rank 1-5): <$10 +281%, $10-100 +41%, $100-1k +33%, $1k-10k -9%, >$10k -53% - i.e. early AND small AND exited wins; early AND huge loses.

### Wallet activity (wallet level, dataset-visible activity)
| class | wallets | buy $M | net $M | ROI | median PnL | % profitable | any exit | gross win $M | gross loss $M |
|---|---|---|---|---|---|---|---|---|---|
| one token | 428,650 | 180 | -145 | -81% | -$5.7 | 12.9% | 44% | 11.1 | -156.3 |
| 2-4 tokens | 125,098 | 51 | -32 | -63% | -$16 | 8.5% | 55% | 4.1 | -36.4 |
| 5-19 | 98,765 | 129 | -62 | -48% | -$43 | 6.0% | 56% | 8.1 | -69.8 |
| 20-99 | 47,897 | 428 | -70 | -16% | -$337 | 8.1% | 55% | 27.8 | -98.1 |
| >=100 tokens or >=300 trades (bot-like) | 11,330 | 1,061 | -163 | -15% | -$1,768 | 15.4% | 94% | 56.9 | -220.1 |
Bot-like wallets (1.6% of wallets) take 53% of gross wins ($56.9M of $108M) AND 38% of gross losses ($220M of $581M); their ROI is -15% (much better than occasional wallets -48% to -81%), so the pros are the least-bad, not clearly profitable as a class. In the top 1% by profit: 1,423 bot-like wallets (+$56.7M), 2,227 active (+$27.2M), 1,262 regular, 613 occasional, 1,475 one-token lucky wallets (+$9.3M). Bottom 1%: 4,821 one-token wallets (-$105M) and 883 bot-like (-$186M). Top 1% profile: median total buy $6.3k, 21 tokens, 48% win-rate of positions, 30% have all positions exited; bottom 1%: median buy $22k, 1 token.
- Median inter-trade gap: wallets with gaps 2 min-1 h (67k, the bulk of capital, $1.5B) net -$238M, ROI -16%; 10 s-2 min wallets (7.5k) ROI -16%; 1-10 s gaps (589 wallets, tiny but profitable: ROI +12%, 61% profitable, median +$0.24); >1 h gaps (99k) ROI -62%, 2.9% profitable.
- Sniper share (entry within 2 s of tape start): wallets that are >=50% snipes (3,972) are the worst: net -$209M, ROI -79% (but 37% win rate - big losers dominate); non-snipers (193k wallets with >=3 tokens) ROI -8%.
- Fast trading (>=50% gaps <=1 s): only 13 wallets, so no inference.
- Total wallet buy size: <$100 ROI -61..-64%; $100-1k -52%; $1k-10k -48%; $10k-100k -52%; >$100k (2,053 wallets) ROI -13%, 63% profitable, median +$10.6k, gross wins $69.6M and gross losses -$230.8M: a polarised group (the whales also own the biggest bags).

### Funding clusters and labelled wallets
- wallet_funding: 15,493 edges, 2,105 wallets, 4,921 funders; only 0.3% of wallets, evidently the labelled/profiled subset, so selection bias is severe. Funders with fan-out >=3 funded wallets: ~160 funders; 700 wallets are in a shared-funder cluster (>=3 wallets), 50 in a pair, 1,340 have a unique funder.
- Cluster members: shared funder (>=3): 700 wallets, ROI -54%, net -$30.7M, median -$648, 16% profitable, median 52 tokens; unique funder: 1,340 wallets, ROI -13%, 22% profitable; no-funding-data: ROI -26%. Hence cluster membership (as far as measurable) is associated with WORSE cash PnL (crews dumping onto each other / holding insider-style bags), not better; 233 of the top-1% winners are in the funding table (3.3% of top vs 0.3% base: over-represented, but it's a profiled subset).
- wallets.parquet types: smart_money 1,599 wallets: net +$9.1M, ROI +10.3%, 68% profitable, 99.7% exit; insider 6,126: net -$180.8M, ROI -15.7%, 24% profitable, but gross wins $62.8M; normal 4,090: ROI -48%, 2.6% profitable; unlabeled 699,925: net -$292M, ROI -49%. Top-1% winners: 582 smart_money, 1,307 insider, 36 normal, 5,075 unlabeled (so 72% of top winners are not tagged).

## Who funds the winners

Mechanics: in the conserving universe the cash identity is participants' net = -(pool/holder residual). The $473M net outflow from participants is (a) unrealised bags still held at the end of each observation window (unquantified - no token amounts) and (b) AMM fees and the pool's retained inventory. The group view:
- Winners: ~7,000 wallets (1%) with median $6.3k committed, 21 tokens, mostly active/bot-like (63% of their profit from classes 3-4), exiting quickly, entering ranks 6-100 or small early, hit rate ~48% of positions. They capture $103M.
- Funders (loss pool, -$581M gross loss at wallet level): (1) 428k one-token wallets losing -$156M (27% of losses; 87% of wallets of that class lose, ROI -81%), (2) occasional/regular wallets -$106M, (3) very large holders: bottom 1% (7,000 wallets, median buy $22k) -$383M (66% of losses) - mostly early big buyers sitting on unsold bags, i.e. the "loss" is partly mark-to-market and may be partially recovered. Late small buyers (rank 51+ , size <$1k) lose a steady 15-57% with low profit rate (5-9%) - they are the reliable funders: rank 51-200 net -$76M, ranks 201+ -$32M.
- Gross wins by rank are fairly flat (47/50/41/23/15/4 $M) while losses are -398 in rank 1-5 - so the winning money comes from ranks 6-100 positions that exit, and the loss from rank 1-5 held positions.

## Caveats / what not to conclude

- Cash PnL ignores unrealised value; any claim "X loses" is a claim about cash out vs in within a 13-minute median window. Wallet-level "profitable" share (10.9%) is a floor for true profitability (open positions that later pumped; 5x+ tokens are <1.5% of core tokens).
- Early rank is within the logged post-graduation tape; bonding-curve snipers, bundlers and dev buys are not captured; rank 1-5 includes insiders/dev. Ext tokens may have missing heads.
- Non-conserving tokens (3.5%, with 67% of reported sell volume) were excluded; if they are real, they would reverse the sign (+$2.2B), so the sign of the aggregate depends on that exclusion. Individual wallet and token level rankings in the top 100 should be inspected for artefacts. Conservation threshold (1.5x buys + $25k) is heuristic; I did not run a sensitivity.
- 20 days, single regime (June 2026); survivorship (graduated tokens only for core); wallet class and sniper definitions are my heuristics (>=100 tokens or >=300 trades for bots); funding coverage 0.3%. smart_money label is circular w.r.t. cash PnL.
