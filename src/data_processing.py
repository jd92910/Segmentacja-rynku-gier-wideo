import ast
import pandas as pd

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
    """Bezpiecznie wyciąga pierwszy element z tekstowego zapisu listy w Pythonie za pomocą AST"""
    if pd.isna(tekst_listy) or tekst_listy.strip() == "" or tekst_listy == "[]":
        return "Nieznane"
    try:
        lista = ast.literal_eval(tekst_listy)
        if isinstance(lista, list) and len(lista) > 0:
            return lista[0]
    except (ValueError, SyntaxError):
        pass
    return "Nieznane"

def wczytaj_i_oczyszczaj_dane(sciezka_do_pliku):
    """Wczytuje plik i przygotowuje unikalny zestaw gier z wyczyszczonymi metrykami"""
    df = pd.read_csv(sciezka_do_pliku)
    
    # Czyszczenie zmiennych numerycznych
    df['plays_count'] = df['Plays'].apply(czysc_wartosc_k)
    df['playing_count'] = df['Playing'].apply(czysc_wartosc_k)
    df['wishlist_count'] = df['Wishlist'].apply(czysc_wartosc_k)
    df['rating_num'] = pd.to_numeric(df['Rating'], errors='coerce')
    
    # Ekstrakcja z list tekstowych tekstów (z użyciem modułu ast)
    df['glowny_gatunek'] = df['Genres'].apply(wyciagnij_pierwszy_element)
    df['glowna_firma'] = df['Team'].apply(wyciagnij_pierwszy_element)
    
    df = df.dropna(subset=['Title']).reset_index(drop=True)
    df['ogolna_popularnosc'] = df['plays_count'] + df['wishlist_count']
    
    # Deduplikacja na poziomie tytułów gier
    df_unikalne = df.drop_duplicates(subset=['Title'], keep='first').copy()
    return df_unikalne