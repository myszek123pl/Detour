# Koszt wykonania i granice możliwego zysku

Stan: 21 listopada 2026. To analiza kosztów i specyfikacji eksperymentu, nie wynik strategii ani obietnica wykonania przyszłego zlecenia.

## Stały budżet zakupu

Zweryfikowano źródła oficjalnego pakietu [`@pump-fun/pump-sdk` 4.3.1](https://www.npmjs.com/package/@pump-fun/pump-sdk/v/4.3.1), archiwum `pump-sdk-4.3.1.tgz`, SHA-256 `c8ff4e850651c81e9f488bfc6dffb4513a041bb4bca0819879dc19d9a72a4641`. Kod odczytano bez uruchamiania pakietu. `getBuyTokenAmountFromSolAmount` odejmuje jeden lamport i dzieli budżet przez `1 + suma stawek prowizji`, z zaokrągleniem całkowitoliczbowym. Sprzedaż odlicza prowizję od wypłaty. Oficjalne [instrukcje swap](https://github.com/pump-fun/pump-fun-skills/tree/main/swap) korzystają z tego kalkulatora.

W floatowym replay przyjmujemy więc `netto_do_krzywej = budżet_SOL / (1 + fee)`. Poprzednie `budżet * (1-fee)` było przybliżeniem. Ta korekta nie odtwarza historycznej taryfy ani wszystkich zaokrągleń instrukcji. Oddzielamy poprawną konwencję rachunkową od niezweryfikowanej historycznej wartości stawki.

Aktualna [strona opłat pump.fun](https://pump.fun/docs/fees) ma datę 16 listopada 2026. Podaje 1,25% na krzywej oraz zmienne taryfy canonical PumpSwap i dodatkową opłatę interfejsu aplikacji od 17 października. Nie przenosimy tej strony wstecz na czerwiec jako dowodu historycznej taryfy. Stawki replay pozostają jawnymi scenariuszami.

## Rzeczywiście zapłacone opłaty sieciowe

Przeliczono cały publiczny [zbiór pumpdata.fun z 15 października](https://huggingface.co/datasets/pumpdatafun/pump-fun-trades-sample), rewizja `c3a429fcd65f15e9ea1feca8a174e617b7e8f396`. Nasz skrypt `b18_execution_costs.py` deduplikuje opłatę po `(slot, idx)`: jedna transakcja z wieloma nogami nie płaci tej samej opłaty kilka razy. Manifest plików i wyniki w `backtest/out/big/execution_costs.json`.

| Własny licznik | Transakcje wykonane | Transakcje nieudane |
|---|---:|---:|
| Liczba z rozpoznaną nogą w eksporcie | 20 865 530 | 20 060 337 |
| Liczba wierszy/nóg | 21 801 882 | 20 428 528 |
| Suma opłat sieciowych, SOL | 2 715,540586766 | 663,702699600 |
| Mediana opłaty sieciowej, lamporty | 7 401 | 6 381 |
| 90. percentyl, lamporty | 147 500 | 20 000 |
| 99. percentyl, lamporty | 1 505 000 | 205 001 |

Wśród udanych transakcji 775 291 miało dodatni zarejestrowany tip. Mediana tipa to zero, 99. percentyl 27 500 lamportów; nie oznacza to, że nowy bot osiągnie tę samą kolejność lub odsetek wykonań bez tipa. Tip nieudanej transakcji jest nieznany w tym eksporcie, a nie potwierdzony jako zerowy.

Podane opłaty sieciowe nie obejmują opłat protokołu, twórcy ani LP. Eksport pomija nieudane trasy multi-hop bez rozpoznanego mintu. Zatem wysoki udział nieudanych prób opisuje wyłącznie obserwowane próby, a nie prawdopodobieństwo niepowodzenia naszego przyszłego zlecenia.

## Co musi przetrwać reguła tradingowa

Z naszej specyfikacji, a nie z samego udziału graduacji, wynikają następujące testy:

1. Wynik netto musi utrzymać się po przesunięciu zarówno wejścia, jak i wyjścia. Stop jest sygnałem wysłania zlecenia, nie gwarantowaną ceną realizacji.
2. Mniejszy budżet ogranicza własny wpływ na cenę, ale zwiększa udział stałych kosztów. Tego kompromisu nie rozstrzyga procent trafnych tokenów.
3. Wynik pozycji musi obejmować wszystkie częściowe sprzedaże i koszt każdej próby. Nierozstrzygnięta reszta pozycji nie znika z rachunku.
4. Portfel potrzebuje limitu nakładających się pozycji. Kilka sygnałów różnych poziomów tego samego tokena nie stanowi kilku niezależnych okazji.
5. Cena na wykresie i widoczna kapitalizacja nie są kapitałem możliwym do wypłaty. Wynik wymaga dostępnej płynności i pokrycia obserwacji w chwili wykonania.

Do końcowej oceny porównujemy dodatnią średnią, jej stabilność między dniami, udział największych trafień i odsetek brakujących wykonań. Sama dodatnia średnia wśród pozycji z widocznym wyjściem nie wystarcza do zakwalifikowania strategii.
