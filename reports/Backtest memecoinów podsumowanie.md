# Backtest memecoinów: podsumowanie

Szczegóły w `research_notes/Trading memecoinów backtest/` i kodzie w `backtest/`.

## Wyniki na prawdziwych danych (9 684 tokeny, czerwiec 2026, świece 15m)
- Bez filtra każda strategia wyjścia traci 17–34% na transakcję (CI95 < 0) przy pozycji 200 USD.
- Pozorny zysk +24–33% z reguł „mało bundlerów/insiderów + płynność” okazał się błędem danych:
  zamrożona kapitalizacja i ucięte serie świec. Na wiarygodnych cechach: −27,5% [−33; −21].
- Model ML poza próbą: najlepsze 5% → +9%, ale CI od −1,5% do +19,6% (brak pewności).
- Moment wejścia (godzina, dzień, wiek tokena) nie daje przewagi. Działają tylko wykluczenia:
  mała płynność, przewaga sprzedających, łapanie spadków >50%.

## Logi prawdziwych botów z GitHuba
- Prawie wszystkie uczciwe wyniki z kosztami są ujemne (np. −8,7%/transakcję na 1 431 transakcjach).
- Stopy na pump.fun przeskakują: stop −18% realizował się średnio przy −84%.
- Kopiowanie portfeli: −22% do −38% poza próbą; kopia top-20 Kolscan: ok. −23% przy 2 s opóźnienia.
- Jedyny zyskowny bot: 938 tys. USD w 111 dni, wejście w tej samej sekundzie co start tokena,
  pozycja ok. 180 USD trzymana ok. 6 s. Nie do powtórzenia z domowym opóźnieniem.

## Mechanika
- pump.fun to gra o sumie ujemnej: suma wyników = −opłaty − SOL uwięziony w puli.
- Po ~55 SOL na krzywej podwojenie ceny na krzywej jest niemożliwe; zrzut 10% podaży na puli = −55% ceny.

## Wniosek
Brak zmierzonej przewagi dla tradera z zewnątrz. Jeśli próbować: tylko filtry wykluczające,
tryb papierowy, mikrokwoty, tysiące transakcji przed oceną, twarde limity strat.

## Co dalej
Najlepsze dane (Hugging Face: 33,6 mln transakcji; Zenodo RED-PUMP) wymagają odblokowania hostów:
huggingface.co, hf.co, cdn-lfs.huggingface.co, cas-bridge.xethub.hf.co, zenodo.org.

## Etap 2: analizy pogłębione (notatki 02–05, 20–29 w research_notes/Trading memecoinów backtest/)
- Reguły wyjścia (10 962 kombinacji, walk-forward): 0 zyskownych w okresie testowym, nawet przy zerowych kosztach.
  473 reguły „zarabiały” na danych uczących — klasyczne przeuczenie.
- Cykl życia: 67% tokenów ma szczyt w pierwszej świecy 15m, 86% w 1 h; mediana po 24 h = 0,65× wejścia;
  powrót do ceny wejścia po −50% tylko 6,6%.
- Kto zarabia: 10,9% portfeli na plusie; 1% portfeli bierze 95% zysku brutto; jednorazowi kupujący −81%;
  boty biorą 53% zysków, ale netto −15%; snajperzy −79%.
- Różnica w wykonaniu: idealnie −7,2%, bot −26,7%, ręcznie −29,2% na transakcję (200 USD). Największy koszt to poślizg ceny.
- Pump i dump: kupno po świecy pumpa → mediana −20% po 1 h, −38% po 4 h; 87% sprzedaży w pumpie robią ci, co kupili wcześniej.
- Wolumen a cena: brak momentum, po +50% odwrócenie; jedyny sygnał (świeca ≥90% zakupów → +17% w 15 min)
  znika przy opóźnieniu o 1 świecę i kłóci się z analizą przepływu zleceń — hipoteza, nie przewaga.
