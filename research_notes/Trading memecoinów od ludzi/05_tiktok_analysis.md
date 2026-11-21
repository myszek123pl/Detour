# 05 - Analiza 9 filmów TikTok (przesłanych przez użytkownika)

Data analizy: 2026-11-21. Tylko publiczne materiały twórców. Notatka faktograficzna, nie porada inwestycyjna.

## 0. Najważniejsze ustalenia

1. **Nie jest to konto @batmanzkatowic i nie ma tu ani jednego wideo o futures MNQ.** Z 9 linków: 6 pobrano (wszystkie to memecoiny/Solana, 6 różnych autorów), 3 się nie udały. Zrzut ekranu z MNQ (1 min, ok. 1:3,5 R:R, +1936,5 USD) NIE pochodzi z żadnego z pobranych filmów - jeśli jest od @batmanzkatowic, jego filmów w tej paczce nie ma lub są wśród 3 niedostępnych (wg przekierowań te 3 to jednak @0xnevsky, @nexus_trades, @trading.calls - czyli też nie on).
2. Żaden pobrany film nie opisuje powtarzalnych reguł strategii (wejście/stop/wyjście/rozmiar pozycji). Są to: screen rejestrowane z "pompy", reklama narzędzia, pokaz bota (z reklamą), emocjonalne reakcje, kompilacje wygranych.
3. Pięć z sześciu filmów zawiera reklamę/ref link/CTA; żaden nie pokazuje strat w sposób reprezentatywny (jedyne straty to pojedyncze pozycje wewnątrz zwycięskiego "dnia").
4. Wyniki typu "+1129%" czy "x19,74" to pojedyncze transakcje wybrane post factum - to nie jest dowód edge'u.

## 1. Status pobierania

| # | Link | Autor (z metadanych) | Status |
|---|------|---------------------|--------|
| 1 | vm.tiktok.com/ZN8mD2hc3 | @baxsiomemcoins | OK (97 s) |
| 2 | vm.tiktok.com/ZN8mDL6kr | @0xnevsky (wideo 7705463162627263777) | BŁĄD yt-dlp: "Video not available, status code 10231" (nie blokada hosta - strona tiktok.com i CDN działają; film niedostępny dla yt-dlp, możliwe ograniczenie regionalne/usunięty/prywatny) |
| 3 | vm.tiktok.com/ZN8mDRaDe | @0xnevsky | OK (28 s) |
| 4 | vm.tiktok.com/ZN8mAEegm | @nexus_trades (to jest *photo post* 7685304304311323912) | BŁĄD: "Unsupported URL" - yt-dlp nie obsługuje postów ze zdjęciami (karuzela); wymaga ręcznego obejrzenia |
| 5 | vm.tiktok.com/ZN8mD8fEd | @trading.calls (wideo 7706667502817856790) | BŁĄD yt-dlp: "Video not available, status code 10231" |
| 6 | vm.tiktok.com/ZN8mAvsPf | @fentsolana | OK (25 s) |
| 7 | vm.tiktok.com/ZN8mAvwgu | @lifeofgreen0x | OK (11 s) |
| 8 | vm.tiktok.com/ZN8mDdDEu | @imeon.pl | OK (36 s) |
| 9 | vm.tiktok.com/ZN8mA7EFG | @ahm_ws | OK (35 s) |

Brak błędów typu "host blocked" - żadnego zablokowanego hosta CDN nie zaobserwowano. Pliki: `/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/tiktok/` (numeracja plików v1..v9 odpowiada numerom z tabeli; v2, v4, v5 brak).

Narzędzia: yt-dlp 2026.10.26, faster-whisper (model small, język pl; dekodowanie przez wav z ffmpeg, bo wersja PyAV miała błąd). Transkrypcja Whisper bywa niedokładna (szczególnie wulgaryzmy/slang), a w filmach z muzyką bez mowy zwraca halucynację "Napisy stworzone przez społeczność Amara.org" (= brak mowy).

## 2. Analiza film po filmie

