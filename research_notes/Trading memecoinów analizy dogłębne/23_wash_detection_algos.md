# Wash-trading and manipulation detection algorithms for DEX/memecoin tokens (for a Solana memecoin bot)

Research constraints: 8 web searches; arxiv.org was NOT reachable via WebFetch (network allowlist), so all paper details come from search-result summaries only. Anything not in a cited snippet is marked UNVERIFIED. Per-paper precision/recall mostly could not be retrieved.

## 1. What do the academic methods (Victor & Weintraud, Cong et al., graph/cycle, MemeTrans) actually do, and what accuracy is reported?

### Takeaway
Victor & Weintraud detect wash trades at account level on order-book DEXes using volume-matching inside strongly connected components (SCCs); Cong et al. only detect exchange-level wash volume statistically (Benford, round-number clustering, tails); MemeTrans is a supervised launch-risk dataset on Solana. None of the sources I could access report clean precision/recall for wash-trade classification; reported numbers are prevalence counts or (MemeTrans) a financial-loss reduction.

### Cited Findings
- Victor & Weintraud (WWW '21, TU Berlin) study IDEX and EtherDelta; they identify a lower bound of wash trading with volume equivalent to 159 million USD; structures are mainly 1-2 accounts but more complex ones exist; self-trades are frequent and "could easily be prevented"; >30% of tokens on both exchanges had wash activity; 10% of EtherDelta tokens were almost exclusively wash traded — [arXiv abstract via search](https://arxiv.org/abs/2102.07001)
- Their algorithm is a volume-matching procedure run within frequently occurring strongly connected components, which avoids exponential time complexity; 3+ account structures were mainly on IDEX — [arXiv listing / search summary](https://arxiv.org/abs/2102.07001v1), [ar5iv](https://ar5iv.labs.arxiv.org/html/2102.07001)
- Their framing is a conservative "lower bound" meeting legal wash-trading definitions (so by design high precision, unknown recall); the closed-cycle topology of wash trades is noted as known from traditional-finance research — [arXiv PDF via search](https://arxiv.org/pdf/2102.07001)
- Cong, Li, Tang, Yang "Crypto Wash Trading" (NBER w30783; Management Science 2023): applies Benford's law on first digits, clustering of trade sizes at round numbers, and power-law tails; sample of 3 regulated and 26 unregulated exchanges (Jul 9–Nov 3, 2019); no wash trading found on regulated exchanges; estimates on average >70% of reported volume on unregulated exchanges is inflated; method identifies exchange-level patterns, not individual trades — [NBER](https://www.nber.org/system/files/working_papers/w30783/w30783.pdf), [arXiv](https://arxiv.org/pdf/2108.10984)
- Intuition: wash volume avoids the round-number clustering of genuine (human) trade sizes — [search summary of Cong et al.](https://arxiv.org/pdf/2108.10984)
- Aloosh & Li (Management Science 2024) validated indirect tests against leaked Mt. Gox internal records (direct wash-trade labels): Benford, trade-size clustering, lognormal conformity and structural-break tests found useful; exact validation statistics NOT retrieved — [INFORMS](https://pubsonline.informs.org/doi/full/10.1287/mnsc.2021.01448)
- Graph/cycle methods (NFT markets, transferable): wash trading appears as cyclic/repetitive trades, more prominent inside SCCs; one large NFT study builds a directed multigraph per NFT, enumerates cycles by DFS and confirms round-trips only when a cycle meets repetition thresholds — [arXiv 2403.10361](https://arxiv.org/pdf/2403.10361), [arXiv 2312.12544](https://arxiv.org/pdf/2312.12544)
- A TUM master's thesis (Wiedenmann, June 2025) builds a Solana wash-trading detection framework using SCCs plus volume-symmetry checks; I could not read it, so thresholds/accuracy unknown — [thesis PDF](https://www.cs.cit.tum.de/fileadmin/w00cfj/sebis/thesis/250610_Wiedenmann_Thesis.pdf)
- Mongardini & Mei, "A Midsummer Meme's Dream" (USENIX Security 2026): 34,988 meme coins on Ethereum, BSC, Solana, Base; among tokens with >100% return, 82.89% show artificial-growth evidence; introduces Liquidity-Pool-Based Price Inflation (LPI); three combined wash-detection methods flag 3,264 potential instances on 377 tokens from OHLCV, and 1,014 events with strong evidence (31.07% of suspected); these are counts/overlap, not precision/recall — [arXiv 2507.01963](https://arxiv.org/abs/2507.01963v2), [USENIX](https://www.usenix.org/conference/usenixsecurity26/presentation/mongardini)
- MemeTrans (Georgia Tech, arXiv 2602.13480; v2 retitled "MELT: A Behavioral Trace Dataset for High-Risk Memecoin Launch Detection"): 41,470 Pump.fun tokens that migrated to Raydium, 122 pre-migration features (launchpad trading behavior, holding concentration, bundle statistics), hybrid risk annotation; high-risk launches show shorter launchpad-sale duration, fewer transactions/buyers, larger per-buyer accumulation; manipulation shows as concentrated holdings, multi-address coordination ("bundles"), suspicious wash trading; models cut financial loss by 56.1%; single launchpad, ~4-month window — [arXiv](https://arxiv.org/abs/2602.13480), [HTML](https://arxiv.org/html/2602.13480), [code](https://github.com/git-disl/MemeTrans)
- A July 2026 preprint (arXiv 2607.02795) reports 1,012 "Persistent Wallet Rings" on pump.fun buyers; method unconfirmed — [arXiv](https://arxiv.org/abs/2607.02795)

### Inferences
- Order-book DEX self-trades (same account both sides) have no direct AMM/bonding-curve analogue: on Solana AMMs/pump.fun a "self-trade" is a wallet buying and selling the same pool, or a cluster of wallets controlled by one entity, so detection must be wallet-cluster + round-trip based, not counterparty-matching.
- Cong et al.'s tests need many trades per window (Benford needs hundreds+); on a young memecoin with few trades they are weak and are better as a slow, venue/token-level prior than a per-trade gate. (Own reasoning.)
- Because Victor & Weintraud is a lower-bound/legal-definition design, expect high precision, low recall; a bot wants the opposite trade-off (flag more, accept false positives).

### Gaps
- No precision/recall retrieved for any of: Victor & Weintraud (likely none reported; no ground truth), Cong et al. (exchange-level), Aloosh & Li validation, TUM thesis, MemeTrans per-model F1/AUC. arxiv.org fetch failed (blocked host); allowing arxiv.org would let a follow-up read exact thresholds (e.g. V&W minimum trade counts and balance tolerance — I could not confirm "1% volume" or "25 trades"; UNVERIFIED).
- MemeTrans exact feature list and wash/bundle definitions not read.

## 2. Concrete real-time-friendly algorithm for a Solana memecoin bot

### Takeaway
Use a tiered pipeline: cheap O(1) per-trade streaming features (bundles at launch, round-trip wallets, concentration), a rolling small-graph cycle/volume-symmetry check on a bounded window, and a slow statistical prior (round-number/size-entropy) — outputs a 0-100 manipulation score with hard-veto rules. All thresholds below are ASSUMPTIONS to be calibrated on labelled data (e.g. MemeTrans dataset); none are from the cited papers unless stated.

### Cited Findings
- Design anchors from literature: SCC + volume-matching (Victor & Weintraud), cycle enumeration with repetition thresholds (NFT studies), bundle/launchpad-sale features and concentration (MemeTrans), round-number clustering (Cong et al.) — sources as in section 1.

### Inferences (design; thresholds = ASSUMPTIONS)
```
# State per token (ring buffer of last W=500 swaps or T=30 min) 
# Event: swap{slot, sig, wallet, side, sol_amt, token_amt, funder(wallet)}

on_swap(tok, s):
  # --- Stage 0: wallet clustering (maintained incrementally) ---
  cluster = union_find.find(s.wallet)
  # union wallets sharing: same funder within 1h, same-slot/same-tx buys at launch (bundle),
  # direct SOL/token transfers between them
  # (ASSUMPTION: funder-sharing and same-slot rules; MemeTrans uses "bundle" traces, details UNVERIFIED)

  # --- Stage 1: O(1) streaming features ---
  upd(tok.cluster_stats[cluster], s)         # buy_sol, sell_sol, n_buys, n_sells, first/last slot
  tok.top10_cluster_share = share of supply held by 10 largest clusters
  tok.bundle_share = supply bought in launch slot(s) 0..2 by clusters / supply sold on curve   # ASSUMPTION window 3 slots

  # --- Stage 2: round-trip / self-trade per cluster ---
  for c in clusters touched:
     rt = min(c.buy_sol, c.sell_sol) / max(c.buy_sol, c.sell_sol, eps)   # volume symmetry
     if c.n_buys>=3 and c.n_sells>=3 and rt>0.85 and c.net_token_position < 5% of its max:  # ASSUMPTION
         wash_vol += min(c.buy_sol,c.sell_sol)
  wash_ratio = wash_vol / total_vol_window

  # --- Stage 3: cycle check every N=20 swaps or 5 s (bounded cost) ---
  G = directed graph over clusters/wallets from token/SOL transfers + swaps vs pool in window
  for scc in tarjan_SCC(G) where 2<=|scc|<=8:             # ASSUMPTION size cap, avoids exponential cost
     matched = volume_match(scc)       # V&W-style: matched volume = min(in,out) per node, balance tol 5% (ASSUMPTION)
     if repeats>=3 (cycle seen >=3x) and matched/ vol_window > 0.2: flag_cycle(scc)

  # --- Stage 4: distribution tests (only if n_trades>=200; else skip) ---
  size_round_share = frac(trade sizes within 1% of {0.1,0.5,1,5,10 SOL}); compare to baseline from
        known-organic tokens; z-score; low share + high trade count = suspect (Cong et al. direction)
  benford_MAD of first digits of sol_amt; MAD>0.015 suspect  # ASSUMPTION (0.015 is a common MAD "nonconformity" cut in Benford literature, UNVERIFIED here)
  interarrival_cv: bot-regular intervals (CV<0.3, ASSUMPTION)

  # --- Stage 5: score ---
  score = 30*clip(wash_ratio/0.4) + 20*clip(top10_cluster_share-0.5)/0.3 + 20*clip(bundle_share/0.25)
        + 15*cycle_flag + 10*dist_flag + 5*regularity_flag          # weights ASSUMPTIONS
  VETO if: wash_ratio>0.5 OR bundle_share>0.4 OR single cluster>30% supply (excl. LP/curve)   # ASSUMPTIONS
  action: score<30 allow; 30-60 reduce size/ tighter stop; >60 or VETO skip
  # Use *wash-adjusted* volume & unique-organic-buyers (excl. flagged clusters) for any volume-momentum signal.
```
- Complexity: Stages 1-2 O(1) per swap; Stage 3 bounded by window size; Stage 4 batched. Fits a Yellowstone/Geyser stream.
- Calibration plan: label via MemeTrans (public dataset/code at github.com/git-disl/MemeTrans), tune thresholds to maximize recall at a fixed false-veto rate (missing a rug costs more than skipping a good token); backtest the "wash-adjusted volume" signal vs raw.
- Failure modes: attackers use many fresh funded wallets (breaks funder clustering), varied round-trip amounts via different routes/DEXes (breaks symmetry), and cross-pool/bridge routing; MEV/arb bots and market makers create legitimate round trips (false positives) — whitelist known arb/MM programs.

### Gaps
- Thresholds are uncalibrated assumptions; no cited paper supplies Solana-AMM-specific values. Cross-token/cross-pool cluster detection and Jito-bundle-aware features not researched. Real-time latency benchmarks not measured.