- Przepływ zleceń: 1% transakcji = 52% wolumenu; 14–33% wolumenu to szybkie kupno+sprzedaż tego samego portfela.
- Reżimy: dobre dni się grupują (r≈0,6), ale żaden dzień czerwca nie był zyskowny; stan rynku to hamulec, nie źródło zysku.
- Deweloperzy/insiderzy: historia dewelopera nic nie przewiduje (AUC 0,52); flagi ostrzegawcze działają
  (dev >20% podaży → 62–69% dumpów vs 38% bazowo).
- Cechy z surowych transakcji: brak wiarygodnej przewagi; kolumny gotowego zrzutu danych zawierają podgląd przyszłości
  (AUC 0,93–0,998), więc wynik ML z etapu 1 jest niewiarygodny.
- Starty i calle: model podnosi trafienia 2× z 26% do 45%, ale zysk zależy od założonej straty przy chybieniu;
  opóźnienie wejścia o 20% zamienia calle w stratę (−9%).

## Wniosek końcowy
Na wszystkich dostępnych danych nie ma wiarygodnej, powtarzalnej przewagi dla tradera z zewnątrz.
Dane dobrze mówią, czego NIE robić: nie gonić pumpów, nie kupować tokenów z dużym udziałem dewelopera/snajperów,
nie trzymać przegranych, trzymać małe pozycje względem płynności.

## Etap 3: porównanie z wypowiedziami praktyków (notatka 06_full_sources_practitioners.md)
Źródła przeczytane w całości: klip Cupsey (YouTube JbWa-Jss-18), AMA „In the Trenches” (Satsdats, Wood/notanicecat69,
Logjam, chang_defi, Coyote; streszczenia redakcyjne), podcast Wu Blockchain (TRUMP/MELANIA), wywiad Odaily (Da Gen),
poradniki Substack oraz praca Ding–Luo–Xu (SBFC 2025, 6 000 tokenów pump.fun). Wszystko to deklaracje, poza pracą
empiryczną; nieosiągalne: FullCryptoGuide (HF, 401), podcasty TG (YouTube 429), Memecoin Podcast (brak transkryptów).
- Zgodne z naszymi danymi: zyski tylko przy skrajnej szybkości i wolumenie (Cupsey: setki tokenów dziennie, trzymanie sekundy–godzina;
  Cented: mediana 7 s); kopiowanie szybkich portfeli traci (test cookin.fun na Cented −21,3% vs nasze ok. −23% dla top-20 Kolscan);
  zyski skoncentrowane (Chang: „90% czasu na minusie”; praca SBFC: zwycięzcy to nadreprezentacja twórców i snajperów);
  małe pozycje (Wood ok. 2,5% majątku, Satsdats stała pula do straty); szybkie cięcie strat; wykluczanie dev/bundli/snajperów.
- Sprzeczne: kupowanie dołków („metoda 40%”, „second dip”) — u nas powrót do ceny wejścia po −50% tylko 6,6%,
  a jedyny praktyk z rozpisanymi stratami (Da Gen: GOAT ok. 900 tys. USD, VINE, BROCCOLI) na tym stracił; gonienie wolumenu/narracji.
- Drabinki wyjść (25% przy 3–4x itd.) i „kapitał na 2x”: brak przewagi w naszych 10 962 regułach OOS; praktycy stosują je do
  rzadkich zwycięzców, więc to rachunkowość ryzyka, nie dowód przewagi. Ich własne przykłady działają w obie strony.
- Nieprzetestowane (luki): wejście dopiero po 48 h (Wood), wejście przy kapitalizacji 5–10 mln z wyjściem 9-EMA/1h (Satsdats),
  tylko tokeny po graduacji (Krabs). Nasza próba to świeże tokeny z świecami 15m; ta kohorta wymaga danych o dłuższym horyzoncie.
- Uwaga: liczby transakcji Cupsey są niespójne (78/dzień wg uwuu, ok. 300 tokenów/dzień wg niego, ok. 1 050/dzień wg Gate) — nie cytować pojedynczej.
