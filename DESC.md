# Opis Projektu: Segmentacja Rynku Gier Wideo

## 1. Postawienie problemu
Branża gier wideo generuje ogromne ilości danych tekstowo-numerycznych dotyczących ocen, zaangażowania graczy czy list życzeń. Analiza tych danych napotyka dwa główne problemy:
1. **Zanieczyszczenie i niespójność danych:** Dane pobierane z platform społecznościowych zawierają duplikaty (różne edycje tej samej gry), skróty tekstowe (np. "17K" zamiast 17000) oraz struktury złożone ukryte w tekście (listy gatunków/twórców).
2. **Wielowymiarowość przestrzeni cech:** Ręczna ocena gry na podstawie 7 różnych metryk jednocześnie jest nieczytelna dla człowieka.

Celem projektu jest oczyszczenie potoku danych, automatyczna ekstrakcja kluczowych wskaźników biznesowych (Top gier, Top deweloperów), a także redukcja wymiarowości przestrzeni cech w celu umożliwienia wizualizacji złożonych struktur rynkowych na płaszczyźnie dwuwymiarowej.

## 2. Opis rozwiązania i sposób implementacji
Projekt został podzielony na niezależne moduły zlokalizowane w katalogu `src/`:
* **Potok czyszczący (`data_processing.py`):** Wykorzystuje moduł `ast` (Abstract Syntax Tree) do bezpiecznej interpretacji struktur tekstowych jako natywnych list Pythona. Przeprowadza deduplikację danych w oparciu o unikalność tytułów, eliminując zakłamania w rankingach popularności.
* **Moduł analityczny (`analysis.py`):** Realizuje operacje agregacji danych grupowych (`groupby`), wyznacza liderów rynkowych oraz generuje zaawansowany wykres słupkowy.

## 3. Szczegóły teoretyczno-matematyczne

### Inżynieria cech (Feature Engineering)
Wzorując się na analizach okienkowych, wprowadzono cechę `rating_trend_3y`, wykorzystującą średnią kroczącą w 3-letnim oknie chronologicznym. Ponadto zaimplementowano wskaźnik ostrości popularności (`popularity_sharpness`), dany wzorem:
$$sharpness = \frac{wishlist\_count}{mediana(wishlist\_count\_w\_danym\_gatunku)}$$

### Redukcja wymiarowości (PCA przez SVD)
Aby przenieść wielowymiarowe cechy na wykres 2D, dane są najpierw standaryzowane (odejmujemy średnią $\mu$ i dzielimy przez odchylenie standardowe $\sigma$). Następnie macierz danych $X$ poddawana jest nisko-poziomowemu rozkładowi na wartości osobliwe (SVD):
$$X = U \cdot S \cdot V^T$$
Gdzie:
* $U$ - macierz lewych wektorów osobliwych (powiązanie próbek ze składowymi),
* $S$ - macierz diagonalna zawierająca wartości osobliwe, odzwierciedlające poziom wariancji,
* $V^T$ - macierz prawych wektorów osobliwych (kierunki nowych osi współrzędnych).

Wariancja wyjaśniana przez pojedynczą składową $i$ obliczana jest według wzoru:
$$explained\_variance\_i = \frac{S_i^2}{n - 1}$$
Rzutowanie danych na nową przestrzeń (współrzędne PCA) realizowane jest poprzez mnożenie macierzyste wycentrowanych danych przez macierz przejścia $V$: $X_{pca} = X_{scaled} \cdot V$.

### Wykres w skali logarytmicznej
Porównanie gier rozegranych (`Plays`) i aktualnie granych (`Playing`) wykazuje dysproporcje rzędu kilku tysięcy procent. Tradycyjna skala liniowa spłaszczyłaby mniejsze wartości do zera. Zastosowano skalowanie logarytmiczne osi Y:
$$Y_{log} = \log_{10}(Y)$$
Dzięki czemu rzędy wielkości $10^2$ (setki graczy) oraz $10^4$ (dziesiątki tysięcy graczy) są równie dobrze widoczne na jednym wykresie.