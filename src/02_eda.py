"""
02_eda.py  -  Analyse exploratoire du panel pauvreté/développement Afrique (2000-2023).
Sortie : reports/figures/poverty_trend.png, distributions.png, correlation_heatmap.png,
         gini_vs_poverty.png
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BASE = os.path.join(os.path.dirname(__file__), "..")
IN_PATH = os.path.join(BASE, "data", "processed", "poverty_africa_2000_2023.csv")
FIG_DIR = os.path.join(BASE, "reports", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

NUM_COLS = ["poverty_rate_300ppp", "gini", "gdp_per_capita", "inflation",
            "youth_unemployment", "employment_agriculture"]


def run():
    df = pd.read_csv(IN_PATH)
    print(f"{df.shape[0]} observations pays-année, {df['country'].nunique()} pays")

    trend = df.groupby("year")["poverty_rate_300ppp"].mean()
    plt.figure(figsize=(8, 5))
    plt.plot(trend.index, trend.values, marker="o", color="firebrick")
    plt.title("Taux de pauvreté moyen ($3/j PPA 2021)  -  Afrique")
    plt.xlabel("Année"); plt.ylabel("Taux de pauvreté (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "poverty_trend.png"), dpi=150)
    plt.close()

    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    for ax, col in zip(axes.flat, NUM_COLS):
        sns.histplot(df[col].dropna(), kde=True, ax=ax, color="darkcyan")
        ax.set_title(col)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "distributions.png"), dpi=130)
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.heatmap(df[NUM_COLS].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Corrélations  -  pauvreté, inégalités et facteurs économiques")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "correlation_heatmap.png"), dpi=150)
    plt.close()

    # Rappel méthodologique : Gini (inégalité relative) vs taux de pauvreté (absolu)  -  pas identiques
    gini_pov = df.dropna(subset=["gini", "poverty_rate_300ppp"])
    plt.figure(figsize=(7, 7))
    plt.scatter(gini_pov["gini"], gini_pov["poverty_rate_300ppp"], alpha=0.6, color="slateblue")
    plt.xlabel("Indice de Gini (inégalité de revenu)")
    plt.ylabel("Taux de pauvreté ($3/j PPA 2021, %)")
    plt.title("Gini vs taux de pauvreté  -  des concepts distincts\n(corrélation imparfaite attendue)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "gini_vs_poverty.png"), dpi=150)
    plt.close()
    print(f"Corrélation Gini / taux de pauvreté : {gini_pov['gini'].corr(gini_pov['poverty_rate_300ppp']):.3f}")

    return df


if __name__ == "__main__":
    run()
