# Technical architecture of a high-performance memecoin trading bot (Solana, briefly EVM)

> Research context and limits (read first): this was researched on 2026-11-20. Direct fetches of helius.dev, chainstack.com, rpcfast.com and docs.jito.wtf were blocked by the research sandbox's network allowlist, so their content comes from search-result summaries rather than full page reads. github.com was reachable and was read directly. The shared web-search budget ran out partway through, so co-location regions, monitoring stacks, analytics databases and EVM topics could not be researched with sources. They appear under Gaps, or as clearly labelled inferences from background knowledge. Most latency numbers below are vendor-run benchmarks and should be treated as directional.

## 1. Real-time data ingestion: Yellowstone/Geyser gRPC, Helius LaserStream/WebSockets, Triton, shred streams, standard WebSockets

### Takeaway
As of November 2026 the practical tiers are as follows, fastest first. **Shred-level feeds** give the earliest, pre-execution signal with less context. The main options are DoubleZero Edge, Triton's shred streaming and Deshred, Shyft RabbitStream, ERPC shared Shreds and OrbitFlare. **Jito ShredStream itself was shut down on 5 Sep 2026.** Next comes **Yellowstone-compatible gRPC** (Triton Dragon's Mouth, Helius LaserStream, QuickNode, Chainstack, Shyft), which gives full post-execution data with logs and balances. **Standard JSON-RPC WebSockets** are the slowest and least reliable. Vendor benchmarks put shred feeds anywhere from ~5 ms (median) to 50-100 ms ahead of Yellowstone gRPC. Serious bots usually run a shred feed for the earliest trigger and gRPC for confirmed state.

