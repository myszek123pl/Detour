# Telegram/Discord ingestion for memecoin signals

NOTE: Search budget was cut short (rate limit hit after 1 of ~6 searches). Only one search returned results. Items marked [UNVERIFIED] come from model background knowledge, not from a source fetched in this session. Writer should treat them as leads.

## Technical approach, rate limits, ban risk, legal/ToS

### Takeaway
Reading public channels via an MTProto user client (Telethon/Pyrogram/TDLib) with your own api_id is the standard way to get low-latency push updates; the Bot API cannot read channels it is not admin of. Ban/restriction risk is real, mostly tied to abuse patterns (spam, bulk joins, request floods) and unofficial-client fingerprinting; use a dedicated throwaway account, read-only, honor FloodWait.

### Cited Findings
- Telegram API Terms require developers to obtain their own api_id; on breach Telegram notifies the account responsible for the app — [Telegram API ToS](https://core.telegram.org/api/terms)
- Telethon docs tell users to comply with Telegram's ToS and API ToS; FAQ shows handling `errors.FloodWaitError` (read `e.seconds`, sleep) and advises not to hammer the API — [Telethon FAQ](https://docs.telethon.dev/en/stable/quick-references/faq.html)
- Telethon FAQ notes third-party libraries are easy to use and therefore misused for spam — [Telethon FAQ](https://docs.telethon.dev/en/stable/quick-references/faq.html)
- Maintainer (Lonami) has said Telegram has learnt some way to detect Telethon and is more likely to restrict such accounts (maintainer opinion, not Telegram statement) — [Telethon issue 4051](https://www.github.com/LonamiWebs/Telethon/issues/4051)
- Community docs claim accounts using unofficial clients are put under automatic observation; MadelineProto advice to email recover@telegram.org before running a userbot (secondhand, not confirmed by Telegram) — [gotd SUPPORT.md](https://raw.githubusercontent.com/gotd/td/main/.github/SUPPORT.md)
- Telethon docs have a page on deleted/limited/deactivated accounts — [Telethon troubleshooting](https://arabic-telethon.readthedocs.io/en/stable/extra/troubleshooting/deleted-limited-or-deactivated-accounts.html)

### Inferences
- Passive listening (event handler on NewMessage for already-joined channels) generates far fewer API calls than polling history, so it carries lower flood/ban exposure than scraping.
- Use one account per ~dozens of channels, separate from any personal/financial-linked account; join channels slowly (mass joins are the typical trigger).

### Gaps (not verified this session; background knowledge only)
- [UNVERIFIED] Library comparison: Telethon and Pyrogram are Python MTProto clients (Pyrogram's upstream maintenance has been sporadic; forks like Kurigram/pyrofork exist); TDLib is Telegram's official C++ library with bindings (tdl, python-telegram, etc.), most robust/official-style; gotd/td is a Go option. Updates are pushed over a persistent connection, so ingest latency is typically sub-second to a few seconds plus message-publish delay [UNVERIFIED].
- [UNVERIFIED] Bot API: bots only see channel posts when added as admin; privacy mode applies in groups; ~30 msgs/sec global send limits, ~20 msgs/min per group; getUpdates/webhooks. Not useful for reading third-party call channels.
- [UNVERIFIED] Specific FloodWait thresholds, join limits per day, and ban incidence numbers: none found.
- Legal: no source found on legality of scraping public channels (GDPR/ToS) or on trading on signals; Telegram's general ToS prohibits spam/abuse; not legal advice.
- Discord: not searched successfully. [UNVERIFIED] Discord ToS/Developer policy prohibits self-bots (automating a user token); account termination is the stated risk. Compliant routes: a bot you add to servers you administer or that authorize it; reading arbitrary servers via user token is a ToS violation. Message Content intent is privileged for bots in 100+ servers.

## Parsing contract addresses and latency

### Takeaway
No sources retrieved; this section is design guidance from background knowledge.

### Cited Findings
- None retrieved this session.

### Inferences
- [UNVERIFIED] Solana addresses: base58, 32-44 chars, regex like `[1-9A-HJ-NP-Za-km-z]{32,44}`, validate by decoding to 32 bytes; many pump.fun mints end in "pump". EVM: `0x[a-fA-F0-9]{40}`. Also extract from DexScreener/Birdeye/pump.fun/photon URLs and message entities (text_link, inline buttons), forwarded bot messages (e.g., scanner bots), and handle obfuscated/spaced addresses and images (OCR) — callers often post screenshots.
- Dedupe by (mint, channel), record message timestamp vs. receipt time to measure latency; for scoring, store first-mention time per channel per token.
- Latency budget is dominated by channel posting delay and on-chain execution, not Telegram delivery; by the time a call is public, alpha is often already priced in [UNVERIFIED].

### Gaps
- No measured latency benchmarks found.

## Evidence on call-channel value vs pump schemes; channel scoring

### Takeaway
Searches on this failed (rate limit), so no empirical evidence was gathered. Do not cite any performance claims from this file.

### Cited Findings
- None retrieved this session.

### Inferences
- [UNVERIFIED] Academic work (e.g., Xu & Livshits "The Anatomy of a Cryptocurrency Pump-and-Dump Scheme", USENIX 2019; Hamrick et al. on Telegram/Discord pumps) documents that organized pump groups yield profit mainly to organizers and early insiders; late followers lose. Worth verifying and citing in a follow-up.
- Scoring proposal (design, not evidence): for each call, record price at message time (+ your realistic fill with slippage/latency), then forward returns at 1m/5m/1h/24h net of fees, rug/honeypot flags, liquidity at call, holder concentration, and whether the channel/callers hold bags (wallet-linking). Score channels by median net return after realistic delay, hit rate, drawdown, and fraction of calls that are first-mention vs repeats of already-trending tokens; flag red signals: coordinated posting bursts, deleted messages, identical shill text across channels, calls on tokens with dev/insider wallet supply, paid-promo disclosures. Run out-of-sample and survivorship-adjusted (log all channels incl. dead ones).

### Gaps
- Need: peer-reviewed/industry data on Telegram call-channel profitability, pump-group studies, Dec 2025-Nov 2026 developments (e.g., enforcement, new Telegram API changes). None obtained.
