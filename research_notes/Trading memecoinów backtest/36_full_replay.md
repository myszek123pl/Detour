# Replay reguł na pełnej przygotowanej kohorcie

Stan obliczeń: **zakończony 21 listopada 2026**, kod zakończenia 0. Przeliczono wszystkie 219 327 tokenów przygotowanej kohorty, 169 505 momentów sygnału i 16 272 480 ocen reguła–opóźnienie–sygnał. Zapisano 439 checkpointów; przebieg z ładowaniem danych trwał 646,469 s. Końcowy `replay_v2_manifest.json` jest dostępny. Hasze kodu symulatora i runnera po zakończeniu nadal zgadzają się z konfiguracją przebiegu.

## Końcowe liczebności i przykład wyniku

Każdy moment sygnału jest sprawdzany przy 32 wyjściach. Dlatego liczba kompletnych wyników poniżej dotyczy ocen reguł, a liczba wejść — unikalnych decyzji poziom–token dla danego opóźnienia.

| Opóźnienie | Sygnały | Wejścia z rozpoznanym wykonaniem | Brak wykonania | Kompletne wyniki ocen reguł | Cenzurowane oceny reguł |
|---|---:|---:|---:|---:|---:|
| 1 s | 169 505 | 165 418 | 4 087 | 2 443 245 | 2 850 131 |
| 5 s | 169 505 | 160 631 | 8 874 | 2 123 083 | 3 017 109 |
| 30 s | 169 505 | 146 668 | 22 837 | 1 297 677 | 3 395 699 |

Zadeklarowany przykład, nie zwycięzca wybrany po wyniku: wejście przy 10% krzywej, stop przy 0,7 ceny bazowej, take-profit przy 1,5, maksymalnie godzina, późniejszy okres testowy. Przy 1 s rozpoznano 6741 z 7442 wykonanych pozycji, a średni kompletny wynik wyniósł **−11,43%**. Przy 5 s było to 5515 z 7431 i **−10,67%**; przy 30 s 3078 z 7261 i **−7,66%**. Zmiana średniej przy spadającym pokryciu **nie oznacza**, że większe opóźnienie poprawia strategię: skład rozpoznanej próby jest inny.

Scenariusz zastępujący cenzurowane pozycje stratą 100% daje dla tego przykładu odpowiednio −19,77%, −33,70% i −60,85%. To ilustracja wrażliwości, nie odzyskany rzeczywisty wynik ani dolna granica. Wnioski o wyborze reguły, rozkładzie dziennym i parach opóźnień wymagają dodatkowej analizy zapisanych wyników; sama średnia po odrzuceniu braków nie uzasadnia tradingu.

## Zamrożony eksperyment

Skrypt `backtest/big/b15_replay.py` odtwarza 32 specyfikacje wyjść ze starszego `b06_rules.py`: trzymanie, 12 kombinacji stop/take-profit, 12 trailing stopów, trzy drabinki i cztery wyjścia czasowe. Każda reguła ma teraz jawny maksymalny horyzont 3600 s; `hold` oznacza więc trzymanie maksymalnie godzinę. Krótsze limity 30/120/600 s zachowano.

Sygnał to pierwsze zaobserwowane przekroczenie 5, 10, 20, 30, 40, 50 lub 60% standardowej krzywej. Pomijamy przypadek, gdy już pierwszy zapis przekracza próg o ponad 3 punkty procentowe. Te same momenty decyzji są sprawdzane przy opóźnieniu wejścia i wyjścia 1, 5 oraz 30 s. Łącznie to 672 warianty poziom–opóźnienie–wyjście, nie 672 niezależne eksperymenty.

Pozycja wynosi 1 SOL; prowizja scenariuszowa 1,25% na stronę, napiwek 0,004285714 SOL za transakcję. Opłata kupna jest naliczana ponad kwotę trafiającą do krzywej: przy budżecie `X` kwota netto to `X/(1+fee)`. To zadeklarowany scenariusz kosztów, nie potwierdzona historyczna taryfa każdego tokena. Opłata puli po migracji w modelu jest odrębnym założeniem odziedziczonym z `simlib`.

