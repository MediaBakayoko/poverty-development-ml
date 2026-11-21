"""
01_build_dataset.py — Construit le panel pays-année Afrique sur la pauvreté, les inégalités
(Gini), le chômage des jeunes, l'inflation et la structure de l'emploi.

Source : World Bank Open Data API, accès libre sans inscription.
    https://api.worldbank.org/v2/country/all/indicator/<CODE>?format=json

Indicateurs :
    SI.POV.NAHC   : taux de pauvreté au seuil national (%)
    SI.POV.DDAY   : taux de pauvreté au seuil $3.00/jour PPA 2021 (%) — cible principale
    SI.POV.GINI   : indice de Gini (inégalités de revenu)
    NY.GDP.PCAP.CD / .KD.ZG : PIB par habitant et croissance
    FP.CPI.TOTL.ZG : inflation (IPC, % annuel)
    SL.UEM.1524.ZS : chômage des jeunes (15-24 ans, %)
    SL.TLF.ACTI.ZS : taux d'activité (population active, %)
    SL.AGR.EMPL.ZS : part de l'emploi agricole (%)

Sortie : data/processed/poverty_africa_full.csv, poverty_africa_2000_2023.csv

IMPORTANT : le taux de pauvreté monétaire (SI.POV.DDAY/NAHC) et l'indice de Gini (inégalité
relative de la distribution des revenus) sont deux concepts DIFFÉRENTS — un pays peut avoir un
Gini élevé (forte inégalité) sans avoir un taux de pauvreté élevé, et inversement. Ce projet les
traite comme deux variables distinctes, jamais comme des synonymes.
"""
import os
import json
import requests
import pandas as pd
from functools import reduce

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

INDICATORS = {
    "poverty_rate_national": "SI.POV.NAHC",
    "poverty_rate_300ppp": "SI.POV.DDAY",
    "gini": "SI.POV.GINI",
    "gdp_per_capita": "NY.GDP.PCAP.CD",
    "gdp_per_capita_growth": "NY.GDP.PCAP.KD.ZG",
    "inflation": "FP.CPI.TOTL.ZG",
    "youth_unemployment": "SL.UEM.1524.ZS",
    "labor_force_participation": "SL.TLF.ACTI.ZS",
    "employment_agriculture": "SL.AGR.EMPL.ZS",
}
NORTH_AFRICA_NAMES = {"Algeria", "Egypt, Arab Rep.", "Libya", "Morocco", "Tunisia"}


def fetch_wb(code, per_page=20000, retries=3):
    all_data, page = [], 1
    while True:
        url = f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page={per_page}&page={page}"
        for attempt in range(retries):
            try:
                r = requests.get(url, timeout=90)
                data = r.json()
                break
            except requests.exceptions.RequestException:
                if attempt == retries - 1:
                    raise
        if len(data) < 2 or not data[1]:
            break
        all_data.extend(data[1])
        if page >= data[0]["pages"]:
            break
        page += 1
    return all_data


def get_africa_iso3():
    r = requests.get("https://api.worldbank.org/v2/country?format=json&per_page=400", timeout=60)
    countries = r.json()[1]
    ssa = {c["id"] for c in countries if c["region"]["value"].strip() == "Sub-Saharan Africa"}
    na = {c["id"] for c in countries if c["name"] in NORTH_AFRICA_NAMES}
    return ssa | na


def load_or_fetch(key, code, force=False):
    path = os.path.join(RAW_DIR, f"{key}.json")
    if not os.path.exists(path) or force:
        print(f"Téléchargement {key} ({code})...")
        data = fetch_wb(code)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def to_df(records, value_name, africa_iso3):
    rows = [
        {"country": r["countryiso3code"], "year": int(r["date"]), value_name: r["value"]}
        for r in records
        if r.get("countryiso3code") in africa_iso3 and r.get("value") is not None
    ]
    return pd.DataFrame(rows)


def build():
    africa_iso3 = get_africa_iso3()
    dfs = []
    for key, code in INDICATORS.items():
        records = load_or_fetch(key, code)
        dfs.append(to_df(records, key, africa_iso3))

    merged = reduce(lambda a, b: pd.merge(a, b, on=["country", "year"], how="outer"), dfs)
    merged.to_csv(os.path.join(OUT_DIR, "poverty_africa_full.csv"), index=False)

    subset = merged[(merged["year"] >= 2000) & (merged["year"] <= 2023)].copy()
    subset.to_csv(os.path.join(OUT_DIR, "poverty_africa_2000_2023.csv"), index=False)

    print(f"Panel complet : {merged.shape[0]} lignes, {merged['country'].nunique()} pays")
    print(f"Panel 2000-2023 : {subset.shape[0]} lignes")
    return merged, subset


if __name__ == "__main__":
    build()
