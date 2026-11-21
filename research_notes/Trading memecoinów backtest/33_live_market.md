# Rynek na żywo: nowe pule, boosty i rotacja trending

Stan pomiaru: **21 listopada 2026, 11:00:21–11:05:42 UTC**, czyli **12:00:21–12:05:42 Europe/Warsaw**. Jest to rzeczywiście pobrana pięciominutowa próbka tego dnia, a nie rekonstrukcja całego listopada. Wyniki są opisem widoczności i kwotowań API; nie są backtestem wykonanych transakcji.

## Co zostało zmierzone

Pięć rund zbierania danych: GeckoTerminal `/networks/solana/new_pools` strony 1–3, `/trending_pools` strona 1 z `duration=1h`, DEX Screener `/token-boosts/latest/v1`, `/token-boosts/top/v1` i `/tokens/v1/solana/{addresses}` dla odkrytych tokenów. Adresy wykryte wcześniej pozostają w rejestrze śledzenia, także po zniknięciu z list odkrywania. Początkowo było 90 adresów, na końcu 222.

Zapisano czas rozpoczęcia i zakończenia każdego żądania, nagłówki HTTP Date/Age/cache oraz SHA-256 odpowiedzi i plików. Zegar klienta i HTTP Date różniły się najwyżej o 2,14 sekundy; daty serwerów zgadzały się z 21 listopada 2026. Odpowiedzi miały do 53 sekund wieku pamięci podręcznej. Jest to wystarczające do krótkiej obserwacji rynku, lecz nie do oceny przewagi przy opóźnieniu 1 sekundy.

