# Security incidents affecting memecoin trading bots and terminals (as of Nov 2026)

Method note: 5 web searches only (search-result summaries; pages not fetched). Figures below are as reported in those summaries; "UNVERIFIED" marks claims from single/low-quality sources or not confirmed by a post-mortem.

## What happened in the major incidents (Banana Gun, Maestro, Unibot, BonkBot/Solareum, DEXX)?

### Takeaway
Incidents split into two classes: (a) smart-contract/router flaws on EVM bots (Maestro, Unibot, Oct 2023), and (b) custodial key/infra compromise (Banana Gun Sept 2024, BonkBot/Solareum Mar 2024, DEXX Nov 2024). The custodial class affects users who never made any mistake.

### Cited Findings
- Maestro (24 Oct 2023): ~280 ETH (~$485k) drained via Maestro Router 2; Maestro paid 610 ETH from its revenue to cover users — [Certik/aggregated via search](https://www.certik.com/blog/maestro-and-unibot)
- Unibot (31 Oct 2023): ~$642k lost via a token-approval exploit in a newly deployed router; attacker could insert an arbitrary transferFrom() to drain tokens users had approved; ran ~9 hours before router was halted; ETH balances unaffected — [Decrypt](https://decrypt.co/203795/unibot-telegram-bot-falls-prey-major-exploit-over-640k-crypto-lost?amp=1), [The Block](https://www.theblock.co/amp/post/260133/unibot-confirms-exploit-and-promises-compensation-as-token-price-plunges)
- CertiK: both Maestro and Unibot routers lacked permission and parameter checks (similar vulnerability) — [CertiK](https://www.certik.com/blog/maestro-and-unibot)
- Unibot reportedly never repaired the old router, only stopped using it, so lingering approvals remain abusable (single-source claim in search summary; treat as UNVERIFIED) — [Revoke.cash](https://revoke.cash/exploits/unibot)
- BonkBot/Solareum (Mar 2024): first estimate ≥$208k (CertiK), later ~$523k, ~300 Solana users reported; BonkBot said victims had exported private keys and later cited 113 victims (<0.1% of users); data pointed to Solareum, which then shut down — [Decrypt](https://decrypt.co/224127/solana-wallets-drained-523k-bonkbot-denies-link), [Decrypt shutdown](https://decrypt.co/224371/solana-telegram-trading-bot-shut-down-users-drained-523k)
- Some BonkBot users disputed that they had exported keys elsewhere; cause disputed between team and users — [Coinpaper](https://coinpaper.com/3786/bon-kbot-claims-to-be-unaffected-by-solana-wallet-exploit-but-users-claim-otherwise)
- Banana Gun (Sept 2024): post-mortem revised loss from ~$2M/36 users to ~$3M from 11 users; cause stated only as a "potential vulnerability" in the Telegram message oracle; victims saw funds moving during bot interaction/notifications; EVM and Solana bots paused, relaunched with a two-hour transfer delay; full refund from treasury (no token sales) — [The Block](https://www.theblock.co/post/318074/banana-gun-exploit-refund), [Rekt](https://rekt.news/bananagun-rekt), [Cointelegraph](https://cointelegraph.com/news/banana-gun-crypto-bot-refunds-3m)
- QuillAudits reading (its own interpretation, not Banana Gun's): attacker intercepted messages and gained unauthorized wallet access — [QuillAudits](https://www.quillaudits.com/blog/hack-analysis/banana-gun-exploit)
- Rekt noted reports of similar Maestro (~$200k) and Unibot exploits around Banana Gun's incident with no detailed reports published — [Rekt](https://rekt.news/bananagun-rekt)
- DEXX (16 Nov 2024): >=900 unique users hit, most losing <$10k, one >$1M; first reported ~$21M, SlowMist later said within ~$30M (varies with memecoin price); >8,600 Solana addresses linked to attacker; founder said the failure was the team's security management practices, not the key-management solution; case filed, compensation discussed; no significant recovery found — [Cointelegraph](https://cointelegraph.com/news/solana-dexx-hack-november-2024-suspicious-wallets), [BraveNewCoin/SlowMist](https://bravenewcoin.com/insights/dexx-hack-investigation-unveils-over-8600-solana-wallet-links-slowmist-report), [Veritas](https://veritasprotocol.com/blog/dexx-founder-addresses-theft-responsibility)
- DEXX note: a separate $21M Hyperliquid private-key theft (Oct 2025) appears in search results; do NOT conflate it with DEXX — [The Block](https://www.theblock.co/news/regulation/2025-10-10-21-million-stolen-from-hyperliquid-user-after-apparent-private-key-compromise-peckshield-374145)

### Inferences
- Router/approval bugs (EVM) hit only users with active approvals; custodial-key incidents hit anyone holding balances, and the loss scale scales with total custody.
- Teams tend to blame users/third parties first (BonkBot) or give vague root causes (Banana Gun "potential"), so root causes often stay unconfirmed.

### Gaps
- No technical post-mortem found for DEXX key exposure; Banana Gun root cause unconfirmed; Maestro Sept/Oct 2024 ~$200k figure is Rekt-reported only.
- No source on whether any 2025-2026 incidents hit these bots (not searched; searches limited).

## Phishing, fake bot clones, and terminal impersonation (Photon/Axiom)

### Takeaway
Impersonation is a separate, ongoing threat: lookalike bots/sites trick users into entering keys or connecting wallets. I found no verified incident of an official Photon or Axiom compromise; evidence is of impersonators.

### Cited Findings
- Medium article (July 2025) claims Axiom has no official Telegram bot and names @AxiomTradingBot and @axiom_tradebot as fake; a victim anecdote (50 SOL) involved a BullX-branded fake bot — UNVERIFIED, single promotional-style source — [Medium](https://medium.com/p/a33b469b6665)
- Fake Photon lookalike site reported (real: photon.tinyastro.io) — [PCRisk](https://www.pcrisk.com/removal-guides/34489-fake-photon-website-scam)
- ScamSniffer: malicious Telegram group scams (fake verification bots, group invites delivering malware) up 2,000% from Nov 2024 to Jan 2025 — [Cointelegraph](https://cointelegraph.com/news/malicious-telegram-group-scams-have-increased-2000-since-november-scam-sniffer)
- May 2025: trader lost >$200k from wallets created by the SIGMA Telegram bot; fake-CAPTCHA phishing suspected, cause not confirmed — [Cryptopolitan](https://www.cryptopolitan.com/crypto-trader-loses-200k-telegram-bot/)
- Fake Telegram support channels as drainer vector — [SEAL radar](https://radar.securityalliance.org/psa-fake-telegram-support-channels-drainers/); [Kaspersky](https://www.kaspersky.com/blog/phishing-and-scam-in-telegram-2025)
- Bonk.fun launchpad website hijacked to serve wallet drainer (date not confirmed in results; not the BonkBot Telegram bot) — [The Block](https://www.theblock.co/post/393345/bonk-fun-hijacked)

### Inferences
- Brand-name collisions (Bonk.fun vs BonkBot; clones of Axiom/Photon/BullX) make verification via official links a core user defense.

### Gaps
- No named, verified Photon/Axiom user-drain case with amounts; no 2026 data gathered.

## Root causes and lessons (custody, key export, session security)

### Takeaway
Custody model dominates risk: bots generate and hold keys server-side, so a single infra/oracle/ops compromise exposes all users. Key export, shared-session/message-channel trust, and approvals are the recurring weak points.

### Cited Findings
- Banana Gun mitigation: added two-hour transfer delay after relaunch (a withdrawal-friction control) — [The Block](https://www.theblock.co/post/318074/banana-gun-exploit-refund)
- BonkBot's stated cause was previously exported keys used in another app (Solareum); users disputed — [Decrypt](https://decrypt.co/224127/solana-wallets-drained-523k-bonkbot-denies-link)
- Unibot: exposure limited to users who approved the vulnerable router; revoking approvals is the remedy — [Revoke.cash](https://revoke.cash/exploits/unibot)
- DEXX founder framed cause as team security management practices — [Veritas](https://veritasprotocol.com/blog/dexx-founder-addresses-theft-responsibility)
- Reimbursement outcomes differ: Maestro and Banana Gun paid users; Unibot promised compensation; DEXX still discussing; Solareum shut down — sources above.

### Inferences (not sourced; analyst judgment)
- Lessons: avoid keeping large balances in bot wallets; export keys only to trusted wallets and treat exported-key wallets as compromised once shared; use separate hot wallets with small funds; revoke router approvals; enable withdrawal delays/whitelists and 2FA where offered; never trust Telegram messages/DMs for support; verify bot handles/domains from official site; teams need HSM/KMS key isolation, strict internal access controls, and published post-mortems.
- Telegram session/message-channel trust (the Banana Gun oracle) implies identity should not rely solely on Telegram-delivered messages for authorizing fund movements.

### Gaps
- No primary Banana Gun/Maestro/DEXX technical write-ups fetched; no data on which bots offer withdrawal whitelists or hardware-backed custody as of Nov 2026.