## Dane i granice interpretacji

Wejście obejmuje wszystkie 219 327 tokenów przygotowanej kohorty i 16 217 167 stanów, bez próbkowania podczas końcowego przebiegu. Przed tym krokiem przeliczono cały surowy korpus 33 581 765 rekordów. Kryteria jakości opisuje `preparation.json`; wykorzystują pełną ścieżkę, więc nie są filtrem możliwym do zastosowania na żywo. Wyniku tej kohorty nie wolno utożsamiać z wynikiem wszystkich startów pump.fun.

Zlecenia korzystają z poprawionego `simlib`: dokładny zegar limitu czasu, serializacja częściowych sprzedaży i cenzurowanie końca pokrycia. Domyślne dopuszczalne zestarzenie stanu wynosi 30 s. Brak rozpoznanego wykonania daje `no_fill`; brak kompletnego wyniku po wejściu daje `NaN` i powód cenzurowania. Nie zamieniamy ich na zerowy zwrot ani potwierdzoną stratę. Późniejsze snapshoty nie mogą wyceniać wcześniejszego zlecenia.

Wpływ własnej pozycji jest kontrfaktycznym przybliżeniem przy utrzymaniu pozostałego przepływu. Kolejność kolektora nie jest zweryfikowaną kolejnością slotów/instrukcji. Brakuje pełnego modelu awarii własnych zleceń, sandwichów, sieci i ograniczeń jednoczesnego kapitału. Wynik pojedynczych okazji nie jest stopą zwrotu portfela.

## Raportowanie bez zgubienia niewiadomych

`replay_v2_summary.csv` pokazuje oddzielnie liczbę sygnałów, wejść z rozpoznanym wykonaniem, braków wykonania, kompletnych wyników i pozycji cenzurowanych. Średnia i mediana dotyczą wyłącznie rozpoznanych wyników. Kolumna `missing_minus100pct_scenario` ilustruje zastąpienie każdej cenzurowanej pozycji stratą 100%; nie jest estymatą ani matematyczną dolną granicą, bo koszty dodatkowych wyjść mogą powiększyć stratę.

`replay_v2_daily.csv` zachowuje sumy i liczebności dzienne do kontroli skupienia wyników i bootstrapu blokami czasu. `replay_v2_reasons.csv` zachowuje powody nierozstrzygnięcia. Surowe wyniki po tokenie, poziomie, opóźnieniu i regule są poza repozytorium, w `SCRATCH/work/replay_v2/parts`. Checkpointy co 500 tokenów umożliwiają wznowienie; konfiguracja odrzuca zmianę haszy kodu albo wejść.

Podział jest według czasu decyzji: przed 8 lipca — trening; 8 lipca 00:00–12:00 UTC — embargo; później — okres testowy. To przekrój czasowy, nie nietknięty holdout: wcześniejsze analizy projektu mogły już widzieć ten okres. Przy porównaniu opóźnień należy dodatkowo użyć par tych samych okazji z kompletnym wynikiem przy wszystkich trzech opóźnieniach. Porównanie samych średnich marginalnych miesza efekt opóźnienia ze zmianą składu próby.

## Odtworzenie

Wymagane: Python, NumPy, pandas, DuckDB i PyArrow. Po pobraniu przypiętej rewizji korpusu i uruchomieniu `b00_audit.py` oraz `b00_prepare.py`:

```text
python backtest/big/b15_replay.py SCRATCH --output backtest/out/big --tag replay_v2
```

Pełny przebieg uruchomiono po testach naprawionego symulatora. Test kontrolny runnera obejmuje zachowanie wszystkich mianowników, granice podziału czasowego i 32 zamrożone specyfikacje. Wynik pozytywnego testu kodu nie jest dowodem przewagi strategii.
