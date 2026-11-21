# Niezależny dzień październikowy: wykonanie i pozorna przewaga przez cenzurowanie

Stan: 21 listopada 2026. **Wykonano pełny test czterech z góry ustalonych reguł na 19 346 kwalifikujących się tokenach**, bez próbkowania końcowego przebiegu. To osobny dzień z późniejszego okresu niż korpus czerwiec–lipiec. Nie jest wielomiesięczną walidacją ani dowodem możliwości wykonania tych zleceń na giełdzie.

## Źródło, mianowniki i kolejność

Źródło: [pumpdatafun/pump-fun-trades-sample](https://huggingface.co/datasets/pumpdatafun/pump-fun-trades-sample), rewizja `c3a429fcd65f15e9ea1feca8a174e617b7e8f396`. Licencja próbki: CC BY 4.0. Dzień: 15 października 2026 UTC. Pobrane pliki oraz ich SHA-256 zapisano w manifeście; dane pozostają poza Git. Uwzględniono poprawiony przez wydawcę 20 listopada porządek `seq`.

Własne liczniki zgadzają się z tabelą wydawcy:

| Część | Liczba rekordów |
|---|---:|
| Udane transakcje krzywej | 4 556 524 |
| Nieudane próby krzywej | 10 396 021 |
| Udane transakcje PumpSwap | 17 245 358 |
| Nieudane próby PumpSwap | 10 032 507 |
| Starty tokenów tego dnia | 46 540 |

Nie znaleziono powielonych kluczy `(slot, idx, seq, failed)`. Udane krzywe SOL obejmują 4 013 534 rekordy, także tokenów rozpoczętych wcześniej. Końcowa kohorta zawiera wyłącznie starty tego dnia, z podażą 1 mld i sześcioma miejscami dziesiętnymi, kwotowaniem WSOL, co najmniej dwiema transakcjami, pierwszą obserwacją w ciągu 10 s oraz co najmniej 99% rekordów zgodnych ze standardowym invariantem w tolerancji 0,5%. Pozostaje **19 346 tokenów i 2 286 485 stanów**; 27 194 starty nie spełniają wszystkich warunków. W kohorcie są 344 zarejestrowane zakończenia krzywej.

To **retrospektywna kontrola jakości**, nie filtr wejścia możliwy do zastosowania na żywo: ocena całej ścieżki używa późniejszych danych. Mayhem nie ma bezpośredniej flagi, więc zgodność invariantu nie zastępuje niezależnej identyfikacji typu tokena.

Rezerwy krzywej `r1/r2` są stanem **po** transakcji. Rezerwy PumpSwap w tym źródle są **przed** transakcją, a część zakupów kończących krzywą łączy jej część z częścią puli. Dlatego nie użyto tych rekordów jako naiwnego szeregu cen puli; wyjścia po migracji pozostają `censored_pool`.

Kolejność to `(slot, idx, seq)`. Zegar stanów i sygnałów przyjęto jako `ts+1`, czyli górny koniec sekundy zapisanej przez blok. Nie interpolowano czasu z przyszłego bloku. Nie trzeba było korygować żadnego spadku czasu w kolejności łańcucha. Ten model dodaje do sekundy zwłoki względem sygnału śródsekundowego; nie usuwa niepewności samego czasu blokowego.

## Reguły zamrożone przed odczytem wyników

Każda reguła wchodzi po pierwszym przekroczeniu 10%, 30% lub 50% postępu krzywej. Warianty opóźnienia wejścia i sprzedaży: 1, 5 i 30 s. Reguły:

1. Stop na 0,7 ceny odniesienia i wyjście po 30 s.
2. Ten sam stop i wyjście po 120 s.
3. Stop 0,7, take-profit 1,25 i limit trzymania 600 s.
4. Trailing 20%, aktywacja przy 1,3 i limit 600 s.

Budżet: 1 SOL. Prowizja scenariusza: 1,25% na stronę; zakup z budżetu netto `X/(1+fee)`. Dodatkowy koszt każdego zlecenia: `0,30/70 SOL`. To jawne założenia, nie odtworzona historyczna taryfa. Nie dodawano nieudanych zleceń strategii, ponieważ częstotliwość cudzych prób nie identyfikuje naszej szansy wykonania. Wpływ własnej pozycji jest addytywnym przybliżeniem przy niezmienionym przepływie innych traderów.

Powstało 8 753 zdarzeń wejścia: 6 205 przy 10%, 1 716 przy 30% i 832 przy 50%. To zdarzenia, nie rozłączne tokeny. Dwa modele pokrycia dały łącznie 210 072 scenariusze; **nie są to niezależne transakcje portfela**.

## Dwa modele pokrycia dają odmienne odpowiedzi

**`trade_supported`** wymaga późniejszych stanów z rzeczywistych zapisanych transakcji i ogranicza wiek użytej obserwacji do 30 s. Brak takiego wsparcia to wynik nieznany.

**`ledger_day_coverage`** jest osobną analizą wrażliwości: przyjmujemy deklarowaną przez receipt kompletność bloków oraz brak niezapisanych zmian wirtualnych rezerw standardowej krzywej. Wtedy cisza po ostatniej transakcji oznacza niezmieniony stan do końca dnia, a nie koniec obserwacji. Przedłużamy ostatni stan niemigrującego tokena do granicy dnia i wyłączamy limit świeżości. To **założenie o kompletności i niezmienności**, nie dodatkowy pomiar rezerw. Byłoby błędne przy pominiętych zdarzeniach lub aktywności Mayhem. Nie przenosimy go na nieciągły korpus kolektora z czerwca–lipca.

Przykład: trailing 20%, aktywacja 1,3, wejście przy 10%, opóźnienie 1 s:

| Model | Wspierane wejścia | Rozstrzygnięte | Nierozstrzygnięte po wejściu | Średnia netto po rozstrzygniętych |
|---|---:|---:|---:|---:|
| Tylko wsparcie transakcjami | 6 101 | 2 589 | 3 512 | **+14,68%** |
| Założenie kompletnego dnia ledger | 6 104 | 6 034 | 70 | **−17,84%** |

Opisowy bootstrap blokami godzinowymi daje odpowiednio przedziały około **[+11,65%; +17,93%]** i **[−19,30%; −16,00%]**. Pierwszy dodatni przedział nie naprawia selekcji: reguła aktywuje trailing dopiero po wzroście, a pominięte ciche pozycje nie są losową grupą. `dropna()` może więc stworzyć statystycznie przekonującą pozorną przewagę.

W modelu pełnego dnia **wszystkie 36 kombinacji reguła–poziom–opóźnienie ma ujemną średnią**, od około −5,72% do −22,45%. Wszystkie opisowe górne granice przedziałów są poniżej zera. To wyniki tego jednego dnia i przyjętego modelu; nie obalają każdej możliwej strategii.

Przedziały wykorzystują 2 000 replik UTC-godzin, ziarno 42, i nie mają korekty na wielokrotne porównania. Nie obejmują ryzyka błędnego źródła, nieznanych wyjść ani zmiany reżimu między dniami.

## Wysoki win rate i dodatnia mediana nie wystarczają

Bracket stop 0,7 / TP 1,25 przy 50% krzywej, opóźnienie 1 s, model pełnego dnia:

- 832 sygnały; 728 wspieranych wejść; 721 rozstrzygniętych pozycji; 7 nieznanych wyjść.
- **56,73%** rozstrzygniętych pozycji na plusie i mediana **+14,62%**.
- Średnia wygrana **+23,75%**, średnia przegrana **−45,14%**.
- Średnia całości **−6,06%**, godzinowy CI około **[−8,59%; −3,41%]**.
- **11,93%** rozstrzygniętych pozycji traci ponad 50%; pierwszy percentyl wynosi około **−90,70%**.

Przy tych średnich wielkościach wygranej i przegranej próg zerowego wyniku wymagałby około **65,5%** wygranych, a nie 50% (rachunek własny, bez nieznanych wyników). Stop jako warunek wysłania zlecenia nie jest gwarantowaną ceną sprzedaży. Wynik nie uzasadnia wymiarowania kapitału tak, jakby maksymalna strata wynosiła 30%.

## Opóźnienie: potrzebna wspólna próba, bez uniwersalnej monotoniczności

`october_paired.csv` porównuje 1/5/30 s tylko dla tych samych zdarzeń z trzema rozstrzygniętymi wynikami. To nadal wyselekcjonowana wspólna próba. Dla przykładowego bracketu przy 10%:

- W `trade_supported`, na 2 796 wspólnych zdarzeniach: średnio **+5,61%, +7,07%, −7,06%**.
- W `ledger_day_coverage`, na 6 043 wspólnych zdarzeniach: **−11,34%, −9,67%, −9,67%**.

Późniejszy zakup może ominąć część początkowego wzrostu i kupić po spadku; równocześnie późniejsza sprzedaż może pogorszyć stop. Opóźnienie dotyczy obu stron. Nie wyciągamy ogólnej tezy „większe opóźnienie zawsze obniża wynik” ani „czekanie daje przewagę”. W tych zamrożonych wariantach nadal nie uzyskano dodatniej średniej na modelu pełnego dnia.

## Praktyczny wniosek do dalszych testów

Nie wybierać reguły według średniej po pominięciu nieznanych wyjść, win rate ani mediany. Dla nowej hipotezy najpierw ustalić źródło informacji ponad sam poziom krzywej, a potem sprawdzić łącznie rozkład strat, kompletność wyjść, koszt i przenoszenie wyniku na inny okres. Ten eksperyment falsyfikuje dodatnią przewagę tych prostych, niefiltrowanych reguł w określonym październikowym modelu. Nie tworzy jeszcze gotowej strategii do realnego handlu.

## Reprodukcja i kontrole

```text
python backtest/big/b19_october_holdout.py SCRATCH --output backtest/out/big --tag october_v3
```

Zakończony przebieg ma 19 346 tokenów i 210 072 wyników scenariuszy; smoke 100 tokenów był tylko kontrolą techniczną. Końcowy przebieg nie używa `--limit-tokens`. Czas lokalnego pełnego przebiegu: około 22 s. Hashe kodu, danych i konfiguracja są w `october_manifest.json`. Kontrole `sygnały = wejścia + brak wejścia` oraz `wejścia = rozstrzygnięte + nieznane` przeszły dla wszystkich 72 grup.

Pliki małych wyników: `october_preparation.json`, `october_summary.csv`, `october_reasons.csv`, `october_paired.csv`, `october_hourly.csv`, `october_uncertainty.csv`, `october_manifest.json`. Wyniki poszczególnych tokenów i przygotowane dane są wyłącznie w `SCRATCH/work/october_v3/`.
