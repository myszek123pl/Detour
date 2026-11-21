# Reguły tradingowe: kryteria oceny zamrożone przed końcem replay

Stan procedury: 21 listopada 2026, 16:26:22 UTC. Kryteria poniżej określono przed odczytem końcowych agregatów dużego replay. Publikacja wyników nie oznacza, że dane były wcześniej całkowicie niewidziane przez projekt.

## Zamrożony wybór

- Jedna para reguła wyjścia–poziom wejścia dla opóźnienia 1 s, wybierana wyłącznie na okresie treningowym.
- Co najmniej 300 wykonanych i 300 rozstrzygniętych pozycji oraz co najmniej 90% rozstrzygniętych wśród wykonanych.
- Najwyższa średnia rozstrzygniętych zwrotów na treningu; przy remisie niższy poziom i identyfikator reguły.
- Trening wyklucza sygnały, których pełny horyzont plus dwa maksymalne opóźnienia wykraczają poza granicę treningu. Dla horyzontu 3600 s i maksymalnego opóźnienia 30 s wykluczenie obejmuje ostatnie 3660 s przed 8 lipca 00:00 UTC.
- Brak przejścia bramki oznacza brak zakwalifikowanej reguły. Najlepsza średnia przy niskim pokryciu może być pokazana wyłącznie jako diagnostyka błędu selekcji.

Przedziały bootstrapu losują całe dni UTC, nie niezależne transakcje. To nadal przedziały warunkowe dla widocznych wyjść, nie oszacowanie pełnego PnL przy informacyjnym cenzurowaniu. Niewiele dni testu ogranicza znaczenie tych przedziałów.

Filtry ustalone bez strojenia na wynikach testu: brak wcześniejszej sprzedaży twórcy, co najmniej ośmiu kupujących, udział trzech największych kupujących poniżej 70%, co najmniej 60% zakupów w ostatnich 60 s i kompletność obserwowanych kwot SOL. Udział zakupów portfeli nie jest udziałem w podaży tokena. Brakujące cechy pozostają jawne; lewy join nie usuwa niewykonanych ani cenzurowanych pozycji.

## Niezależny październik: źródło pozornego zysku

W pliku `october_summary.csv` reguła trailing 20%, uzbrojenie 1,3x, wejście przy 10% krzywej i opóźnienie 1 s daje średnio **+14,68%** przy modelu wymagającym dalszych transakcji. Wynik obejmuje tylko **2589 z 6101** wykonanych wejść; **3512** pozostaje nierozstrzygniętych.

Jawna analiza wrażliwości, zakładająca stały ostatni stan krzywej do końca kompletnego dnia ledgerowego, obejmuje **6034 z 6104** wejść i daje **−17,84%**. Nie jest to czysta interwencja na identycznej próbie: również trzy wejścia różnią się między modelami. Analiza nie gwarantuje ceny realizacji ani nie dowodzi, że przyszły bot uzyska takie wykonanie. Pokazuje natomiast, że warunkowanie na dalszej aktywności tokena może radykalnie zmienić znak mierzonego wyniku.

Październik obejmuje jeden dzień, a reguły były ustalone przed jego testem. Nie daje niezależnych dni do wnioskowania o trwałości przewagi. Pełna ocena i jej ograniczenia w notatce39.

## Wyniki pełnego replay

Zweryfikowano wszystkie **219 327 tokenów** i **16,272,480** wyników scenariuszy. To warianty reguł i opóźnień, nie niezależne transakcje portfela.

Bramkę liczebności i pokrycia przeszło **27 z 224** par poziom–wyjście na treningu.

### coverage_gate_training_selection: br_sl0.85_tp1.25, poziom 50%

