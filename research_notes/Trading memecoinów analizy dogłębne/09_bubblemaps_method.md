# Bubblemaps methodology and how to replicate it in a bot

Research status (Nov 2026): only 2 of ~5 searches returned results (the rest hit a rate limit), and WebFetch of wiki.bubblemaps.io and thenextweb.com failed (hosts not in session network allowlist). Most of this file is therefore thin on primary-source detail. Items marked [UNVERIFIED] come from model memory or inference, not from a fetched source. To finish: allow wiki.bubblemaps.io, blog.bubblemaps.io, docs.bubblemaps.io and thenextweb.com, then re-run.

## How are clusters built (transfer links, funding, time windows)?

### Takeaway
Per the official wiki summary, a bubble is a top holder (250 shown), a link is a direct on-chain transfer between two holders, and a cluster is a set of linked holders. Bubblemaps itself calls clusters a prompt for investigation, not proof. Exact thresholds, funding-source logic and time windows were not found in any source I could reach.

### Cited Findings
- Each bubble is a top holder; bigger bubble = larger share; the map shows the 250 top holders — [Bubblemaps wiki, how does it work](https://wiki.bubblemaps.io/bubblemaps-v2/how-does-it-work) (via search snippet)
- A line between two bubbles marks an on-chain transfer between those holders; clicking it shows transferred tokens and the date of the last transfer — same source
- Linked bubbles form clusters, meaning they sent funds to each other; the wiki states clusters are not proof of wrongdoing and gives innocent examples (employer paying employee, VC distributing tokens) — same source
- Magic Nodes: suggested non-holder addresses that act as an intermediate address connecting wallets that would otherwise look unrelated — same source
- Real-world case descriptions imply funding-based grouping: $MYSTERY (May 2026) "90 newly funded wallets bought 90% of supply at launch"; Cupsey allegation of ~30 connected wallets; $NEIRO sellers hid profits via ~400 intermediary wallets — [Cointelegraph via search summary](https://regional-front.cointelegraph.com/news/bubblemaps-flags-mystery-over-90-wallet-launch-sniping-cluster), [Crypto Briefing](https://cryptobriefing.com/bubblemaps-alleges-cupsey-solana-wallet-scheme/)

### Inferences
- Because only holders are nodes, a pure holder-to-holder graph misses wallets that were funded by a shared non-holder source; Magic Nodes exist to patch exactly that gap (1-hop shared intermediary).
- The 250-holder cap means the tool sees only concentrated supply; insiders who split into hundreds of small wallets can fall below the cap.

### Gaps
- Minimum transfer size to draw a link, whether links consider native token (SOL/ETH) funding versus only the token itself, how far back history is scanned, any time-window rule for "bundled" buys: not found. [UNVERIFIED] everything beyond the bullets above.

## Magic Nodes and V2 features

### Takeaway
Magic Nodes are suggested intermediary (non-holder) addresses that reveal hidden connections. V2 specifics (UI, time travel, timeline) were only partly visible.

### Cited Findings
- Magic Nodes definition (above) — [Bubblemaps wiki](https://wiki.bubblemaps.io/bubblemaps-v2/how-does-it-work)
- A "time travel" feature exists for viewing insider activity and rug pulls historically — [Cointelegraph headline](https://cointelegraph.com/news/bubblemaps-time-travel-for-insider-activity-rug-pulls) (headline only, article not read)
- Bubblemaps is positioned as moving "from post-mortem to pre-trade" — [The Next Web headline](https://thenextweb.com/news/bubblemaps-onchain-forensics-pre-trade-rug-pull-risk) (article not read)

### Gaps
- Full V2 feature list, dates, and Magic Node discovery algorithm: not retrieved.

## Insider / bundle scoring added in 2026, and API

### Takeaway
I could not verify any named insider score, bundle score, or API endpoint list. Intel Desk cases do report an "insiders hold X% of supply" figure, which is the closest verified metric.

### Cited Findings
- Reported insider-share figures: $DADDY 30% across 21 wallets (June 2024); $TOES 66% (July 2026), matching $BULLISH pattern (~70%, Nov 2025); $CWU 90% bundled — [Cryptopolitan](https://www.cryptopolitan.com/bubblemaps-pippin-rally-insider-trading/), [Bubblemaps blog](https://blog.bubblemaps.io/presidential-bundles-manipulation-interesting-events/) (via search summary, details not fetched)
- Intel Desk: crowdsourced investigations governed with the BMT token; users vote on priorities — search summary of [Bubblemaps blog](https://blog.bubblemaps.io/bubblemaps-wrap-up-seoul-scandals-memecoin-szn/)
- Bubblemaps is available as a QuickNode add-on/listing ("bubblemaps by bubblemaps team") — [QuickNode](https://www.quicknode.com/nl/builders-guide/tools/bubblemaps-by-bubblemaps-team) (listing only; endpoints not read) [UNVERIFIED as to what it exposes]

### Gaps
- Official API docs (auth, endpoints, rate limits, pricing), the 2026 scoring release, and its formula: not found.

## Documented investigations, accuracy and false positives

### Takeaway
Bubblemaps findings are presented as allegations from on-chain inference. The only explicit accuracy caveat found is the vendor's own: clusters are not proof of identity. No independent accuracy or false-positive rate was found.

### Cited Findings
- Cases: $DADDY (June 2024), $NEIRO (July 2024), Libra and Melania memecoins linked to a single entity — [The Block](https://www.theblock.co/amp/post/341238/bubblemaps-links-single-entity-to-libra-and-melania-memecoins), Cupsey ($1.74M, ~30 wallets), $MYSTERY (May 2026), $TOES (July 2026), $LAB (~95% drop in days), AVA AI sniping, a PEPE launch concentration analysis — Cointelegraph/CryptoSlate links in search results
- Innocent explanations the wiki itself lists (payroll, VC distribution) are the built-in false-positive classes — [Bubblemaps wiki](https://wiki.bubblemaps.io/bubblemaps-v2/how-does-it-work)

### Inferences (false-positive sources, from first principles)
- Exchange hot wallets, market makers, launchpad/bonding-curve and DEX pool accounts, team/vesting contracts, and airdrop distributors will all look like clusters unless labeled and excluded.
- Fresh-wallet sniping can come from genuinely independent users using the same bot/funding hub (e.g. an exchange withdrawal address), producing a false "single entity".
- Counter-evasion: splitting across more than 250 holders, long delays, or mixed funding sources lowers recall.

### Gaps
- No independent audit, precision/recall, or retraction data found.

## How to replicate in a bot (design based on the above; my inference, not Bubblemaps' disclosed method)

1. Holder snapshot: pull top N holders (go beyond 250, e.g. 500-1000) via Helius/RPC `getProgramAccounts`/token-largest-accounts or a holder API; drop known non-user addresses (pool vaults, bonding curve, burn, CEX, program-owned accounts).
2. Edges: (a) direct token transfers between holders; (b) funding edges: first SOL/native funder of each wallet (parse earliest inbound transfer), grouping wallets sharing a funder within a time window.
3. Magic-node step: for each pair of holders, find common non-holder counterparties (shared funder or shared sink); promote an intermediary if it links at least 2 holders, excluding labeled hubs (CEX, routers).
4. Bundle detection: wallets that buy in the same slot or within a few slots of launch/mint, or funded in one batch before launch. Thresholds (slots, SOL amounts) must be tuned empirically.
5. Clusters: connected components (union-find) over weighted edges; require at least 2 independent evidence types before flagging high confidence.
6. Score: cluster supply % (sum of balances), count of wallets, newness of funding (wallet age at first buy), funding concentration, sell-down speed. Report "insider/bundle supply %" analogous to the vendor figures above.
7. Validate: backtest on tokens with known outcomes (the cases above), measure precision against rugs versus organic launches, and keep a whitelist of known hubs.
8. If the official API turns out to be accessible, use it as a cross-check rather than building everything; verify terms and pricing first [UNVERIFIED].
