---
title: "Services du Premier ministre"
order: 2
description: "Direction interministérielle du numérique : IA dans l'État. Données publiques pour l'IA, code agentique souverain, évaluation des modèles, coaching produit."
textposition: "above"
cover: { src: "/media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-288x288.png", srcset: "/media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-288x288.png 288w,/media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-576x576.png 576w" }
images:
  - { src: "/media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-640x.png", srcset: "/media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-320x.png 320w, /media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-640x.png 640w, /media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-960x.png 960w, /media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-1280x.png 1280w", width: 576, height: 578 }
---
**Direction interministérielle du numérique, Services du Premier ministre 🇫🇷**  
*AI Product Lead : depuis janvier 2026*

Au sein du département IA dans l'État (IAE, ex-Etalab) de la DINUM, je contribue à intégrer l'IA dans les services publics : dans les outils des agents comme dans les services accessibles aux citoyens.

### Le contexte

Les données publiques françaises sont abondantes mais mal exposées pour l'IA. Le trafic humain sur les portails baisse, les appels API explosent (340 M en 2025 sur la DILA, ×2 par rapport à 2024). Les agents et assistants IA deviennent de gros consommateurs de données publiques, mais ces données ne sont pas dans les formats dont ils ont besoin.

> *Le problème n'est pas le modèle, c'est la donnée. Et la donnée n'est pas absente : elle est mal exposée.*

### La mission : cinq fronts

- **Ouvrir les données publiques à l'IA** : coordination des serveurs MCP, CLI et skills qui connectent les modèles aux données publiques, et accompagnement des administrations qui exposent leurs propres données.
- **Équiper les développeurs de l'État** : une stack de code agentique souveraine, avec les standards de l'État embarqués dès la conception (design system, accessibilité RGAA, sécurité).
- **Structurer les pratiques d'évaluation IA** : jeux de données de référence, LLM-as-a-judge, méthodes adaptées à chaque type de produit.
- **Veille sur l'IA agentique et les nouveaux usages**, pour en tirer des enseignements actionnables.
- **Coaching produit** des équipes de l'incubateur IA de l'État (ALLiaNCE) et réflexion sur la stratégie des services IA aux citoyens.

### L'approche : initialiser, prouver, transférer

Sur chaque sujet : on fait une première version pour montrer que c'est possible, on met en circulation et on collecte des retours, puis on transfère à l'administration métier qui prend la main et améliore.

### Réalisations

**Évaluation LLM verticalisée : une méthode réplicable**  
- Jeu de données de référence de 100 questions sur 8 catégories juridiques, construit à partir de conversations réelles  
- LLM-as-a-judge pour comparer plusieurs approches  
- +16 % de qualité par rapport à la référence avec l'approche hybride retenue, déployée en production

**Évaluation de la transcription audio**  
- Benchmark de modèles ouverts et commerciaux sur un corpus représentatif de l'administration : environ 10 % de taux d'erreur en moins  
- Contribution au benchmark open source qui porte la méthode

**Stack de code agentique souveraine**  
- 30+ entretiens dans les ministères  
- Benchmark comparatif d'agents de code sur inférence souveraine, 3 POC livrés  
- Standards de l'État embarqués sous forme de skills : design system, accessibilité, sécurité

**Skills État : les standards de l'État dans les assistants de code**  
- Dépôt [etalab-ia/skills](https://github.com/etalab-ia/skills), dont je suis l'auteur : DSFR, RGAA, sécurité ANSSI, data.gouv.fr, La Suite

### Coordination de l'exposition des données

- **Serveur MCP data.gouv.fr** : coordination et suivi produit du serveur qui connecte les modèles d'IA à l'open data français ; 45 M de requêtes en 100 jours.
- **Accompagnement des administrations** qui exposent leurs données dans des formats prêts pour l'IA (MCP, CLI, skills) : data.gouv, ANSSI, IGN, France Travail, DILA / Légifrance, Éducation nationale, CEA ; retours d'expérience, questions-réponses, aide à la conception, articles de vulgarisation.

### Convictions portées

- L'IA pour le secteur public se gagne sur les données et leur disponibilité dans le bon format au bon moment, pas sur le modèle  
- Les Skills État sont aussi un levier de sécurisation proactive : les bonnes pratiques (ANSSI, RGAA) intégrées dès le développement plutôt qu'auditées après coup  
- Une bonne offre data est multi-format *by design* : un même dataset doit être disponible en API, MCP, Parquet, collection vectorielle selon l'usage
