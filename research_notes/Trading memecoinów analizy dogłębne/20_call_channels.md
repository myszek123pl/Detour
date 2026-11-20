# Performance of Telegram/Discord memecoin call channels (as of Nov 2026)

Method note: 6 searches run (1 rate-limited); every WebFetch failed (arxiv.org, substack, doesitpay.org, cryptoactu.com not in session's allowed network). All figures below come from search-result summaries, NOT from reading the full pages. Treat as [UNVERIFIED - snippet only] unless stated.

## 1. Returns after calls: idealized vs realistic entry; median vs mean

### Takeaway
The one granular dataset found (a single-author Substack on Pump.fun call channels) shows a huge mean driven by outliers, a roughly zero/negative median, and edge that vanishes with even 15-30s entry delay. No peer-reviewed study of modern memecoin call channels was found.

### Cited Findings
- 770 Pump.fun calls collected (about 375 with usable performance curves); idealized "buy at call, sell 30s later" gave mean +552.2% but median -4.0%. [UNVERIFIED - snippet] — [Money Leaves Clues](https://moneyleavesclues.substack.com/p/inside-the-economics-of-pumpfun-call)
- With a 30s entry delay, share of calls later reaching +20% fell from 56.4% to 31.4%; 15s entry/30s exit gave median gross return +0.2%, which author says disappears after fees, slippage, latency. [UNVERIFIED - snippet] — same source
- CoinWire tracking: 1,567 memecoins promoted by 377 X accounts; after one week 80% lost 70%+, only 3% ever rose 10x. [UNVERIFIED, secondary, X not Telegram] — [Does It Pay](https://doesitpay.org/signal-and-call-groups/)
- calls.team leaderboard measures each call's PEAK multiple vs entry on 15-minute candles (2x hit rate, median peak multiple) - an upside metric, not realizable return; self-run. — [calls.team](https://calls.team/)
- Groups selectively share winning screenshots and hide most losses (qualitative). — [SecurityHero](https://www.securityhero.io/telegram-crypto-pump-dump/)

### Inferences
- Peak-multiple leaderboards overstate realizable returns; any evaluation must use post-latency entry and a fixed or realistic exit, and report median plus tail share.
- Mean-driven claims ("average 5x") are consistent with a median near zero or negative; heavy-tailed returns.

### Gaps
- No independent academic dataset on 2024-2026 memecoin call channels; Substack sample is small and unreplicated. Could not read full pages.

## 2. Pump-group mechanics

### Takeaway
Classic organized pump-and-dump research (2018 data) shows insiders profit at followers' expense; modern forensic cases (Solidus PumpCell, CertiK) show the same structure on Solana/BNB with bots and copy traders as exit liquidity.

### Cited Findings
- Hamrick et al. (Information Processing & Management 58, 2021): 952 Discord and 2,469 Telegram pumps over six months in 2018; most pumps on Telegram; Binance and Bittrex dominant venues; median price increase about 4.8% for top-75 coins vs about 19% for coins ranked below 500; 10% of Telegram pumps beat the increases of pumps on dominant coins. — [search listing, Hamrick et al.](https://cris.huji.ac.il/en/publications/an-examination-of-the-cryptocurrency-pump-and-dump-ecosystem/)
- Xu & Livshits, "Anatomy of a Cryptocurrency Pump-and-Dump Scheme": 220 Telegram pumps, Jul 21-Nov 18 2018; built a model predicting pumped coins. — [arXiv 1811.10109](https://arxiv.org/pdf/1811.10109v1)
- Does It Pay cites a Telegram-pump study with insiders' estimated return averaging 18% [UNVERIFIED, original study not identified]. — [Does It Pay](https://doesitpay.org/signal-and-call-groups/)
- Solidus Labs "PumpCell" ring (reported Dec 2025): invite-only Telegram group using bots, fabricated narratives, rapid token launches on Solana and BNB Chain; artificial hype drew copy traders before insiders exited. One report says it netted about $800k in a month [UNVERIFIED]. — [Pulse](https://www.pulse.bot/crypto/news/telegram-ring-ran-pump-and-dump-network-that-netted-800k-in-a-month-solidus-labs-cace8ba5-a639-4447-b610-6bce2c9c40b8)
- CertiK: three Telegram channels using hired actors to endorse fake tokens; wallets linked on-chain. — [CertiK](https://www.certik.com/blog/beware-the-honeypot-how-telegram-channels-used-actors-to-promote-scams)

### Inferences
- Insider-entry-before-call is the core edge; the call is the exit event. Followers' returns are negative-sum minus fees.

### Gaps
- Kamps & Kleinberg paper and arXiv 2605.09431 not read (fetch blocked); relevance of the latter unknown.

## 3. Paid call economics

### Takeaway
Little quantified evidence found. Qualitatively: promoters know exposure/entry/payment; revenue likely from paid shills, subscriptions, trading-bot referral fees, and own-bag selling.

### Cited Findings
- A paid call relies on information asymmetry: promoter knows exposure, entry price, payment terms. — [CryptoActu](https://cryptoactu.com/enquetes/call-groups-telegram-kol/) [UNVERIFIED - snippet, French]
- Maestro reportedly offers call-channel auto-buy among features. — search summary of vendor guides (e.g. [CoinCodeCap](https://coincodecap.com/telegram-bots-to-trade-memecoins-on-solana)) [UNVERIFIED]

### Inferences
- Referral-fee/bot-integration revenue (not verified here) would give callers an incentive for call volume over quality.

### Gaps
- No verified prices of paid calls, subscription fees, or caller revenue; no enforcement outcomes against paid-call operators found.

## 4. Channel scoring methods

### Takeaway
Public scoring is mostly peak-multiple/hit-rate leaderboards (calls.team, Trojan Chart caller markers), which are optimistic; the better method is fixed-delay entry with median/tail reporting.

### Cited Findings
- calls.team: 2x hit rate, median peak multiple, 15-minute candles. — [calls.team](https://calls.team/)
- Trojan Chart shows caller markers on charts. — [Trojan Chart](https://trojanchart.com/)
- Substack method: vary entry delay (0/15/30s) and exit horizon; report mean, median, share reaching +20%. [UNVERIFIED snippet] — [Money Leaves Clues](https://moneyleavesclues.substack.com/p/inside-the-economics-of-pumpfun-call)

### Inferences
- Robust scoring: first-mention timestamp, entry at delayed price incl. slippage/fees, survivorship (include deleted calls), cap per-call influence.

### Gaps
- No academic channel-scoring methodology found.

## 5. Can auto-trading calls work after latency and slippage?

### Takeaway
Evidence is against it for the typical call: edge decays within seconds, and bots/insiders exploit copy traders. Vendor speed claims are unverified marketing.

### Cited Findings
- arXiv 2601.08641: analysis of manipulative bots in memecoin markets under copy-trading settings (post-$TRUMP launch, Jan 17 2025); describes bots preying on naive copy traders; defenses underexplored. — [arXiv](https://arxiv.org/html/2601.08641) [UNVERIFIED - snippet only]
- Odinbot claims 15% of its copy trades land in the same block; founder says others take 1-2s [sponsored, self-reported]. — [Decrypt](https://decrypt.co/314700/how-solana-copy-trading-platform-odinbot-is-achieving-zero-block-latency?amp=1)
- Solana submission-to-confirmation under 1s normally (vendor guide). — [ThisDay](https://www.thisdaylive.com/2026/05/01/best-telegram-bot-for-high-frequency-traders-latency-multi-wallet-bundling-and-tip-optimization-compared/)
- Delay and median figures from the Pump.fun call study (section 1) imply no net edge at 15-30s.

### Inferences
- Human-readable calls plus bot execution (typically >1-2s) land after insiders/snipers; viable only if caller is verifiably early-entry-free or edge is in tokens with slower dynamics (unmeasured).

### Gaps
- No independent measured slippage/latency data for call-channel auto-buy; no net-PnL study of auto-trading calls over a long horizon.
