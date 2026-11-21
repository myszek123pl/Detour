# Practitioner memecoin tactics vs. our measured evidence

Date: 2026-11-21. Data reference: `reports/Backtest memecoinów podsumowanie.md` (9,684 tokens, June 2026, 15m candles; bot logs; wallet/order-flow analyses).

## Method and limits (read first)
- WebFetch failed for every page tried (DNS/allowlist): threadingontheedge.substack.com, insightfulinfo.substack.com, docs.mobula.io, madeonsol.com, www.publish0x.com, fomo.family. These hosts need allowing in the session network settings before the full guides can be read. I did not try to bypass this.
- Everything below comes from WebSearch result summaries (secondary, not full-text reads). Numeric thresholds are as reported by those summaries; treat as unverified.
- GitHub: `search/repositories` found only `buddies2705/awesome-memecoin-trading` (24 stars, tool list; repo access returned 403, content not read). No "trenches guide" repos found for the queries tried (trenches guide, handbook, pump.fun strategy, gmgn guide).
- Most sources are vendor/affiliate or anonymous. None publishes measured returns. The practitioner side is therefore heuristics, not evidence.

## Sources (search-surfaced, not fully read)
- Dextools tutorials: how-to-spot-a-good-memecoin, memecoin-checklist-2026-entry-guide, how-to-trade-meme-coins-professional-guide, what-is-the-dev-sold-meaning (dextools.io/tutorials/...)
- Mobula "detecting snipers/bundlers": https://docs.mobula.io/almanac/detecting-snipers-bundlers
- Substack "The ultimate trenches playbook": https://threadingontheedge.substack.com/p/the-ultimate-trenches-playbook-and
- Substack "Stop roundtripping your massive memecoin": https://insightfulinfo.substack.com/p/stop-roundtripping-your-massive-memecoin
- Publish0x Axiom pro guide: https://www.publish0x.com/wallet-trackers-copy-trading-analysis/axiom-pro-trading-guide-sol-bnb-eth-crypto-exchange-xmgmezr
- fomo.family trader write-ups (notanicecat69, logjam): https://fomo.family/blog/learn/notanicecat69-memecoin-trading-strategy
- MadeOnSol CTO radar guide: https://madeonsol.com/blog/solana-community-takeovers-cto-radar-guide ; PumpSwap/graduation explainers on same site
- crypto.news CTO explainer; crypto.news "what are the trenches" slang; airdropalert glossary; Notion "Memecoin Trading Rules checklist"; Telegram t.me/s/ctrlhub/2011
- The Block on PumpSwap (Mar 2025) and BOOST graduation change (Jul 2026): https://theblock.co/post/409815/pump-fun-token-graduation-rate-jumps-boost-changes-launch-incentives
- Nansen top memecoin wallets: https://nansen.ai/post/top-10-memecoin-wallets-to-track-for-2025
- Academic paper surfaced: https://sbfc.sydney.edu.au/2025/papers/SBFC2025_4G3_P154.pdf (not read)

## Tactic-by-tactic comparison

