import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import svd

# =====================================================================
# KROK 1: Analiza eksploracyjna i inżynieria cech (Wzorowane na COVID/Olympics)
# =====================================================================

# 1.1. Ładowanie przykładowych danych (symulacja pobranego zbioru z Kaggle)
# W rzeczywistym projekcie użyjesz: pd.read_csv('popular_video_games.csv')
np.random.seed(42)
n_games = 500

data = {
    'game_id': range(1, n_games + 1),
    'title': [f'Game_{i}' for i in range(1, n_games + 1)],
    'release_year': np.random.randint(1980, 2024, size=n_games),
    'user_rating': np.random.uniform(1.0, 10.0, size=n_games),
    'critic_rating': np.random.uniform(10.0, 100.0, size=n_games),
    'plays_count': np.random.exponential(scale=100000, size=n_games),
    'wishlist_count': np.random.exponential(scale=20000, size=n_games),
    'genre': np.random.choice(['RPG', 'Action', 'Strategy', 'Sports', 'Indie'], size=n_games)
}
df = pd.DataFrame(data)

# 1.2. Inżynieria cech - Obliczanie metryk dynamiki i popularności
# Sortujemy po roku, aby poprawnie obliczyć okna czasowe (podobnie jak w zadaniu z COVID)
df = df.sort_values('release_year').reset_index(drop=True)

# Obliczamy średnią kroczącą (rolling) ocen użytkowników w oknie 3-letnim
# Jeśli w oknie brakuje danych, wstawiamy NaN (zgodnie z wytycznymi z zadań)
df['rating_trend_3y'] = df['user_rating'].rolling(window=3, min_periods=3).mean()

# Definiujemy miarę "sharpness" (ostrości/skoku) popularności gry 
# jako stosunek jej liczby dodań do wishlisty do mediany w danym gatunku
genre_medians = df.groupby('genre')['wishlist_count'].transform('median')
df['popularity_sharpness'] = df['wishlist_count'] / genre_medians

# Czyszczenie braków powstałych w wyniku operacji okienkowych
df = df.dropna().reset_index(drop=True)

print("--- KROK 1: Przykładowe przetworzone dane ---")
print(df[['title', 'genre', 'rating_trend_3y', 'popularity_sharpness']].head())


# =====================================================================
# KROK 2: Redukcja wymiarowości za pomocą SVD (Wzorowane na PCA/Digits)
# =====================================================================

# 2.1. Przygotowanie macierzy cech X (tylko zmienne numeryczne)
features = ['user_rating', 'critic_rating', 'plays_count', 'wishlist_count', 'rating_trend_3y', 'popularity_sharpness']
X = df[features].to_numpy()

# 2.2. Standaryzacja danych (odejmowanie średniej i dzielenie przez odchylenie standardowe)
# W zadaniu z Digits wymagane było samo centrowanie, tutaj ze względu na różne skale cech
# (np. rating vs plays_count) stosujemy pełną standaryzację (jak w zadaniu Wine)
X_mean = np.mean(X, axis=0)
X_std = np.std(X, axis=0)
X_scaled = (X - X_mean) / X_std

# 2.3. Własna implementacja PCA przy użyciu rozkładu SVD: X = U * S * Vt
U, S, Vt = svd(X_scaled, full_matrices=False)

# Współrzędne próbek w przestrzeni PCA (rzutowanie na główne składowe)
# X_pca = U * S  lub  X_scaled * V (gdzie V to transpozycja Vt)
V = Vt.T
X_pca = X_scaled @ V

# 2.4. Obliczanie wariancji wyjaśnianej przez kolejne składowe
n_samples = X.shape[0]
explained_variance = (S ** 2) / (n_samples - 1)
total_variance = np.sum(explained_variance)
explained_variance_ratio = explained_variance / total_variance
cumulative_variance = np.cumsum(explained_variance_ratio)

print("\n--- KROK 2: Analiza PCA (SVD) ---")
for i, ratio in enumerate(explained_variance_ratio):
    print(f"PC{i+1}: wyjaśnia {ratio*100:.2f}% wariancji (skumulowana: {cumulative_variance[i]*100:.2f}%)")

# 2.5. Wyznaczenie liczby składowych dla progów 80% i 90%
for threshold in [0.80, 0.90]:
    n_components = np.argmax(cumulative_variance >= threshold) + 1
    print(f"Liczba składowych potrzebna do wyjaśnienia {threshold*100:.0f}% wariancji: {n_components}")

# 2.6. Wizualizacja: Wykres punktowy PC1 i PC2 z podziałem na gatunki gier
plt.figure(figsize=(10, 6))
genres = df['genre'].unique()

for genre in genres:
    indices = df['genre'] == genre
    plt.scatter(X_pca[indices, 0], X_pca[indices, 1], label=genre, alpha=0.7, edgecolors='k')

plt.title('Rzutowanie gier wideo na przestrzeń dwóch pierwszych składowych głównych (PC1 vs PC2)')
plt.xlabel(f'PC1 ({explained_variance_ratio[0]*100:.1f}%)')
plt.ylabel(f'PC2 ({explained_variance_ratio[1]*100:.1f}%)')
plt.legend(title='Gatunek gry')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()