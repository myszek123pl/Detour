# Pełne publikacje o graduacji manipulacji i copy tradingu

Stan wersji sprawdzony 21 listopada 2026. Podstawą są pełne teksty HTML arXiv, obejmujące metody, wyniki, tabele i dodatki, a nie fragmenty wyszukiwarki. Poniżej odróżniamy wynik autorów od naszej oceny jego przydatności do backtestu. Nie jest to niezależna replikacja obliczeń publikacji.

Najważniejsze rozróżnienie: przewidywanie migracji, ograniczenie strat i dodatnia stopa zwrotu to trzy różne zadania. Literatura dostarcza sygnałów do testowania, lecz sama klasyfikacja tokena lub portfela nie zastępuje odtworzenia wejścia i wyjścia.

## Przewidywanie graduacji na pump.fun

Marino, Naviglio, Tarantelli i Lillo, **2602.14860v1**, 16 lutego 2026. Kohorta: nowe tokeny z września 2025; sukces oznacza osiągnięcie progu krzywej, nie późniejszy zysk. Autorzy podają 655 770 tokenów i 4 338 graduacji. Ich iloraz wynosi **0,662%** (obliczenie własne), choć tekst podaje około 0,63%. [Pełny tekst, rozdziały IV–IX](https://arxiv.org/html/2602.14860v1).

Stan krzywej i liczba transakcji do pierwszego przekroczenia progu różnicują prawdopodobieństwo graduacji. Bot oznacza tutaj sposób wywołania programu, nie potwierdzoną tożsamość operatora. Portfele i twórców wybiera się w pierwszej połowie miesiąca, a sprawdza w drugiej. Niektóre „najlepsze” portfele wyłącznie sprzedają: wpływy SOL nie dowodzą odtwarzalnego wyniku samofinansującego się tradera. [VII](https://arxiv.org/html/2602.14860v1#S7).

Breakeven `P(graduacja) > (vSOL/115)^2` pomija gaz, prowizje i wykonanie dużej pozycji. Autorzy zakładają stratę całości przy braku graduacji. To punkt odniesienia, nie realistyczny backtest. Rozdział o top-10 twórcach opisuje przekroczenie breakeven przy małej próbie, natomiast konkluzja neguje poprawę względem baseline: tej niespójności nie rozstrzygamy. [VI–VII, IX](https://arxiv.org/html/2602.14860v1).

**Wniosek audytu:** testować tempo akumulacji przy tym samym stanie krzywej. Nie przenosić krzywej prawdopodobieństwa bezpośrednio na oczekiwany PnL; zweryfikować mianowniki i kalibrację na nowym okresie.

## MemeTrans zmienił nazwę na MELT

Hu, Tekin, Xu i Liu, **2602.13480v2**, 21 maja 2026: aktualny tytuł to *MELT: A Behavioral Trace Dataset for High-Risk Memecoin Launch Detection*. Zbiór obejmuje **41 470 wyłącznie migrujących tokenów**, z okresu grudzień 2024 – marzec 2025, oraz 218,53 mln transakcji. Nie opisuje pełnego uniwersum startów. [Pełny tekst, 3](https://arxiv.org/html/2602.13480v2#S3).

Etykieta ryzyka łączy minimum ceny z pierwszych 20 minut po migracji i ręczną ocenę manipulacji. Cechy pochodzą sprzed migracji; wspólne finansowanie i identyfikatory Jito wspierają grupowanie portfeli. Eksperyment usuwa tokeny z fazą sprzedaży poniżej minuty lub mniej niż 100 holderami. Pozostaje 21 635 tokenów. Podział według czasu utworzenia: 70/30; strojenie obejmuje pięciokrotną walidację na treningu. [3.3–4.1](https://arxiv.org/html/2602.13480v2).

Tabela 10: przy top-100 MLP zmniejsza stratę z **60,71% do 26,64%**. Symulacja kupuje po cenie migracji i losuje 100 chwil sprzedaży w następnej godzinie; nie odtwarza opóźnionych zleceń z rezerw. Redukcja strat nie oznacza dodatniego zwrotu. [4.4, tabela 10](https://arxiv.org/html/2602.13480v2#S4.SS4).

**Wniosek audytu:** materiał wspiera filtr ryzyka po migracji. Użycie ukończonych cech przed migracją byłoby wyciekiem przyszłości; przed wykorzystaniem grup portfeli trzeba też ustalić moment dostępności ich powiązań.

## Boty manipulacyjne i kopiowanie portfeli

Luo, Feng, Xu i Liu, **2601.08641v3**, 5 lutego 2026; arXiv podaje publikację WWW 2026. Wersja obejmuje **6 000 projektów**; przykład to pierwsze wejście pary portfel–token, etykieta oznacza znak zrealizowanego wyniku. Podział chronologiczny wynosi 70/15/15. [Wersja i metody](https://arxiv.org/abs/2601.08641), [4–5](https://arxiv.org/html/2601.08641v3).

Detektory bundle/sniper korzystają z kolejności bloków; bump z powtarzanych przeciwnych transakcji; komentarze klasyfikuje LLM. To heurystyki, a nie niezależnie potwierdzone etykiety właścicieli. Trzy agenty oceniają portfel, token i moment wejścia. Autorzy raportują około **14% dla lidera i 3% dla kopiującego**; najwyższe AUC osiąga XGBoost, nie system agentowy. [4.3, 5.2–5.3](https://arxiv.org/html/2601.08641v3).

Model ekonomiczny kopiuje natychmiast tę samą liczbę tokenów po transakcji lidera. Dowód dodatniej kary za kopiowanie dotyczy tego modelu. Wzory nie zawierają jawnych taryf opłat ani opóźnień; brak testu 1/5/30 sekund i czasu wnioskowania LLM. Określenie „realistic market frictions” nie wystarcza do odtworzenia kosztów. [5.3 i A.6](https://arxiv.org/html/2601.08641v3).

**Wniosek audytu:** +3% to dodatni wynik konkretnej symulacji, nie potwierdzenie zysku wdrożonego bota. Replikacja wymaga danych wejściowych, reguł selekcji oraz pełnej specyfikacji wykonania. Nie należy też utożsamiać kolejnego zakupu po liderze z zakupem za identyczny budżet SOL.

## A Midsummer Meme’s Dream

Mongardini i Mei, **2507.01963v2**, 2 stycznia 2026. Początkowa lista z agregatorów zawiera 34 988 tokenów. Po ograniczeniu do czterech sieci i kontroli adresów pozostaje 31 811; porównanie cen październik 2024 – styczeń 2025 obejmuje 20 327. Analiza wysokich zwrotów dotyczy **707 tokenów ze wzrostem ponad 100%**, nie wszystkich premier pump.fun. [Pełny tekst, 3–4](https://arxiv.org/html/2507.01963v2).

W tej wybranej grupie autorzy znajdują 586 tokenów z przynajmniej jednym wskaźnikiem podejrzanej aktywności: **82,89%** według 586/707, wobec 82,8% w abstrakcie. Wskaźnik łączy wash trading, inflację ceny przy niskiej płynności i anomalie koncentracji. Nie oznacza 82,8% prawnie lub przyczynowo dowiedzionych oszustw. [5.1–5.4](https://arxiv.org/html/2507.01963v2#S5).

Heurystyki dziennych OHLCV są uzupełniane transakcjami; późniejsze pump-and-dump bada się na danych godzinowych. Praca jest analizą opisową, bez treningowego/testowego portfela i symulacji opóźnionej egzekucji. Kwota ponad 9,3 mln USD łączy zrealizowane straty pump-and-dump z utraconym kapitałem pozostałych holderów przy rug pullach; to różne reguły rachunkowe. [6.4](https://arxiv.org/html/2507.01963v2#S6.SS4).

**Wniosek audytu:** wzrost na wykresie przy małej płynności nie jest możliwym do zrealizowania zwrotem. Wynik jest argumentem za sprawdzaniem rezerw i koncentracji, bez przenoszenia częstości z wyselekcjonowanych zwycięzców na całą populację.

## Co nauka rzeczywiście wspiera

Wspólny kierunek badań jest użyteczny operacyjnie: znaczenie ma stan rynku w momencie decyzji, rzeczywista koncentracja ekspozycji i kolejność transakcji. Ocena samej ceny, liczby portfeli albo trafności klasyfikacji pozostawia niewycenione ryzyko wykonania.

Żadna z tych czterech publikacji nie ustanawia uniwersalnej, powtarzalnej przewagi dla nowego tradera pump.fun przy opóźnieniach 1, 5 i 30 sekund. To ograniczenie zakresu dowodów, a nie dowód niemożliwości zarabiania. W szczególności dodatnia symulacja jednej strategii nie potwierdza wszystkich strategii, a nieudana strategia ich wszystkich nie obala.

Do uznania przewagi w tym projekcie potrzebujemy jednocześnie:

1. Cech i etykiet z określonym momentem dostępności; rozdzielenia niewidzianego wyniku od potwierdzonej porażki.
2. Zamrożenia reguły przed testem w późniejszym okresie i kontroli wspólnych tokenów, portfeli oraz epizodów rynkowych między próbami.
3. Symulacji rezerw w kolejności transakcji, z wejściem i wyjściem po opóźnieniu, opłatami, nieudanymi zleceniami oraz końcem obserwacji.
4. Wyników netto, niepewności liczonej po blokach czasu, udziału największych zwycięzców w PnL i oddzielnego testu nowych danych.

To kryteria naszego audytu. Same te publikacje ich łącznie nie weryfikują; pełny backtest pozostaje osobnym eksperymentem.