### Film 1 - @baxsiomemcoins (97 s, 51,7 tys. wyświetleń)
- **Pokazano:** Axiom (terminal memecoinów, Solana), wykres w interwale sekundowym/minutowym, pozycja z P&L rosnącym: +351% -> +467% -> +1129% (+1,02K USD) -> chwilowo +1106%/+1082% -> sprzedaż 25% przy +1251% (+1,13K USD). Koszt/baza ok. 90 USD, wartość pozycji do ok. 1,08K USD. Wejście wyglądało na kilka transakcji (znaczniki B/S), brak informacji o instrumencie (nazwa tokena) ani stopie.
- **Powiedziane:** wyłącznie reakcje emocjonalne ("to działa!", "sprzedaj, sprzedaj!", "trzeba dłochać" - tj. "trzymać", "nowa zasada"), po ok. 55 s zmiana tematu na narzekanie na słuchawki (prawdopodobnie sklejone nagranie). Zero reguł strategii.
- **Straty:** nie pokazane.
- **Promocja:** nakładka "axiom.trade/@baxref" na całym filmie (**link referral Axiom**) + opis "DISCORD W BIO" (prowadzenie do społeczności, możliwie płatnej/z refami).
- **Ocena:** pojedyncza wygrana ~x12 na małym kapitale (90 USD) - wybrana do filmu; brak kontekstu.

### Film 2 - @0xnevsky - NIEPOBRANY (video not available).

### Film 3 - @0xnevsky (28 s, 2,1 tys. wyświetleń, 2026-11-20): "New terminal test today #trading #grok #memcoin"
- **Pokazano:** "Grok Bot Terminal" - dashboard bota (Scanner / Rug check / Sizer / Executor / Logger), tryb "paper off - live". Time-lapse: saldo $150 start -> $203,91 (23h) -> $280,97 -> $538,34 (2h32) -> $1306,03 (3h58) -> $2130,96 (5h25) -> $4101,13 (6h51), 87 transakcji, 61 W / 26 L (win rate ok. 70%). Stopka "@0xNevsky".
- **Powiedziane:** brak mowy (muzyka); wg Whisper tylko halucynacja napisów.
- **Straty:** pokazane (np. -57,09 USD, -5,83), ale w kontekście łącznego wzrostu x27 w ~7 h.
- **Promocja:** jawnie brak CTA, ale to materiał lead-gen dla "terminala" (konto X). Wygląda na grafikę/animację dashboardu (stylizowane UI, nierealnie gładkie wyniki: +2700% w 7 h) - **brak weryfikowalnego dowodu on-chain**.
- **Ocena:** nieweryfikowalne. Tempo wzrostu x27 w 7 h przy ~33% kapitału na pozycję i 70% WR jest ekstremalne i niezgodne z typową dystrybucją wyników memecoinów; traktować jako marketing/symulację.

### Film 4 - @nexus_trades - NIEPOBRANY (photo post; yt-dlp nie obsługuje).

### Film 5 - @trading.calls - NIEPOBRANY (video not available).

### Film 6 - @fentsolana (25 s, 23,3 tys.): "dryflip polski poradnik"
- **Pokazano:** rozszerzenie przeglądarki **DryFlip** (paper trading memecoinów na prawdziwych cenach, działa na Axiom/GMGN/DexScreener; ustawiasz saldo np. 3 SOL). Ekran przeglądarki Chrome Web Store, panel "Portfel i Transakcje".
- **Powiedziane (PL):** "Chcesz spróbować sił w memecoinach, ale boisz się wpłacić prawdziwe pieniądze? ... fejkowy portfel prosto na akcjomie (Axiom) ... bez podpinania portfela, bez ryzyka. Jest darmowa ... Obserwuj po więcej!"
- **Straty/wyniki:** nie dotyczy (brak wyników).
- **Promocja:** promocja darmowego narzędzia + CTA "obserwuj"; brak widocznego refa. Ciekawe z perspektywy badawczej: paper trading to sensowny sposób testu strategii (ale uwaga: paper trading nie modeluje poślizgu, MEV/sniperów, opłat priorytetowych, rugów - zawyża wyniki).

### Film 7 - @lifeofgreen0x (11 s, 201,6 tys. wyświetleń, 22,5 tys. polubień): "you have no idea"
- **Pokazano:** screen z terminala (Axiom/Padre-podobny), gwałtowne pompy świeczek (tokeny EKM, KEKIUS, CALI?, kilkadziesiąt znaczników zakupów/sprzedaży), napis "Memecoins are dead" (ironiczne). Pokazane wejścia jako gęste kropki na pionowej świecy - przypuszczalnie snajpowanie/skalpowanie pierwszych sekund po launchu.
- **Powiedziane:** brak mowy.
- **Straty:** brak. Brak wartości P&L czytelnych na klatkach.
- **Promocja:** brak widocznej; zasięg wysoki (engagement ~11%) - typowy "engagement bait".

