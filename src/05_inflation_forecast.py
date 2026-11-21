"""
05_inflation_forecast.py — Prévision de l'inflation (séries temporelles) pour quelques pays
représentatifs, via lissage exponentiel de Holt (tendance), en complément d'une analyse de la
volatilité inflationniste continentale.

Sortie : reports/figures/inflation_forecast.png, reports/inflation_summary.txt
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

BASE = os.path.join(os.path.dirname(__file__), "..")
IN_PATH = os.path.join(BASE, "data", "processed", "poverty_africa_2000_2023.csv")
REPORT_DIR = os.path.join(BASE, "reports")
FIG_DIR = os.path.join(REPORT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

FOCUS_COUNTRIES = ["CIV", "NGA", "ZAF", "EGY", "KEN", "GHA"]
FORECAST_HORIZON = 5


def run():
    df = pd.read_csv(IN_PATH).dropna(subset=["inflation"])

    fig, axes = plt.subplots(2, 3, figsize=(18, 9))
    summary_lines = []
    for ax, country in zip(axes.flat, FOCUS_COUNTRIES):
        sub = df[df["country"] == country].sort_values("year")
        if len(sub) < 8:
            ax.set_visible(False)
            continue
        series = sub.set_index("year")["inflation"]
        years_index = series.index.to_list()
        series_reset = series.reset_index(drop=True)  # index RangeInt pour éviter l'avertissement statsmodels

        try:
            model = ExponentialSmoothing(series_reset, trend="add", damped_trend=True).fit()
            forecast = model.forecast(FORECAST_HORIZON)
            last_year = years_index[-1]
            forecast_years = range(last_year + 1, last_year + 1 + FORECAST_HORIZON)

            ax.plot(series.index, series.values, marker="o", label="Observé", color="steelblue")
            ax.plot(list(forecast_years), forecast.values, marker="s", linestyle="--",
                    label="Prévision", color="darkorange")
            ax.set_title(country)
            ax.legend(fontsize=8)
            summary_lines.append(f"{country}: inflation {last_year}={series.iloc[-1]:.1f}%, "
                                  f"prévision {last_year+FORECAST_HORIZON}={forecast.iloc[-1]:.1f}%")
        except Exception as e:
            ax.set_visible(False)
            summary_lines.append(f"{country}: échec du modèle ({e})")

    plt.suptitle("Prévision de l'inflation (lissage exponentiel de Holt amorti)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "inflation_forecast.png"), dpi=150)
    plt.close()

    with open(os.path.join(REPORT_DIR, "inflation_summary.txt"), "w", encoding="utf-8") as f:
        f.write("Prévisions d'inflation par pays (horizon 5 ans, Holt amorti):\n\n")
        f.write("\n".join(summary_lines))
    print("\n".join(summary_lines))
    return summary_lines


if __name__ == "__main__":
    run()
