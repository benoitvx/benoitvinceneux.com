---
title: "Services du Premier ministre"
order: 2
description: "Direction Interministérielle du Numérique — Services du Premier ministre 🇫🇷 CPO MCP & Données — depuis janvier 2026"
textposition: "above"
cover: { src: "/media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-288x288.png", srcset: "/media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-288x288.png 288w,/media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-576x576.png 576w" }
images:
  - { src: "/media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-640x.png", srcset: "/media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-320x.png 320w, /media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-640x.png 640w, /media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-960x.png 960w, /media/pages/services-du-premier-ministre/cfed094263-1777404734/dinum-1280x.png 1280w", width: 576, height: 578 }
---
**Direction Interministérielle du Numérique — Services du Premier ministre 🇫🇷**  
*CPO MCP & Données — depuis janvier 2026*

Pilote de la brique « données & MCP » du socle interministériel d'IA générative de l'État, au sein du département **IA dans l'État (IAE, ex-Etalab)** de la DINUM.

### Le contexte

Les données publiques françaises sont abondantes mais mal exposées pour l'IA. Le trafic humain sur les portails baisse, les appels API explosent (340 M en 2025 sur la DILA, ×2 vs 2024). Les agents et assistants IA deviennent des gros consommateurs de données publiques — mais ces données ne sont pas dans les formats dont ils ont besoin.

> *Le problème n'est pas le modèle, c'est la donnée. Et la donnée n'est pas absente — elle est mal exposée.*

### La mission

Rendre les données publiques françaises exploitables par l'IA — et accompagner les administrations pour qu'elles fassent de même avec leurs données.

- Piloter l'offre données & MCP du socle interministériel d'IA générative  
- Concevoir les fonctionnalités IA d'accès à la donnée publique pour les usagers  
- Lien produit avec l'Opérateur des Produits Interministériels, en particulier data.gouv.fr  
- Accompagner le déploiement de projets IA dans les ministères via l'incubateur ALLiaNCE

### L'approche : initialiser, prouver, transférer

Sur chaque sujet : on fait une première version pour montrer que c'est possible, on met en circulation et on collecte des retours, puis on transfère à l'administration métier qui prend la main et améliore.

### L'offre data : 3 piliers + 1 chantier

**Pilier 1 — Données Publiques pour l'IA**  
Accompagner les administrations pour exposer leurs données dans les formats IA-natifs (MCP, CLI, skill, llms.txt) et donner de la visibilité sur l'existant via un catalogue.

**Pilier 2 — RAG as a Service**  
Infrastructure mutualisée de collections vectorielles pour les administrations.

**Pilier 3 — Gouvernance des données**  
Pousser un GT interministériel sur la doctrine d'accès aux données comme pré-requis à la diffusion de l'IA.

**Chantier — IA pour les devs**  
Équiper les développeurs de l'État (doctrine, skills, outils souverains), changer les pratiques.

### Réalisations clés

**MCP data.gouv — accès programmatique à l'open data français pour les LLMs**  
- 3 millions de requêtes par semaine en production  
- Buzz com inédit pour le numérique public, 100 % retours positifs  
- Démocratisation de l'usage en langage naturel

**ia.data.gouv.fr — premier catalogue européen multi-format natif IA pour les données publiques**  
- Pour chaque source de données : statut des formats disponibles (API, MCP, Parquet, collection vectorielle, Skill, llms.txt) avec lien direct

**Accompagnement des administrations pour déployer de nouveaux formats (MCP, CLI, skill)**  
data.gouv, ANSSI, IGN, France Travail, DILA / Légifrance, Éducation nationale, CEA — retex, Q&A, aide à la conception, série d'articles de vulgarisation.

**Évaluation LLM verticalisée**  
- Élaboration de Golden Dataset  
- LLM-as-a-judge sur différentes méthodes d'optimisations des systèmes évalués  
- +16 % de qualité vs baseline avec l'approche retenue, déployée en production

**Déploiement d'une stack souveraine d'IA pour le développement**  
- Évaluation des solutions clés du marché  
- Package d'expérimentation : Skills, Agent et environnement de travail (VM)  
- Repository [`etalab-ia/skills`](https://github.com/etalab-ia/skills) publié sur GitHub. Premières skills : Design System, ANSSI, RGAA / accessibilité,

### Convictions portées

- L'IA pour le secteur public se gagne sur les données et leur disponibilité dans le bon format au bon moment, pas sur le modèle  
- Les Skills État sont aussi un levier de sécurisation proactive : les bonnes pratiques (ANSSI, RGAA) intégrées dès le développement plutôt qu'auditées après coup  
- Une bonne offre data est multi-format *by design* : un même dataset doit être disponible en API, MCP, Parquet, collection vectorielle selon l'usage
