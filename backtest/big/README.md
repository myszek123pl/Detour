# Odtwarzalny eksperyment na pełnym korpusie

To badanie warunkowych reguł wejścia/wyjścia, a nie bot podłączony do portfela. Surowych danych ani lokalnych wyników każdej pozycji nie dodajemy do Git.

## Dane i kohorta

Zamrożone rewizje wejściowe są zapisane w `b00_download.py`. Pliki LFS są weryfikowane SHA-256, a manifesty zapisują pochodzenie. Korpus jocry zawiera 33 581 765 transakcji i 798 430 tokenów; nie każdy rekord ma rezerwy potrzebne do symulacji. `corpus_audit.json` zawiera własne przeliczenie braków, dat i źródeł.

`b00_prepare.py` tworzy retrospektywną kohortę jakościową: 219 327 standardowych tokenów, 16 217 167 stanów po deduplikacji. Nie wolno nazywać tej selekcji filtrem dostępnym przy starcie tokena ani uogólniać wyników na odrzucone tokeny.

Osobny październikowy eksport pumpdata.fun ma kolejność `(slot, idx, seq)`, nieudane transakcje i deklarowany audyt pokrycia bloków. Rozdzielamy go od kolejności kolektora jocry. Sekundowa rozdzielczość czasu nie pozwala twierdzić, że znamy dokładną latencję wewnątrz sekundy.

## Uruchomienie

Python 3.12, pakiety z `requirements.txt`. Polecenia poniżej wykonujemy z katalogu repozytorium. `SCRATCH` oznacza wybrany katalog danych poza repozytorium; pobranie obu zbiorów i dodatkowych snapshotów zajmuje około 8 GB, a wyniki i pliki robocze wymagają dodatkowego miejsca.

```text
python -m pip install -r backtest/big/requirements.txt
python backtest/big/b00_download.py SCRATCH --october --snapshots
python backtest/big/b00_audit.py SCRATCH --output backtest/out/big/corpus_audit.json
python backtest/big/b00_prepare.py SCRATCH --report backtest/out/big/preparation.json
python -m pytest -p no:cacheprovider backtest/big/test_simlib.py
python backtest/big/b15_replay.py SCRATCH --output backtest/out/big --tag replay_v2
python backtest/big/b16_entry_features.py SCRATCH --out-dir backtest/out/big
python backtest/big/b18_execution_costs.py SCRATCH/datasets/pumpdatafun --output backtest/out/big/execution_costs.json
```

`b19_october_holdout.py --help` i `b20_strategy_review.py --help` opisują niezależną walidację oraz przegląd reguł po ukończeniu replay. Nazwa `--tag` identyfikuje zamrożony eksperyment: wznowienie z innym kodem, konfiguracją lub wejściami jest odrzucane. Zmiana założeń wymaga nowej nazwy; nie należy nadpisywać już przejrzanego wyniku.

## Kontrakt wyników

Replay porównuje 32 reguły, siedem pierwszych przekroczeń poziomu krzywej i latencje 1/5/30 s. Każda reguła ma jawny maksymalny horyzont (domyślnie godzina). Rozmiar 1 SOL, prowizja 1,25% oraz tip 0,30/70 SOL są scenariuszem, nie dowodem historycznie płaconych kosztów.

- `no_fill` oznacza brak popartego danymi wejścia. Nie jest równoznaczne z odrzuceniem rzeczywistego zlecenia.
- `censored` oznacza nierozstrzygniętą pozycję. Nie jest zerowym wynikiem, automatyczną stratą całości ani zyskiem po ostatnim kursie.
- `grad_snapshot` opiera się na dostępnych rezerwach puli; nadal jest przybliżeniem wykonania na snapshotach.
- Średnia tylko z rozstrzygniętych pozycji podlega selekcji zależnej od wyniku. Nawet duża próba i bootstrap nie usuwają tego problemu.
- Przypisanie brakującym pozycjom −100% jest scenariuszem wrażliwości, nie estymatą ani ścisłą dolną granicą po kosztach.
- Porównanie latencji na różnych zbiorach rozstrzygniętych pozycji miesza opóźnienie ze zmianą próby. Dlatego pokazujemy także wspólne pozycje, z jawnym zastrzeżeniem tej selekcji.

Model cech przewiduje etykietę kolektora w 24 h. Dojrzałość etykiety, dni luk i końcowe niedojrzałe okna mają osobne wykluczenia. Trafność tej prognozy nie jest wynikiem handlowym. Wybór reguły tradingowej następuje na wcześniejszym okresie; późniejsza próba i październik służą ocenie, nie dobieraniu progów.

Interpretacja: notatki 35–40 w `research_notes/Trading memecoinów backtest/`.
