# Audyt wykonania: poprawiona chronologia i jawne cenzurowanie

Stan: 21 listopada 2026. Audyt kontynuuje wcześniejszy zapis problemów. Zmiany dotyczą `backtest/big/simlib.py`; testy w `test_simlib.py` są syntetycznymi kontrolami poprawności, nie dowodem skuteczności strategii.

## Zamknięte błędy

1. **Zegar wejścia:** `tf` oznacza czas decyzji plus opóźnienie, a `state_t` czas ostatniego znanego stanu. Wejście po końcu obserwacji jest odrzucane. Niedostępny, nieuporządkowany albo niepoprawny stan nie daje zlecenia.
2. **Wyjście czasowe:** termin wynosi `entry.tf + tmax`, niezależnie od tego, kiedy następuje kolejna transakcja. Opóźnienie sprzedaży dolicza się do tego terminu. Po oczekiwaniu na częściową sprzedaż przeterminowany timer działa najwcześniej od chwili jej wykonania.
3. **Jedno oczekujące wyjście:** po wykonaniu częściowej sprzedaży skanowanie wznawia się za stanem wykonania. Nie można ponownie wykorzystać wcześniejszego szczytu jako nowego sygnału. Trailing zachowuje szczyt zaobserwowany podczas oczekiwania.
4. **Koniec danych:** nie jest sygnałem sprzedaży. Pozostała pozycja bez potwierdzonego wyjścia zwraca `NaN, censored`, także po wcześniejszych częściowych sprzedażach. Przyszła data graduacji w metadanych sama nie zamienia urwanej ścieżki w znany wynik.
5. **Opóźniona sprzedaż:** gdy wykonanie wypada po końcu pokrycia, wynik jest cenzurowany. Nie używamy ostatniego rekordu jako bezterminowo aktualnej ceny. Domyślna tolerancja świeżości stanu to 30 s; można ją jawnie zmienić parametrem `max_state_age`.
6. **Migracja:** domyślny model wymaga faktycznie dostępnych dodatnich `liquidity_quote` i `liquidity_base`, nie tylko ceny. Wybiera ostatni snapshot nie późniejszy niż chwila wykonania i odrzuca snapshot starszy niż `max_pool_age` (domyślnie 30 s). Brak danych daje `censored_pool`; brak poprawnych rezerw `invalid_pool`. Wynik z tej ścieżki ma nazwę `grad_snapshot`, aby nie mylić go z odtworzeniem transakcji on-chain.
7. **Cena po migracji:** usunięto wybór przyszłego snapshotu, obcinanie mnożnika do przedziału 0,1–3 oraz automatyczne podstawianie syntetycznej ceny przy brakach. Dawne modele `fixed` i `price_approx` pozostają wyłącznie jawnie wybranymi scenariuszami.
8. **Budżet i opłata zakupu:** domyślnie net SOL = budżet / (1 + stawka opłaty), a napiwek jest dodatkowym kosztem. Koordynator potwierdził strukturę wzoru w oficjalnym [pakiecie pump-sdk 4.3.1](https://registry.npmjs.org/@pump-fun/pump-sdk/4.3.1), funkcja `getBuyTokenAmountFromSolAmount`. Wersja float pomija odjęcie jednego lamporta i zaokrąglenia całkowitoliczbowe SDK. Dawny `budget * (1-fee)` jest dostępny tylko jako jawny `fee_model=deducted` dla porównań.
9. **Granica krzywej:** duże wejście przekraczające po dodaniu net SOL standardowy próg graduacji jest odrzucane zamiast symulować niemożliwą transakcję.

## Kontrakt dla nowych obliczeń

`entry(...)` zachowuje API i zwraca słownik albo `None`. `exit_sim(...)` zwraca `(net_return, kind, executed_sell_count)`. **NaN nie jest zerem ani stratą całości.** Licznik wykonanych częściowych sprzedaży nie oznacza, że wynik całej pozycji jest znany. Raport musi pokazać liczbę sygnałów, niewykonanych wejść, rozwiązanych pozycji i pozycji cenzurowanych. Średnia po `dropna()` opisuje tylko pozycje rozwiązane i może być silnie selekcyjna.

Przy równoczesnym sygnale i upływie czasu stosowana jest deterministyczna kolejność; po wykonaniu wyjścia nie odtwarzamy ponownie sygnałów z tego samego rekordu. To konwencja dyskretnego modelu, nie identyfikacja kolejności instrukcji w slocie.

## Weryfikacja

Uruchomienie:

```text
python -m pytest -p no:cacheprovider backtest/big/test_simlib.py -q
```

**29 testów przeszło.** Obejmują dokładny timer na rzadkich zdarzeniach, opóźnienia 1/5/30 s, brak terminalnego wymuszenia sprzedaży, przyszłą graduację, nieznany wynik reszty po częściowej sprzedaży, zachowanie trailing peak podczas oczekiwania, nieaktualne rezerwy, niepoprawne wartości i opóźnienia, brak rezerw puli, poprawny budżet fee-on-top oraz przepełnienie krzywej. Kontrola niezmiennego rynku sprawdza, że round trip traci wyłącznie przyjęte opłaty i napiwki.

## Pozostałe granice modelu

- Kolejność `event_time/id` pochodzi od kolektora, nie ze zweryfikowanego `slot/transaction/instruction index`.
- Tolerancja 30 s jest scenariuszem świeżości; nie dowodzi ciągłości feedu. Nie odtwarza zleceń pominiętych wewnątrz luki.
- Addytywna zmiana rezerw własną pozycją utrzymuje historyczny przepływ innych uczestników. Nie modeluje ich reakcji, zmiany kolejki, sandwichy, limitów poślizgu ani prawdopodobieństwa lądowania. To przybliżenie kontrfaktyczne.
- Snapshot puli nie jest transakcją wykonania i nie dowodzi dostępności tej płynności w dowolnym momencie między pomiarami.
- Bieżący wzór SDK nie potwierdza **historycznej stawki opłaty** w czerwcu/lipcu. Wartości fee, napiwków i SOL/USD w skryptach są parametrami scenariusza; potrzebują analizy wrażliwości, nie etykiety „zmierzone” bez źródła.
- Retrospektywna selekcja jakości całej ścieżki nie jest filtrem dostępnym przy starcie tokena. Wynik takiej kohorty nie opisuje automatycznie całej populacji.

Pełny korpus został wcześniej przeliczony: 33 581 765 transakcji, 6 122 166 bez kompletu rezerw, brak transakcji z 3 i 12 lipca. Przygotowano 219 327 tokenów i 16 217 167 stanów po deduplikacji; źródła i kryteria są w `backtest/out/big/corpus_audit.json` i `preparation.json`. Nowy przebieg strategii musi wskazywać hash poprawionego kodu i te warunki; historycznych wyników nie należy automatycznie przepisywać jako wyników nowego symulatora.
