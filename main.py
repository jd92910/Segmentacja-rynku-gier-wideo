from src.data_processing import wczytaj_i_oczyszczaj_dane
from src.analysis import generuj_raporty_i_wykres

def main():
    # Ścieżka do pliku z danymi umieszczonego w strukturze projektu
    sciezka_danych = 'data/games.csv'
    
    # 1. Pipeline przetwarzania i oczyszczania (w tym usunięcie duplikatów Minecrafta)
    df_czyste = wczytaj_i_oczyszczaj_dane(sciezka_danych)
    
    # 2. Generowanie raportów biznesowych oraz wykresu logarytmicznego
    generuj_raporty_i_wykres(df_czyste, wybrany_gatunek='RPG')

if __name__ == '__main__':
    main()