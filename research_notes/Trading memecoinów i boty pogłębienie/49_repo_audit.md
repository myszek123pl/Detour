# Solana memecoin bot repos: reputable vs malicious, red flags, safe evaluation

Method note: 2 web searches succeeded (third hit a rate limit); WebFetch of primary pages (cointelegraph, research.jfrog.com) failed with DNS errors (hosts not in session allowlist). All cited findings below are therefore from search-result summaries (secondary), not read in full. Items marked [UNVERIFIED] come from model background knowledge, not from sources fetched in this session. No code was downloaded or run.

## Which documented malware campaigns target Solana bot users on GitHub/npm/PyPI?

### Takeaway
There are multiple documented campaigns (2025-2026): fake "pump.fun bot" repos with inflated stars/forks that pull a malicious npm dependency, plus npm/PyPI packages that steal Solana keypairs. The payload is often NOT in the repo's own files but in a dependency or a download URL.

### Cited Findings
- SlowMist reported a fake "solana-pumpfun-bot" repo under account zldp2002, with many stars/forks, that scanned for wallet files/private keys and sent them to an attacker server; a victim reported losses on 2 July 2025; stolen funds moved to exchanges with weak KYC such as FixedFloat — [crypto-economy summary of SlowMist](https://crypto-economy.com/slowmist-uncovers-malicious-github-project-targeting-solana-users/) (via search snippet)
- The payload was in a dependency, `crypto-layout-utils`, fetched from an external URL (bypassing normal npm review); after npm removed one package the attacker swapped the download link — same source set (search snippet; see also [Cointelegraph](https://cointelegraph.com/news/solana-trading-bot-github-malware-scam), [OKX Learn](https://www.okx.com/en-au/learn/malicious-github-solana-wallets), not opened)
- A later SlowMist warning described further repos where the malicious code also targeted `.env` files and Solana `id.json` keypairs; SlowMist advised rotating all credentials (wallet keys, mnemonics, npm tokens, SSH keys) — [MEXC News repost](https://www.mexc.com/news/59206) (search snippet; sources disagree on exact repo names and campaign count)
- JFrog "Solana FakeFix" (dated June 2026 in search summary): ~25 malicious npm and PyPI packages posing as Solana tooling; payloads scan for Solana keypairs, SSH keys, AWS creds, .env, wallet files; one package `solana-mev-bot` posed as a profitable MEV/sandwich bot and asked the user to paste a private key — [JFrog](https://research.jfrog.com/post/solana-fakefix/) (search snippet; page not opened, date unverified)
- Socket: five typosquatted npm packages hook wallet functions and send keys to a hardcoded Telegram bot token/chat ID before returning the expected result; one (`base-x-64`) obfuscated; PyPI `web3x` (3,405 downloads) exfiltrated mnemonics to Telegram — [Socket threat report](https://socket.dev/blog/2025-blockchain-and-cryptocurrency-threat-report), [Security Affairs](https://securityaffairs.com/173249/cyber-crime/malicious-npm-and-pypi-target-solana-private-keys.html) (snippets)
- Earlier waves (Jan 2025): npm packages exfiltrating Solana keys via Gmail SMTP; PyPI libraries stealing Solana id.json — Socket / [SC World brief](https://www.scworld.com/brief/solana-private-key-exfiltration-facilitated-by-illicit-npm-packages) (snippet)
- A DEV.to piece claims almost every Polymarket trading bot on GitHub is malicious (same pattern, different venue; low-authority source, not read) — [DEV](https://dev.to/nevosaynevo/why-almost-every-polymarket-trading-bot-on-github-is-malicious-28o7)

### Inferences
- The attacker playbook is stable: popular-looking bot repo + trojanized dependency + exfil to Telegram/HTTP/SMTP; swapping a dependency URL lets them re-arm after takedowns, so a clean commit today does not prove a clean repo tomorrow.
- Because victims must supply a private key to a "bot", the bot category is inherently high-risk.

### Gaps
- Could not open primary SlowMist/JFrog/Socket pages; exact repo names beyond zldp2002/solana-pumpfun-bot, dates, and IOCs unconfirmed.
- No search done on Check Point/Sophos-style infostealer campaigns that use fake bots (third search was rate-limited).

## Which open-source Solana bot repos are reputable/maintained?

### Takeaway
I could not verify any specific "reputable" memecoin sniper/copy-trade repo in this session. Reputability should be judged by the criteria in the last section, not by a name list.

### Cited Findings
- None obtained in this session.

### Inferences
- [UNVERIFIED, background knowledge] Generally lower-risk categories: official SDK/infra repos (solana-labs/solana-web3.js, Jito's jito-ts/searcher examples, Raydium and Meteora SDKs, Anchor, Metaplex) and well-known multi-year projects with identifiable maintainers and issues history. Verify each one's current maintenance before relying on this; I did not check any.
- [UNVERIFIED] Small "sniper"/"copy trader"/"pump.fun bot" repos with a Telegram link and a promise of profit are the typical bait category; treat as hostile by default.

### Gaps
- No verified list of maintained sniper/copy-trade repos with stars/last-commit data; a follow-up could use the GitHub API (mcp__github tools) to pull metadata for named candidates.

## Red flags in code and repos

### Takeaway
Red flags concentrate in dependencies, install scripts, key handling and outbound network calls.

### Cited Findings
- Dependency fetched from an external URL rather than the npm registry (crypto-layout-utils case) — crypto-economy/SlowMist summary above
- Code reading `.env` or `id.json` and sending content out; hardcoded Telegram bot tokens/chat IDs; passing raw private key strings through `bs58.decode()` into wrapped functions; outbound calls to Telegram Bot API — Socket/Security Affairs and SlowMist summaries above
- Package asks user to paste a private key into a "profit" MEV bot (solana-mev-bot) — JFrog snippet
- Fake repos have high stars/forks that look inflated (zldp2002 case) — SlowMist summary

### Inferences
- [UNVERIFIED but standard practice] Also check: npm `preinstall`/`postinstall` scripts, `eval`/`Function`/base64/hex-obfuscated blobs, `child_process`, git-URL or tarball dependencies, lockfile `resolved` hosts outside registry.npmjs.org, typosquatted package names, brand-new accounts, single-commit history, stars far above issues/forks/commit activity, README pushing a Telegram/Discord "premium" version, and "fee wallet" hardcoded in transaction construction (dev-fee drains are a softer scam).

### Gaps
- No quantitative data on fake-star prevalence for Solana bot repos.

## How to safely evaluate before running

### Takeaway
Never run it with a real key on your main machine: read first, install with scripts disabled, then run only in an isolated VM/container with a burner wallet and network egress limited.

### Cited Findings
- SlowMist guidance: treat any bot requesting a private key as high risk, review dependencies, and rotate credentials if exposed — crypto-economy summary above
- Defensive reviewers suggest grepping builds for Telegram Bot API calls — Security Affairs/Socket snippet

### Inferences
- [UNVERIFIED, general practice] Checklist: (1) check account age, commit history, contributors, issues, releases; (2) read package.json/Cargo.toml/requirements for odd sources; (3) `npm ci --ignore-scripts` / `pip download` and inspect, use socket.dev, `npm audit`, OSV (note OSV has MAL- entries such as MAL-2026-5338 per search listing) and `cargo audit`; (4) grep for fetch/axios/requests/http/telegram/webhook/eval/exec/readFile on .env/id.json/keypair; (5) run in a disposable VM with no access to ~/.config/solana, browser profiles, SSH keys; (6) burner wallet funded with a trivial amount, never the main key; (7) egress allowlist to your RPC only, and watch traffic with mitmproxy/tcpdump; (8) pin dependency versions and hashes; (9) prefer building your own thin bot on official SDKs, or hardware/session-key limited signing; (10) if a key was ever pasted, treat as burned and move funds.

### Gaps
- Did not verify tool-specific commands or current Socket/OSV features this session.
