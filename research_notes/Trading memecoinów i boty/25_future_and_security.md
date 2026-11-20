# Future structural shifts in memecoin markets (late 2026+) and trading-bot operational security

Research basis: 8 web searches (budget ~10), snippet-level summaries only; no primary pages fetched. Most sources are news/aggregators, flagged where relevant.

## Solana protocol upgrades (Alpenglow, Firedancer, CU limits)

### Takeaway
Alpenglow went live on mainnet on 21 Oct 2026 (target finality ~150 ms vs 12.8 s) and the block CU limit rose to 100M on 29 Jul 2026. Firedancer was NOT part of the Alpenglow migration; multi-client parity is the open question. Bots must treat timing, confirmation and CU assumptions as config, not constants.

### Cited Findings
- Alpenglow reached mainnet-beta ~14:00 UTC on 21 Oct 2026 (slot 459,653,000), replacing TowerBFT; Solana Foundation lists ~150 ms target finality, down from 12.8 s — [The Block](https://theblock.co/news/ecosystems/2026-10-21-anzas-alpenglow-goes-live-on-solana-cutting-finality-to-150-milliseconds-421508); [Decrypt](https://decrypt.co/381484/solana-alpenglow-goes-live-in-most-ambitious-upgrade-since-ethereums-merge,2026-10-21T14%2B00,2026-10-21T17%2B00,0.5256,positive); [Solana Foundation](https://solana.com/upgrades/alpenglow)
- Foundation page says neither Firedancer nor Frankendancer was supported for the migration; validators were directed to Agave v4.3.2, Jito-Solana, or Harmonic Salsa — [Solana Foundation](https://solana.com/upgrades/alpenglow)
- Firedancer reported as running in production on a subset of validators (May 2026) without serving consensus votes; Chainstack says no production Votor implementation in Firedancer yet — [DEXTools May 2026](https://www.dextools.io/news/solana-alpenglow-firedancer-jito-tvl-recovery-may-2026-news); [Chainstack](https://chainstack.com/solana-alpenglow-votor-towerbft/amp/). Sources inconsistent on Firedancer mainnet timing (one says live since late 2025) — [The Block](https://www.theblock.co/amp/post/382411/jump-cryptos-firedancer-hits-solana-mainnet-as-the-network-aims-to-unlock-1-million-tps)
- Block CU limit raised 60M -> 100M via SIMD-0286 (authored by Jito Labs), mainnet 29 Jul 2026 (epoch 1009). Per-account write cap stays 12M CU (12% of block at 100M). >70% of stake enabled XDP. 11.2% of blocks used >=56M CU between Jul 2025 and the increase. Foundation advises RPC providers/indexers/exchanges to verify they handle sustained 100M-CU blocks — [Solana Foundation](https://solana.com/upgrades/100m-cu-blocks); [Solana Compass](https://solanacompass.com/news/solana-raises-mainnet-block-compute-limit-66-to-100m-cus-with-simd-0286-at)
- SIMD-0306 (per-account cap as % of block, -> 40M CU) mentioned by one source only; status unverified — [Solana Compass](https://solanacompass.com/news/solana-raises-mainnet-block-compute-limit-66-to-100m-cus-with-simd-0286-at)

### Inferences
- Faster finality (~150 ms) shrinks the window between "seen" and "final", likely compressing latency edge and changing confirmation/retry/blockhash-expiry logic; bots should parametrize commitment levels and timeouts (inference, not sourced).
- Larger blocks (100M CU) mean more room for bot transactions and hot-account contention is relatively relaxed; CU-price/priority-fee models calibrated at 48-60M should be re-measured.

### Gaps
- No source on Alpenglow's concrete effects on fee markets, Jito bundle/tip behavior or priority-fee dynamics post-activation.
- No confirmed date for Firedancer full consensus participation post-Alpenglow.

## Launchpad wars, creator/content coins, AI-agent tokens, memecoin market size

### Takeaway
Launchpad economics are in flux (pump.fun reversed its dynamic-fee model in Jan 2026; fee sharing/ownership transfer added). Market size is volatile and token survival is very poor. Little reliable data found on Bonk.fun/Zora creator coins and AI-agent tokens.

### Cited Findings
- Pump.fun Dynamic Fees V1 (Sep 2025, Project Ascend; creator fee by market cap, PumpSwap only) was replaced in Jan 2026: creators can share fees with up to 10 wallets and transfer ownership; pump.fun said it concluded the model encouraged low-risk token spam; stated direction is market-based (traders decide whether narrative justifies creator fees). March 2026: deployers limited to one post-launch change of fee distribution — [The Block](https://www.theblock.co/news/markets/2026-01-09-pump-fun-overhauls-creator-fees-token-launches-highest-daily-september-384975); [Blockworks](https://www.blockworks.co/news/pumpdotfun-fee-model); [Cointelegraph](https://cointelegraph.com/news/pump-fun-creator-fee-cap-update-memecoin-model)
- Launchpad share is volatile: Bonkfun briefly took 77% of launchpad revenue share in July 2025 ($37.4M); pump.fun later 68.2% (Aug 2025); a secondary report cites 73-80% of Solana launches — [Blockworks](https://www.blockworks.co/news/pumpdotfun-fee-model); [CoinMarketCap Academy](https://coinmarketcap.com/academy/article/pumpfun-overhauls-creator-fees-amid-launch-spike). No current primary 2026 share figure found.
- Memecoin market cap fell ~75% from late-2024 peak to ~$34-47B by end-2025; rebounded early 2026 ($38B -> $47.7B); crypto.news puts it ~ $30B entering Q4 2026 (unverified elsewhere, sources conflict on whether recovery held) — [DEXTools](https://www.dextools.io/tutorials/are-memecoins-dead-onchain-data-2026); [Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/memecoins-making-comeback-2026-crypto-120215128.html); [crypto.news](https://crypto.news/memecoin-outlook-for-q4-2026-can-the-sector-find-lasting-buyers/)
- Survival stats: ~79% of launched tokens had no trades after day one (Bitquery via KuCoin); 1 in 58 pump.fun launches graduated in one sample; pump.fun daily creations down ~80% from ~72k/day peak (Jan 2025) — [KuCoin](https://www.kucoin.com/news/flash/solana-memecoin-frenzy-leaves-79-of-tokens-stopped-after-day-one); [crypto.news](https://crypto.news/memecoin-outlook-for-q4-2026-can-the-sector-find-lasting-buyers/)
- AI-agent token creation reportedly dropped 99.5% (article appears late 2025; dated) — via search summary of [CoinGecko 2025 State of Memecoins](https://assets.coingecko.com/reports/2025/CoinGecko-2025-State-of-Memecoins-Report.pdf) / aggregators; treat as low confidence.

### Inferences
- Creator-fee and fee-sharing changes alter the incentive to launch and the per-trade cost structure; bots need a per-venue fee model loaded from on-chain/config, not hard-coded.
- Launchpad share can flip within a month, so multi-venue support with venue-level kill switches is a durable design.

### Gaps
- No reliable data on Bonk.fun, Zora/creator-coin volumes, or Alpenglow-era launchpad shares; no good 2026 AI-agent token data; no Galaxy/Messari/Blockworks research reports retrieved.

## Memecoin perps (Hyperliquid), Binance Alpha, memecoin ETFs

### Takeaway
Hyperliquid HIP-3 (permissionless builder-deployed perps) is a large, growing venue, but I found no confirmation of memecoin-specific HIP-3 markets or Binance Alpha listing data. Dogecoin has a spot ETF; Bonk/TRUMP ETFs unconfirmed.

### Cited Findings
- HIP-3 launched mid-Oct 2025: anyone staking 500,000 HYPE can deploy perp markets; HIP-3 markets charge 2x fees and deployer keeps 50% — [Cointelegraph](https://cointelegraph.com/news/hyperliquid-now-allows-builders-to-deploy-perpetual-futures-contracts); [CryptoRank](https://cryptorank.io/news/feed/6af8b-hyperliquid-goes-permissionless-with-hip-3-challenging-cex-but-entry-costs-500000-hype)
- HIP-3 hit $62B monthly volume in May 2026, Hyperliquid at record 6.63% of global perps (14.4% vs Binance) — [The Block](https://www.theblock.co/post/403384/hyperliquid-record-share-global-perps-market-hip-3-tops-62-billion-monthly-volume)
- Binance launched equity/pre-IPO perps ($280M cumulative in first five days) — same source above.
- 21Shares Dogecoin spot ETF (TDOG, Nasdaq) trading as of Jan 2026, described as first standalone spot memecoin ETF; Rex-Osprey DOJE (1940 Act, Sep 2025) conflicts on "first" — [Crypto.news](https://crypto.news/21shares-launches-first-dogecoin-spot-etf-in-us/); [The Block](https://www.theblock.co/amp/post/380416/nyse-arca-certifies-bitwise-dogecoin-etf-signaling-imminent-launch)
- Bonk 2x ETF (Tuttle filing) "alive" per Balchunas; no approval found; TRUMP/BONK Rex-Osprey filings (Jan 2025) no confirmed approval; Balchunas predicted an active memecoin fund in 2026 (prediction only) — [Crypto.news](https://crypto.news/balchunas-confirms-bonk-2x-etf-possibility-remains-strong/); [CryptoRank](https://cryptorank.io/news/feed/9b695-first-meme-coin-etf-could-arrive-by-2026-eric-balchunas)

### Inferences
- Perp venues (Hyperliquid HIP-3) enable long/short and hedging of memecoin exposure and may pull liquidity/attention from spot DEX launches; a future-proof bot could treat perp funding/OI as a signal (inference, not sourced).
- ETFs affect majors like DOGE, not Solana long-tail launches; limited direct relevance for sniping bots.

### Gaps
- No evidence found on Binance Alpha listing mechanics/price impact in 2026; no memecoin-specific HIP-3 data; Bonk/TRUMP ETF status as of Nov 2026 unverified.

## Why bots became obsolete / adaptability

### Takeaway
Documented breakpoints: Jito mempool shutdown (Mar 2024) and pump.fun fee/launch model changes. Anti-sniper mechanics specifics not found.

### Cited Findings
- Jito Labs suspended its Block Engine mempool in March 2024 after sandwich-attack surge; its anti-sandwich filtering became a "cat-and-mouse game"; bundles/Block Engine stayed operational — [Blockworks](https://www.blockworks.com/news/jito-labs-suspends-mempool-functionality); [CoinDesk](https://www.coindesk.com/business/2024/03/08/solana-client-developer-jito-announces-end-of-mempool-function); [The Block](https://www.theblock.co/news/ecosystems/2024-03-09-solana-client-jito-labs-axes-mempool-function-following-increase-in-mev-attacks-281504)
- A 2026 piece argues launchers use bundles (dev buys in launch transaction) so snipers have no front-run gap; promotional/secondary, unverified — [Cryptonews](https://cryptonews.net/editorial/technology/how-solana-bundlers-became-essential-infrastructure-for-pump-fun-launches-in-2026/)
- Pump.fun fee model reversal (see above) is another example of a venue rule change in <5 months.

### Inferences
- Adaptability design: abstract venue adapters (launchpad program IDs, fee schedules), pluggable tx-landing layer (Jito/other/staked RPC), feature flags and dry-run/paper mode, per-strategy PnL kill switches, and monitoring of upstream announcements/SIMDs. Tied to the evidence that rules changed repeatedly (inference).

### Gaps
- No source found on pump.fun anti-sniper fees or launch-time fee decay; no source on other historic obsolescence events.

## Security: keys, hot wallets, malicious bots/packages, drainers

### Takeaway
Documented attacks directly target Solana bot users: fake "solana-pumpfun-bot", typosquatted npm packages, MEV-bot lures, and the compromised @solana/web3.js. Treat any key touching an infected machine as compromised.

### Cited Findings
- Fake "solana-pumpfun-bot" (SlowMist, Jul 2025) impersonated a legitimate project and uploaded wallet/private-key content to an attacker server; related packages crypto-layout-utils, bs58-encrypt-utils (created 12 Jun 2025) — [Security Affairs](https://securityaffairs.com/173249/cyber-crime/malicious-npm-and-pypi-target-solana-private-keys.html); [Cointelegraph](https://cointelegraph.com/news/solana-trading-bot-github-malware-scam)
- Socket (Jan 2025): solana-transaction-toolkit, solana-stable-web-huks etc. used Nodemailer/Gmail to exfiltrate keys and auto-drain wallets — [Socket](https://socket.dev/blog/gmail-for-exfiltration-malicious-npm-packages-target-solana-private-keys-and-drain-victim-s)
- JFrog "Solana FakeFix": 20+ malicious npm/PyPI packages; one fake MEV-bot asked users to paste a private key — [JFrog](https://research.jfrog.com/post/solana-fakefix/)
- @solana/web3.js 1.95.6 and 1.95.7 compromised 2 Dec 2024 (~5-hour window) with a key-stealing backdoor; affected projects handling raw private keys that updated in the window, including bots — [ReversingLabs](https://reversinglabs.com/blog/malware-found-in-solana-npm-library-with-50m-downloads); [The Register](https://www.theregister.com/2024/12/05/solana_javascript_sdk_compromised/); [CNCF TAG](https://tag-security.cncf.io/community/catalog/compromises/2024/solana_web3js/)
- Remediation advice in sources: treat any key on an infected machine as compromised, move funds, audit lockfiles/dependencies — [Security Affairs](https://securityaffairs.com/173249/cyber-crime/malicious-npm-and-pypi-target-solana-private-keys.html)

### Inferences (best-practice, not from searched sources)
- Hot wallet holds only the capital needed for N hours of trading; sweep profits automatically to cold/multisig; dedicated wallet per strategy; no main-wallet key on the bot host.
- Pin exact dependency versions, commit lockfiles, use `npm ci`, delay adopting new releases (cooldown), run Socket/audit scanning, build in isolated container/VM with egress allowlist, never run unreviewed GitHub bots, load keys from a KMS/secret manager or signer service, not .env in repo.
- Use transaction-level guardrails: per-tx and per-day spend caps, program allowlist, simulation before send, alerting on unexpected outflows.

### Gaps
- No 2026 incident data (new campaigns, drainers, phishing stats) retrieved; SlowMist/Chainalysis 2026 reports not found within budget; drainer-kit and phishing specifics (e.g., approval/ownership-change phishing on Solana) not researched.
