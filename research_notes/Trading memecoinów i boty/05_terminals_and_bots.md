# Memecoin trading terminals and Telegram trading bots: landscape, fees, market share, security, lessons (as of Nov 2026)

> Research method note: the network blocked direct page fetches for this session (cryptobriefing.com, rekt.news, solanacompass.com, gate.com, theblock.co, api.llama.fi all refused or unresolvable), and the shared web-search budget ran out after about 12 searches. Every figure below comes from search-engine result summaries of the linked pages, not from reading the full pages. Treat exact numbers as approximate and check them against live DefiLlama pages (defillama.com/protocol/axiom, /trojan, /bonkbot) before publishing. Many "comparison" sites in this niche are affiliate or referral marketing, and that is flagged where relevant.

## 1. Features, fee levels, volumes and revenue of the major terminals and bots

### Takeaway
By late 2026 the market has moved from Telegram-native bots (Trojan, BonkBot, Maestro, Banana Gun) to web "trading terminals" (Axiom, GMGN, FOMO, Photon, Padre). Axiom was the volume and fee leader through mid-2026. From about August 2026 the mobile/social app FOMO (about 0.5% fee) and GMGN have matched or overtaken it on trailing-30-day revenue. The standard platform fee is still about 1% per swap (0.5% to 1% range), plus priority and Jito tips.

### Cited Findings

