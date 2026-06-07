import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def czysc_wartosc_k(wartosc):
    """Konwertuje stringi typu '17K' na liczby float 17000.0"""
    if pd.isna(wartosc):
        return 0.0
    wartosc_str = str(wartosc).strip().upper()
    if 'K' in wartosc_str:
        try:
            return float(wartosc_str.replace('K', '')) * 1000
        except ValueError:
            return 0.0
    try:
        return float(wartosc_str)
    except ValueError:
        return 0.0

def wyciagnij_pierwszy_element(tekst_listy):
    """Bezpiecznie wyciąga pierwszy element z tekstowego zapisu listy w Pythonie"""
    if pd.isna(tekst_listy) or tekst_listy.strip() == "" or tekst_listy == "[]":
        return "Nieznane"
    try:
        lista = ast.literal_eval(tekst_listy)
        if isinstance(lista, list) and len(lista) > 0:
            return lista[0]
    except (ValueError, SyntaxError):
        pass
    return "Nieznane"

def przeprowadz_analize_rynkowa(sciezka_do_pliku, wybrany_gatunek='RPG'):
    """
    Wykonuje agregacje danych eliminując zduplikowane tytuły gier.
    Generuje poprawne statystyki oraz czytelny wykres.
    """
    print(f"--- ROZPOCZĘCIE ANALIZY STATYSTYCZNEJ (Z USUWANIEM DUPLIKATÓW) ---")
    
    # 1. Wczytanie i czyszczenie podstawowych typów danych
    df = pd.read_csv(sciezka_do_pliku)
    
    df['plays_count'] = df['Plays'].apply(czysc_wartosc_k)
    df['playing_count'] = df['Playing'].apply(czysc_wartosc_k)
    df['wishlist_count'] = df['Wishlist'].apply(czysc_wartosc_k)
    df['rating_num'] = pd.to_numeric(df['Rating'], errors='coerce')
    
    df['glowny_gatunek'] = df['Genres'].apply(wyciagnij_pierwszy_element)
    df['glowna_firma'] = df['Team'].apply(wyciagnij_pierwszy_element)
    
    df = df.dropna(subset=['Title']).reset_index(drop=True)
    df['ogolna_popularnosc'] = df['plays_count'] + df['wishlist_count']

    df_unikalne = df.drop_duplicates(subset=['Title'], keep='first').copy()
    print(f"Liczba wierszy przed usunięciem duplikatów: {len(df)}")
    print(f"Liczba unikalnych tytułów gier w bazie: {len(df_unikalne)}")

    # ZADANIE A: Najpopularniejsza gra z wyznaczonego gatunku (na danych unikalnych)
    df_gatunek = df_unikalne[df_unikalne['glowny_gatunek'].str.lower() == wybrany_gatunek.lower()]
    
    if not df_gatunek.empty:
        najpopularniejsza_w_gatunku = df_gatunek.sort_values(by='ogolna_popularnosc', ascending=False).iloc[0]
        print(f"\n[A] Najpopularniejsza unikalna gra z gatunku '{wybrany_gatunek}':")
        print(f"    -> Tytuł: {najpopularniejsza_w_gatunku['Title']}")
        print(f"    -> Liczba rozegrań (Plays): {int(najpopularniejsza_w_gatunku['plays_count'])}")
        print(f"    -> Ocena: {najpopularniejsza_w_gatunku['rating_num']}/5")
    else:
        print(f"\n[A] Nie znaleziono gier z gatunku '{wybrany_gatunek}'")

    # ZADANIE B: POPRAWIONE Top 10 najczęściej rozegranych gier (bez powtórzeń)
    top10_rozegranych = df_unikalne.sort_values(by='plays_count', ascending=False).head(10).reset_index(drop=True)
    
    print("\n[B] Poprawione Top 10 najczęściej rozegranych gier ogółem (unikalne tytuły):")
    for idx, row in top10_rozegranych.iterrows():
        print(f"    {idx+1}. {row['Title']} — {int(row['plays_count'])} rozegrań")

    # ZADANIE C: Top 5 firm z najpopularniejszymi grami
    df_firmy = df_unikalne[df_unikalne['glowna_firma'] != 'Nieznane']
    top5_firm = (df_firmy.groupby('glowna_firma')['ogolna_popularnosc']
                 .sum()
                 .reset_index()
                 .sort_values(by='ogolna_popularnosc', ascending=False)
                 .head(5))
    
    print("\n[C] Top 5 firm/studiów deweloperskich (na bazie unikalnych gier):")
    for idx, row in top5_firm.reset_index(drop=True).iterrows():
        print(f"    {idx+1}. {row['glowna_firma']}")

    # ZADANIE D: Wykres różnic (Plays vs Playing) dla NOWEGO, poprawnego Top 10
    tytuly = top10_rozegranych['Title'].tolist()
    rozegrane = top10_rozegranych['plays_count'].to_numpy()
    w_trakcie = top10_rozegranych['playing_count'].to_numpy()
    
    # Formatowanie nazw pod wykres, żeby tekst na siebie nie nachodził
    tytuly_skrocone = [t[:18] + '...' if len(t) > 18 else t for t in tytuly]
    
    x = np.arange(len(tytuly_skrocone))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    rects1 = ax.bar(x - width/2, rozegrane, width, label='Ukończone / Rozegrane (Plays)', color='#1f77b4')
    rects2 = ax.bar(x + width/2, w_trakcie, width, label='Wciąż grane (Playing)', color='#ff7f0e')
    
    ax.set_title('Porównanie liczby gier rozegranych do wciąż granych — POPRAWIONE TOP 10', fontsize=14, pad=15)
    ax.set_xlabel('Tytuł gry', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(tytuly_skrocone, rotation=25, ha='right')
    ax.legend(fontsize=11)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    
    # Skala logarytmiczna chroni wykres przed spłaszczeniem małych wartości "Playing"
    ax.set_yscale('log')
    ax.set_ylabel('Liczba operacji/graczy (Skala logarytmiczna)', fontsize=12)

    plt.tight_layout()
    
    nazwa_wykresu = 'porownanie_plays_playing.png'
    plt.savefig(nazwa_wykresu, dpi=300)
    print(f"\n[D] Poprawny wykres został zapisany jako plik: '{nazwa_wykresu}'")
    plt.close()

def main():
    przeprowadz_analize_rynkowa('games.csv', 'RPG')

if __name__ == "__main__":
    main()