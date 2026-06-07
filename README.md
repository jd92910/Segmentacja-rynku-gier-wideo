# Segmentacja rynku gier wideo oraz analiza trendów

Kompleksowy projekt z zakresu Data Science i uczenia nienadzorowanego, realizujący pełny potok przetwarzania (Pipeline) na bazie rzeczywistych danych rynkowych z serwisu *Backloggd* (`games.csv`). Projekt łączy techniki inżynierii cech, redukcji wymiarowości oraz zaawansowanej agregacji biznesowej.

## 📂 Struktura Projektu i Główne Moduły

* **`data_processing.py` (Inżynieria Cech & Czyszczenie):** Automatyczna konwersja danych tekstowych, usuwanie anomalii zapisu (np. formaty liczbowe typu `17K`), bezpieczne parsowanie list strukturalnych za pomocą modułu `ast` oraz obliczanie średnich kroczących w oknach czasowych.
* **`dimensionality_reduction.py` (Redukcja Wymiarowości):** Własna, niskopoziomowa implementacja algorytmu PCA oparta na rozkładzie zmiennych osobliwych (SVD): $X = U \Sigma V^T$.
* **`main.py` (Potok Statystyczno-Analityczny):** Główny moduł wykonawczy odpowiedzialny za deduplikację danych, generowanie zestawień biznesowych oraz eksport zaawansowanych wykresów porównawczych.

---

## 📊 Zakres Przeprowadzanych Analiz Biznesowych

Skrypt po wczytaniu danych automatycznie przeprowadza czyszczenie bazy z duplikatów edycyjnych i platformowych (`.drop_duplicates()`), a następnie wyznacza:

1. **Najpopularniejszy Tytuł z Wybranego Gatunku:** Identyfikacja lidera rynkowego w obrębie zdefiniowanej kategorii (domyślnie: `RPG`) na podstawie autorskiego wskaźnika ogólnej popularności:
   $$Popularność = Plays + Wishlist$$
2. **Top 10 Najczęściej Rozegranych Tieli:** Globalne zestawienie unikalnych gier o największym historycznym wolumenie ukończonych rozgrywek.
3. **Top 5 Studiów Deweloperskich:** Ranking producentów i wydawców gier (kolumna `Team`), których produkcje osiągnęły najwyższy skumulowany sukces komercyjny.

---

## 📈 Wizualizacja Różnic Rynkowych (Plays vs Playing)

W ramach projektu generowany jest zaawansowany, grupowany wykres słupkowy (`porownanie_plays_playing_poprawne.png`) prezentujący dysproporcję pomiędzy zaangażowaniem historycznym a bieżącym dla 10 najpopularniejszych gier świata.

### Kluczowe aspekty techniczne wykresu:
* **Skala Logarytmiczna ($\log_{10}$):** Zastosowana na osi Y ze względu na kolosalne różnice w rzędach wielkości danych (wartości `Plays` są często od 10 do 50 razy większe od zmiennej `Playing`). Zastosowanie tej skali chroni wykres przed spłaszczeniem mniejszych słupków i pozwala na rzetelne porównanie cech.
* **Optymalizacja Pozycji Słupków:** Słupki są rysowane obok siebie z przesunięciem o wektor $\pm \frac{width}{2}$, co zapewnia pełną czytelność porównawczą.
* **Odporność Środowiskowa:** Wykres jest bezpośrednio eksportowany do pliku bez wymogu posiadania interaktywnego backendu graficznego systemu operacyjnego (brak błędów typu `FigureCanvasAgg`).

---

## 🛠️ Instrukcja Uruchomienia

1. Zainstaluj wymagane zależności systemowe i pythonowe:
   ```bash
   pip install numpy pandas scipy matplotlib scikit-learn