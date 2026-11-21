"""
03_classification.py — Classification des ménages/pays à risque de pauvreté élevée
(seuil $3/jour PPA 2021 > 40%, médiane approximative de l'échantillon africain) via Random Forest,
comparé à une régression logistique.

Sortie : reports/classification_report.txt, reports/figures/feature_importance.png,
         reports/figures/roc_curve.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, roc_curve, classification_report

BASE = os.path.join(os.path.dirname(__file__), "..")
IN_PATH = os.path.join(BASE, "data", "processed", "poverty_africa_2000_2023.csv")
REPORT_DIR = os.path.join(BASE, "reports")
FIG_DIR = os.path.join(REPORT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

FEATURES = ["gdp_per_capita", "gini", "inflation", "youth_unemployment",
            "employment_agriculture", "labor_force_participation"]
THRESHOLD = 40  # % de la population sous $3/jour PPA 2021


def run():
    df = pd.read_csv(IN_PATH).dropna(subset=["poverty_rate_300ppp"])
    df["pauvrete_elevee"] = (df["poverty_rate_300ppp"] > THRESHOLD).astype(int)

    feats = [f for f in FEATURES if f in df.columns]
    df_model = df.dropna(subset=feats)
    X, y = df_model[feats], df_model["pauvrete_elevee"]
    print(f"{len(df_model)} observations modélisables, répartition cible:\n{y.value_counts()}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    scaler = StandardScaler()
    X_train_s, X_test_s = scaler.fit_transform(X_train), scaler.transform(X_test)

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "RandomForest": RandomForestClassifier(n_estimators=300, max_depth=8, class_weight="balanced", random_state=42),
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    results = {}
    plt.figure(figsize=(6, 6))
    for name, model in models.items():
        Xtr = X_train_s if name == "LogisticRegression" else X_train
        Xte = X_test_s if name == "LogisticRegression" else X_test
        model.fit(Xtr, y_train)
        proba = model.predict_proba(Xte)[:, 1]
        pred = model.predict(Xte)
        auc = roc_auc_score(y_test, proba)
        cv_scores = cross_val_score(model, Xtr, y_train, cv=cv, scoring="roc_auc")
        results[name] = {"AUC_test": auc, "AUC_cv_mean": cv_scores.mean(), "AUC_cv_std": cv_scores.std()}
        fpr, tpr, _ = roc_curve(y_test, proba)
        plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")
        print(f"=== {name} === {results[name]}")
        print(classification_report(y_test, pred))

    plt.plot([0, 1], [0, 1], "k--")
    plt.xlabel("Taux de faux positifs"); plt.ylabel("Taux de vrais positifs")
    plt.title(f"Courbes ROC — pauvreté élevée (>{THRESHOLD}% sous $3/jour PPA)")
    plt.legend(); plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "roc_curve.png"), dpi=150)
    plt.close()

    best_name = max(results, key=lambda n: results[n]["AUC_test"])
    best_model = models[best_name]
    if hasattr(best_model, "feature_importances_"):
        importances = pd.Series(best_model.feature_importances_, index=feats).sort_values(ascending=False)
        plt.figure(figsize=(7, 5))
        importances.plot(kind="barh", color="crimson")
        plt.gca().invert_yaxis()
        plt.title(f"Facteurs associés à une pauvreté élevée ({best_name})")
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, "feature_importance.png"), dpi=150)
        plt.close()
        print(importances)

    with open(os.path.join(REPORT_DIR, "classification_report.txt"), "w", encoding="utf-8") as f:
        f.write(f"Seuil 'pauvreté élevée' : taux $3/jour PPA 2021 > {THRESHOLD}%\n\n")
        for name, r in results.items():
            f.write(f"{name}: {r}\n")
        f.write(f"\nMeilleur modèle: {best_name}\n")
        if hasattr(best_model, "feature_importances_"):
            f.write("\nFacteurs les plus discriminants:\n" + importances.to_string())

    return results


if __name__ == "__main__":
    run()
