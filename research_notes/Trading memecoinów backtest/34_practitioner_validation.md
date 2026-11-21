# Wood i Satsdats: audyt możliwości testu na pełnym korpusie

Stan: 21 listopada 2026. To **wykonany audyt pokrycia danych**, nie wynik strategii ani ocena zysków tych osób. Obliczenia dotyczą rewizji `bd8aed6452fb81665a74e6c308323f2c825dc82a` zbioru [jocry/Pumpfun_Memecoin_Corpus](https://huggingface.co/datasets/jocry/Pumpfun_Memecoin_Corpus). Skrypt: `backtest/practitioners/coverage_audit.py`; pełne liczebności, progi i SHA-256 użytych plików: `backtest/out/practitioners/coverage_audit.json`.

## 1. Co właściwie testujemy

Wood, według redakcyjnego opisu AMA, rozważa token dopiero po co najmniej 48 godzinach od startu, jeżeli utrzymuje siłę i ma widoczną społeczność. Satsdats wskazuje kapitalizację 5–10 mln USD oraz wychodzenie przy utracie 9-EMA na wykresie godzinnym. To deklarowane procesy uznaniowe, nie kompletne algorytmy. Źródła są opisami odcinków, a nie zweryfikowanymi historiami transakcji: [Wood, FOMO](https://fomo.family/blog/memecoins/notanicecat69-memecoin-trading-strategy), [Satsdats, FOMO](https://fomo.family/blog/trading-strategies/satsdats-crypto-trading-blowups-onchain-strategy).

Własne rozstrzygnięcie metodologiczne: reguła wieku, kapitalizacji lub EMA nie odtwarza samodzielnie doboru społeczności, narracji, informacji z prywatnej grupy ani rozmiaru i sposobu wykonania pozycji. Wynik takiego automatu należałoby nazwać testem określonego proxy. Brak przewagi na świeżych tokenach z poprzednich notatek nie rozstrzyga wyniku późniejszych wejść.

## 2. Co jest naprawdę dostępne

Odczytano lokalne pliki `tokens.parquet`, `postgard_snapshots.parquet`, `postgard_outcomes.parquet` i `migrations.parquet`. Nie zastąpiono cen wykonania etykietą końcową ani maksymalną kapitalizacją. Otrzymano:

| Wielkość | Odczyt z plików |
|---|---:|
| Wszystkie tokeny / unikalne minty | 798 430 / 798 430 |
| Tokeny z `graduated_at` | 5 689 |
| Tokeny Mayhem | 109 561 |
| Snapshoty po migracji / unikalne minty | 1 392 133 / 5 701 |
| Minty ze snapshotów, które dają się połączyć z tabelą tokenów | 5 697 |
| Minty z prawidłową ceną według warunku audytu | 5 689 |
| Minty z prawidłową ceną w wieku co najmniej 72 h | 123 |
| Minty z prawidłową ceną w wieku co najmniej 9 dni | 16 |

„Prawidłowa” oznacza tutaj wyłącznie `price_usd > 0`, `incomplete_data = false` i czas snapshotu nie wcześniejszy niż zapisane `graduated_at`. Nie stanowi niezależnej walidacji ceny dostawcy ani możliwości sprzedaży. Wiek liczony jest od `detected_at`, ponieważ ten eksport nie zawiera osobnego, zweryfikowanego on-chain czasu utworzenia. Jest to **wiek od wykrycia**, nie potwierdzony wiek od startu.

Ograniczenia eksportu są jawnie udokumentowane w [KNOWN_ISSUES.md](https://huggingface.co/datasets/jocry/Pumpfun_Memecoin_Corpus/blob/bd8aed6452fb81665a74e6c308323f2c825dc82a/KNOWN_ISSUES.md). Użyte w audycie liczby pochodzą z naszego odczytu plików, nie z opisu marketingowego zbioru.

## 3. Wood: po 48 godzinach zostaje mała i ucięta próba

Ustalono z góry okno możliwego wejścia: pierwsze 30 minut po ukończeniu 48 h od wykrycia. Wynik:

| Warunek | Tokeny |
|---|---:|
| Jakikolwiek snapshot od wieku 48 h | 769 |
| Prawidłowa cena od wieku 48 h | 768 |
| Prawidłowa cena w oknie 48 h–48 h 30 min | 661 |
| Powyższe, dodatkowo dodatnia płynność i dodatni `volume_1h` | 268 |
| Z tych 268: jakakolwiek późniejsza prawidłowa cena co najmniej 24 h po pierwszym kandydacie wejścia | 15 |

Ostatni warunek to tylko konieczny test dostępności późniejszej ceny, nie kompletność ścieżki między wejściem i wyjściem. Nie oznacza, że 253 tokeny umarły lub przyniosły stratę. Nie można odróżnić braku dalszej obserwacji od zakończenia handlu wyłącznie na podstawie uciętej serii.

Nie wykonano średniej stopy zwrotu na 15 kompletniejszych rekordach. Selekcja próby warunkiem późniejszej dostępności mogłaby usunąć niewygodne wyniki; pozostawienie urwanych ścieżek po ostatniej cenie mogłoby je z kolei sztucznie polepszyć. Obie decyzje wymagałyby jawnego modelu cenzurowania i testów wrażliwości. Snapshoty obejmują przede wszystkim tokeny po migracji, więc nie reprezentują wszystkich tokenów żywych po 48 h. „Widoczna społeczność” oraz „siła” nie mają tutaj ustalonej miary ani historii.

**Werdykt:** korpus pozwala policzyć ograniczone pokrycie wejścia po 48 h, ale nie uzasadnia wniosku, że przetestowaliśmy strategię Wooda.

## 4. Satsdats: dziewięć tokenów w wymaganej kapitalizacji

Warunek korzysta z zaobserwowanego w danym snapshocie `market_cap_usd`, nie z płynności, FDV ani szczytu znanego po fakcie. W całym pliku istnieją tylko **223 snapshoty dziewięciu tokenów** z kapitalizacją 5–10 mln USD. Wszystkie dziewięć ma przynajmniej jeden taki snapshot z dodatnią ceną, płynnością i `volume_1h`.

Dla pierwszego zaobserwowanego spełnienia warunku przez każdy token sprawdzono dostępność dziewięciu kolejnych, już zakończonych godzin przed decyzją:

- **3 z 9** ma jakąkolwiek prawidłową obserwację w każdej z dziewięciu godzin.
- **0 z 9** ma komplet dziewięciu godzin z ostatnią obserwacją nie starszą niż pięć minut przed końcem godziny.

Pięciominutowa tolerancja jest jawnym, konserwatywnym warunkiem tego audytu. Nie jest regułą Satsdatsa. Nawet spełnienie jej dałoby jedynie proxy zamknięć godzinnych: dokładna EMA wymaga zdefiniowania inicjalizacji i odpowiednio długiej wcześniejszej historii. Dziewięć godzin to minimalny sprawdzany warunek, nie gwarancja pełnego rozgrzania EMA.

Pierwsze wejścia w próg przypadają na siedem dni: 30 czerwca (2 tokeny), 1 lipca (1), 4 lipca (1), 6 lipca (1), 7 lipca (1), 8 lipca (2), 14 lipca (1). Nie dobierano podziału trening/test tak, aby poprawić wynik. Tak mała próba, dodatkowo z brakami cen, nie daje podstaw do wiarygodnej oceny poza próbą ani do testowania opóźnień 1/5/30 s na snapshotach.

**Werdykt:** nie oszacowano P&L ani skuteczności EMA. Dane nie zamykają wymaganej luki.

## 5. Co trzeba poprawić w dotychczasowym szkielecie

Własny przegląd istniejących skryptów ujawnił kwestie, które należy rozwiązać przed ich użyciem:

1. `p01_universe.py` wybiera tylko tokeny po graduacji ze znalezioną parą, po czym łączy próbę losową U z osobnym, nadpróbkowanym segmentem H wysokiej wczesnej kapitalizacji. Nie wolno raportować nieważonej średniej U+H jako wyniku całego rynku. Wejściowe pliki i katalogi wskazują starą sesję.
2. `plib.py` używa czasu graduacji jako początku wieku. Dwa dni po graduacji mogą przypadać znacznie później niż dwa dni po starcie. `SUPPLY=1e9` nie obejmuje Mayhem z podażą 2 mld; do progu kapitalizacji należy użyć aktualnej, punktowej wartości i sprawdzonej podaży.
3. Ten sam plik uzupełnia brakujące godziny ostatnią ceną i zakłada płynność jako stałą część kapitalizacji. Pusta godzina nie dowodzi, że można było zrealizować zlecenie po zachowanej cenie. Takie wyniki to scenariusz modelowy, nie odtworzone wykonania.
4. `p02_fetch.py` pobiera świece godzinne. Nawet poprawne OHLCV nie odtwarza różnic wejścia o 1, 5 i 30 s. Potrzebne są transakcje lub dostatecznie częste, oznaczone czasem stany pul oraz opłaty i reguła wykonania.
5. `run_filters.py` testuje wczesne świece 15-minutowe, a nie strategię wieku 48 h lub wejścia 5–10 mln. Flag holderów i insiderów nie wolno przenieść jako punktowych sygnałów bez weryfikacji czasu ich wyznaczenia.

Nie zmieniono tych plików: brakuje ich historycznych wejść z poprzedniej sesji, a niniejszy etap ustala możliwość rzetelnego testu. Reprodukowalny audyt nie zależy od tych ścieżek ani od ich silnika symulacji.

## 6. Warunki następnego rzeczywistego testu

Potrzebna jest zamrożona kohorta premier z czasem utworzenia, niezależną obserwacją przeżycia oraz cenami i płynnością przez co najmniej 48 h przed wejściem i ustalony horyzont po nim. Do EMA: kompletna historia godzinnych zamknięć, jawny sposób inicjalizacji oraz decyzja dopiero po zamknięciu świecy; do wykonania: transakcje lub stany rezerw po decyzji. Do reguły Wooda trzeba osobno zdefiniować i zamrozić mierniki siły i społeczności. Kryteriów nie dobieramy po obejrzeniu zwrotów.

Następnie chronologiczny podział po dacie możliwego wejścia, kontrola nakładających się horyzontów i wspólnych twórców, zachowanie martwych/nieobserwowanych tokenów, jawne koszty, oddzielne opóźnienia oraz analiza koncentracji wyniku. Do tej chwili poprawne stwierdzenie brzmi: **wcześniejszy wynik na nowych tokenach nie testuje tych dwóch strategii; pełny korpus nadal ma za mało odpowiedniego pokrycia, żeby rozstrzygnąć ich skuteczność.**

## Reprodukcja i kontrola

```text
python backtest/practitioners/coverage_audit.py --data-dir <lokalny_katalog_jocry> --output backtest/out/practitioners/coverage_audit.json
```

Uruchomiono na czterech plikach o sumach zapisanych w wyniku. DuckDB 2.0.1, strefa UTC, bez próbkowania, bez użycia końcowych etykiet do wyboru kandydatów wejścia. Skrypt nie liczy żadnej stopy zwrotu. Sprawdzono jego kompilację i zgodność liczebności z odczytem tabel; pozostałe ograniczenia odnoszą się do danych i definicji strategii.