### Film 8 - @imeon.pl (36 s, 2,2 tys.): "#grokbot #memecoin #solana"
- **Pokazano:** wideo ekranowe terminala (Axiom Pulse + wykres TAO/USD? na launchpadzie), napis "SELLS 75% (1 SOL)", w rogu licznik "+15.2 SOL". Wyniki to kilka SOL zysku.
- **Powiedziane:** brak mowy (muzyka). Hashtag #grokbot sugeruje to samo narzędzie, co w 3 i 9 ("Grok Bot").
- **Straty:** brak.
- **Promocja:** pośrednia (hasztagi bota).

### Film 9 - @ahm_ws (35 s, 134,8 tys. wyświetleń, 11,4 tys. polubień, 2026-11-07): "Good day #success #trading #memecoins #cupsey #kimchi"
- **Pokazano:** aplikacja "Grok Terminal / Grok Bot" w stylu fintech: saldo $44,00 start -> $87,50 (+98,9%) -> kupno JIMMY, sprzedaż JIMMY przy 7,0x (+$418,88, saldo $474,89) -> $868,59 (+1874%, 19,74x) -> ekran "Withdraw $4 872,06". Terminal z logiem Python ("pilot.py --live", budżet $44, rozmiar 40%, stop -6%, "half at 2x, trail 10%") - ma to wyglądać jak realny bot; venue: "fomo.family" (aplikacja społecznościowa z handlem memecoinami).
- **Powiedziane:** tylko okrzyki ("O boże, to jest...") + "dobra, dobra".
- **Straty:** pokazano jedną stratę -2,98 USD (stop -6%) i oznaczono jako część ścieżki - typowy "pokaz" z asymetrią x7 vs -6%.
- **Promocja:** brak CTA w filmie, ale to ten sam format co film 3 - "Grok Bot" jest powielanym memem/trendem u wielu twórców (@0xnevsky, @imeon.pl, @ahm_ws), co wskazuje na koordynowany/viralowy marketing narzędzia lub referów fomo. Czy wideo 3 i 9 to ten sam produkt - nie da się ustalić.
- **Ocena:** wynik x110 (44 -> 4872 USD) w kilka dni; wiarygodność niska/nieweryfikowalna (brak adresu portfela, brak historii on-chain).

## 3. Ocena: czy jest spójna, testowalna strategia?

**Nie w tych materiałach.** Zawierają wyłącznie:
- (a) zrzuty pojedynczych wygranych (film 1, 7, 8),
- (b) pokazy botów z agregowanym wynikiem (3, 9),
- (c) reklamę narzędzia (6).

Jedyne elementy zbliżone do reguł pojawiają się w tekstach z ekranu bota (film 9): wielkość pozycji 40% wolnej gotówki, max 2 pozycje, stop -6%, wyjście połowy na 2x, trailing 10%, filtry płynności (liq >= 41K, wiek 2 min, 8 checków). To są parametry, a nie edge - brak reguły selekcji (co wchodzi i dlaczego), brak liczby transakcji i rozkładu wyników.

### Jakiego R:R i win rate trzeba (wzory)
Próg rentowności (przed kosztami): WR* = 1/(1+R), gdzie R = średnia wygrana / średnia strata.
- R = 1:1 -> WR 50%; R = 1:2 -> 33,3%; **R = 1:3,5 (jak na zrzucie MNQ) -> 22,2%**; R = 1:5 -> 16,7%.
- Oczekiwana wartość E = WR*R - (1-WR) w jednostkach R. Przykład: R=3,5, WR=30% -> E = +0,35R; WR=22,2% -> 0.
- Po kosztach (K w jednostkach R): WR* = (1+K)/(1+R). W memecoinach K jest duże: opłata platformy ~1%, priority fee + Jito tip, poślizg 2-10% na płytkich pulach, podatek tokena; przy stopie -6% i kosztach round-trip np. 3-4% koszt wynosi K ~ 0,5-0,7R -> WR* dla R=3,5 rośnie do ok. 33-38%. Stop -6% przy poślizgu bywa w ogóle niewykonalny (gap, rug -> strata -100%), czyli faktyczny rozkład strat ma gruby ogon, którego "R" nie uwzględnia.
- Statystycznie: aby odróżnić WR 30% od 22% (E=+0,35R vs 0) z istotnością ~95% potrzeba rzędu 250-300+ transakcji; kilkadziesiąt pokazanych transakcji (87 w filmie 3) tego nie rozstrzyga, a przy nieweryfikowalnych danych tym bardziej.

