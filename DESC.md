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

