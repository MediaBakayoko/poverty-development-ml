"""
04_clustering.py  -  Classification du niveau de vie des pays africains (clustering K-Means sur
PIB/habitant, pauvreté, Gini, chômage des jeunes, structure de l'emploi) pour construire des
catégories socioéconomiques homogènes.

Sortie : data/processed/country_clusters.csv, reports/cluster_profiles.csv,
         reports/figures/elbow_silhouette.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

BASE = os.path.join(os.path.dirname(__file__), "..")
IN_PATH = os.path.join(BASE, "data", "processed", "poverty_africa_2000_2023.csv")
OUT_DIR = os.path.join(BASE, "data", "processed")
REPORT_DIR = os.path.join(BASE, "reports")
FIG_DIR = os.path.join(REPORT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

CLUSTER_VARS = ["gdp_per_capita", "poverty_rate_300ppp", "gini", "youth_unemployment",
                "employment_agriculture"]


def run():
    df = pd.read_csv(IN_PATH)
    latest = df.sort_values("year").groupby("country").last().reset_index()
    latest_full = latest.dropna(subset=CLUSTER_VARS)
    print(f"{len(latest_full)} pays avec toutes les variables disponibles (dernière année)")

    X = latest_full[CLUSTER_VARS]
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    k_range = range(2, 6)
    inertias, sils = [], []
    for k in k_range:
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(Xs)
        inertias.append(km.inertia_)
        sils.append(silhouette_score(Xs, km.labels_))

    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(list(k_range), inertias, marker="o", color="tab:blue")
    ax1.set_xlabel("k"); ax1.set_ylabel("Inertie", color="tab:blue")
    ax2 = ax1.twinx()
    ax2.plot(list(k_range), sils, marker="s", color="tab:red")
    ax2.set_ylabel("Silhouette", color="tab:red")
    plt.title("Choix du nombre de catégories socioéconomiques")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "elbow_silhouette.png"), dpi=150)
    plt.close()

    best_k = list(k_range)[int(np.argmax(sils))]
    km = KMeans(n_clusters=best_k, n_init=10, random_state=42).fit(Xs)
    latest_full["cluster"] = km.labels_
    latest_full.to_csv(os.path.join(OUT_DIR, "country_clusters.csv"), index=False)

    profiles = latest_full.groupby("cluster")[CLUSTER_VARS + ["country"]].agg(
        {**{v: "mean" for v in CLUSTER_VARS}, "country": lambda x: ", ".join(x)}
    )
    profiles["n_pays"] = latest_full.groupby("cluster").size()
    profiles.to_csv(os.path.join(REPORT_DIR, "cluster_profiles.csv"))
    print(f"k retenu : {best_k}")
    print(profiles[CLUSTER_VARS + ["n_pays"]])
    return latest_full, profiles


if __name__ == "__main__":
    run()