Było 55 odpowiedzi HTTP 200, dwie 429 dla trending oraz jeden timeout danych par DEX Screener. Nie uzupełniano ich zerami ani ostatnią znaną wartością. Dwie brakujące listy trending pominięto w obliczeniach rotacji. Planowany odstęp 60 sekund został wydłużony przez czas odpowiedzi w jednej rundzie; metryki używają rzeczywistych czasów pobrań. Kolektor wysyłał cztery żądania GeckoTerminal na rundę, poniżej opublikowanego limitu 10/min; odpowiedzi 429 mimo tego pokazują, że dostępność endpointu nie jest gwarantowana. Kod kolejnych uruchomień respektuje Retry-After i przy 429 wprowadza co najmniej minutę przerwy dla hosta. [Publiczny interfejs GeckoTerminal](https://www.geckoterminal.com/dex-api), [DEX Screener API](https://docs.dexscreener.com/api/reference).

## Nowe pule: obserwowany napływ, bez ekstrapolacji na całą sieć

| Pomiar UTC | Odrębne pule na trzech stronach | Najstarsze utworzenie | Najnowsze utworzenie |
|---|---:|---|---|
| 11:00:21 | 51 | 10:56:49 | 10:59:20 |
| 11:01:21 | 46 | 10:57:49 | 11:00:01 |
| 11:03:24 | 55 | 11:00:08 | 11:02:25 |
| 11:04:24 | 41 | 11:01:20 | 11:03:03 |
| 11:05:24 | 51 | 11:02:25 | 11:04:13 |

Łącznie zaobserwowano **179 różnych identyfikatorów pul**, z czego 51 było w pierwszej rundzie, a 128 pojawiło się w kolejnych. Wśród całej unii **100 pul ma timestamp utworzenia mieszczący się w oknie zbierania**. Daje to **18,69 obserwowanych utworzeń/min** w tej próbce. Wśród tych 100: 72 miały venue `pump-fun`, 5 `pumpswap`, 15 `meteora-damm-v2`, 6 `meteora-dbc`, po jednej `stonkfun` i `bags-fm`.

To **nie jest liczba wszystkich nowych tokenów na pump.fun ani tempo emisji całej Solany**. Mierzymy zarejestrowane pule z konkretnych stron API; tworzenie puli i mint tokena to różne zdarzenia. Strony były pobierane kolejno, a indeks w międzyczasie się zmieniał: trzy strony po 20 rekordów nie dały 60 odrębnych pul. Są nakładki i możliwe pominięcia, opóźnione indeksowanie oraz brak ostatniej części okna. Nie mnożymy 18,69 przez dobę ani miesiąc. Specyfikacja powiązanego endpointu dokumentuje do 20 pul/stronę i ograniczony zakres nowych pul. [Opis nowych pul](https://docs.coingecko.com/reference/latest-pools-network).

## Trending: widoczna rotacja w kilka minut

Użyteczne listy top 20 otrzymano w rundach 0, 2 i 4. `duration=1h` określa wariant rankingu, nie godzinę naszego pomiaru.

| Dwa udane pobrania | Rzeczywisty odstęp | Wspólne pule | Retencja pierwszej listy | Jaccard | Weszło / wyszło |
|---|---:|---:|---:|---:|---:|
| 0 → 2 | 182,17 s | 14/20 | 70% | 0,538 | 6 / 6 |
| 2 → 4 | 119,90 s | 10/20 | 50% | 0,333 | 10 / 10 |
| 0 → 4 | ok. 302 s | 12/20 | **60%** | **0,429** | **8 / 8** |

Średnia bezwzględna zmiana pozycji wspólnych pul wyniosła 3,57 miejsca dla 0→2 i 8,50 dla 2→4. Wniosek pomiarowy: skład i kolejność listy potrafią istotnie zmienić się w kilka minut. Nie wyznaczamy z trzech list średniego czasu trwania trendu ani miesięcznej częstości rotacji. Pula mogła wyjść i wrócić pomiędzy pobraniami. HTTP 429 nie jest dowodem, że wszystkie pule wypadły z rankingu.

## Boosty: porównanie kwotowań, bez dowodu przewagi

Klasyfikację zamrożono na pierwszym pomiarze. „Widoczny boost” oznacza dodatnie `boosts.active` w danych pary **lub** obecność adresu na pobranej liście boostów. „Boost niezgłoszony” oznacza brak takiego sygnału w tych odpowiedziach; nie dowodzi braku wcześniejszej płatnej promocji. Jednostką analizy jest token, z jedną parą o największej podanej płynności w chwili pierwszego pomiaru. Dalszą zmianę ceny liczymy dla **tej samej pary**, nie wybieramy później innej korzystniejszej.

Z 90 tokenów tylko 44 miały dodatnią podaną płynność USD. Pozostałe 46 wyłączono zamiast uznać brak płynności za zero. Przez to porównanie **nie reprezentuje wszystkich świeżych tokenów na krzywej**. Z 44 kwalifikujących się par 25 działało na PumpSwap, pozostałe na innych DEX-ach; samo venue PumpSwap nie stanowi pełnej weryfikacji pochodzenia tokena.

| Cecha pierwszej kohorty | Widoczny boost | Boost niezgłoszony |
|---|---:|---:|
| Liczba tokenów z płynnością USD | 20 | 24 |
| Mediana wieku wybranej pary | 6,11 dnia | 27,28 dnia |
| Mediana płynności | 39 765 USD | 168 909 USD |
| Mediana wolumenu ostatnich 5 min | 185 USD | 6 852 USD |
| Mediana późniejszej zmiany kwotowania | −0,038% | 0,000% |

Późniejsze kwotowanie było dostępne dla wszystkich 44 par, po 301,5–307,8 sekundy od ich pierwszego odczytu. Te proste mediany **nie są porównaniem podobnych grup**: różnią się wiekiem i płynnością, a kohorta pochodzi z odmiennych list odkrywania.

Dlatego przeprowadzono dopasowanie bez zwracania kontroli: ten sam DEX, wiek pary w granicach czynnika 2 i płynność w granicach czynnika 2; kolejność wyboru ustalona po adresie tokena, a najbliższa kontrola według sumy odległości logarytmicznych. Z 20 tokenów z boostem udało się dopasować tylko **3**; wszystkie trzy dopasowania dotyczyły PumpSwap. Różnice późniejszej zmiany kwotowania wyniosły −0,69, +2,15 i +4,15 pkt proc. (mediana +2,15 pkt proc.). **Próba trzech dopasowań nie rozstrzyga ani kierunku, ani trwałości efektu boostów.**

To nie jest efekt przyczynowy reklamy. Nie znamy historii wydatków na boost, wcześniejszego momentum, finansowania zespołu ani pełnej publiczności tokena. Cena z API nie jest ceną realizacji pozycji: nie odjęto prowizji, price impact, napiwków ani nieudanych zleceń. Na tych pomiarach nie da się uczciwie stwierdzić, że kupowanie boostowanych tokenów zarabia lub traci.

## Pliki, odtworzenie i dalsze dane

- Kolektor: `backtest/live/collect.py`.
- Obliczenia: `backtest/live/analyze.py`.
- Wyniki: `backtest/out/live/summary.json`, `baseline_tokens.csv`, `matched_pairs.csv`, `request_audit.csv`.
- Surowe pięć plików JSON: lokalny katalog roboczy `../live_market/` względem klonu repo; SHA-256 i rozmiary w `summary.json`. Surowych odpowiedzi nie dodano do repozytorium.
- Trzy testy regresji w `backtest/live/test_analyze.py` przechodzą: 429 pozostaje brakiem obserwacji, same błędy nie generują zmian rankingu, kilka par nie dubluje tokena w kohorcie.

```text
python backtest/live/collect.py --output PATH_TO_RAW --rounds 5 --interval 60 --pages 3
python backtest/live/analyze.py --input PATH_TO_RAW --output backtest/out/live --expected-date 2026-11-21
python -m unittest discover -s backtest/live -p test_*.py
```

Do testu rentowności boostów potrzebny jest oddzielny, dłuższy panel: uniwersum z pierwszego wykrycia przed zakupem promocji, chwila i kwota pierwszego boosta, kontrola dobrana przed nim, identyczny horyzont, brakujące/martwe tokeny i odtworzenie kosztu wykonania. Bieżący pomiar ustala metodę i wykazuje szybką rotację widoczności; takiego testu nie zastępuje.