| Practitioner tactic (as reported) | Our data | Verdict |
|---|---|---|
| **Holders tab in first minutes**: no wallet >2-3% supply (ex LP/burn); top-10 >15-20% = dump risk; many red-flagged/bundled wallets = avoid | Dev >20% supply -> 62-69% dumps vs 38% base; dev/sniper-heavy tokens bad; but "low bundlers/insiders + liquidity" rule that looked profitable was a data bug (-27.5% on reliable features) | Agrees as an exclusion filter. Conflicts if read as an entry signal: passing the filter does not make a token profitable. |
| **Snipers**: Snipers Max ~3, no snipers in top 20, "snipers haven't sold = yellow flag" | Snipers net -79%; sniper-held supply is a warning | Agrees (avoid). Note we measure snipers as losers, which cuts against the idea that they are the informed dump source; exit liquidity risk still holds. |
| **Bundles**: same-block multi-wallet buys hide insider ownership; check GMGN red flags | Insider flags work as warnings; 14-33% of volume is same-wallet fast buy+sell (wash-like) | Agrees; volume/holder counts are manipulable, so the holders tab itself is noisy. |
| **Dev history / dev sold** as a check | Developer history predicts nothing (AUC 0.52); dev share does | Partial conflict: check dev holdings, not dev track record. |
| **Read the chart early; enter on momentum/volume** | 67% of tokens peak in first 15m candle, 86% in 1h; median 0.65x entry at 24h; no momentum; reversal after +50%; buying after pump candle = median -20% (1h), -38% (4h); 87% of pump-candle sells are earlier buyers | Conflicts. Chasing strength loses. Only candidate signal (>=90% buy-share candle -> +17% in 15m) vanishes with one candle of delay. |
| **Buy dip / "second leg"** after -50% (not clearly defined in sources found) | Return to entry after a -50% drop only 6.6%; catching >50% drops is an exclusion rule | Conflicts. Second legs are rare in our sample; survivorship bias in anecdotes. |
| **Migration play**: buy at 50-70% curve fill, sell into graduation surge | Curve: after ~55 SOL doubling is infeasible; 10% supply dump on pool = -55% price; pump.fun zero-sum minus fees/trapped SOL; most tokens never graduate (sources agree) | Conflicts/unsupported. We have no clean graduation-event study; BOOST (Jul 2026 buys/burn first 5 min) postdates our June data, so effect untested. Flag as gap. |
| **CTO plays**: dev gone, community revives; verify dev sold, who controls socials, fake CTOs | No CTO-specific measurement; "dev holds small stake" can be CTO per sources; our data show 6.6% recovery after -50% | Untested. Prior is negative given recovery rate. Practitioners themselves warn of fake CTOs. |
| **Narrative rotation** | Not measured; regime analysis: good days cluster (r~0.6) but no June day was profitable | Unsupported; regime acts as brake, not source of profit. |
| **Wallet tracking / copy smart money** (Nansen, Axiom/GMGN trackers, Kolscan) | 10.9% of wallets profitable; 1% take 95% of gross profit; copy-trading -22% to -38% OOS; top-20 Kolscan -23% at 2s lag; bots take 53% of profit but net -15% | Conflicts strongly. Winners are concentrated and not copyable under latency; Nansen itself lists whale manipulation. |
| **Take initials at 2x**, scale out (e.g. 25% @ +100%, 50% @ +500%, 75% @ +1000%), keep runner bag | 10,962 exit-rule combinations walk-forward: 0 profitable out of sample even at zero cost; 473 profitable in-sample (overfit); stops slipped (-18% stop filled ~-84%) | Neutral-to-conflict. Taking initials is risk bookkeeping, not an edge; no exit schedule beat the baseline. Stops are unreliable on pump.fun. Practical: can't rely on stop-loss execution. |
| **Position sizing**: 1-2% of portfolio per coin, 5-10% total memecoin allocation, "only what you can lose" | Per-trade loss -17% to -34% at 200 USD with no filter; execution gap (ideal -7.2%, bot -26.7%, manual -29.2%) dominated by slippage; size small vs liquidity | Agrees. Sizing is the only advice the data directly supports. |
| **Speed / sniping**: be early | Only profitable bot entered in the same second as launch, ~180 USD, ~6 s hold, 938k USD/111 days; home latency not replicable | Agrees that speed is the edge; disagrees that retail can get it. |
| **Timing (hour/day/token age)** (not prominent in sources) | No edge | Neutral. |
| **Liquidity/seller-dominance checks** | Exclusions that work: low liquidity, seller dominance, falling knives | Agrees. |

## Vocabulary (from glossaries; definitions as reported)
- Bundle: several wallets buying in the same block, usually one controller, hiding insider ownership.
- Sniper: bot buying in the first moments of a launch.
- CTO: community takeover of an abandoned token (fake CTOs by the dev's second account exist).
- Dev sold: creator exited; usually bearish, small dev stake can precede a CTO.
- Paper hands: sells at first fear. Runner: coin climbing for days/weeks.
- Take initials: sell enough (typically at ~2x) to recover the original stake.
- Graduation/migration: pump.fun curve completes (~$69k-era threshold, may change) and liquidity moves to PumpSwap (since Mar 2025; 0.25% fee, no 6 SOL migration fee).
- Cook: used for a coordinated group controlling supply (inferred from a Telegram post, not formally defined).
- The trenches: earliest, riskiest new-token stage.

## Summary
- Agree with data: exclusion filters (dev/insider/sniper concentration, low liquidity, seller dominance), small sizing, not chasing pumps' aftermath, slippage matters.
- Conflict: chasing momentum, dip-buying second legs, copy-trading smart wallets, believing that exit schedules (initials/scale-out) create edge, bonding-curve migration front-running.
- Untested in our data (gaps): clean graduation-event study, CTO outcomes, narrative rotation, post-BOOST (Jul 2026) behavior. A 100%-fill graduation dataset and the unread full-text guides (hosts above) would close these.
- Caveat on practitioner side: survivorship bias, affiliate incentives, no reported denominators.