| Okres i opóźnienie | Sygnały | Wejścia | Rozstrzygnięte | Nieznane | Średnia widocznych | Scenariusz braków −100% |
|---|---:|---:|---:|---:|---:|---:|
| train_lat1 | 1580 | 1561 | 1508 | 53 | -4.19% | -7.44% |
| train_lat5 | 1580 | 1552 | 1483 | 69 | -4.41% | -8.66% |
| train_lat30 | 1580 | 1519 | 1333 | 186 | -9.87% | -20.90% |
| test_lat1 | 2085 | 2075 | 2050 | 25 | -3.89% | -5.05% |
| test_lat5 | 2085 | 2073 | 2016 | 57 | -4.21% | -6.84% |
| test_lat30 | 2085 | 2042 | 1848 | 194 | -6.97% | -15.81% |

Test 1 s: 6 dni z rozstrzygniętymi pozycjami, w tym 0 dodatnich. Warunkowy bootstrap dni: [-5.22%; -2.23%].
Średnia po usunięciu największego dodatniego wyniku: -3.93%; po pięciu: -4.07%.
Na wspólnej próbie 1843 rozstrzygniętych zdarzeń średnie dla 1/5/30 s wynoszą odpowiednio -1.99%/-1.68%/-7.10%. To wynik warunkowej wspólnej próby.

### resolved_only_diagnostic_NOT_qualified: trail0.1_arm2.0, poziom 20%

| Okres i opóźnienie | Sygnały | Wejścia | Rozstrzygnięte | Nieznane | Średnia widocznych | Scenariusz braków −100% |
|---|---:|---:|---:|---:|---:|---:|
| train_lat1 | 29324 | 26215 | 1117 | 25098 | 83.39% | -92.19% |
| train_lat5 | 29324 | 23146 | 1083 | 22063 | 81.06% | -91.53% |
| train_lat30 | 29324 | 18854 | 912 | 17942 | 72.03% | -91.68% |
| test_lat1 | 5690 | 5685 | 1498 | 4187 | 87.44% | -50.61% |
| test_lat5 | 5690 | 5679 | 1358 | 4321 | 84.95% | -55.77% |
| test_lat30 | 5690 | 5613 | 1022 | 4591 | 83.40% | -66.61% |

Test 1 s: 6 dni z rozstrzygniętymi pozycjami, w tym 6 dodatnich. Warunkowy bootstrap dni: [85.95%; 89.63%].
Średnia po usunięciu największego dodatniego wyniku: 87.25%; po pięciu: 86.69%.
Na wspólnej próbie 867 rozstrzygniętych zdarzeń średnie dla 1/5/30 s wynoszą odpowiednio 94.04%/92.70%/87.35%. To wynik warunkowej wspólnej próby.

### Filtry wejścia

Wyniki zamrożonych filtrów są w `strategy_review_filters.csv`. Każdy ma osobno liczebność, brak cech, brak wykonania i cenzurowanie. Nie wybieramy najlepszego filtra po wyniku testu. Predykcje modelu graduacji nie są filtrem live: obecny plik ma je wyłącznie dla retrospektywnie kwalifikowanych okien etykiet.

### Decyzja badawcza

Dodatnia średnia widocznych wyjść i jej bootstrap nie identyfikują wyniku wszystkich pozycji. Scenariusz −100% dla nierozstrzygniętych jest analizą wrażliwości, nie ścisłą dolną granicą. Retrospektywna selekcja jakości kohorty dodatkowo uniemożliwia proste potraktowanie jej jako filtra działającego przy starcie tokena.

Październikowy test wcześniej ustalonych reguł nie potwierdził dodatniej przewagi w modelu pokrycia całego dnia. Żadnej reguły nie kwalifikujemy tutaj do handlu realnym kapitałem. Dalszy kandydat wymaga prospektywnego paper replay z pełnym rejestrem wszystkich sygnałów, prób i zamknięć; kolejnego progu nie należy dobierać na tym samym teście.

Reprodukcja: `python backtest/big/b20_strategy_review.py SCRATCH --out backtest/out/big`. Manifest i checkpointy muszą potwierdzać pełną kohortę.
