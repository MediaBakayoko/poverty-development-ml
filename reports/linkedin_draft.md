# Post LinkedIn — brouillon en français (à valider)

🌍 DEUX AFRIQUES ÉCONOMIQUES : CE QUE 23 ANS DE DONNÉES RÉVÈLENT SUR LA PAUVRETÉ

J'ai mené une analyse de Machine Learning sur la pauvreté et le développement économique en
Afrique, à partir des données ouvertes de la Banque Mondiale — 53 pays, 23 ans de données (2000-2023).

🎯 Objectif : identifier les facteurs associés à la pauvreté monétaire, construire des catégories
socioéconomiques de pays, et prévoir les tendances d'inflation.

📊 Résultats clés :
• Classification du risque de pauvreté élevée : AUC = 0,87-0,88 en validation croisée
• Clustering : 2 groupes nets émergent — pays à économie diversifiée (13% de pauvreté moyenne,
  21% d'emploi agricole) vs pays à dominante agricole (45% de pauvreté moyenne, 53% d'emploi agricole)
• Facteur le plus discriminant : la part de l'emploi agricole dans l'économie
• Carte : RD Congo (85%), Mozambique (81%), Soudan du Sud (77%) les plus touchés ; Algérie,
  Tunisie, Égypte, Maurice sous les 4%
• Prévisions d'inflation 2028 : Nigeria et Égypte restent en zone critique (>25%), la zone UEMOA
  (Côte d'Ivoire) en zone de stabilité (2%)

⚠️ Précision méthodologique importante : l'indice de Gini (inégalité relative) et le taux de
pauvreté (seuil absolu) sont deux concepts différents — corrélation mesurée de seulement 0,31 sur
cet échantillon. Les confondre conduirait à mal cibler les politiques publiques : une politique
anti-inégalités ne réduit pas nécessairement la pauvreté absolue, et inversement.

💡 Implication : la diversification économique hors de l'agriculture de subsistance ressort comme
le levier structurel le plus associé à la réduction de la pauvreté sur ce panel continental.

💻 Code, méthodologie et résultats complets en open-source :
🔗 https://github.com/MediaBakayoko/poverty-development-ml

#DataScience #MachineLearning #Pauvrete #Developpement #Afrique #GeoAI #DonneesOuvertes #WorldBank
