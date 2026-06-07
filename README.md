# Segmentacja Rynku Gier Wideo — Instrukcja Uruchomienia

Projekt realizuje potok przetwarzania danych (Data Pipeline) oraz analizę statystyczno-komparatywną rynku gier wideo (1980–2023) na podstawie danych z serwisu *Backloggd*.

## 🛠️ Wymagania Środowiskowe
Projekt został przygotowany w języku **Python 3.8+** i wymaga instalacji standardowych bibliotek do analizy danych.

### Wymagane pakiety:
* `numpy` (wersja >= 1.20) - operacje macierzowe i implementacja SVD
* `pandas` (wersja >= 1.3) - wczytywanie i agregacja danych tabelarycznych
* `scipy` (wersja >= 1.7) - obliczenia numeryczne (rozkład zmiennych osobliwych)
* `matplotlib` (wersja >= 3.4) - generowanie wykresów statystycznych

## 🚀 Instalacja i Uruchomienie

1. **Klonowanie/Wejście do katalogu projektu:**
   ```bash
   cd /home/yanoosh/Dokumenty/Dane_AI/Segmentacja-rynku-gier-wideo/
   ```
2. **Stworzenie środowiska i uruchomienie**
    ```bash
    python3 -m venv .env
    source .env/bin/activate
    ```
3. **Instalacja zależności za pomocą managera pakietów pip:**
    ```bash
    pip install numpy pandas scipy matplotlib
    ```
4. **Uruchomienie głównego programu:**
    ```bash
    python3 main.py
    ```