# Backtest memecoinów: podsumowanie

Szczegóły w `research_notes/Trading memecoinów backtest/` i kodzie w `backtest/`.

## Wyniki na prawdziwych danych (9 684 tokeny, czerwiec 2026, świece 15m)
- Bez filtra każda strategia wyjścia traci 17–34% na transakcję (CI95 < 0) przy pozycji 200 USD.
- Pozorny zysk +24–33% z reguł „mało bundlerów/insiderów + płynność” okazał się błędem danych:
  zamrożona kapitalizacja i ucięte serie świec. Na wiarygodnych cechach: −27,5% [−33; −21].
- Model ML poza próbą: najlepsze 5% → +9%, ale CI od −1,5% do +19,6% (brak pewności).
- Moment wejścia (godzina, dzień, wiek tokena) nie daje przewagi. Działają tylko wykluczenia:
  mała płynność, przewaga sprzedających, łapanie spadków >50%.

## Logi prawdziwych botów z GitHuba
- Prawie wszystkie uczciwe wyniki z kosztami są ujemne (np. −8,7%/transakcję na 1 431 transakcjach).
- Stopy na pump.fun przeskakują: stop −18% realizował się średnio przy −84%.
- Kopiowanie portfeli: −22% do −38% poza próbą; kopia top-20 Kolscan: ok. −23% przy 2 s opóźnienia.
- Jedyny zyskowny bot: 938 tys. USD w 111 dni, wejście w tej samej sekundzie co start tokena,
  pozycja ok. 180 USD trzymana ok. 6 s. Nie do powtórzenia z domowym opóźnieniem.

## Mechanika
- pump.fun to gra o sumie ujemnej: suma wyników = −opłaty − SOL uwięziony w puli.
- Po ~55 SOL na krzywej podwojenie ceny na krzywej jest niemożliwe; zrzut 10% podaży na puli = −55% ceny.

## Wniosek
Brak zmierzonej przewagi dla tradera z zewnątrz. Jeśli próbować: tylko filtry wykluczające,
tryb papierowy, mikrokwoty, tysiące transakcji przed oceną, twarde limity strat.

## Co dalej
Najlepsze dane (Hugging Face: 33,6 mln transakcji; Zenodo RED-PUMP) wymagają odblokowania hostów:
huggingface.co, hf.co, cdn-lfs.huggingface.co, cas-bridge.xethub.hf.co, zenodo.org.
