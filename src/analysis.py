import numpy as np
import matplotlib.pyplot as plt

def generuj_raporty_i_wykres(df_unikalne, wybrany_gatunek='RPG'):
    """Wyznacza rankingi z unikalnych danych i generuje logarytmiczny wykres słupkowy"""
    
    # A. Najpopularniejsza gra z wyznaczonego gatunku
    df_gatunek = df_unikalne[df_unikalne['glowny_gatunek'].str.lower() == wybrany_gatunek.lower()]
    if not df_gatunek.empty:
        najpopularniejsza = df_gatunek.sort_values(by='ogolna_popularnosc', ascending=False).iloc[0]
        print(f"\n[A] Najpopularniejsza unikalna gra z gatunku '{wybrany_gatunek}':")
        print(f"    -> Tytuł: {najpopularniejsza['Title']}")
        print(f"    -> Liczba rozegrań (Plays): {int(najpopularniejsza['plays_count'])}")
        print(f"    -> Ocena: {najpopularniejsza['rating_num']}/5")

    # B. Top 10 najczęściej rozegranych gier ogółem
    top10 = df_unikalne.sort_values(by='plays_count', ascending=False).head(10).reset_index(drop=True)
    print("\n[B] Poprawione Top 10 najczęściej rozegranych gier ogółem (unikalne tytuły):")
    for idx, row in top10.iterrows():
        print(f"    {idx+1}. {row['Title']} — {int(row['plays_count'])} rozegrań")

    # C. Top 5 firm z najpopularniejszymi grami
    df_firmy = df_unikalne[df_unikalne['glowna_firma'] != 'Nieznane']
    top5_firm = (df_firmy.groupby('glowna_firma')['ogolna_popularnosc']
                 .sum()
                 .reset_index()
                 .sort_values(by='ogolna_popularnosc', ascending=False)
                 .head(5))
    print("\n[C] Top 5 firm/studiów deweloperskich (na bazie unikalnych gier):")
    for idx, row in top5_firm.reset_index(drop=True).iterrows():
        print(f"    {idx+1}. {row['glowna_firma']}")

    # D. Wykres różnic (Plays vs Playing) z użyciem skali logarytmicznej
    tytuly_skrocone = [t[:18] + '...' if len(t) > 18 else t for t in top10['Title']]
    x = np.arange(len(tytuly_skrocone))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, top10['plays_count'], width, label='Ukończone / Rozegrane (Plays)', color='#1f77b4')
    ax.bar(x + width/2, top10['playing_count'], width, label='Wciąż grane (Playing)', color='#ff7f0e')
    
    ax.set_title('Porównanie liczby gier rozegranych do wciąż granych — POPRAWIONE TOP 10', fontsize=14, pad=15)
    ax.set_xlabel('Tytuł gry', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(tytuly_skrocone, rotation=25, ha='right')
    ax.legend(fontsize=11)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    
    # Kluczowa skala logarytmiczna z teorii matematycznej projektu
    ax.set_yscale('log')
    ax.set_ylabel('Liczba operacji/graczy (Skala logarytmiczna)', fontsize=12)

    plt.tight_layout()
    plt.savefig('porownanie_plays_playing.png', dpi=300)
    print(f"\n[D] Poprawny wykres został zapisany jako plik: 'porownanie_plays_playing.png'")
    plt.close()