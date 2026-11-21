# Backtest memecoinów na publicznych danych

Dane (nieskomitowane, pobrane do scratchpada sesji): ian05012/solana-memecoin-dataset (GMGN, czerwiec 2026),
Erin-Blockchain/solana-pumpfun-launches (28k startów, lip–wrz 2026), Smurfetc/solana-memecoin-calls-dataset (13k calli).

Skrypty: backtest.py (symulacja ścieżki na świecach 15m), filters.py (reguły + LightGBM, podział czasowy),
rules.py, robust.py (wrażliwość progów), other_datasets.py. Wyniki w out/.

Wnioski etapu 1: bez filtra wszystkie strategie wyjścia tracą 17–34%/transakcję (CI95 < 0).
Pozorny zysk reguły „mało bundlerów/insiderów + płynność ≥10k” pochodzi wyłącznie z rekordów,
gdzie liquidity_usd > 0,6 × market_cap (fizycznie mało prawdopodobne) — podejrzenie look-ahead.
