# Wallet labeling sources for Solana and EVM (CEX hot wallets, Arkham, Nansen, Solscan, open datasets, sanctions)

NOTE: Search budget was effectively exhausted (4 of 5 searches rate-limited / 5-hour limit hit). Only the sanctions item is source-backed. Everything marked [UNVERIFIED] comes from model background knowledge (cutoff mid-2026) and must be checked against vendor pages before use. Prices and tiers especially change often.

## 1. Which label sources exist, their coverage, and access/pricing?

### Takeaway
Only the sanctions-list part was verified: OFAC address lists are free and machine-readable via OFAC itself and community GitHub extractors. Commercial label providers (Arkham, Nansen, Solscan, Dune) are described from background knowledge only; confirm current pricing and API terms.

### Cited Findings
- 0xB10C/ofac-sanctioned-digital-currency-addresses parses OFAC's official SDN XML and outputs TXT/JSON per asset, regenerated nightly by GitHub Actions on a `lists` branch; MIT licence, Python; repo last pushed March 2025 per an aggregator — [GitHub](https://github.com/0xB10C/ofac-sanctioned-digital-currency-addresses), [aggregator metadata](https://awesome.ecosyste.ms/projects/github.com%2F0xb10c%2Fofac-sanctioned-digital-currency-addresses)
- Forks/related: sambacha/ofac-list (ETH focus), vile/ofac-sdn-list (JSON/TOML/CSV/TXT, daily 6AM UTC check) — [sambacha](https://github.com/sambacha/ofac-list), [vile](https://awesome.ecosyste.ms/projects/github.com%2Fvile%2Fofac-sdn-list)
- OFAC says SDN data is downloadable in multiple formats, and designated addresses sit in a "Digital Currency Address" field; Treasury lists are not exhaustive — [OFAC FAQ 562/563 index](https://ofac.treasury.gov/faqs/563)
- Tornado Cash addresses were delisted by OFAC in March 2025, so cached/old lists may wrongly include them — [OFAC recent action 2025-03-21](https://ofac.treasury.gov/recent-actions/20250321) (via search result snippet; verify content)

### Unverified background (not sourced)
- [UNVERIFIED] Arkham: free web UI with entity labels and de-anonymisation of CEXs/funds/protocols; deposit vs hot vs cold wallet distinctions for major CEXs; supports Solana and EVM chains; API access historically invite/limited and not clearly priced; Arkham's ARKM token tied to its Intel Exchange (bounties for labels).
- [UNVERIFIED] Nansen: paid; 500M+ labelled addresses claimed, "Smart Money", fund, CEX labels; Solana support added 2024-25; tiers roughly from ~$100-150/mo (Pioneer/Professional) to enterprise, API priced separately (credits). Check pricing page.
- [UNVERIFIED] Solscan (Etherscan family): free account tags/labels (e.g. "Binance 1", "Coinbase", programs); Pro API plans paid; label lookups via account metadata endpoints. Solana FM: similar free labels and API with free tier.
- [UNVERIFIED] Dune: `labels` schema / `labels.addresses` (Spellbook, community-contributed incl. CEX, cex_evms, cex_solana-style tables); free to query within Dune credit limits. Open GitHub sets: brianleect/etherscan-labels (scraped, EVM), eth-labels (dawsbot), Flipside/other label exports, Solana token-list/`solana-labels`-style community lists (names uncertain).

### Inferences
- A practical stack: free (Dune labels, Solscan/Etherscan tags, Arkham UI, OFAC lists) for a bot MVP; paid Nansen/Arkham API only if scale or Smart Money flags are needed.

### Gaps
- Current (Nov 2026) pricing/API terms for Arkham, Nansen, Solscan Pro, Solana FM, Dune not verified (search blocked).
- Exact coverage numbers per chain not verified.
- Chainalysis free sanctions oracle / TRM / Elliptic not covered.

## 2. How to use labels for funding-source tracing (e.g. fresh wallet funded from Binance hot wallet)?

### Takeaway
Method (background, [UNVERIFIED] as to specifics): take the wallet's first inbound SOL/native transfer(s), resolve the sender via label DB; if sender is a known CEX hot wallet, tag as "CEX-funded"; if unlabelled, hop up 1-3 levels while flagging fan-out/fan-in patterns.

### Cited Findings
- None sourced beyond OFAC use (screening addresses against SDN list) — [OFAC FAQ](https://ofac.treasury.gov/faqs/563)

### Inferences
- Algorithm: (1) fetch first N incoming transfers via RPC/Helius/Solscan API; (2) lookup sender in label table; (3) classify: CEX hot / CEX deposit / bridge / mixer / sanctioned / unknown; (4) cluster wallets sharing same funder within short time window (sniper/sybil clusters); (5) score: many fresh wallets funded from same unlabelled parent within minutes = coordinated insider/bundler cluster; CEX funding is weak signal (withdrawal addresses are shared by thousands of users) and mostly useful to exclude clusters, not to link wallets.
- For CEXs, withdraw from hot wallet is shared so do not cluster on it; deposit addresses (per-user) sweeping into hot wallets are the linking signal on the deposit side.
- Sanctioned/mixer hit should be a hard filter for compliance and as a risk flag.

### Gaps
- No sourced guidance on CEX-withdrawal timing heuristics or on rate limits of label APIs.

## 3. Accuracy issues and building your own label DB

### Takeaway
Labels are probabilistic and decay; build a versioned DB with provenance and confidence per row. (All background; [UNVERIFIED].)

### Cited Findings
- Tornado Cash delisting (Mar 2025) shows sanctions lists change; stale snapshots mislead — [OFAC](https://ofac.treasury.gov/recent-actions/20250321)
- OFAC lists are acknowledged as not exhaustive — [OFAC FAQ](https://ofac.treasury.gov/faqs/563)

### Inferences
- Schema suggestion: (chain, address, entity, type[cex_hot/cex_deposit/bridge/dex/mixer/sanctioned/mm/fund], source, confidence, first_seen, last_verified, evidence_url). Ingest: OFAC nightly lists, Dune labels exports, Solscan/Etherscan tags, exchange proof-of-reserves address disclosures, own heuristics (address sweeping to known hot wallet = deposit address; high-degree hub with symmetrical in/out = exchange/MM).
- Known accuracy pitfalls (general): scraped Etherscan labels are stale; same entity rotates hot wallets; EVM addresses are shared across chains but not always same owner (contracts, smart wallets); label of a deposit address can mislead if CEX reassigns; Solana token-account vs owner-wallet confusion (label the owner wallet, not ATA); Arkham/Nansen heuristics can mislabel and are not ground truth.
- Re-verify periodically; expire labels not seen active in N months.

### Gaps
- No verified data on error rates of any commercial provider.
- Licence terms for redistributing scraped labels not checked.
