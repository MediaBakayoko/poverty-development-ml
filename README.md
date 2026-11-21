# Machine Learning for Poverty and Development Analysis in Africa

## Problématique
Quels facteurs économiques et structurels expliquent les écarts de pauvreté monétaire entre pays
africains, et comment les inégalités de revenu, le chômage des jeunes et l'inflation s'articulent-ils ?

## Données
**World Bank Open Data**, API publique sans inscription.
- Source : https://api.worldbank.org/v2/
- Indicateurs : taux de pauvreté ($3/jour PPA 2021 et seuil national), indice de Gini, PIB par
  habitant et croissance, inflation, chômage des jeunes, taux d'activité, part de l'emploi agricole
- Couverture : 53 pays africains, 2000-2023 (1 272 observations pays-année)
- Licence : CC BY 4.0

## Objectifs
1. Identifier les pays/périodes à risque de pauvreté élevée (classification).
2. Construire des catégories socioéconomiques de pays (clustering).
3. Analyser le chômage des jeunes et les facteurs associés.
4. Prévoir les tendances d'inflation pour quelques économies clés.
5. Mesurer les disparités territoriales de pauvreté (cartographie).

## Précision méthodologique : Gini ≠ taux de pauvreté
Le **taux de pauvreté** (part de la population sous un seuil absolu de revenu) et l'**indice de
Gini** (mesure relative de dispersion des revenus) sont deux indicateurs distincts — un pays peut
avoir une distribution très inégale (Gini élevé) sans forte pauvreté absolue, et inversement. La
corrélation observée dans ce projet entre les deux indicateurs est modérée (r=0,31), confirmant
empiriquement qu'ils ne doivent pas être utilisés l'un pour l'autre.

## Méthodologie
1. **Construction du panel** (`src/01_build_dataset.py`) : fusion de 9 indicateurs World Bank.
2. **EDA** (`src/02_eda.py`) : tendances, distributions, corrélations, relation Gini/pauvreté.
3. **Classification** (`src/03_classification.py`) : prédiction du statut "pauvreté élevée"
   (>40% sous $3/jour) par régression logistique vs Random Forest.
4. **Clustering** (`src/04_clustering.py`) : catégories socioéconomiques de pays (K-Means).
5. **Prévision d'inflation** (`src/05_inflation_forecast.py`) : lissage exponentiel de Holt
   amorti pour 6 économies représentatives (Côte d'Ivoire, Nigeria, Afrique du Sud, Égypte,
   Kenya, Ghana).
6. **Cartographie** (`src/06_mapping.py`) : carte choroplèthe du taux de pauvreté par pays.

## Résultats clés
- Classification : AUC=0,87-0,88 en validation croisée (régression logistique et Random Forest
  proches) — performance solide sur 186 observations. Facteurs les plus associés (régression
  logistique, meilleur modèle) : indice de Gini, part de l'emploi agricole, PIB par habitant.
- Clustering : 2 catégories nettes — pays à économie diversifiée (PIB élevé, 13% pauvreté
  moyenne, 21% d'emploi agricole) vs pays à dominante agricole (PIB faible, 45% pauvreté
  moyenne, 53% d'emploi agricole).
- Corrélation Gini/pauvreté : 0,31 — confirme la distinction conceptuelle.
- Prévisions d'inflation 2028 : Nigeria et Égypte restent en zone de forte inflation (>25%),
  Côte d'Ivoire et Kenya en zone modérée (<8%).
- Carte : RD Congo (85%), Mozambique (81%), Soudan du Sud (77%) les plus touchés ; Algérie,
  Maurice, Seychelles, Tunisie, Égypte sous les 4%.

## Reproductibilité
```bash
pip install -r requirements.txt
python src/01_build_dataset.py
python src/02_eda.py
python src/03_classification.py
python src/04_clustering.py
python src/05_inflation_forecast.py
python src/06_mapping.py
```

## Article complet
Voir [`ARTICLE.md`](ARTICLE.md) pour l'analyse narrative complète avec interprétation et
recommandations.

## Auteur
Média Marcel Bakayoko — Expert géomatique / données géospatiales & agricoles / GeoAI / Suivi-Évaluation.

## Licence des données
World Bank Open Data — CC BY 4.0.
