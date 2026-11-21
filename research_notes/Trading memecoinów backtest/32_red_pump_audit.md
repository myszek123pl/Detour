# RED-PUMP-2026: niezależny audyt danych i wycofanych wniosków

Stan sprawdzenia: 21 listopada 2026. Źródło: Arati Kamat, [RED-PUMP v1.6, rekord 23018519](https://zenodo.org/records/23018519), CC BY 4.0 dla danych i tekstu. Analiza własna poniżej; depozyt pozostaje poza repozytorium.

## Wynik

**Z RED-PUMP nie da się rzetelnie wyliczyć rzeczywistej stopy graduacji ani przetrwania tokenów.** Pole `GRADUATED` jest terminalną etykietą kolektora, a `TIMEOUT` nie oznacza potwierdzonego braku graduacji, śmierci tokena ani utraty całego kapitału. Zadanie zmieniamy więc z estymacji sukcesu tokenów na audyt pomiaru. Nie ma tu podstaw do odtworzenia strategii transakcja po transakcji.

Najnowszy opis depozytu wycofuje wnioski survival ze starszych wydań, w tym popularną liczbę 0,198% i wcześniejszy efekt Telegrama. Nowsze uwagi do publikacji dodatkowo korygują interpretację nieudanej walidacji modelu. Historyczna [wersja 1.4](https://zenodo.org/records/21923106) ma już ostrzeżenie, że tych wniosków nie należy cytować jako wskaźników platformy.

## Co rzeczywiście sprawdzono

Pobrano cały pakiet v1.6: **348 529 377 bajtów**. MD5 `c9c056392d91646bc6af8e2a2794d2eb` zgadza się z metadanymi Zenodo. Niezależnie zweryfikowano **71 z 71** wewnętrznych SHA-256, bez rozbieżności. Nie uruchamiano kodu autora ani nie deserializowano pliku modelu `.pkl`.

Własny skrypt `backtest/red_pump/audit_counts.py` czyta surowe gzipy oraz wybrane tabele Parquet z archiwum. Wynik: `backtest/out/red_pump/audit_counts.json`.

| Obiekt | Własne przeliczenie | Znaczenie |
|---|---:|---|
| Wiersze launch JSONL | 860 213 | Rekordy kolektora, nie udowodniona pełna populacja platformy |
| Unikalne minty launch JSONL | 860 194 | 19 dodatkowych rekordów tych samych mintów |
| Pierwszy / ostatni `seenAt` | 8 maja 17:17:38.493 / 10 czerwca 18:11:08.532 UTC | Granice zapisanych obserwacji |
| Wiersze opublikowanej kohorty głównej | 749 816 | Przeliczenie dostarczonego pośredniego pliku; nie rekonstrukcja selekcji od zera |
| Etykiety w tej kohorcie | 1 597 `GRADUATED`, 748 219 `TIMEOUT` | Udział dodatniej etykiety 0,21299%; **nie stopa graduacji** |
| Development | 387 152 rekordy, 794 dodatnie etykiety | Przeliczenie flag opublikowanej kohorty |
| Validation | 362 664 rekordy, 803 dodatnie etykiety | Przeliczenie flag opublikowanej kohorty |

Surowy outcome CSV ma **833 192 fizyczne linie danych**. Zawiera mieszankę dwóch schematów, nieescapowane przecinki oraz podziały wiersza wewnątrz symboli. Proste `split(',')` albo bezwarunkowy standardowy import CSV zmieniają przypisanie kolumn. Nasz wynik zachowuje oddzielnie rygorystyczne liczenie fizycznych rekordów i ostrożną rekonstrukcję sąsiednich fragmentów; ta druga odzyskuje 39 rekordów rozciętych przez nową linię. Żadnego z tych liczników nie nazywamy populacyjną liczbą graduacji. Historyczna notatka o wadliwych wierszach nie zastępuje kontroli parsera.

## Dlaczego nie liczymy krzywej przetrwania

Dołączone `OUTCOME_ASCERTAINMENT_MECHANISM.md` opisuje kolektor odpytujący tylko 50 najnowszych tokenów. Po wyparciu tokena z listy rzeczywiste zakończenie krzywej mogło nie zostać odnotowane; upływ 24 godzin w pamięci procesu nie jest 24 godzinami obserwacji stanu on-chain. To informacyjne braki obserwacji, których nie naprawia przypisanie wszystkim `TIMEOUT` porażki.

W dostarczonej kohorcie mediana **zrekonstruowanego**, a nie zweryfikowanego czasu widoczności wynosi 1,501 minuty; percentyl 99 to 5,500 minuty. Wykryliśmy 43 oznaczone naruszenia rekonstrukcji; w 42 zdarzenie zapisano dokładnie przy odpytywaniu, które rekonstrukcja nazwała pierwszym niewidocznym. Potwierdza to rachunek z korekty autora, nie dowodzi błędnej etykiety w 42 tokenach. Brak pełnych logów obserwacji i niezależnych zdarzeń on-chain uniemożliwia uznanie tych czasów za wiarygodne cenzurowanie dla Kaplan-Meiera/Coxa.

Pakiet zawiera memo audytu kolektora, ale nie pełne wskazane w nim zachowane pliki JS. Główna procedura budowy kohorty w dostarczonym kodzie wczytuje już `reconstructed_mint_observation_windows_v1.parquet`. Nasza kontrola potwierdza liczby w zamrożonym materiale, a nie pełną reprodukcję procesu zbierania danych.

## Walidacja: co potwierdza rachunek, a czego nie

Własne ponowne obliczenie AUROC metodą rang oraz Brier score z zapisanych `Y,p` odtwarza metryki autora:

| Próbka | AUROC | Brier |
|---|---:|---:|
| Development | 0,8593551232 | 0,0020274304 |
| Validation | 0,4641688683 | 0,0022129276 |

Nie odtworzono dopasowania modelu ani bootstrapu 500 replik. W walidacji 286 227 z 362 664 prawdopodobieństw jest poniżej `1e-8`, a 39 905 to dokładnie zero. Wynik nie uzasadnia tezy, że sygnały rynkowe przestały działać: najnowsze uwagi Zenodo wskazują przede wszystkim źle identyfikowaną końcową bazę zamrożonego splajnu kalendarzowego. W zapisanym pliku współczynników jej estymata wynosi -1156,29 przy SE 5714,41. [ArXiv v4](https://arxiv.org/html/2607.02823v4) należy czytać wraz z późniejszymi korektami depozytu, nie samodzielnie.

Potwierdziliśmy też selekcję ostatniej doby: do kohorty weszło **56** wykrytych wtedy mintów, wszystkie z dodatnią etykietą. Po ich wyłączeniu AUROC tych samych, wcześniej zapisanych predykcji wynosi **0,4948472637** (362 608 rekordów, 747 dodatnich). To jawna analiza wrażliwości, bez ponownego dopasowania i bez przedziału ufności; nie naprawia modelu ani etykiet. Dowodzi natomiast, że interpretacja 0,464 jako rynkowego odwrócenia sygnału jest szczególnie nieuzasadniona.

Pozostałe korekty autora: 30 SOL jest masą punktową pola początkowego, nie progiem graduacji; protokół był uprzednio określoną ponowną analizą już badanego zbioru, nie prospektywną prerejestracją; przyczyna 183 nieudanych bootstrapów dotyczy pustych kolumn splajnu. Nie przenosimy tych liczb na nowe dane.

## Grupy snajperów są osobnym zbiorem i osobnym problemem

Surowe RED-PUMP zawierają metadane launchy i terminalne etykiety. Nie zawierają szeregu zakupów/sprzedaży z adresami nabywców, kolejnością slotów, transferami i źródłami finansowania. Nie można z nich odtworzyć snajperów ani przypisać wyniku tokena grupie portfeli. Do tego potrzebny jest osobny zbiór, z kontrolą znaku transakcji i kompletności zapisu.

[Publikacja o grupach snajperów, 2607.02795v4](https://arxiv.org/pdf/2607.02795v4), ma na pierwszej stronie korektę z października: rekordy kupujących mieszały zakupy ze sprzedażami i pomijały wiele zakupów. **Wszystkie jej wyniki liczbowe zostały wycofane**, włącznie z katalogiem „1 012 grup” i estymatą +16,1%. Nie traktujemy ich jako potwierdzonych własności rynku. Pomysł wyłączenia własnych transakcji grupy z mierzonego późniejszego przepływu pozostaje sensownym zabezpieczeniem metodologicznym do przyszłego testu, a nie zweryfikowaną strategią.

## Włączenie do projektu

RED-PUMP nadaje się do testów jakości importu, replikacji opublikowanych liczników i badania błędów kolektora. Nie włączamy jego etykiet do targetu „zyskowny token”, nie przyjmujemy `TIMEOUT = -100%` i nie uzupełniamy nimi ścieżek cenowych. Dla rzeczywistej graduacji potrzeba zdarzeń zakończenia krzywej/migracji z niezależnego źródła; dla przetrwania jawnej definicji aktywności/płynności oraz kompletnego późniejszego okna obserwacji.

Reprodukcja naszego audytu po pobraniu wskazanego archiwum (Python, numpy, pyarrow):

```text
python backtest/red_pump/audit_counts.py --archive PATH_TO_ZIP --output backtest/out/red_pump/audit_counts.json
```
