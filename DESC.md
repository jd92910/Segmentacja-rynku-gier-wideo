# Opis Projektu: Segmentacja Rynku Gier Wideo

## 1. Postawienie problemu (Business & Data Understanding)

Współczesny rynek gier wideo generuje gigantyczne wolumeny danych pochodzących z platform społecznościowych, sklepów cyfrowych oraz serwisów agregujących oceny (np. *Backloggd*). Dane te stanowią cenne źródło informacji dla deweloperów, wydawców i analityków rynkowych. Efektywne wyciąganie wniosków z takich zbiorów napotyka jednak trzy kluczowe bariery:

1. **Niski stopień strukturyzacji i zanieczyszczenie danych:** Dane tekstowe często zawierają zniekształcenia (np. formaty liczbowe typu `17K` zamiast `17000`), duplikaty (wielokrotne wpisy tej samej gry wynikające z różnych edycji lub wersji platformowych) oraz złożone kolekcje zapisane jako zwykły tekst (`"['Adventure', 'RPG']"`).
2. **Problem wielowymiarowości:** Opisanie sukcesu gry wymaga jednoczesnej analizy wielu metryk (oceny, liczba rozegrań, zaangażowanie bieżące, listy życzeń). Człowiek nie jest w stanie efektywnie analizować i wizualizować danych w przestrzeni wielowymiarowej.
3. **Brak naturalnego podziału (Segmentacji):** Gry różnią się modelami biznesowymi – niektóre opierają się na jednorazowym, masowym przejściu historii fabularnej, inne na długofalowym utrzymaniu bazy aktywnych graczy. Bez automatycznych metod uczenia nienadzorowanego ręczne pogrupowanie tysięcy gier o podobnej charakterystyce rynkowej jest niemożliwe.

---

## 2. Opis rozwiązania i sposób implementacji

Projekt wdraża kompletny potok przetwarzania danych (Data Pipeline) podzielony na niezależne moduły w katalogu `src/`:

* **Moduł czyszczenia i inżynierii cech (`data_processing.py`):** Odpowiada za unifikację typów danych. Wykorzystuje moduł `ast` (Abstract Syntax Tree) do bezpiecznego parsowania struktur danych ukrytych w tekście, dokonuje agresywnej deduplikacji unikalnych tytułów (eliminując błędy powtarzających się gier w rankingach) oraz wyznacza zaawansowane wskaźniki rynkowe.
* **Moduł analityczno-komparatywny (`analysis.py`):** Wyznacza liderów rynkowych w obrębie gatunków, najpopularniejszych wydawców oraz buduje zaawansowany wykres porównawczy zaangażowania graczy z wykorzystaniem skali logarytmicznej, co zapobiega spłaszczeniu wykresów w środowiskach nieinteraktywnych.
* **Moduł uczenia nienadzorowanego (`clustering.py`):** Zawiera autorską, napisaną od zera w czystym `NumPy` klasę algorytmu **K-Means**, realizującą automatyczny podział rynku gier na spójne segmenty ekonomiczno-behawioralne bez posiłkowania się gotowymi szablonami z biblioteki `scikit-learn`.

---

## 3. Szczegóły teoretyczno-matematyczne

### 3.1. Inżynieria Cech i Agregacja
W celu zidentyfikowania specyfiki konsumpcji dóbr cyfrowych, w projekcie zaimplementowano wektor całkowitej popularności rynkowej pozycji jako sumę historycznego wolumenu rozegrań oraz potencjału zakupowego na listach życzeń:
$$Popularność = Plays + Wishlist$$

### 3.2. Skalowanie Logarytmiczne w Wizualizacji Komparatywnej
Analiza porównawcza zmiennych `Plays` (liczba historycznych ukończeń gry) oraz `Playing` (liczba graczy aktualnie uruchamiających grę) ujawnia dysproporcje rzędu kilku tysięcy procent. Użycie standardowej skali liniowej spowodowałoby matematyczne "stłamszenie" mniejszych wartości (słupki aktywnej rozgrywki byłyby niewidoczne, zlewając się z osią X). 