### Sygnały survivorship / selektywnej publikacji
- Pojedyncze wygrane na małym kapitale (90 USD, 44 USD, 150 USD) - łatwo wylosować x10+ przy rozkładzie z grubym ogonem; film jest publikowany tylko po wygranej.
- Brak: liczby prób, pełnego rachunku P&L (np. wg adresu portfela), wszystkich pozycji z dnia, kosztów.
- Nagłówki "Good day", "you have no idea", "Memecoins are dead" - narracja emocjonalna.
- Zasięgi mierzą viralność, nie rentowność: 201 tys. wyświetleń dla 11-sekundowego klipu bez treści.
- Referral/CTA (axiom.trade/@baxref, Discord w bio) - realna zachęta ekonomiczna twórcy do pokazywania wygranych (przychód z prowizji od wolumenu obserwujących, nawet gdy ci tracą).
- Dashboardy botów (film 3, 9) wyglądają na renderowane/nieweryfikowalne, a ich zyski (x27 w 7 h, x110 w kilka dni) są poza realistycznym zakresem dla stabilnego edge'u.

## 4. Przełożenie na memecoiny vs kontrakty na indeksy (MNQ)

- **MNQ (CME):** płynny rynek, stały koszt (ok. 0,5-1,5 USD/kontrakt prowizji + 1 tick poślizgu ~0,5 USD), stop wykonuje się blisko ceny, wyniki historyczne można zbacktestować na danych tickowych. R:R 1:3,5 przy WR 25-35% jest realnym profilem strategii breakout/trend z małym stopem (np. 10-15 pkt). +1936,5 USD przy 2 USD/pkt na 1 MNQ to ok. 968 pkt-kontraktów, czyli np. 10 kontraktów x ok. 97 pkt - kwotę tłumaczy rozmiar pozycji, nie sam R:R 1:3,5. (To wyliczenie orientacyjne; nie mam samego zrzutu w tych materiałach.)
- **Memecoiny:** ujemna asymetria kosztów i ryzyka wykonania: poślizg, MEV/snajperzy, rugi/honeypoty, brak ciągłości cen (stop nie gwarantuje wyjścia), manipulacja wolumenem, informacja asymetryczna (insiderzy, boty KOL). R:R "x7-x19" jest możliwe, ale jest efektem rozkładu z grubym ogonem (większość tokenów -> 0), więc WR jest niska (np. 10-25%), a o wyniku decyduje selekcja i szybkość (infrastruktura), nie "setup" z wykresu. Strategie z MNQ (price action 1 min) nie przenoszą się 1:1; przenosi się jedynie: ustalanie stopu z góry, stała jednostka ryzyka (np. 0,5-1% kapitału), dziennik transakcji i wymóg próby >= 300 transakcji.
- **Co jest testowalne dla memecoinów:** hipoteza + reguła selekcji (np. wejście wg metryk płynności/wieku/portfeli smart money) + reguły wyjścia (np. połowa na 2x, trailing) -> backtest na historycznych danych pul (np. API DexScreener/Birdeye/Bitquery) z modelem poślizgu i opłat; następnie paper trading (np. DryFlip, z zastrzeżeniem o braku modelu poślizgu) i dopiero mały real.

## 5. Rekomendacje dla dalszego researchu
1. Zweryfikować, czy @batmanzkatowic faktycznie jest autorem wideo MNQ; te 9 linków to inni autorzy. Poprosić użytkownika o właściwe linki lub o ręczne pobranie zdjęć/karuzeli z @nexus_trades (nieobsługiwane przez yt-dlp).
2. Dla filmów o futures: szukać jawnie reguł (sesja, setup, stop w punktach, rozmiar), liczby tradeów, wyciągów z konta (prop-firm payouts, Tradovate/NinjaTrader), obecności reklam kursu/prop-firmy/refów.
3. Dla memecoinów z tej paczki: najbardziej wartościowy element to **narzędzie** (DryFlip) i **parametry bota** (stop -6%, half at 2x, trail 10%) jako hipotezy do przetestowania, nie jako dowód skuteczności.

## 6. Transkrypcje (faster-whisper small, pl)

Uwaga: surowe, niezredagowane; liczne błędy rozpoznania (zwłaszcza film 1). Filmy 3, 7, 8 praktycznie bez mowy (halucynacja Whisper).

