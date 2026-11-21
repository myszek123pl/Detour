# Cechy wejścia: niewielka informacja ponad stan krzywej

Analiza własna z 21 listopada 2026. Reprodukcja: `python backtest/big/b16_entry_features.py SCRATCH --out-dir backtest/out/big`. Zbiór: `jocry/Pumpfun_Memecoin_Corpus`, rewizja `bd8aed6452fb81665a74e6c308323f2c825dc82a`. Małe wyniki: `backtest/out/big/entry_features_summary.json` oraz `entry_features_rates.csv`.

**Wynik:** pełny model zachowania osiąga AUC 0,8054, lecz sama krzywa już 0,7986. Większość rozróżniania pochodzi z poziomu zaawansowania tokena. Na wczesnym poziomie 5% model zachowania ma AUC 0,524, a zamrożony próg selekcji daje niższą częstość etykiety sukcesu niż cała grupa. To nie jest gotowy sygnał zakupu ani wynik PnL.

## Co rzeczywiście policzono

Przejrzano wszystkie 219 327 tokenów przygotowanej kohorty jakościowej. Po odnalezieniu pierwszego przekroczenia poziomów 5%, 10%, 20%, 30%, 40%, 50% i 60% krzywej powstało **169 505 zdarzeń**. Wyłączono 110 379 przypadków token–poziom, w których już pierwszy dostępny stan przekraczał dany próg o więcej niż 3 punkty procentowe; sześć tokenów miało mniej niż dwa stany przed końcem fazy krzywej. Pozostałe brakujące zdarzenia oznaczają nieosiągnięte poziomy. Jeden token może dostarczyć kilka skorelowanych sygnałów, często z tej samej transakcji; liczba zdarzeń nie jest liczbą niezależnych inwestycji.

Kohorta została wybrana na podstawie jakości **całych** ścieżek: niestandardowe tokeny, flagi koncentracji, kompletność rezerw i zgodność z inwariantem. Taka retrospektywna selekcja nie jest filtrem możliwym do zastosowania na żywo. Wynik nie obejmuje wszystkich 798 430 startów ani wszystkich 33,58 mln transakcji.

Predyktory używają wyłącznie prefiksu ścieżki do decyzji włącznie: rzeczywistego postępu krzywej, wieku od `detected_at`, liczby zakupów i sprzedających, liczby unikalnych kupujących, przepływu SOL, koncentracji sum zakupów, wcześniejszych sprzedaży twórcy, historii twórcy z wcześniejszych startów i graduacji oraz tempa zmiany stanu. `detected_at` to czas detekcji kolektora, nie zweryfikowany on-chain czas utworzenia.

Nie używano `dev_pct`, `snipe_delta`, flag trybu cashback ani gotowych wskaźników holderów jako danych znanych przy decyzji. Historia twórcy obejmuje tylko wcześniejsze zdarzenia z korpusu w oknie 30 dni. Początek korpusu ucina historię i może zmieniać rozkład tej cechy.

## Braki nie są zerami

Kwotowe cechy z okna mają `NaN`, gdy dowolna objęta nimi transakcja ma brakującą lub odrzuconą kwotę. Nie zamieniamy braków na zerowy przepływ. Koncentracja sum zakupów nie jest koncentracją podaży u holderów; sprzedaże i transfery mogą zmieniać ekspozycję.

Przy 19,32% zdarzeń nie da się obliczyć wiarygodnej koncentracji sum zakupów. Brak przepływu SOL z ostatnich 60 s dotyczy 0,106% zdarzeń. Cechę liczby snajperów z pierwszych 3 s dopuszczono tylko przy pierwszym zapisie nie później niż 1 s od detekcji; **91,91% sygnałów nie spełnia tego warunku**. Ten materiał nie wspiera powszechnego filtrowania startów na podstawie kompletnej obserwacji pierwszych trzech sekund.

