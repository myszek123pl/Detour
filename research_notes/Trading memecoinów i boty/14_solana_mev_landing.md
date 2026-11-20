# MEV and Transaction Landing on Solana for Memecoin Trading Bots (as of November 2026)

> **Research-process caveat for the report writer:** This session had severe tool limits. Every direct page fetch failed (hosts not on the network allowlist: docs.jito.wtf, helius.dev, solana.com, dev.to, cryptoslate.com, cryptobriefing.com, blockworks.co), and the shared web-search budget ran out after about 10 queries. Every finding below comes from **search-engine result summaries**, not from reading the full pages. Treat the numbers as indicative and check them against the primary pages before publishing. Background knowledge that I could not source is kept in the Gaps sections and marked "unverified".

## 1. Jito block engine, bundles, tips, the Jito mempool, and how common sandwiches are

### Takeaway
Jito's public mempool was shut down in March 2024, but sandwiching continued through private mempools and Jito bundles. Estimates of how much sandwich bots take from Solana users range from about $30M (Bitquery, gross, one window) to $370–500M over 16 months (sandwiched.me), depending on method. Several sources in 2025–2026 report that sandwiching is declining. Memecoin traders using high slippage are the main victims.

### Cited Findings
**Jito mempool and private mempools**
- Jito Labs abruptly shut down its mempool function in March 2024. Its terms of service had banned front-running, but sandwich attacks happened anyway, and Jito called MEV, including sandwich attacks, a drag on the Solana ecosystem — [CoinDesk, 2024-03-08](https://www.coindesk.com/business/2024/03/08/solana-client-developer-jito-announces-end-of-mempool-function); [The Block](https://www.theblock.co/news/ecosystems/2024-03-09-solana-client-jito-labs-axes-mempool-function-following-increase-in-mev-attacks-281504); [Blockworks](https://blockworks.co/news/jito-labs-suspends-mempool-functionality)
- Helius says the suspension cost Jito significant revenue and immediately reduced harmful MEV — [Helius, Solana MEV Report](https://www.helius.dev/blog/solana-mev-report)
- After the shutdown, "underground"/private mempools that enable sandwiching appeared. The Solana Foundation removed 32 validators from its delegation program for taking part in sandwich attacks. CoinDesk, citing anonymous sources, said most of them were run by Russian citizens. This was a removal from the delegation program, not a protocol-level ban — [Forklog](https://forklog.com/en/solanas-jito-mempool-disabled-amid-mev-bot-surge/); [Unlock-bc](https://www.unlock-bc.com/124423/solana-foundation-expels-validators-facilitating-sandwich-attacks-delegation-program)

**Bundle-level defence: `jitodontfront`**
- If you add any public key that starts with `jitodontfront` to an instruction as a read-only account, the Jito block engine requires that any bundle containing that transaction place it at index 0. The account never has to exist on-chain. For example, `[trade, tx_with_dontfront, arbitrage, tip]` is rejected — [Solana docs: MEV Protection with Jito DontFront](https://solana.com/docs/defi/mev-protection); [Chainstack docs](https://docs.chainstack.com/docs/solana-mev-protection.md)
- Limits: it only protects transactions sent through the Jito block engine (transactions sent straight to validators are not covered). Jito says it "may help reduce" sandwiches but does not guarantee it. Solana's guide recommends tight slippage alongside it, and it does not work on devnet or localhost — [Solana docs](https://solana.com/docs/defi/mev-protection)

**How much sandwiching there is**
- sandwiched.me launched in June 2024 as a sandwich-only tracker. Its researchers say they analyzed 8.5B trades and about $1T of Solana DEX volume, and estimate that sandwich bots took **$370M–$500M** from Solana users over about 16 months — [Solana Compass, "Scale or Die at Accelerate 2025: The State of Solana MEV"](https://solanacompass.com/learn/accelerate-25/scale-or-die-at-accelerate-2025-the-state-of-solana-mev)
- The top sandwich bot on sandwiched.me ("B91") reportedly made about 7,800 SOL gross in 30 days from nearly 80,000 victims — [Solana Compass, Accelerate 2025](https://solanacompass.com/learn/accelerate-25/scale-or-die-at-accelerate-2025-the-state-of-solana-mev) (secondary summary; not verified on the live site)
- Validator "sandwich rate" is the share of a validator's blocks with at least one sandwich in a 30-day window. The average is reported at around 5%, with outliers at 30–60% — [Solana Compass, Accelerate 2025](https://solanacompass.com/learn/accelerate-25/scale-or-die-at-accelerate-2025-the-state-of-solana-mev) (the exact attribution is unclear in the search summary)
- Bitquery estimated **$29.7M** taken by Solana sandwich bots "before costs". It values SOL at the minute of each attack and does not measure net profit — [CryptoSlate](https://cryptoslate.com/solana-sandwich-bots-took-29-7-million-before-costs-bitquery-estimates/). It conflicts with the sandwiched.me figure by more than 10x, which points to different time windows and detection methods.
- MEV Monitor (Mirror post, written for a Helius hackathon) found **87,061 sandwiches in one week**, taking about **$620k** from users. Attacker costs were mostly Jito tips (about 352 SOL), with base fees around 1.2 SOL, for an estimated net attacker profit of about $571k — [Mirror: MEV Monitor, Solana Sandwich Attacks](https://mirror.xyz/0x7c855e1bF411Ab5975235bC8C74E032615073044/mwh7Bkqp_nmsOkW6T7ee4tqXyXYgaRwLQd8zi38HbcY)
- Ghost's analysis says **"wide" (multi-slot) sandwiches** took about **529,000 SOL** over a year. In wide sandwiches the front-run and back-run land in different slots, often sent by colluding leaders or private mempools rather than as a single Jito bundle. Ghost also found sandwichers made less money in one period than in the same months a year earlier — [Ghost thread via ThreadReader](https://threadreaderapp.com/thread/1978555200802885699)
- sandwiched.me tracks wide sandwiches and lets users look up a transaction or wallet — [Solana Compass, Accelerate 2025](https://solanacompass.com/learn/accelerate-25/scale-or-die-at-accelerate-2025-the-state-of-solana-mev)
- Anza's Max Resnick said "the sandwiching rate [is] way down" — [Blockworks](https://blockworks.co/news/solana-sandwich-attacks-down)
- A three-year study reported that Jupiter Ultra users face fewer sandwich attacks than other users. I saw only the headline — [CryptoBriefing](https://cryptobriefing.com/jupiter-ultra-sandwich-attacks-study/)
- Other datasets: Flipside "Sandwiches on Solana" dashboard ([Flipside](https://api.flipsidecrypto.com/MostlyData_/sandwiches-on-solana-oEkMtY)), Solscan sandwich leaderboard ([Solscan](https://info.solscan.io/exploring-sandwiches-activity-leaderboard)), Chorus One MEV analysis ([Chorus One](https://chorus.one/articles/analyzing-mev-instances-on-solana-part-2))

### Inferences
- With no public Jito mempool, the remaining sandwich risk comes from (a) RPCs or relays that leak order flow to searchers, (b) validators running private mempools, who can do wide, multi-slot sandwiches without bundles, and (c) transactions sent to Jito without `jitodontfront`. A bot's main defence is to control where its order flow goes.
- The 529k SOL/year wide-sandwich figure and the 5% / 30–60% validator sandwich rates suggest that a small group of leaders causes most of the harm. Leader-aware routing, meaning not sending, or sending only protected transactions, when a known high-sandwich-rate validator is leader, is a sensible defence.
- Memecoin swaps on bonding curves and new AMM pools are the most exposed because users set very high slippage (often 10–50% in bot UIs). Sandwich profit is capped by slippage tolerance, so these trades are the most profitable to attack.

### Gaps
- I could not read sandwiched.me's live dashboard or a 2026 total. The $370–500M figure dates from around mid-2025 (Accelerate 2025).
- I found no arXiv or peer-reviewed paper on Solana sandwiching; the search budget ran out before that query.
- Unverified (training knowledge, not sourced here): Jito bundles hold up to 5 transactions, run atomically and in order, and are sold in an auction about every 200 ms. The minimum tip is 1,000 lamports, paid to one of 8 tip accounts. A tip-floor API reports percentile tips. "Uncle bandit" risk means bundle transactions from forked/uncled blocks can be rebroadcast without the bundle's protection. The madeonsol "5-TX Max" page in search results ([madeonsol](https://madeonsol.com/blog/what-is-jito-mev-solana)) seems to confirm the 5-transaction limit, but I did not read it.
- I found no 2026 figure for total Jito tips. Indirectly: Jito protocol revenue fell 45% quarter-on-quarter to $1.28M in Q2 2026 — [Solana Compass](https://solanacompass.com/news/jito-q2-2026-protocol-revenue-falls-45-to-128m-as-bam-reaches-33-of-solana-stake)

## 2. Priority fees and compute units: how to set them dynamically

### Takeaway
Priority fee = compute-unit limit × compute-unit price (micro-lamports per CU) ÷ 1,000,000, and you pay for the **requested** limit, not the CUs actually used. The standard method: simulate to get CUs consumed, add a 10–20% buffer, then set the price from recent fees on the **specific accounts** you write to, at a percentile that matches how urgent the trade is (for example, Helius `getPriorityFeeEstimate`).

### Cited Findings
- Priority fee = CU limit × CU price (micro-lamports), divided by 1e6 to get lamports. The fee is based on the requested limit, so an oversized or default limit wastes money — [Helius: Priority Fees Best Practices](https://www.helius.dev/docs/priority-fee/best-practices); [Metaplex: Compute Units and Priority Fees](https://www.metaplex.com/docs/solana/compute-units-and-priority-fees)
- The default is 200,000 CU per instruction, with a maximum of 1,400,000 CU per transaction — [Metaplex](https://developers.metaplex.com/solana/compute-units-and-priority-fees)
- Run `simulateTransaction` with a high placeholder limit, read `unitsConsumed`, and set the limit to that plus a 10–20% buffer — [Helius docs](https://docs.helius.dev/guides/how-to-set-up-priority-fees-on-solana); [GetBlock guide](https://docs.getblock.io/guides/how-to-optimize-solana-transactions-with-priority-fees)
- Use `getPriorityFeeEstimate` with the serialized transaction containing all real instructions (except the fee instruction), or with `accountKeys` and `priorityLevel` (for example "High"). The recommended value goes into `setComputeUnitPrice` — [Helius best practices](https://www.helius.dev/docs/priority-fee/best-practices)
- Fee estimation means taking recent fees on the specific accounts used, at a percentile. For contested accounts, pay higher fees or retry with exponential backoff — [OrbitFlare: Solana Priority Fee Estimation](https://orbitflare.com/blog/developers/solana-priority-fee-estimation); [GetBlock](https://docs.getblock.io/guides/how-to-optimize-solana-transactions-with-priority-fees)
- Raydium and Chainstack publish guides on priority-fee tuning and the compute budget — [Raydium docs](https://docs.raydium.io/integration-guides/priority-fee-tuning.md); [Chainstack](https://docs.chainstack.com/docs/solana-compute-budget.md)
- A rough baseline of 1,000–5,000 micro-lamports per CU for general use, with a warning to monitor recent fees for your use case — [Metaplex](https://www.metaplex.com/docs/solana/compute-units-and-priority-fees) (not applicable to contested memecoin launches)

### Inferences
- For a memecoin bot, the useful fee signal is per-account: the bonding-curve or pool account of the token being traded, not the global network median. A hot launch can need fees orders of magnitude above the network median while the rest of the chain is quiet.
- Two separate "bids" decide landing: the priority fee (orders transactions inside the scheduler) and the Jito/landing-service tip (gets the transaction into a bundle or a fast lane). Many landing services require a minimum tip on top of the priority fee, so a bot should tune both.
- A tight CU limit (simulated plus buffer) lowers cost and can help scheduling, because the leader's scheduler packs blocks by CU and per-account CU limits.

### Gaps
- I could not verify the 2026 block CU limit (it has been raised in steps; unverified: 48M → 50M → 60M CU proposals) or how Alpenglow changes fee markets.
- I found no source on the exact percentile mapping of Helius `priorityLevel` values (Min/Low/Medium/High/VeryHigh/UnsafeMax) in 2026.

## 3. Landing services (Jito, bloXroute, Nozomi/Temporal, Helius Sender, NextBlock, 0slot, SWQoS) and latency comparisons

### Takeaway
Landing services send a signed transaction along several fast paths at once (Jito block engine plus staked/SWQoS connections to upcoming leaders) and usually require a tip to their own tip account. No neutral, current, head-to-head benchmark exists. The published figures are vendor-produced and often old, so a bot should benchmark from its own region and spread transactions across several services.

### Cited Findings
- **Helius Sender:** sends in parallel to Jito and Helius's own staked paths across about 7 regions. It requires a minimum tip of about 0.001 SOL and uses no API credits — [Helius Sender page](https://www.helius.dev/sender) (via search summary). A case study by RPC Fast, a competitor, reported typical landing in 200–300 ms, best about 15 ms, usually within 1 slot — [RPC Fast copy-trading bot case study](https://rpcfast.com/blog/copy-trading-bot-case-study)
- **bloXroute benchmark (old, vendor-run):** bloXroute's swQoS mode had P90 latency of 1.414 s, 100/100 landed, P90 +3 slots. Temporal/Nozomi had P90 1.875 s, 99/100 landed, P90 +4 slots. The benchmark is about 686 days old and was published by bloXroute, so it is not neutral — [bloXroute: Benchmarking Solana Transaction Speeds and Landing Rates](https://bloxroute.com/pulse/benchmarking-solana-transaction-speeds-and-landing-rates/)
- A 2026 roundup cites "Beam" averaging 330 ms to land versus 457 ms on standard RPC. Beam routes through several providers, including bloXroute, so the figure does not isolate any one service — [RPC Fast: Top 8 Solana RPC for MEV in 2026](https://rpcfast.com/blog/solana-rpc-for-mev) (attribution unclear from the summary)
- **0slot:** described as a staked-connection `sendTransaction` that connects straight to its validator node, with dedicated SWQoS per user. One measurement gave 0.561 ms round-trip from an Amsterdam VPS to 0slot, which is network proximity, not landing time — [AllenHark: What Is 0-Slot Landing](https://allenhark.com/blog/what-is-0-slot-landing-solana); [Arct.cloud: Solana Trading VPS](https://www.arct.cloud/blog/solana-trading-vps)
- Comparison overviews of relays and landing services: [AllenHark: Solana MEV Relay Services Comparison 2025](https://allenhark.com/blog/solana-mev-relay-services-comprehensive-comparison); [Astralane: Solana MEV Wars](https://medium.com/@astralaneio/solana-mev-wars-understanding-the-game-protecting-your-alpha-43ba5e4846e9)
- Leader rotation: the leader changes about every 1.6 s (4 slots × ~400 ms), so endpoint latency depends heavily on where the server sits relative to the current leader — [Chainflow: Lifetime of a Solana Transaction](https://chainflow.io/lifetime-of-a-solana-transaction-from-sender-to-confirmation/) (via search summary)
- **Jito BAM latency:** a Jito BAM upgrade reportedly cut bundle delays by about 50 ms — [CryptoBriefing](https://cryptobriefing.com/jito-bam-upgrade-cuts-bundle-delays/)

### Inferences
- Common setup in 2026: build the transaction with a dynamic priority fee and tip, then send it at the same time to 2–4 services (for example Jito plus Helius Sender plus one SWQoS relay such as Nozomi, bloXroute, 0slot or NextBlock). The same signature gets deduplicated, so only one copy lands, but each service may require its own tip instruction. A bot should therefore either include only one service's tip or accept paying tips that end up redundant. (This follows from the minimum-tip requirements above; confirm with each provider's docs.)
- Co-locate servers in the regions where most leader stake sits (Frankfurt, Amsterdam, New York, Tokyo are typical) and send to the nearest regional endpoint for the current or next leader.

### Gaps
- I could not reach Jito, Temporal/Nozomi, NextBlock or 0slot docs, so I have no verified 2026 minimum tips, tip-account lists, rate limits or pricing for these providers.
- I found no independent 2026 benchmark comparing all services under the same conditions.
- Unverified (training knowledge): SWQoS (stake-weighted QoS), live since early 2024, reserves leader QUIC connection capacity in proportion to stake (about 80% for staked peers). This is why unstaked RPCs drop transactions under load and why "staked connections" are sold as a product. Helius Sender also offers a `swqos_only` mode with a lower minimum tip. NextBlock and Nozomi each require a tip to their own tip addresses (amounts not verified).

## 4. Slippage settings vs sandwich risk; MEV-protected RPCs

### Takeaway
Slippage tolerance is the maximum an attacker can take from a trade, so tight or dynamic slippage is the first line of defence. The second is order-flow privacy: use RPCs or relays that do not leak transactions, use `jitodontfront`, or use aggregator execution paths (for example Jupiter Ultra) that report lower sandwich rates.

### Cited Findings
- Solana's DontFront guide recommends tight slippage alongside `jitodontfront` — [Solana docs](https://solana.com/docs/defi/mev-protection)
- Jupiter Ultra users face fewer sandwich attacks than others in a three-year study — [CryptoBriefing](https://cryptobriefing.com/jupiter-ultra-sandwich-attacks-study/); [edgeX news mirror](https://pro.edgex.exchange/en-US/news/article/solana-sandwich-attacks-jupiter-ultra-study)
- Overviews of MEV bots and protection for retail Solana traders (Jito bundles, slippage, private routes) — [SolanaHub: MEV on Solana](https://solanahub.de/en/knowledge/mev-on-solana/); [madeonsol: MEV Bots on Solana Explained](https://madeonsol.com/blog/mev-bots-on-solana-explained)
- MEV-oriented RPC/landing roundup for 2026 — [RPC Fast: Top 8 Solana RPC for MEV in 2026](https://rpcfast.com/blog/solana-rpc-for-mev)

### Inferences
- Practical rule for a bot: compute expected price impact from pool reserves (bonding curve or AMM), then set slippage to roughly price impact plus a small volatility buffer, rather than a fixed 10–30%. Never broadcast high-slippage transactions through public or unknown RPCs.
- When the trade is urgent (snipes), accept the risk of failing over the risk of being sandwiched: a failed transaction costs only fees, while a sandwich takes the full slippage.

### Gaps
- I found no quantitative source linking slippage levels to sandwich probability or loss per trade on Solana.
- I could not verify which RPC providers explicitly sell "MEV-protected" sending in 2026 or what their guarantees are.

## 5. Validator-level changes in 2025–2026: Alpenglow, Jito BAM, Firedancer

### Takeaway
Two major changes are now live. **Jito BAM** (Block Assembly Marketplace, with ordering inside TEEs and plugins) went live on mainnet around September 2025 and reached roughly 33–40%+ of stake by Q3/Q4 2026. **Alpenglow** consensus activated on mainnet on 21 October 2026, with a target of about 150 ms finality, though early readings were much higher. Firedancer/Frankendancer runs on a meaningful minority of stake, and BAM was ported to it ("FireBAM") in 2026.

### Cited Findings
**Jito BAM**
- Mainnet launch is reported as September 2025 (one source says 25 Sep 2025) — [Blockworks: Jito launches BAM on Solana mainnet](https://blockworks.co/news/jito-bam-solana-mainnet); [SolanaHub](https://solanahub.de/en/news/jito-bam-majority-validators/)
- Stake on BAM: about 12% in January 2026; 378 validators and about 33% of stake (about $10.6B delegated SOL) at end of June 2026 per the Blockworks Advisory Q2 report; 34.1% by 9 Sep 2026 when BAM preconfirmations went live; about 37% per CryptoBriefing; and **more than 40% (about 173.6M SOL across 380 validators)** per Solana Compass in late Sept/Oct 2026 — [Solana Compass Q2 2026](https://solanacompass.com/news/jito-q2-2026-protocol-revenue-falls-45-to-128m-as-bam-reaches-33-of-solana-stake); [Solana Compass: BAM preconfirmations go live (34%)](https://solanacompass.com/news/jito-bam-preconfirmations-go-live-on-solana-covering-34-of-network-stake); [Solana Compass: BAM crosses 40%](https://solanacompass.com/news/jitos-bam-crosses-40-of-solana-stake-with-1736m-sol-across-380-validators); [CryptoBriefing](https://cryptobriefing.com/jito-bam-upgrade-cuts-bundle-delays/). An earlier forum figure was 27% — [BlockEden forum](https://blockeden.xyz/forum/t/jitobam-now-controls-27-of-solana-stake-using-tees-is-this-mev-protection-or-a-dangerous-centralization-vector/2420)
- BAM **preconfirmations** went live in September 2026 — [Solana Compass](https://solanacompass.com/news/jito-bam-preconfirmations-go-live-on-solana-covering-34-of-network-stake)
- A BAM upgrade cut bundle delays by about 50 ms — [CryptoBriefing](https://cryptobriefing.com/jito-bam-upgrade-cuts-bundle-delays/)
- **FireBAM** (BAM on Frankendancer, which runs about 12% of mainnet stake) had testnet and early mainnet access from 13 May 2026, with a broader mainnet release expected in July 2026 — [SolanaHub: Jito FireBAM](https://solanahub.de/en/news/jito-firebam-bam-frankendancer-testnet/)
- BAM uses trusted execution environments (TEEs) for private transaction ordering. Critics raise the question of centralization and trust in TEE hardware — [Blockdaemon: What is JitoBAM](https://www.blockdaemon.com/blog/what-is-jitobam-and-why-does-it-matter-for-institutional-solana-staking); [BlockEden forum](https://blockeden.xyz/forum/t/jitobam-now-controls-27-of-solana-stake-using-tees-is-this-mev-protection-or-a-dangerous-centralization-vector/2420)
- Jito's quarterly call covered BAM and a "JTX" launch — [HeyBeluga](https://heybeluga.com/articles/jito-quarterly-call-bam-jtx-launch/)
- Jito protocol revenue fell 45% to $1.28M in Q2 2026 — [Solana Compass](https://solanacompass.com/news/jito-q2-2026-protocol-revenue-falls-45-to-128m-as-bam-reaches-33-of-solana-stake)

**Alpenglow**
- Activated on mainnet-beta on **21 Oct 2026**. Reported details: slot 459,653,000 at about 14:00 UTC (The Block); epoch 1064 at about 13:36 UTC (solana.com); about 13:54 UTC (Cointelegraph). The sources disagree on the exact time — [The Block](https://theblock.co/news/ecosystems/2026-10-21-anzas-alpenglow-goes-live-on-solana-cutting-finality-to-150-milliseconds-421508); [Solana: Alpenglow upgrade page](https://solana.com/upgrades/alpenglow); [Cointelegraph](https://cointelegraph.com/news/solanas-alpenglow-launches-mainnet-99-faster-finality)
- Finality target of about 150 ms, down from about 12.8 s under TowerBFT. Solana describes this as a target — [Solana](https://solana.com/upgrades/alpenglow); [QuickNode](https://blog.quicknode.com/solana-alpenglow-upgrade)
- Early mainnet reading: about 6.6 s finality and about 4,721 TPS on the dashboard at press time, far from the target. It is unclear whether this was a transitional state — [Cointelegraph](https://cointelegraph.com/news/solanas-alpenglow-launches-mainnet-99-faster-finality)
- 150 ms is consensus finality, not end-to-end trading or API latency. Alpenglow also changes RPC behaviour (Votor) — [RPC Fast: Alpenglow is live](https://rpcfast.com/blog/alpenglow-solana-150ms-finality-explained)
- The test cluster reached 96% fast-path finalization — [Solana Compass](https://solanacompass.com/news/what-solanas-alpenglow-upgrade-changes-validator-costs-finality-and-96-fast-path-finalization-from-the-test-cluster)
- A second phase, **Rotor**, is expected to replace Turbine for block propagation — [Solana](https://solana.com/upgrades/alpenglow)
- Background on Votor/Rotor and validator impact — [Kiln](https://www.kiln.fi/post/solanas-alpenglow-upgrade-what-it-means-for-stakers-and-validators); [Alchemy](https://www.alchemy.com/blog/solana-alpenglow.md); [BlockEden](https://blockeden.xyz/blog/2026/04/04/solana-alpenglow-consensus-overhaul-votor-rotor-100ms-finality/)

### Inferences
- For bots, Alpenglow mainly shortens the time to know a trade is final (relevant for chained actions such as a buy followed by a quick sell, and for confirmation polling). It does not by itself remove sandwich risk, which depends on the leader and block builder.
- With 40%+ of stake on BAM, a large and growing share of leaders order transactions inside TEEs with Jito-defined plugins. This could reduce leader-side private-mempool sandwiching on those slots. Wide sandwiches by non-BAM leaders remain a risk, so leader-aware routing is more useful than before (send sensitive flow when a BAM or low-sandwich-rate leader is in the schedule).
- BAM preconfirmations could give bots a faster inclusion signal than waiting for confirmation.

### Gaps
- I could not verify Firedancer's full-client (not Frankendancer) mainnet stake share as of November 2026.
- I could not verify whether Alpenglow changed slot time (unverified: it keeps ~400 ms slots in phase 1) or the leader-schedule and fee mechanics.
- I found no data on how BAM affects sandwich rates (no before/after study).
- I could not check details of other 2025–2026 MEV-relevant proposals (unverified from training knowledge: multiple concurrent proposers / MCP, raised block CU limits, Harmonic and other alternative block builders).