**Market share and revenue (2026)**
- On DefiLlama data dated 14 Aug 2026, Axiom had about 39% of trailing-30-day fees across the combined "Trading App" and "Telegram Bot" categories, with GMGN second at about 36%. This comes via aggregator and affiliate sites, so precision is low. — [Datawallet](https://www.datawallet.com/crypto/best-telegram-crypto-trading-bots); [Axiompedia compare](https://axiompedia.com/compare)
- Axiom's share of Solana bot or terminal volume is reported very differently depending on source and metric:
  - "60–72% by mid-2026" (likely an affiliate figure, metric unclear). — [thetradingmarkets](https://thetradingmarkets.com/axiom-trade-review-2026/); [memegateway](https://memegateway.com/academy/axiom-trading-bot-guide/)
  - About 44.6% of Solana terminal volume in June 2026, falling below 30% by 23 Aug 2026. — [Solana Compass](https://solanacompass.com/news/fomo-overtakes-axiom-as-solanas-top-daily-trading-terminal-by-volume)
- Photon's share collapsed. It was above 30% in early 2025 and under 10% later. An earlier Dune snapshot shows it falling from 31.8% to 20.4%. — [Gate Learn (data-driven look at trading bots)](https://www.gate.com/learn/articles/a-data-driven-look-at-trading-bots-solana-remains-the-main-battleground-as-newcomers-surpass-veterans-in-multi-scenario-competition/8411); [Datawallet](https://www.datawallet.com/crypto/best-telegram-crypto-trading-bots)
- On 6 Aug 2026, FOMO first overtook Axiom as Solana's top daily trading terminal by volume. — [Solana Compass](https://solanacompass.com/news/fomo-overtakes-axiom-as-solanas-top-daily-trading-terminal-by-volume)
- FOMO became the top revenue-generating trading app, at about $19.88M revenue over 30 days (on about $20.99M fees, per DefiLlama) and about 46% of Solana terminal volume. FOMO charges about 0.5% against Axiom's about 1%. — [CryptoBriefing](https://cryptobriefing.com/fomo-overtakes-axiom-top-revenue-trading-app/); [Solana Compass – FOMO 46%](https://solanacompass.com/news/fomo-captures-46-of-solana-trading-platform-spot-volume-as-weekly-revenue)
- A TokenPost report (about Oct 2026) gave these figures:
  - 30-day revenue: FOMO $18.02M vs Axiom $16.34M.
  - Seven-day revenue: Axiom led, $2.67M vs $2.36M.
  - September 2026 monthly revenue: FOMO $31.53M vs Axiom $18.35M.
  - Methodology caveat: DefiLlama nets referral and cashback payouts out of Axiom's revenue but not out of FOMO's, so the two are not like-for-like. — [TokenPost](https://www.tokenpost.com/news/business/35852)
- One site reports near-parity in 30-day volume to 8 Nov 2026: Axiom $1.43B vs FOMO $1.37B. This is FOMO's own site, so it is self-interested. — [fomotrading.app](https://fomotrading.app/)
- GMGN overtook Axiom in 24-hour revenue (exact date not visible). In the 30 days to 28 Sep 2026, fees per DefiLlama were about $37M for Axiom and about $51M for GMGN. — [CryptoBriefing – GMGN overtakes Axiom](https://cryptobriefing.com/gmgn-overtakes-axiom-24-hour-revenue/); [Datawallet](https://www.datawallet.com/crypto/best-telegram-crypto-trading-bots)
- A DefiLlama snapshot for Axiom showed:
  - about $50.88M in 30-day fees,
  - about $1.59M in 24-hour revenue,
  - about $198.93M in cumulative fees and revenue (snapshot date unknown).
  DefiLlama counts Axiom "revenue" after referral and cashback payouts, and its volume is a floor because it excludes unindexed venues. — [DefiLlama – Axiom](https://defillama.com/protocol/axiom); [DefiLlama – Axiom Pro](https://defillama.com/protocol/axiom-pro)
- Conflicting estimates of Axiom's cumulative revenue:
  - "Over $390M since its 2024 launch". — [heybeluga](https://heybeluga.com/articles/top10-crypto-protocol-highest-revenue/)
  - About $453M cumulative, set against GMGN's about $115M annualized run-rate. — [Datawallet](https://www.datawallet.com/crypto/best-telegram-crypto-trading-bots)
  - DL News on Axiom's early growth ("$150M revenue", 2025). — [DL News](https://www.dlnews.com/articles/defi/solana-bot-axiom-takes-over-cursor-with-150m-revenue/)
- Trading terminals posted their first $1B volume day since January 2025 (2026 article). — [The Defiant](https://thedefiant.io/news/defi/trading-terminals-post-first-usd1-billion-day-since-january-2025)
- Trojan's cumulative fees are about $227–228M (DefiLlama, 2026 snapshots). — [DefiLlama – Trojan](https://defillama.com/protocol/trojan)
- BONKbot's cumulative fees are about $89.7–95.0M (DefiLlama, varying snapshot dates). — [DefiLlama – BONKbot](https://defillama.com/protocol/bonkbot)
- On 24 Oct 2025 Pump.fun acquired Padre, a multichain terminal on Solana, Base, Ethereum and BNB. Padre had about 5% market share per Dune at the time. The PADRE token lost its utility and fell about 67%, and Pump.fun promised an airdrop to compensate. Pump.fun's rationale was that terminals capture most ecosystem volume. — [Cointelegraph](https://cointelegraph.com/news/pumpfun-acquires-padre-trading-terminal-solana-memecoins); [Blockworks](https://blockworks.co/news/pump-acquires-padre); [The Defiant](https://thedefiant.io/news/defi/pumpfun-acquires-memecoin-trading-terminal-padre); [DL News](https://www.dlnews.com/articles/defi/pump-fun-placates-padre-tokenholders-with-airdrop-promise/)

**Fee levels**
- Platform fees per swap (sources conflict, mostly affiliate calculators):

  | Bot or terminal | Reported fee |
  |---|---|
  | Trojan | 0.9% (1% advertised, 0.9% with referral; higher rebate tiers reach about 0.5%) |
  | BonkBot | 1% |
  | Photon | about 1% (one source says 0.5%) |
  | GMGN | about 1% (one source says 0.5%) |
  | BullX | about 1% (one source says 0.5%) |
  | Bloom | 0.9% or 1% |
  | Banana Gun | 0.5% (cheapest on MadeOnSol) |
  | Padre | 0.5% or lower |
  | Axiom | about 1% |
  | FOMO | about 0.5% |

  Network and priority fees (Jito tips) are charged on top of all of these. — [solanatools fees](https://solanatools.io/solana-trading-bot-fees); [solanatools blog](https://solanatools.io/blog/solana-trading-bot-fees-compared); [MadeOnSol calculator](https://madeonsol.com/compare-bots); [traderview calculator](https://traderview.com/tools/fee-calculator); [StakePoint](https://stakepoint.app/blog/solana-telegram-trading-bot-fees-2026); [uwuu.ai Trojan review](https://uwuu.ai/blog/trojan-bot-review); [CryptoBriefing](https://cryptobriefing.com/fomo-overtakes-axiom-top-revenue-trading-app/)
- Bot fees on Solana have converged at about 1%, and products compete on where the fee goes (referral, cashback, rebates). — [StakePoint](https://stakepoint.app/blog/solana-telegram-trading-bot-fees-2026)
- Feature roundups (sniping, copy trade, limit orders) for Trojan, GMGN and Bloom are available from RPC vendors. These are vendor content. — [Dysnix](https://dysnix.com/blog/top-solana-sniper-bot); [RPC Fast](https://rpcfast.com/blog/top-solana-sniper-bot); [CoinCodeCap GMGN review](https://coincodecap.com/gmgn-review); [Gate top-10 meme bots](https://www.gate.com/learn/articles/top-10-meme-trading-bots/5195)

### Inferences
- **Fees are commoditized.** About 1% was the norm, and the 2026 challengers (FOMO, Padre, Banana Gun) are winning partly on fees of 0.5% or less. A custom bot saves the 0.5–1% platform fee per side, which is about 1–2% per round trip. For high-frequency memecoin trading that is often larger than the edge itself.
- **Leadership is volatile.** Photon went from above 30% to under 10% in about a year. Axiom went from roughly 45% to under 30% in two months. Distribution (social or mobile UX, referral programs, launchpad integration such as Pump.fun + Padre) matters more than execution technology.
- **Revenue figures are not comparable** across platforms. DefiLlama nets referrals and cashback for some platforms and not others.
- **Telegram bots are a declining share.** Trojan's cumulative fees (about $228M) remain large, but new volume goes mostly to web or mobile terminals.

### Gaps
- No sourced 2026 data was found for Maestro, Banana Gun, Sigma, Sol Trading Bot, BullX Neo or Photon revenue. Searches were exhausted before the ETH/Base/BSC bot queries ran.
- Feature matrices were not verified from official docs, because the doc sites could not be fetched. The following is training knowledge only, unverified for Nov 2026, and the writer should verify or label it:
  - Most Solana terminals (Axiom, GMGN, Photon, BullX Neo, Padre) offer:
    - Pump.fun / bonding-curve "new pairs" feeds and "migration" columns,
    - limit / TP / SL orders,
    - wallet tracking and copy trading,
    - Jito-bundle or "anti-MEV" submission.
  - Telegram bots (Trojan, BonkBot, Bloom, Maestro, Banana Gun) offer:
    - auto-buy on contract paste,
    - sniping (Banana Gun and Maestro on ETH, first-block snipes),
    - copy trade,
    - limit orders.
  - Banana Gun and Maestro are EVM-first bots that later added Solana.
- The live DefiLlama "Telegram Bot" and "Trading App" category rankings for Nov 2026 could not be retrieved, because the API was blocked.
- The Axiompedia or memegateway "Axiom (ex-Photon)" naming looks wrong, since Axiom and Photon are separate products. Do not repeat it.

## 2. Security incidents and custody models

### Takeaway
Bot exploits fall into three classes:
1. **Router or contract approval bugs.** Maestro and Unibot, Oct 2023.
2. **Server-side key compromise** at custodial "hot wallet" bots. Banana Gun Sept 2024 ($3M), Solareum Mar 2024 ($523K), DEXX Nov 2024 ($21–30M), Bloom Oct 2026 (about $947K).
3. **Insider misuse of user data.** Axiom, Feb 2026.

Established bots usually refunded victims from treasury. Smaller ones shut down. Custody has shifted from "bot holds your private key" toward TEE-based embedded wallets (Axiom on Turnkey), but the operator still controls signing policy and sees all user data.

### Cited Findings
- **Maestro (Oct 2023).** An external-call vulnerability in the Router 2 contract on Ethereum lost about 280 ETH (about $485–500K). Maestro removed the exploit within about 30 minutes, refunded users, and said wallet credentials were not compromised. — [The Defiant](https://thedefiant.io/maestro-trading-bot-exploited-for-usd500k); [BeInCrypto](https://beincrypto.com/maestro-refunds-after-attack)
- **Unibot (31 Oct 2023).** A token-approval exploit on its new router lost about $600–640K. The root cause was a CALL injection that let the attacker move tokens users had approved. Unibot paused the router and compensated users. — [Blockworks](https://blockworks.co/news/telegram-trading-tool-unibot-suffers-exploit); [Rekt – Unibot](https://www.rekt.news/unibot-rekt); [Revoke.cash](https://https-revoke_cash.proxy.bugsmash.io/exploits/unibot)
- **CertiK's common root cause:** both router contracts lacked permission and parameter checks, so attackers could abuse users' existing token approvals. — [CertiK](https://www.certik.com/blog/maestro-and-unibot)
- **Banana Gun (19 Sept 2024).**
  - Loss: about $3M across 11 users. Early reports said about $2M from 36 users.
  - Cause: Banana Gun blamed a "potential vulnerability in the Telegram message oracle". The attacker manually transferred ETH out of users' bot wallets while the bot was active.
  - Response: full refunds from the treasury without selling BANANA tokens, and the EVM and Solana bots were temporarily disabled.
  — [The Block](https://www.theblock.co/post/318074/banana-gun-exploit-refund); [Cointelegraph](https://cointelegraph.com/news/banana-gun-crypto-bot-refunds-3m); [The Defiant](https://thedefiant.io/banana-gun-pledges-to-pay-back-victims-of-usd3-million-exploit); [Rekt](https://rekt.news/bananagun-rekt)
- **Solareum (29 Mar 2024).**
  - Loss: about 2,800 SOL (about $523K) from 302 users, likely through leaked private keys. The team suspected compromised Telegram bot tokens exposing keys in message history.
  - BONKbot was initially suspected. It said 113 victims had used BONKbot but had exported their keys elsewhere.
  - Solareum shut down citing insufficient funds.
  — [Decrypt](https://decrypt.co/224371/solana-telegram-trading-bot-shut-down-users-drained-523k); [Decrypt – BONKbot denies link](https://decrypt.co/224127/solana-wallets-drained-523k-bonkbot-denies-link); [Cointelegraph](https://cointelegraph.com/news/telegram-trading-bot-solareum-shutters-after-520k-exploit)
- **DEXX (Nov 2024).** A private-key management leak was reported at about $21M (8,600+ wallets) and also cited as about $30M. The figures conflict. — [CyberMaterial](https://cybermaterial.com/over-8-6k-solana-wallets-linked-to-dexx-hack); [Helius – Solana hacks](https://www.helius.dev/blog/solana-hacks)
- **Bloom (26 Oct 2026).**
  - Loss: 9,408 SOL (about $947K) drained in about 94 seconds from 48–49 wallets belonging to 9 users.
  - Cause: Bloom blamed a third-party module RCE vulnerability and said no keys were compromised. Other reporting says the transfers were signed by the wallets' own keys, or blames a copied key. These accounts conflict.
  - Response: users were fully refunded the same day.
  — [CryptoSlate](https://cryptoslate.com/hackers-drain-9400-sol-from-bot-wallets-and-a-copied-key-is-blamed/); [investingLive](https://investinglive.com/cryptocurrency/solana-trading-bot-bloom-drained-of-947-000-in-sol-as-nine-users-wallets-emptied/); [Bitcoin.com](https://news.bitcoin.com/security/solana-trading-bot-hacked-nearly-1m-49-wallets-drained/); [parameter.io](https://parameter.io/bloom-trading-bot-suffers-9408-sol-hack-all-users-refunded-within-hours/)
- **Axiom insider allegations (26 Feb 2026).**
  - ZachXBT alleged that senior BD employee Broox Bauer (plus "Ryucio") used internal customer-support tools to de-anonymize private user wallets, including KOL wallets, for insider trading. Bauer allegedly tracked 10–20 wallets at a time, with "virtually no monitoring and access controls".
  - Axiom removed employee access to the tools and promised an investigation.
  - Specific trades were not proven without Axiom's internal logs.
  - Polymarket bettors front-ran the reveal: $59.8K turned into $109K.
  — [The Block](https://www.theblock.co/post/391423/zachxbt-investigation-into-alleged-employee-insider-trading); [Decrypt](https://decrypt.co/359223/y-combinator-backed-axiom-employees-accused-insider-trading-zachxbt); [The Defiant](https://thedefiant.io/news/defi/zachxbt-accuses-axiom-staff-of-insider-trading-using-wallet-data); [Unchained](https://unchainedcrypto.com/zachxbt-accuses-axiom-employee-of-misusing-private-wallet-data/); [DeFi Rate](https://defirate.com/news/axiom-insider-data-abuse-allegations-expose-crypto-compliance-gaps/)
- **Custody models.**
  - Axiom's wallets are described as non-custodial on Turnkey infrastructure, with keys handled inside TEEs (AWS Nitro Enclaves). Turnkey says it never holds usable key material.
  - No independent audit of Axiom's wallet setup was found.
  - Phishing and scams still cost Axiom users money.
  — [Turnkey case study](https://turnkey.com/customers/axiom-global-defi-trading-platform); [Turnkey embedded wallets](https://www.turnkey.com/embedded-wallets); [Turnkey docs](https://docs.turnkey.com/security/non-custodial-key-mgmt); [Solana Compass – Axiom](https://solanacompass.com/projects/axiom); [Ryder](https://ryder.id/blogs/post/is-axiom-trade-safe-what-the-wallet-holds-and-what-the-platform-knows)
  - The privacy terminal Genius also uses Turnkey. — [Turnkey – Genius](https://www.turnkey.com/customers/genius-privacy-trading-terminal)
  - The Trojan review flags custody risk for Telegram bots that generate and store user keys server-side. — [uwuu.ai](https://uwuu.ai/blog/trojan-bot-review)

### Inferences
- **Telegram bots are effectively custodial hot wallets.** The operator generates and stores keys so it can sign instantly. A server, dependency or "oracle" compromise drains users directly (Banana Gun, Solareum, DEXX, Bloom). TEE embedded wallets (Turnkey) reduce key exfiltration risk. They do not remove operator data-visibility risk, as the Axiom case shows.
- **Router contracts with unlimited approvals are a second attack surface** on EVM.
- **Practical rule for users:** keep only working capital in bot wallets and sweep profits out often. Several incidents drained idle balances.
- **Lessons for a custom bot:**
  - Self-host keys in a dedicated hot wallet holding minimal balance.
  - Never import a main wallet's key into a third-party bot.
  - Avoid infinite approvals, and audit third-party modules and dependencies (the Bloom RCE).
  - Isolate the signing service from the Telegram or front-end layer (the Banana Gun "message oracle").
  - Using your own bot also removes the platform-insider risk of others watching your wallets.

### Gaps
- No primary post-mortems were read. Rekt and the Bloom statement were blocked, so technical root causes are second-hand.
- No 2025–2026 incident data was found for Photon, GMGN, BullX, Trojan or Maestro beyond the above. The search budget was exhausted.
- The outcome of Axiom's internal investigation is unknown.

## 3. What differentiates profitable usage, and what bots cannot do

### Takeaway
The searches did not return hard data on bot-user profitability. The structural evidence points the same way: about 1% fees per side, priority and Jito tips, and the shift of market share toward cheaper venues all erode edge. The terminals sell speed and information (new-pair feeds, wallet tracking, copy trade), and the operators themselves showed that information asymmetry is the real edge (the Axiom insider case). Bots cannot create alpha. They execute faster on public information that everyone else on the same terminal also sees.

### Cited Findings
- Platform fees of about 0.5–1% are charged on top of network and priority fees, so effective cost per trade exceeds the headline rate. — [solanatools blog](https://solanatools.io/blog/solana-trading-bot-fees-compared); [StakePoint](https://stakepoint.app/blog/solana-telegram-trading-bot-fees-2026)
- Volume moved quickly to a terminal charging about 0.5% (FOMO) over about 1% (Axiom), suggesting active traders are fee-sensitive. — [CryptoBriefing](https://cryptobriefing.com/fomo-overtakes-axiom-top-revenue-trading-app/)
- In the Axiom case, staff allegedly used internal dashboards linking wallets to identities to track KOL wallets and trade ahead of them. Wallet-level information, not execution speed, was the exploited edge. — [Decrypt](https://decrypt.co/359223/y-combinator-backed-axiom-employees-accused-insider-trading-zachxbt); [The Block](https://www.theblock.co/post/391423/zachxbt-investigation-into-alleged-employee-insider-trading)
- Terminals and bots earn hundreds of millions in cumulative fees regardless of whether users profit. Examples: Trojan about $228M, BONKbot about $90M, and Axiom's cumulative revenue estimated anywhere from about $199M (DefiLlama snapshot) to $390–453M (secondary sources). — [DefiLlama – Trojan](https://defillama.com/protocol/trojan); [DefiLlama – BONKbot](https://defillama.com/protocol/bonkbot); [heybeluga](https://heybeluga.com/articles/top10-crypto-protocol-highest-revenue/)

### Inferences
- **Fees compound against frequent trading.** At a 1% round-trip-per-side fee, a trader making 10 round trips a day pays about 20% of deployed capital per day in platform fees, before slippage and tips. Fee minimization (a custom bot, or 0.5% venues with rebates) is a precondition for any small edge to survive.
- **Copy trading of public "smart wallets" is crowded.** Thousands of terminal users follow the same wallets (GMGN and Axiom both feature wallet tracking), so followers buy after the leader and become exit liquidity. Tracked wallets can also deliberately bait followers. This is inference; no study was retrieved.
- **Migration sniping and new-pair sniping are latency races.** Professional searchers with co-located RPC and Jito bundles beat retail terminal users. A custom bot only wins this with comparable infrastructure (private RPC, Jito or other block-engine bundles, staked connections).
- **What bots cannot do:**
  - They cannot detect rugs or bundled dev supply with certainty.
  - They cannot guarantee fills during congestion.
  - They cannot protect against operator compromise or insider misuse.
  - They cannot remove the negative-sum structure of memecoin trading after fees, creator rewards and MEV.
- **Likely profitable niches for a custom bot:**
  - lower fees,
  - private signal sources not shared with the terminal crowd,
  - disciplined automated exits (TP/SL, time stops),
  - strict risk caps per token,
  - filtering (holder concentration, dev-wallet behavior, bundle detection) rather than raw speed.

### Gaps
- No Dune or academic data on the percentage of bot or terminal users who are profitable was retrieved. Searches for "bot users profitability" and "copy-trade front-running" hit the exhausted search budget. The writer should rely on adjacent researcher notes (memecoin trader PnL distributions) or flag this as unverified.
- MEV protection effectiveness (Jito bundles, "anti-MEV" modes) and sandwich rates against bot users on Solana in 2026 were not sourced.
- The current state of Jito's mempool and bundle policy and its effect on bot sniping was not researched.