Adres wykluczany według dokumentacji dostawcy oraz brakujące identyfikatory nie są liczone jako uczestnicy rynku. Jego tożsamości nie potwierdzono niezależnie; nazwa `is_sys` w przygotowanych danych jest historyczna. Wszystkie identyfikatory twórców w tej kohorcie były dostępne.

## Etykieta i uczciwy podział czasu

Celem jest **odnotowana przez dostawcę graduacja w ciągu 24 h po sygnale**. Brak takiej etykiety nie jest niezależnie potwierdzonym brakiem migracji, śmiercią tokena ani utratą kapitału. Przewidywanie tej etykiety nie wycenia wejścia lub wyjścia.

Trening obejmuje tylko sygnały tokenów wykrytych przed 8 lipca 00:00 UTC, których całe 24-godzinne okno wyniku kończy się przed tą granicą. Test obejmuje tokeny wykryte od 8 lipca 12:00 UTC. Wyłączono okna przecinające brakujące dni 3 i 12 lipca, niedojrzałe przy końcu korpusu lub przekraczające planowane 48 h śledzenia od detekcji. Planowane śledzenie nie dowodzi rzeczywistej ciągłości kolektora.

| Próba | Zdarzenia | Tokeny | Dodatnie etykiety w zdarzeniach | Częstość |
|---|---:|---:|---:|---:|
| Trening | 124 429 | 85 238 | 1 137 | 0,914% |
| Test | 19 158 | 9 831 | 1 239 | 6,467% |

Wśród wszystkich sygnałów 7 193 nie spełnia dojrzałości etykiety, a 6 900 przecina lukę kolektora; przyczyny mogą się nakładać. Pozostałe wyłączenia wynikają z granicy treningu, embargo i zakazu mieszania tokenów między próbami. Test ma tylko **cztery dni startów**: 8, 9, 10 i 13 lipca. Zmiana częstości etykiety między próbami może wynikać ze zmiany pokrycia i składu kohorty; sama nie dowodzi zmiany rynku.

To późniejszy okres w tym samym wcześniej eksplorowanym zbiorze, nie niezależny, nienaruszony eksperyment prospektywny.

## Wartość informacji ponad krzywą

Wszystkie trzy modele mają ten sam z góry ustalony typ i pojemność: histogramowy gradient boosting, głębokość 3, 120 iteracji, minimalny liść 200. Nie strojono parametrów na teście. Próg selekcji ustala się z rozkładu wyników treningowych; nie wybiera się najlepszych kilku procent po obejrzeniu etykiet testu.

| Model | AUC trening | AUC test | Average precision test | Brier test | Log loss test |
|---|---:|---:|---:|---:|---:|
| Poziom i rzeczywisty stan krzywej | 0,8902 | 0,7986 | 0,2121 | 0,05490 | 0,21587 |
| Krzywa i tempo | 0,9049 | 0,8019 | 0,2335 | 0,05481 | 0,21619 |
| Pełne zachowanie | 0,9257 | 0,8054 | 0,2361 | 0,05437 | 0,21161 |

Przyrost AUC pełnego modelu ponad krzywą to **0,0069**, a ponad krzywą z tempem 0,0035. Przedziały bootstrapu po dniu startu są szerokie i oparte tylko na czterech blokach: AUC krzywy 0,786–0,836, pełny model 0,798–0,830. Ich nakładanie nie jest formalnym testem różnicy; potrzebny jest sparowany test oraz dalszy okres. Kalibracja pełnego modelu na teście ma nachylenie 0,618 zamiast idealnego 1: skrajnych ocen nie wolno traktować jako dobrze skalibrowanych prawdopodobieństw.

Rozbicie według tego samego poziomu krzywej pokazuje, ile znika z pozornie wysokiego globalnego AUC:

