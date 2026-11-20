# Self-hosted Solana RPC node (Agave/Firedancer/Jito-Solana) vs paid providers for a trading bot (as of Nov 2026)

Method note: 3 web searches done; WebFetch failed (chainstack.com and cherryservers.com did not resolve in this session's network allowlist), so only search-result summaries were available. Nearly all sources are vendor marketing. Figures are marked UNVERIFIED where they come from vendors or from no cited source.

## 1. Hardware requirements and monthly cost of self-hosting

### Takeaway
Self-hosting a production Solana RPC node realistically means dedicated bare metal in the ~$1,200-2,000+/month range (vendor estimate), with 32c/64t-class CPUs and very large RAM. No official Anza RPC spec was found, so numbers are provider-sourced.

### Cited Findings
- Solana Foundation (June 2026) recommends dedicated bare metal for production validators over AWS/GCP/containers, saying operator control of NIC, core pinning and kernel helps meet the 100M CU target — [Solana Foundation](https://solana.com/news/why-solana-validators-run-on-bare-metal)
- Cherry Servers lists validator at 24c/48t @2.8GHz+ and RPC node at 32c/64t; RPC hardware should exceed validator minimums; a single RPC node under heavy getProgramAccounts load can use hundreds of GB RAM (vendor claim, UNVERIFIED) — [Cherry Servers validator HW](https://www.cherryservers.com/blog/solana-validator-hardware-requirements)
- Agave guidance: accounts and ledger should be on separate disks; storage requirements described as similar for Agave and Firedancer (vendor-summarized, UNVERIFIED) — [Cherry Servers](https://www.cherryservers.com/blog/solana-node-cost)
- Cherry Servers cost table: ~$400-700/mo testnet/small validator, ~$700-1,200/mo production validator, ~$1,200-2,000+/mo large validators/RPC operators (vendor, UNVERIFIED) — [Cherry Servers](https://www.cherryservers.com/blog/solana-node-cost)
- Velia: European bare-metal validator $800-1,200/mo depending on CPU, storage, connectivity; claims bare metal is 60-70% cheaper than comparable cloud at scale (vendor claim, UNVERIFIED) — [Velia](https://www.velia.net/blog/solana-validator-server-requirements-2026/)
- Solana Compass profile: Cherry "Large RPC" config (Threadripper PRO 7975WX, 768 GB RAM) ~EUR 1,249/mo, entry ~EUR 877/mo; may be stale — [Solana Compass](https://solanacompass.com/projects/cherry-servers)

### Inferences
- A trading-grade full RPC (not just a validator-lite) lands around EUR 900-1,500/mo hardware before staff time, i.e. roughly $1k-2k/mo.

### Gaps
- No official Anza/Firedancer RPC hardware page retrieved; exact RAM/NVMe/ledger-size figures unverified.
- Bandwidth/egress requirements (commonly cited as multi-Gbps, ~hundreds of TB/month for full RPC) — no citable source found.
- Firedancer vs Agave vs Jito-Solana status/RPC-suitability in Nov 2026 — not found (Firedancer RPC-serving maturity unverified).

## 2. Bare-metal providers (Latitude, Cherry Servers, TeraSwitch)

### Takeaway
Cherry Servers has published Solana-oriented pricing and PNI with TeraSwitch; Latitude.sh and TeraSwitch plan prices were not found. Latitude and TeraSwitch host a large share of validator stake, which matters for co-location.

### Cited Findings
- Cherry Servers has a private interconnect with TeraSwitch in Amsterdam and Frankfurt, claiming ~0.1 ms latency to Jito infrastructure in Amsterdam; also direct links to Jito and AllNodes in Amsterdam, Frankfurt, Chicago (vendor claim, UNVERIFIED) — [Cherry PNI post](https://www.cherryservers.com/blog/pni-with-teraswitch)
- Chainstack, citing Helius data (Aug 2025): Latitude.sh hosts ~19% of Solana validators by stake, behind TeraSwitch; Cherry ~8.45%, OVHcloud ~8.65% (third-party, dated) — [Chainstack](https://chainstack.com/best-blockchain-infrastructure-providers-2026/)
- Cherry offers customizable bare metal plus pre-configured Solana validator/RPC setups — [Cherry Solana servers](https://www.cherryservers.com/solana-servers)

### Inferences
- Co-locating where stake and leaders concentrate (TeraSwitch/Latitude facilities, Amsterdam/Frankfurt/Chicago/etc.) gives low latency to leaders, but this is the same footprint paid providers use.

### Gaps
- Latitude.sh and TeraSwitch pricing: not found. Data-center-by-city leader density: not found.

## 3. Staked connections (SWQoS) and latency gains

### Takeaway
Self-hosting alone does not give staked transaction-landing; SWQoS requires peering the RPC with a staked validator, so a self-hosted bot still needs paid stake access (or own stake), which erodes the self-host advantage for sending. Self-hosting mainly helps reads/streams (local gRPC/shreds).

### Cited Findings
- SWQoS works when a trusted RPC node peers with a staked validator; stake belongs to the block-producing validator, not the RPC server — [RPC Fast](https://rpcfast.com/blog/solana-swqos-staked-connections)
- Plain JSON-RPC sendTransaction goes via gossip/TPU and is lossy under congestion; priority fees only reorder what the leader already sees, while SWQoS raises odds the leader sees the tx — [RPC Fast](https://rpcfast.com/blog/solana-swqos-staked-connections); [Chainstack](https://chainstack.com/learn/compare/solana-rpc-hft-market-making-providers-2026/)
- Chainstack argues a 40 ms provider using gossip can underperform an 80 ms one with a staked path (vendor argument) — [Chainstack](https://chainstack.com/learn/compare/solana-rpc-hft-market-making-providers-2026/)
- Helius sells staked connections as standalone endpoint; Triton One, Syndica are other Solana-first providers — [Helius](https://www.helius.dev/staked-connections); [DEV roundup](https://dev.to/crypto_blog/solana-rpc-providers-the-full-2025-list-how-to-choose-benchmark-and-ship-with-confidence-224a)
- "Up to 99% landing" claim is a vendor figure, UNVERIFIED — [Helius/RPC Fast pages above]

### Inferences
- Best-practice hybrid: own node for low-latency reads/Yellowstone gRPC + paid staked/Jito-bundle senders for writes.

### Gaps
- No independent benchmarks of self-hosted vs provider latency or landing rate; no millisecond gain figure found.

## 4. Maintenance burden and when it pays off

### Takeaway
Not sourced quantitatively. Direction: self-hosting pays off only for high-volume/latency-critical bots; otherwise paid plans are cheaper once ops time is counted.

### Cited Findings
- Cherry cost range for RPC operators (~$1.2-2k+/mo) vs paid provider plans: provider pricing not retrieved in this session — see section 1 source.

### Inferences (UNVERIFIED, from general knowledge, not from fetched sources)
- Typical dedicated/gRPC provider plans are of order hundreds to ~$1-2k/mo, so self-hosting ($1.2-2k+/mo plus engineer time, upgrades each Agave/Firedancer release, snapshot catch-up, disk wear) breaks even mainly when you need unrestricted request volume, custom indexes, or co-located streaming, or run several bots sharing the node.
- Catch-up lag and downtime after restarts are the main operational risk for a bot.

### Gaps
- Engineer-hours/month, uptime data, provider price comparisons and break-even thresholds: no citable source found (WebFetch blocked for chainstack.com and cherryservers.com; may need allowlisting).
