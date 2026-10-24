---
title: "Services du Premier ministre"
order: 2
description: "Direction interministérielle du numérique : IA dans l'État. Données publiques pour l'IA, évaluation des modèles, code agentique souverain, interventions MCP."
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

### Évaluation des modèles d'IA

Choisir un modèle sur des chiffres plutôt que sur une démo, savoir ce que vaut un produit en production, mesurer l'effet de chaque changement.

**Un assistant juridique : une méthode réplicable**  
- Jeu de données de référence de 100 questions sur 8 catégories juridiques, construit à partir de conversations réelles  
- LLM-as-a-judge pour comparer plusieurs approches  
- +16 % de qualité par rapport à la référence avec l'approche hybride retenue, déployée en production

**Transcription audio et documents scannés**  
- Benchmark de modèles ouverts et commerciaux sur un corpus représentatif de l'administration : environ 10 % d'erreurs en moins par rapport au système actuel  
- Contribution au banc d'évaluation open source [eval-transcript](https://github.com/etalab-ia/eval-transcript), qui mesure le taux d'erreur mot et qualifie la gravité des erreurs avec un panel de LLM juges  
- Auteur d'[eval-ocr-htr](https://github.com/etalab-ia/eval-ocr-htr), banc d'évaluation open source qui compare des modèles de reconnaissance de texte (OCR et HTR) sur des documents manuscrits scannés, via l'inférence souveraine de l'État

**Un guide public pour l'État**  
- J'ai rédigé le [guide des évaluations de systèmes d'IA](https://guides.ia.numerique.gouv.fr/guides/evaluations-des-systemes-dia), qui recense les pratiques d'évaluation de l'administration pour que chaque équipe réutilise ce qui existe au lieu de repartir de zéro

### Code agentique souverain

Les agents publics utilisent déjà des assistants de code commerciaux, et les standards de l'État (design system, accessibilité, sécurité) restent à configurer à la main, projet par projet.

**Une stack open source pour les agents publics**  
- [Albert Code](https://github.com/etalab-ia/albert-code), porté par la DINUM : un agent de code open source branché sur l'inférence souveraine de l'État, exécuté dans une machine virtuelle isolée, avec les skills État préinstallées  
- Albert Code est lui-même développé avec un agent de code

**Investigation et prototypes**  
- 30+ entretiens dans les ministères  
- Benchmark comparatif d'agents de code sur inférence souveraine, 3 POC livrés

**Skills État : les standards de l'État dans les assistants de code**  
- Dépôt [etalab-ia/skills](https://github.com/etalab-ia/skills), dont je suis l'auteur : DSFR, RGAA, sécurité ANSSI, data.gouv.fr, La Suite

### Coordination de l'exposition des données

- **Serveur MCP data.gouv.fr** : coordination et suivi produit du serveur qui connecte les modèles d'IA à l'open data français ; 45 M de requêtes en 100 jours.
- **Accompagnement des administrations** qui exposent leurs données dans des formats prêts pour l'IA (MCP, CLI, skills) : data.gouv, ANSSI, IGN, France Travail, DILA / Légifrance, Éducation nationale, CEA ; retours d'expérience, questions-réponses, aide à la conception, articles de vulgarisation.

### Interventions

- **Claude Code Paris 02**, février 2026 : *MCP Leading the People*, connecter les assistants IA aux données publiques françaises. [Slides de Claude Code Paris 02](https://benoitvx.github.io/claude-code-paris-02/)
- **Atelier MCP, rencontre de l'incubateur IA de l'État (ALLiaNCE)**, 20 janvier 2026 : le Model Context Protocol expliqué à des agents publics non techniques, avec des démonstrations branchées sur le serveur MCP de data.gouv.fr. [Slides de l'atelier MCP](https://benoitvx.github.io/atelier-mcp-slides/)
- **Sovereign Agents Blitz Hackathon 2026**, 29 avril 2026 : présentation des serveurs MCP de l'État aux participants.
- Plusieurs talks donnés dans l'administration sur les nouveaux formats de données pour l'IA.

### Convictions portées

- L'IA pour le secteur public se gagne sur les données et leur disponibilité dans le bon format au bon moment, pas sur le modèle  
- Les Skills État sont aussi un levier de sécurisation proactive : les bonnes pratiques (ANSSI, RGAA) intégrées dès le développement plutôt qu'auditées après coup  
- Une bonne offre data est multi-format *by design* : un même dataset doit être disponible en API, MCP, Parquet, collection vectorielle selon l'usage