W celu zachowania rzetelności wizualizacji, oś rzędnych (Y) poddano transformacji logarytmicznej o podstawie 10:
$$Y_{new} = \log_{10}(Y)$$
Dzięki temu odległości na wykresie odzwierciedlają zmiany rzędów wielkości ($10^2, 10^3, 10^4$), co umożliwia jednoczesną, czytelną ocenę obu metryk na jednym wykresie.

### 3.3. Algorytm K-Means i Inicjalizacja K-Means++
Proces automatycznej segmentacji rynku opiera się na podziale przestrzeni $d$-wymiarowej na $K$ klastrów, dążąc do zminimalizowania wewnątrzklastrowej sumy kwadratów odległości (współczynnika inercji):
$$\arg\min_{\mathbf{S}} \sum_{i=1}^{K} \sum_{\mathbf{x} \in S_i} \left\| \mathbf{x} - \boldsymbol{\mu}_i \right\|^2$$
Gdzie $\boldsymbol{\mu}_i$ to środek (centroid) klastra $S_i$.

Przed uruchomieniem algorytmu dane podlegają **standaryzacji**, czyli wycentrowaniu i przeskalowaniu względem odchylenia standardowego:
$$\mathbf{x}_{scaled} = \frac{\mathbf{x} - \mu}{\sigma}$$
Zabieg ten wyrównuje "wagi" poszczególnych osi, dzięki czemu cechy o wysokich wartościach (np. `plays_count` idące w tysiące) nie dominują nad cechami o małej rozpiętości (np. `rating_num` w skali 0-5).

Standardowy algorytm K-Means cierpi na podatność na losową inicjalizację. Aby temu zapobiec, zaimplementowano ulepszoną metodę **K-Means++**:
1. Pierwszy centroid $\boldsymbol{\mu}_1$ wybierany jest całkowicie losowo z rozkładu jednostajnego.
2. Dla każdego punktu danych $\mathbf{x}$ obliczana jest odległość $D(\mathbf{x})$ do najbliższego, wybranego już centroidu.
3. Wybór kolejnego centroidu $\boldsymbol{\mu}_k$ odbywa się losowo, ale prawdopodobieństwo $P(\mathbf{x})$ wyboru punktu $\mathbf{x}$ jest wprost proporcjonalne do kwadratu jego odległości:
$$P(\mathbf{x}) = \frac{D(\mathbf{x})^2}{\sum_{\mathbf{x}' \in X} D(\mathbf{x}')^2}$$

Dzięki temu początkowe punkty skupień są maksymalnie od siebie oddalone geometrycznie, co drastycznie przyspiesza zbieżność algorytmu i zapobiega uwięzieniu w lokalnych minimach funkcji kosztu.

---

## 4. Interpretacja Wyników Działania Programu

Program na bazie czyszczenia danych eliminuje anomalie wielokrotnego zliczania tego samego tytułu, dostarczając precyzyjne wyniki:
* **Rankingi popularności:** Wykazują dominację rynkową tytułów globalnych o charakterze piaskownicy (*Minecraft*) oraz otwartych światów akcji (*GTA V*, *Zelda*).
* **Segmentacja K-Means:** Wyodrębnia trzy kluczowe klastry biznesowe:
  * *Klaster 0: Elita Rynkowa (Blockbustery)* – Gry o ekstremalnie wysokiej liczbie rozegrań, potężnym zaangażowaniu społecznym i bardzo dobrych ocenach.
  * *Klaster 1: Gry Kultowe/Niszowe* – Tytuły o umiarkowanym zasięgu masowym, ale najwyższych ocenach od lojalnej społeczności.
  * *Klaster 2: Średnia Rynkowa / Masowa Produkcja* – Gry o standardowym, niższym zaangażowaniu i przeciętnych ocenach (0-3).