| Poziom | Zdarzenia test | Etykieta 24 h | AUC samej krzywej | AUC zachowania |
|---|---:|---:|---:|---:|
| 5% | 4 332 | 1,062% | 0,431 | 0,524 |
| 10% | 4 757 | 1,640% | 0,447 | 0,564 |
| 20% | 3 604 | 4,162% | 0,559 | 0,574 |
| 30% | 2 459 | 8,093% | 0,504 | 0,596 |
| 40% | 1 778 | 13,386% | 0,576 | 0,607 |
| 50% | 1 306 | 20,291% | 0,558 | 0,614 |
| 60% | 922 | 28,525% | 0,564 | 0,661 |

Wyższa częstość graduacji blisko końca krzywej nie jest darmową przewagą: cena wejścia jest już wyższa, do możliwej migracji zostaje mniej wzrostu, a wykonanie może się nie udać. Tę zależność musi rozstrzygnąć osobny replay netto.

## Reguły praktyczne i ich ograniczenia

Prosta reguła „twórca ma wcześniejszą graduację” ma w treningu 2,884% etykiet wobec 0,914% bazowo, lecz w teście **6,569% wobec 6,467%**. Silny treningowy lift prawie znika. Wybór wyłącznie na podstawie tej historii nie ma tu mocnego uzasadnienia.

Próg pełnego modelu równy 90. percentylowi treningu **wewnątrz poziomu 5%** przepuszcza 1 072 sygnały testowe. Ich częstość etykiety to 0,746% wobec 1,062% całej grupy, lift **0,70**. Na poziomie 60% taki próg daje 52 sygnały i 38,46% wobec 28,52%, lift 1,35; to tylko 52 zależne od selekcji obserwacje, bez wyniku kosztów. Podwyższanie progów po obejrzeniu tych wyników byłoby kolejnym dopasowaniem.

Filtry „co najmniej 10 kupujących”, „top-3 poniżej 70% sumy zakupów” czy dodatni przepływ mają wyższą częstość etykiety w zbiorczej próbie, ale mieszają poziomy, wiek i tempo tokenów. Nie są samodzielnym dowodem dodatkowego sygnału. W szczególności wyższy udział zakupów nie oznacza automatycznie lepszego wyniku; grupa z co najmniej 80% zakupów ma w teście mniej etykiet niż cała próba.

**Kandydat do falsyfikacji**, nie rekomendacja: porównywać model i prostą regułę zawsze przy tym samym poziomie wejścia, z progiem zamrożonym przed nowymi danymi. Dla pierwszego nowego okresu nie zmieniać progów; mierzyć wszystkie sygnały, nieudane wejścia, cenzurowane wyjścia, opłaty i wpływ największych zwycięzców. Odrzucić hipotezę przewagi, jeśli poprawa etykiety nie przechodzi w dodatni wynik netto na opóźnieniach 1, 5 i 30 s. Reguły wczesnego wejścia na 5% nie otrzymują tu potwierdzenia.

## Łączenie z replay i reprodukcja

Lokalne pliki poza Git:

- `SCRATCH/work/entry_features.parquet`: klucz `(mid, lv)`, `decision_t`, `L`, cechy, etykiety i flagi `label24_mature`, `label24_gap_free`, `split`.
- `SCRATCH/work/entry_features_predictions.parquet`: ten sam klucz, `decision_t`, podział i `p_curve_only`, `p_curve_and_pace`, `p_behavior_extended` dla treningu/testu. Wyłączone rekordy mają brak predykcji.

Przy łączeniu trzeba sprawdzić zgodność `decision_t`. Podział dojrzałych etykiet z tej notatki **nie jest** podziałem populacji wykonań w replay; nie wolno przez join niejawnie usunąć wszystkich strat lub cenzurowanych transakcji. Wymagany jest lewy join i jawne mianowniki.

Kontrola syntetyczna potwierdziła, że zmiana transakcji po sygnale nie zmienia jego cech; brak kwoty nie tworzy zerowego przepływu lub sztucznie niskiej koncentracji. Osiągnięta trafność dotyczy etykiet kolektora. W tej analizie nie wyliczano PnL i nie uznano żadnego modelu za gotową strategię handlową.
