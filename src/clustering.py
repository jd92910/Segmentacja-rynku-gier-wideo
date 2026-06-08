import numpy as np
import pandas as pd
from src.data_processing import wczytaj_i_oczyszczaj_dane

class WlasnyKMeans:
    def __init__(self, n_clusters=3, max_iter=300, tol=1e-4):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.centroids = None
        self.labels = None

    def _inicjalizuj_kmeans_plus_plus(self, X):
        n_samples, n_features = X.shape
        centroids = np.empty((self.n_clusters, n_features))
        
        pierwszy_idx = np.random.randint(0, n_samples)
        centroids[0] = X[pierwszy_idx]
        
        for k in range(1, self.n_clusters):
            odleglosci_kwadrat = np.zeros(n_samples)
            for i in range(n_samples):
                roznice = centroids[:k] - X[i]
                odleglosci_do_k = np.sum(roznice**2, axis=1)
                odleglosci_kwadrat[i] = np.min(odleglosci_do_k)
            
            suma_odleglosci = np.sum(odleglosci_kwadrat)
            if suma_odleglosci == 0:
                prawdopodobieństwa = np.ones(n_samples) / n_samples
            else:
                prawdopodobieństwa = odleglosci_kwadrat / suma_odleglosci
                
            nastepny_idx = np.random.choice(n_samples, p=prawdopodobieństwa)
            centroids[k] = X[nastepny_idx]
            
        return centroids

    def fit(self, X):
        self.centroids = self._inicjalizuj_kmeans_plus_plus(X)
        
        for _ in range(self.max_iter):
            stare_centroids = self.centroids.copy()
            
            macierz_odleglosci = np.zeros((X.shape[0], self.n_clusters))
            for k in range(self.n_clusters):
                roznice = X - self.centroids[k]
                macierz_odleglosci[:, k] = np.sum(roznice**2, axis=1)
            
            self.labels = np.argmin(macierz_odleglosci, axis=1)
            
            for k in range(self.n_clusters):
                indeksy_klastra = (self.labels == k)
                if np.sum(indeksy_klastra) > 0:
                    self.centroids[k] = np.mean(X[indeksy_klastra], axis=0)
            
            if np.all(np.sqrt(np.sum((self.centroids - stare_centroids)**2, axis=1)) < self.tol):
                break
                
        return self

def przeprowadz_segmentacje_rynku(df_unikalne):
    cechy = ['rating_num', 'plays_count', 'wishlist_count']
    X = df_unikalne[cechy].dropna().to_numpy()
    
    X_mean = np.mean(X, axis=0)
    X_std = np.std(X, axis=0)
    X_std[X_std == 0] = 1.0
    X_scaled = (X - X_mean) / X_std
    
    model = WlasnyKMeans(n_clusters=3)
    model.fit(X_scaled)
    
    df_wynik = df_unikalne.dropna(subset=cechy).copy()
    df_wynik['cluster'] = model.labels
    
    print("\n--- WYNIKI SEGMENTACJI RYNKOWEJ K-MEANS ---")
    for k in range(3):
        klaster_gier = df_wynik[df_wynik['cluster'] == k]
        print(f"\n[Klaster {k}] Liczba gier: {len(klaster_gier)}")
        print(f"  -> Średnia ocena: {klaster_gier['rating_num'].mean():.2f}/5")
        print(f"  -> Średnia liczba rozegrań: {int(klaster_gier['plays_count'].mean())}")
        print(f"  -> Przykładowe gry: {klaster_gier['Title'].head(3).tolist()}")
        
    return df_wynik