### v1
[0s] Pocz, co się dzieje? Kurwa!
[2s] O, oj, co się dzieje? Kurwa, nie?
[3s] O kurwa, ty!
[5s] Przed wszystkimi kurwa się wiebałem, nie?
[6s] O Lirus, kurwa, kurwa!
[8s] J-o, pierdule!
[9s] J-o, pierdule!
[10s] Ale czemu to?
[11s] Co tu się oddala?
[12s] Proszę, do góry.
[13s] O kurwa...
[14s] Ja dojęcie kurwa w dół.
[15s] Nie, ja nawet...
[16s] Pogdaj, pogdaj, pogdaj, pogdaj.
[18s] To działa, kurwa! To działa, pa!
[20s] To działa, kurwa! To działa!
[22s] Ty, to działa, to działa!
[24s] To działa, to działa, kurwa!
[26s] Pocz, kurwa!
[27s] Trzeba dłochać, kurwa!
[28s] Nowa zasada, damy, kurwa!
[30s] Trzeba dłochać, kurwa!
[32s] Ci ja pierdule!
[33s] Pocz, ciedziej, kurwa!
[35s] Przedaj, sprzedaj, sprzedaj!
[36s] Sprzedaj, kurwa!
[38s] Sprzedaj, kurwa!
[39s] I opierdule!
[40s] I opierdule!
[41s] Kurwa, kurwa!
[42s] I opierdule!
[43s] Ja dojęcie się jeszcze.
[44s] Ale ty się tu kurwa ruszczy, ty się tu ruszczy.
[46s] A co ty jesteś dziś?
[47s] To jest kurde mocy, kurwa.
[48s] Ja pierdule, ja pierdule!
[50s] Ja brycie wyprowadziły z równowagi.
[52s] Ej, kurwa, przeciąga mnie.
[54s] Jutro, kurwa, wstaję.
[55s] Pierwsze co robię, kurwa.
[56s] Zapierdalam do jebanego media.
[57s] Expert kupuje normalne suchawki bezprzewodowe.
[60s] Ty kupiłem suchaki bezprzewodowe, kurwa.
[62s] Są bez kabla, kurwa, nie?
[64s] Ty trzymarz te kurwy więcej na kablu, kurwa.
[66s] Nishta kablowa jebanym.
[67s] Popierdoli mnie, kurwa, zaraz.
[69s] Teraz one są bezprzewodowe.
[71s] One są bezprzewodowe, co nie?
[72s] A ja je teraz trzęłam, kurwa, na kablu.
[74s] Cza idzie? Cały dzień je kurwa c*** na kablu,
[76s] bo się rozładowują, kurwa.
[77s] Popierdoli mnie.
[78s] Jopierdol...
[79s] Ty co się tu odpierdala?
[80s] Jebany jabry.
[81s] P*** się tu, kurwa.
[82s] Ja pierdole, nie?
[84s] Ty 100%
[85s] Ja pierdole...
[86s] Po co się dzieje, kurwa?
[88s] Po co się dzieje, po co się dzieje, kurwa?
[90s] Ja pierdole...
[91s] Po co się dzieje, po co się dzieje, po co się dzieje?
[93s] Ja pierdole...
[94s] Kurwa, kurwa, kurwa, kurwa, kurwa!
### v3
[0s] Napisy stworzone przez społeczność Amara.org
### v6
[0s] Chcesz spróbować sił w MemeCoinach, ale boisz się wpłacić prawdziwe pieniądze?
[4s] Mam na to sposób.
[6s] Ktyczka Drive Flip daje ci fejkowy portfel prosto na akcjomie.
[9s] Ustawiasz saldo, na przykład 3 solany.
[12s] Kupujesz i sprzedajesz po prawdziwych cenach, a twoje wejścia i wejścia lądują na wykresie.
[17s] Bez podpinania portfela bez ryzyka.
[20s] Jest darmowa i działa też na GMGN czy dekscreenerze.
[23s] Obserwuj po więcej!
### v7
[0s] Napisy stworzone przez społeczność Amara.org
### v8
[0s] Napisy stworzone przez społeczność Amara.org
[30s] Napisy stworzone przez społeczność Amara.org
### v9
[0s] O boże...
[2s] To jest...
[11s] O boże, to jest...
[14s] O boże, to jest...
[20s] O boże...
[26s] O boże...
[28s] Dobra, dobra, dobra, dobra.