### Cited Findings
- Yellowstone gRPC ("Dragon's Mouth") is Triton One's gRPC interface built around Solana's Geyser plugin interface. It streams slots, blocks, transactions, deshred pre-execution transactions and account updates. It supports server-side filters on commitment, accounts (by pubkey, owner, data filters, `accounts_data_slice`), transactions (vote, failed, signature, account include/exclude/required), blocks and block meta. It also has unary methods such as GetLatestBlockhash and IsBlockhashValid, plus ping/keepalive for load balancers. The license is AGPL-3.0. — [GitHub rpcpool/yellowstone-grpc](https://github.com/rpcpool/yellowstone-grpc)
- A `SubscribeDeshred` stream delivers transactions earlier, before execution. It is available only on Triton's extension servers, not in the open-source server. — [GitHub rpcpool/yellowstone-grpc](https://github.com/rpcpool/yellowstone-grpc)
- Yellowstone gives full post-execution data (logs, balance changes). Shred feeds give the earliest signal with less context. Shyft frames it as "shreds = raw, immediate signal; Yellowstone = reliable, full report". — [Shyft: Solana Shreds vs Yellowstone gRPC](https://wp-origin.shyft.to/?p=8); [RPC Fast: Shreds, gRPC, JSON-RPC breakdown](https://rpcfast.com/blog/shredstream-vs-geyser-vs-standard-rpc)
- Latency claims for shred feeds vs Yellowstone conflict, even within one vendor:
  - RPC Fast tables claim shreds are ~50-100 ms faster. — [RPC Fast](https://rpcfast.com/blog/shredstream-vs-geyser-vs-standard-rpc)
  - A different RPC Fast piece claims its Aperture shred feed is ~30-40 ms faster. — [RPC Fast: Aperture gRPC explained](https://rpcfast.com/blog/aperture-grpc-explained)
  - An RPC Fast head-to-head from Frankfurt over 58,688 shared transactions measured only a **4.82 ms median and 16.04 ms p95** lead for ShredStream gRPC over Yellowstone gRPC. — [RPC Fast: Solana data streaming guide](https://rpcfast.com/blog/solana-data-streaming-guide)
- Shyft's own benchmark (Frankfurt and New York) reports its RabbitStream arrived first in 97.19% and 96.52% of transactions vs Jito ShredStream in two NY runs. This is a competitor-run test. — [Shyft: RabbitStream vs Jito ShredStream](https://shyft.to/blog/rabbitstream-vs-jito-shredstream)
- **Jito ShredStream was deprecated with a 60-day notice and fully shut down on 5 September 2026.** Jito recommended DoubleZero Edge as the replacement. Chainstack notes that the Jito ShredStream proxy setup in its guide no longer works. — [Chainstack ShredStream guide (update note)](https://chainstack.com/how-to-improve-solana-rpc-latency-with-shredstream/); [OrbitFlare: Jito ShredStream's Last Slot](https://orbitflare.com/blog/developers/jito-shredstreams-last-slot); [Jito docs](https://docs.jito.wtf/lowlatencytxnfeed/)
- DoubleZero launched **Edge**, a low-latency on-chain data delivery service on its fiber network, in April 2026. — [The Block, 2026-04-16](https://www.theblock.co/news/business/2026-04-16-doublezero-rolls-out-edge-a-low-latency-onchain-data-delivery-service-on-its-global-fiber-depin-infrastructure-397715)
  - DoubleZero claims ~28 ms better p95 than Jito ShredStream. — [index.vn summary](https://index.vn/en/news/doublezero-launches-edge-beta-with-28ms-faster-solana-block-views-and-rapid-publisher-growth)
  - On 9 Sep 2026 it removed unauthorized shred retransmitters and claimed a "70%+ lead" over competitors. This is self-reported. — [Solana Compass](https://solanacompass.com/news/doublezero-removes-unauthorized-shred-retransmitters-claims-70-plus-lead-over-all-competitors)
  - Validator participation in Edge passed 58%, including Coinbase's validator. — [Solana Compass](https://solanacompass.com/news/coinbases-solana-validator-joins-doublezero-edge-as-participation-crosses-58)
- Triton offers its own shred streaming product. — [Triton docs: shred streaming](https://docs.triton.one/chains/solana/shred-streaming)
- Triton's analysis of the network layer is a competitor perspective. — [Triton blog: rethinking the network beneath the blockchain](https://blog.triton.one/rethinking-the-network-beneath-the-blockchain/)
- ERPC states its shared Shreds and Geyser gRPC endpoints continue to operate and added HTTPS support in August 2026. — [ERPC news 2026-08-28](https://erpc.global/en/news/2026/08/28/erpc-shared-endpoints-https-http-dual-support-20260828/)
- Helius LaserStream SDK:
  - It supports TypeScript/JS (Rust core with NAPI bindings), Rust and Go, with auto-reconnect.
  - Replay mode resumes from the last processed slot, with backfill of **up to 3,000 slots (~20 minutes)** through `from_slot`. `subscribeReplayInfo` reports the oldest replayable slot.
  - It supports Gzip/Zstd compression and claims "70-80% bandwidth reduction" with Zstd.
  - It claims the JS SDK is 40x faster than the Yellowstone JS client (1.3 GB/s vs 30 MB/s).
  - The license is MIT.
  - [GitHub helius-labs/laserstream-sdk](https://github.com/helius-labs/laserstream-sdk)
- Helius states that LaserStream now powers all Helius WebSocket services and products. — [Helius blog: LaserStream WebSockets](https://www.helius.dev/blog/laserstream-websockets)

### Inferences
- Reference pattern: subscribe to a shred-level feed (DoubleZero Edge, Triton Deshred, or a third-party shred gRPC) for the earliest "new pool / dev buy" trigger. Use Yellowstone or LaserStream gRPC at `processed` commitment, filtered by program owner (pump.fun, PumpSwap, Raydium LaunchLab/CPMM/AMMv4, Meteora DAMM v2), for confirmed state, balances and logs. Keep standard WebSockets only as a fallback or for low-frequency monitoring.
- Because the vendor benchmarks disagree by an order of magnitude (5 ms vs 100 ms), any team should measure feeds side by side from its own region. Malbec Labs' `shredtop` tool appeared in results as an open-source shred feed benchmarking tool, but I did not read it.
- LaserStream's ~20-minute replay window is an operational advantage for crash recovery over plain Yellowstone, where reconnection gaps are otherwise lost.

### Gaps
- No independent, third-party, apples-to-apples latency benchmark across LaserStream, Triton, QuickNode and shred feeds was found. All figures are vendor-produced.
- DoubleZero Edge pricing and access terms for non-validators were not found.
- Helius "Enhanced WebSockets" and webhooks latency figures could not be retrieved, because helius.dev was blocked from direct fetch.

## 2. RPC providers and pricing tiers (Helius, Triton, QuickNode, Shyft, Chainstack, dedicated)

### Takeaway
Entry-level gRPC streaming for a serious bot costs roughly **$49-$500 per month** on shared infrastructure. Typical examples are Helius Business at $499 (LaserStream mainnet, 10 connections), QuickNode Scale at $499 with gRPC included since June 2026, a Chainstack add-on from $49 to $149, and Shyft from ~$199. Dedicated nodes and shred feeds sit higher. Transaction sending is increasingly priced per transaction through SOL tips rather than through plan credits.

### Cited Findings
- **Helius plans:**
  - Free costs $0. Developer costs $49/mo with 10M credits, Business $499/mo with 100M credits, and Professional $999/mo with 200M credits.
  - LaserStream on mainnet requires Business or Professional. Devnet is available from Developer.
  - Active LaserStream connections are capped at 10 on Business and 100 on Professional.
  - LaserStream bills 2 credits per 0.1 MB.
  - Data add-ons start at $400/mo.
  - [Helius billing plans](https://www.helius.dev/docs/billing/plans.md); [Helius pricing](https://www.helius.dev/pricing.md)
  - A third-party site (CostBench) lists Developer at $24.50/mo, which conflicts with Helius's own $49. — [CostBench](https://www.costbench.com/software/blockchain-nodes/helius-rpc/)
- From 7 April 2026, Helius cut data-streaming add-on prices by up to 20% for gRPC and Enhanced WebSockets. It also let Business customers use up to 10 concurrent gRPC connections, which Helius frames as a 50% cut in gRPC access cost. — [Helius billing plans](https://www.helius.dev/docs/billing/plans.md)
- **Helius Sender:**
  - Sender does not consume API credits. It is paid per transaction through a SOL tip.
  - The "Sender Max" minimum tip is **0.001 SOL**, which routes through all paths: Helius, Jito, Harmonic, Rakurai, and others. The SWQOS-only tier costs **0.000005 SOL**.
  - Tips between those amounts are best-effort through fewer paths.
  - Every Sender transaction must include a tip transfer and a compute unit price, and `skipPreflight: true` is mandatory.
  - Staked connections are automatic on paid plans.
  - [Helius docs: Sender](https://docs.helius.xyz/docs/sending-transactions/sender); [Helius: land trades with Sender](https://www.helius.dev/docs/sending-transactions/guides/land-trades-with-sender)
  - Older sources cite 0.0002 SOL as the minimum, which is likely outdated. — [Helius Sender skill page](https://www.helius.dev/docs/agents/mcp/skills/sender)
- **QuickNode:** since a June 2026 post, Solana gRPC is included in the Scale and Business plans at no extra charge. Build and Accelerate users can still buy the add-on. QuickNode's own example: Accelerate ($249/mo) plus the gRPC add-on ($499/mo) totals $748/mo, versus Scale at $499/mo with gRPC included. — [QuickNode blog](https://blog.quicknode.com/solana-grpc-is-now-included-with-scale-and-business-plans/)
- **Chainstack:** the Yellowstone gRPC add-on costs $49/mo for 2 concurrent streams and $149/mo for 7 streams, on Growth plans and above. — [Chainstack: Yellowstone gRPC more streams same price](https://chainstack.com/yellowstone-grpc-more-streams-same-price/); [Chainstack changelog Sep 2025](https://docs.chainstack.com/changelog/chainstack-updates-september-30-2025)
- **Shyft:** Yellowstone gRPC starts from ~$199/mo, per a third-party comparison dated August 2026. I found no official Shyft pricing page. — [RPC Fast: 7 best Solana gRPC providers 2026](https://rpcfast.com/blog/best-solana-grpc-providers)
- **Triton One:** no public Dragon's Mouth price list was found. Triton's mission page points to usage-based, open-access pricing. — [Triton mission](https://triton.one/mission)
- Other gRPC and shred vendors in 2026 comparisons include RPC Fast (Aperture), OrbitFlare, ERPC, Corvus Labs and GetBlock. — [RPC Fast comparison](https://rpcfast.com/blog/best-solana-grpc-providers); [OrbitFlare](https://orbitflare.com/products/solana-grpc); [Corvus Labs pricing comparison](https://docs.corvus-labs.io/platform/pricing-comparison)
- Solana RPC billing falls into roughly "5 main billing systems": credits, compute units, request-based, flat/dedicated, and bandwidth. — [RPC Fast: Solana RPC pricing in 2026](https://rpcfast.com/blog/solana-rpc-pricing)

### Inferences
- A budget build for a solo or small team: QuickNode Scale or Helius Business (~$499/mo) for gRPC and RPC, plus per-transaction tips through Sender or Jito-style relays. A Chainstack add-on ($49-149) is the cheapest sanctioned Yellowstone access found.
- A competitive build: a dedicated or bare-metal node or a dedicated gRPC endpoint, plus a shred feed. Expect costs in the low thousands of USD per month, but this was not verified with sources (see Gaps).
- Pricing changed several times in 2026 (Helius in April, QuickNode in June), so the report should present these as point-in-time figures.

### Gaps
- Dedicated node pricing (Helius dedicated, Triton dedicated, bare metal from Latitude, Teraswitch or OVH) was not retrieved, because pages were blocked and the search budget was exhausted.
- Official Shyft and Triton price sheets were not found.
- QuickNode plan RPS and credit limits were not retrieved.

## 3. Transaction building: pump.fun / PumpSwap / Raydium parsing, ALTs, compute budget, retries, confirmation

### Takeaway
Modern Solana trade execution comes down to five habits:
- Precompute everything off the hot path, including the blockhash or a durable nonce, ATAs and PDAs.
- Never call RPC inside the trade path.
- Use v0 transactions with ALTs and explicit compute-budget instructions.
- Fan the same signed transaction out to several landing services in parallel: Jito, Helius Sender, NextBlock, 0slot, Temporal, bloXroute, Astralane and others.
- Use a durable nonce when sending to several relays, so only one copy can land.

pump.fun's programs change often. Bonding-curve trades are now at v3 and PumpSwap at v2, and new mandatory accounts appear regularly. Parsers and IDLs need active maintenance.

### Cited Findings
- **pump.fun public docs** cover the bonding-curve program and the PumpSwap AMM. Current instructions:
  - Creation: `create_v2`.
  - Bonding curve: `buy`/`sell`, `buy_v2`/`sell_v2`, `buy_exact_quote_in_v2`, and `buy_v3`/`sell_v3`/`buy_exact_quote_in_v3`.
  - PumpSwap: `buy_v2`/`sell_v2`/`buy_exact_quote_in_v2` plus `multi_hop_swap`.
  - Fees: `sweep_protocol_fee` and `sweep_creator_fee`.
  - [GitHub pump-fun/pump-public-docs](https://github.com/pump-fun/pump-public-docs)
- **Recent pump.fun breaking changes:**
  - `user_volume_accumulator` and the `sharing_config` PDA are mandatory on all buys and sells.
  - New quote accounts were added: `quote_mint` and `associated_quote_*`. A USDC quote mint was announced.
  - `real_sol_reserves` and `virtual_sol_reserves` were renamed to `real_quote_reserves` and `virtual_quote_reserves`.
  - `virtual_quote_reserves` can be negative from 30 Sep 2026, so treat it as signed.
  - Fees stay on the curve or in the pool until swept.
  - "Synthetic migration" was introduced: the buy that empties the curve has no max size.
  - Holder-rewards coins were added and cashback was deprecated.
  - Depth-2 pump-coin quotes via `create_v2` arrived on 13 Oct 2026.
  - [GitHub pump-fun/pump-public-docs](https://github.com/pump-fun/pump-public-docs)
- **sol-trade-sdk (0xfnzero), Rust, MIT, ~362 stars, 691 commits.**
  - Protocols: PumpFun, PumpSwap, Bonk, Raydium LaunchLab, StonkFun, Meteora DAMM V2, Raydium AMM V4 and Raydium CPMM.
  - Submission services: Jito, NextBlock, ZeroSlot, Temporal, bloXroute, FlashBlock, BlockRazor, Astralane, Glaive, LunarLander and SpeedLanding.
  - Fan-out: it submits "through every configured SWQoS provider plus the default RPC lane" in parallel and returns on the first accepted result.
  - ALT support comes via `.address_lookup_table_account(alt)`.
  - The default V0 mode uses ComputeBudget instructions, with `cu_price` in micro-lamports per CU converted to total lamports with ceiling division. A "V1" mode embeds the CU limit and priority fee in the transaction config, allows transactions up to 4096 bytes, and does not support ALTs.
  - A durable nonce (`.durable_nonce(nonce_info)`) is recommended when using multiple MEV services.
  - Trade execution never queries RPC for blockhash, account or balance. The caller supplies them.
  - [GitHub 0xfnzero/sol-trade-sdk](https://github.com/0xfnzero/sol-trade-sdk)
- The companion repos are `sol-parser-sdk` (v0.11.0, for DEX transaction and account event parsing in Rust, Node.js, Python and Go) and `solana-streamer` (v6.0.0, for gRPC and ShredStream subscriptions). — [GitHub 0xfnzero/sol-trade-sdk](https://github.com/0xfnzero/sol-trade-sdk); [docs.rs sol-parser-sdk grpc-vs-rpc](https://docs.rs/crate/sol-parser-sdk/0.4.6/source/docs/grpc-vs-rpc.md)
- Helius Sender requires a tip plus a compute unit price and `skipPreflight: true`, so simulation must happen client-side or not at all. — [Helius docs: Sender](https://docs.helius.xyz/docs/sending-transactions/sender)
- Helius's Rust SDK has an `optimized_transaction` module, which handles CU estimation and priority fee setting. — [docs.rs helius optimized_transaction.rs](https://docs.rs/crate/helius/1.1.0/source/src/optimized_transaction.rs)

### Inferences
These are background knowledge; I did not verify them with sources in this session.
- Set `SetComputeUnitLimit` close to the simulated usage, since a tighter limit lowers the fee and improves scheduling. Set `SetComputeUnitPrice` from a recent priority-fee estimate, for example Helius `getPriorityFeeEstimate`.
- Use `processed`, or the shred-level signal, for triggers. Use `confirmed` for position accounting.
- Track landing through gRPC signature or account subscriptions rather than polling `getSignatureStatuses`.
- Rebroadcast the same signed transaction until the blockhash expires, about 150 slots or roughly 60-90 s, rather than re-signing with a new blockhash. Re-signing risks double-fills unless you use a durable nonce.
- Pre-create wSOL ATAs and token ATAs where possible, and use idempotent ATA creation.
- Keep a per-wallet nonce account when fanning out to several relays.
- Because pump.fun adds mandatory accounts frequently, hard-coded instruction layouts break. Teams should vendor the IDL and run canary transactions after each program upgrade.

### Gaps
- Official Raydium LaunchLab, CPMM and AMMv4 instruction layout docs were not fetched.
- Jito bundle and tip mechanics in late 2026 (minimum tips, tip accounts, block engine regions) could not be verified, because docs.jito.wtf was blocked.
- Landing-rate statistics per relay (Jito vs Sender vs NextBlock and others) were not found.

## 4. Language/stack choices and notable open-source bots/SDKs

### Takeaway
Rust dominates the latency-critical path. The most complete open-source memecoin trading SDK found is Rust (0xfnzero's sol-trade-sdk family), and Helius's LaserStream JS SDK itself wraps a Rust core. TypeScript is viable for strategy and orchestration, and is preferable when built on Rust-backed SDKs. Python suits research and analytics, not the hot path. Most "sniper bot" repositories on GitHub are low quality or outright scams; prefer SDKs from infrastructure vendors and well-maintained library authors.

### Cited Findings
- sol-trade-sdk (Rust, MIT, 362 stars, 691 commits) is an SDK rather than a turnkey bot. It ships examples such as `pumpfun_sniper_trading` and copy-trading. Its benchmarks are explicitly "local CPU measurements, not production latency". — [GitHub 0xfnzero/sol-trade-sdk](https://github.com/0xfnzero/sol-trade-sdk); [awesome.ecosyste.ms entry](https://awesome.ecosyste.ms/projects/github.com%2F0xfnzero%2Fsol-trade-sdk)
- The sol-trade-sdk crate's version history runs from 0.1.x to 4.0.x on crates.io. The API changes frequently between releases. — [docs.rs sol-trade-sdk 3.6.1](https://docs.rs/crate/sol-trade-sdk/3.6.1); [docs.rs sol-trade-sdk 4.0.8 helius.rs](https://docs.rs/crate/sol-trade-sdk/4.0.8/source/src/swqos/helius.rs)
- The Helius LaserStream SDK (TS, Rust, Go; MIT; ~59 stars) uses a Rust core with NAPI bindings for JS and claims 40x the throughput of the Yellowstone JS client. — [GitHub helius-labs/laserstream-sdk](https://github.com/helius-labs/laserstream-sdk)
- Yellowstone gRPC (Triton) is the reference server and client implementation, licensed AGPL-3.0. Its copyleft matters if you modify and serve it. — [GitHub rpcpool/yellowstone-grpc](https://github.com/rpcpool/yellowstone-grpc)
- `sol-parser-sdk` offers parsing bindings in Rust, Node.js, Python and Go, which supports a polyglot design: Rust ingest and parse, with other languages for strategy and analytics. — [GitHub 0xfnzero/sol-trade-sdk](https://github.com/0xfnzero/sol-trade-sdk)

### Inferences
- Recommended split: a Rust ingest, decision and execution core (tokio, yellowstone-grpc-client or laserstream, solana-sdk). TS or Python for dashboards, backtesting and the Telegram/UI layer. A message bus between them, such as NATS or Redis Streams.
- The quality signals to check in open-source bots are licence, commit recency, how well they track pump.fun program changes (for example `buy_v3` and volume-accumulator accounts), whether they read private keys from env or files safely, and the absence of obfuscated code or hard-coded "dev fee" wallets. Many GitHub "pump.fun sniper" repos are known to be drainer scams. This is background knowledge; I found no source in this session that quantifies it.

### Gaps
- No comparison was found of other notable repos: Jupiter, the Raydium SDK v2 TS SDK, Anchor clients, Solana Agent Kit, or Python libraries such as solana-py/solders.
- No measured TS vs Rust end-to-end latency numbers were found, beyond Helius's SDK throughput claim.

## 5. Infrastructure: co-location, monitoring, state management, analytics DB (and EVM)

### Takeaway
Only fragments could be sourced. RPC Fast's head-to-head benchmark was run from Frankfurt, and Shyft benchmarked in Frankfurt and New York, which reflects where streaming vendors themselves place infrastructure. The network layer, meaning DoubleZero fiber and shred retransmission, is now a key competitive dimension. Co-location specifics, monitoring tooling, database choices and EVM architecture could not be researched with sources in this session.

### Cited Findings
- Benchmarks of shred and gRPC feeds are run from Frankfurt (RPC Fast) and from Frankfurt plus New York (Shyft). These are the de facto regions where streaming providers host infrastructure close to stake. — [RPC Fast data streaming guide](https://rpcfast.com/blog/solana-data-streaming-guide); [Shyft RabbitStream benchmark](https://wp-origin.shyft.to/?p=1782)
- DoubleZero runs a dedicated global fiber network (DePIN) carrying leader shreds. More than 58% of stake had joined Edge by late 2026. — [The Block](https://www.theblock.co/news/business/2026-04-16-doublezero-rolls-out-edge-a-low-latency-onchain-data-delivery-service-on-its-global-fiber-depin-infrastructure-397715); [Solana Compass](https://solanacompass.com/news/coinbases-solana-validator-joins-doublezero-edge-as-participation-crosses-58)
- Corvus Labs publishes a "latency stack" breakdown of the layers that contribute to bot latency. — [Corvus Labs: latency stack](https://docs.corvus-labs.io/platform/latency-stack)
- A RPC Fast article on data streaming for AI trading agents covers latency considerations for agent-driven bots. — [RPC Fast](https://rpcfast.com/blog/solana-data-streaming-for-ai-trading-agents)

### Inferences
These are background knowledge, not verified in this session; the report writer should label them as such.
- Solana stake is concentrated in the Frankfurt and Amsterdam area (EU) and the New York and Ashburn area (US East), with secondary clusters in Tokyo and Singapore. Bots typically co-locate bare metal in Frankfurt or Amsterdam and New York, and some route sends to the region of the upcoming leader using the leader schedule.
- State management: hold hot state in memory, such as pool reserves updated from account subscriptions, a positions map, and a blockhash or nonce cache. Persist to Postgres or TimescaleDB for positions and PnL. Use ClickHouse or QuestDB for tick and trade analytics. Use Prometheus and Grafana for metrics such as feed lag per source, send-to-land latency, landing rate per relay and failed-transaction reasons. Use a lightweight alerting channel such as Telegram or PagerDuty.
- EVM (brief): memecoin sniping centres on Base, BSC (four.meme) and Ethereum mainnet. The stack is mempool or pending-transaction streams (bloXroute, node `newPendingTransactions`), private order flow or builders (Flashbots Protect / MEV-Share on Ethereum, Base's sequencer ordering), and Uniswap V2/V3/V4 router or pool contract calls. Rust (alloy) or Go (go-ethereum) is typical. None of this was sourced in this session.

### Gaps
- Sourced data on validator and stake geography, leader-region routing, and bare-metal provider pricing (Latitude, Teraswitch, Cherry Servers, OVH) is missing because the search budget was exhausted.
- No sources were gathered on monitoring stacks or analytics databases used by production bots.
- EVM-side architecture (Base, BSC, ETH sniping, private relays, sequencer behaviour on Base) is entirely unsourced and needs follow-up research.
- helius.dev, chainstack.com, rpcfast.com and docs.jito.wtf need to be allowed in the research sandbox's network settings to read full pages.
