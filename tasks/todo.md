# #12 [CONTENU] presidence-de-la-republique : résultats Datalma, équipe, pérennisation

Branche : `feat/bv-12-presidence` (déjà créée). PR `Closes #12` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Aucune décision de #2 en jeu (contenu seul, ni dépendance, ni réglage, ni secret).
Texte appliqué : version finale de #12, réponses de Benoit du 22/10/2026 incluses :
- dates : **octobre 2024 à décembre 2025** ;
- « au-delà d'un changement de gouvernement » : **retiré**, on garde « Service pérennisé après 15 mois » ;
- « 5 à 6 réactions ministérielles en 6 mois » : **retiré** (absent de la proposition : ne pas l'ajouter).

## Critères d'acceptation

- [ ] Titre de page inchangé : `Présidence de la République` (donc `<title>` inchangé).
- [ ] Chapeau = texte de l'issue (trois paragraphes : rôle et programme ; *Octobre 2024 à décembre 2025* en italique ; Datalma développement conjoint + cible), les trois liens actuels conservés.
- [ ] Citation actuelle conservée (voir points d'attention).
- [ ] « Mission » : texte actuel, « — » remplacé par une virgule.
- [ ] « Réalisations » : 3 blocs dans l'ordre de l'issue, mot pour mot : Datalma Alerting (avec « 5 minutes » et « 5 meilleures opportunités par e-mail à 9 h »), Plateforme décisionnelle : observatoire santé (« livré en 1 semaine, repris par la presse, toujours en ligne »), Une équipe et un service qui durent (équipe de 10 personnes, pérennisé après 15 mois).
- [ ] Plus aucune trace de : « septembre 2024 », « shippé », « comme alternative aux rapports institutionnels », « Plateforme d'intelligence décisionnelle », « réactions ministérielles », « changement de gouvernement », « start-up d'état ».
- [ ] « Stack » : `Python, Metabase, Dagster, dbt, React, embeddings Qwen3, Mistral, Docker.`
- [ ] Meta description cohérente avec le nouveau chapeau (l'issue n'en donne pas : reprendre la première phrase du chapeau, voir étape 1).
- [ ] Aucun « — », « · », « | » dans le texte visible, le `<title>` et la meta description de la page.
- [ ] URL, slug, `order`, `textposition`, `cover`, `images` inchangés ; liens existants inchangés (datalma.beta.gouv.fr, eig.numerique.gouv.fr, numerique.gouv.fr, explore.data.gouv.fr/grippe/). Aucun lien ajouté.
- [ ] `public/llms.txt` et `public/llms-full.txt` : passages Présidence alignés (étape 2).

## Tests (catalogue #10)

Aucun test à ajouter (l'issue n'en demande pas). Tests existants qui doivent rester verts sans modification :

| ID | Fichier | Lien avec #12 |
|---|---|---|
| T-BV-BUILD-01 | `npx astro build` + `tests/test_dist.py` | build de la page modifiée |
| T-BV-CONT-01, T-BV-CONT-02, T-BV-CONT-03 | `tests/test_content.py` | front matter (`description` non vide, `cover`/`images` existants), pas de KirbyText |
| T-BV-SPE-01 | `tests/test_dist.py` | URL `benoitvinceneux.com/...` des `llms*.txt` : `/presidence-de-la-republique` est bien 200 dans `legacy-urls.txt` ; n'ajouter aucune URL du domaine |
| T-BV-SEO-01 | `tests/test_dist.py` | canonical, meta description non vide, `<title>` unique |
| T-BV-LNK-01, T-BV-LNK-02, T-BV-HOST-01 | `tests/test_links.py` | hôtes déjà dans `tests/allowed-hosts.txt` ; aucun nouvel hôte |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` (+ `tests/test_repo.py`) | HTML de la page |
| T-BV-HTTP-01 | `tests/http_check.sh` sur Apache local servant `dist/` | page et `llms*.txt` en 200 |
| T-BV-A11Y-01, T-BV-A11Y-02 | `tests/e2e/a11y.spec.ts`, `tests/test_a11y.py` | axe sur la page |
| Autres (ART, INV, SPE-02..06, HTA, CSP, BUD, DEP, WF, GUARD, IMP) | `tests/*.py` | non concernés, doivent rester verts |

Commande : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html"`, puis Apache local + `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh`, puis `npx playwright test`.

## Fichiers modifiés (3, rien à créer)

1. `src/content/projects/presidence-de-la-republique.md` : front matter `description` + corps entier.
2. `public/llms.txt` : ligne 9 seulement.
3. `public/llms-full.txt` : section `## Présidence de la République — Datalma` seulement (lignes ~124 à 160, jusqu'au `---` qui précède `## 🍿 Curated Adventures`).

Hors périmètre (ne pas toucher) : `src/pages/a-propos.astro` ligne 28 (dates et « · » du parcours) et la ligne 29 de `public/llms-full.txt` (parcours de la section À propos) relèvent de #13 (qui porte déjà « octobre 2024 à décembre 2025 ») et #22. Gabarit, séparateur du `<title>` : #14.

## Étapes

### 1. Page projet

Garder `title`, `order`, `textposition`, `cover`, `images` à l'octet. Remplacer `description` par :

```
description: "Directeur Produit / CPO de la startup d'État Datalma, programme Entrepreneur d'intérêt général de la Direction interministérielle du numérique (DINUM)."
```

Corps cible (conventions Markdown actuelles : `###` pour les sections, deux espaces en fin de ligne pour les retours à la ligne dans un bloc) :

```markdown
**Directeur Produit** / **CPO** de la startup d'État [Datalma](https://datalma.beta.gouv.fr/), programme [Entrepreneur d'intérêt général](https://www.eig.numerique.gouv.fr/) de la [Direction interministérielle du numérique](https://www.numerique.gouv.fr/) (DINUM).

*Octobre 2024 à décembre 2025*

Datalma est un développement conjoint des Services du Premier ministre (DINUM) et de la Présidence de la République : une plateforme d'aide à la décision pour le sommet de l'État. Cible : Président, ministres, conseillers, directeurs de cabinet, directeurs d'administration centrale.

> *« Contribuer à une action publique à la fois plus performante et plus ouverte, en transformant l'accès aux données gouvernementales pour les décideurs et à terme pour les citoyens. »*

### Mission

Faciliter l'accès aux données publiques et inter-administratives non ouvertes pour permettre des décisions politiques éclairées et rapides, y compris en mobilisant l'IA pour trouver des corrélations entre les données.

### Réalisations

**Datalma Alerting : un agent de veille push, presse × données internes**  
Chaque matin, le système repère dans la presse les sujets sur lesquels l'État dispose de données pour éclairer le débat public, et envoie les 5 meilleures opportunités par e-mail à 9 h.  
- Pipeline en 4 étapes : ingestion RSS (environ 30 articles par jour), embeddings Qwen3-Embedding-0.6B, similarité cosinus avec le catalogue de jeux de données, e-mail du top 5  
- Une veille manuelle de plusieurs heures ramenée à 5 minutes  
- Stack 100 % souveraine

**Plateforme décisionnelle : observatoire santé**  
- Tableaux de bord internes pour le Président, Matignon et le ministère de la Santé sur des indicateurs non ouverts (épidémies, hospitalisations…)  
- [Observatoire grand public du suivi de la grippe](https://explore.data.gouv.fr/grippe/) : livré en 1 semaine, repris par la presse, toujours en ligne

**Une équipe et un service qui durent**  
- Équipe de 10 personnes constituée et animée : data science, data engineering, développement, go-to-market  
- Service pérennisé après 15 mois

### Stack  
Python, Metabase, Dagster, dbt, React, embeddings Qwen3, Mistral, Docker.
```

### 2. Fichiers LLM (mêmes faits que la page, aucun ajout)

- `public/llms.txt` ligne 9 : remplacer par l'entrée validée dans #22 (mêmes faits que la page) :
  `- [Présidence de la République](https://benoitvinceneux.com/presidence-de-la-republique): CPO Datalma, startup d'État (octobre 2024 à décembre 2025). Plateforme d'aide à la décision pour le sommet de l'État. Datalma Alerting (veille de plusieurs heures ramenée à 5 minutes), observatoire grippe livré en 1 semaine, service pérennisé après 15 mois.`
- `public/llms-full.txt` : réécrire la section entre `## Présidence de la République — Datalma` et le `---` qui précède `## 🍿 Curated Adventures` comme transcription texte de la page : titre `## Présidence de la République : Datalma`, ligne `URL :` inchangée, puis chapeau (rôle, dates, développement conjoint + cible), citation, `### Mission`, `### Réalisations` (3 blocs, intitulés de la page, même contenu), `### Stack`. Sans « — » ni « · ». Style du fichier : pas de gras Markdown, pas de liens Markdown, puces `- `.

### 3. Vérification locale

1. `npx astro build`, puis les commandes du tableau Tests.
2. Séparateurs :
   - `grep -nE '—|·|\|' dist/presidence-de-la-republique.html` : résultats acceptables seulement hors `<title>`, meta description et `<main>` (gabarit, #14) ;
   - `sed -n '9p' public/llms.txt | grep -E '—|·|\|'` : 0 résultat ;
   - `awk '/^## Présidence/,/^## 🍿/' public/llms-full.txt | grep -nE '—|·|\|'` : 0 résultat.
3. `grep -nE "septembre 2024|shippé|alternative aux rapports|intelligence décisionnelle|réactions|changement de gouvernement" dist/presidence-de-la-republique.html public/llms.txt` (ligne 9) et la section Présidence de `llms-full.txt` : 0 résultat.
4. `git diff --stat` : seulement les 3 fichiers + `tasks/todo.md` ; `cover`/`images` identiques.

### 4. Commit

`content: Présidence de la République, résultats Datalma, équipe et pérennisation (#12)` (inclut `tasks/todo.md`).

## Points d'attention

- Citation : l'issue n'en parle pas (ni « conservé » ni « supprimé ») et ne la reprend pas dans le chapeau ; le chapeau est « conservé, sans changement de fond » et le Constat ne demande pas son retrait : on la garde à l'identique. Si un relecteur lit l'omission comme un retrait, le signaler plutôt que trancher seul.
- Liens du chapeau : l'issue donne le texte sans liens ; règle de parité (aucun lien ne change) : on garde les trois liens actuels sur les mêmes mots. Gras actuel sur « Directeur Produit » / « CPO » conservé.
- Attribution : ne rien ajouter. Pas de « 5 à 6 réactions », pas de « changement de gouvernement », pas de lien nouveau, pas de chiffre hors issue. « Équipe de 10 personnes constituée et animée » mot pour mot, sans reformulation.
- Ne jamais citer ni nommer les « Sources » de l'issue (documents privés), ni de doctrine non publiée.
- « × » (presse × données internes) et « / » (Directeur Produit / CPO) ne sont pas des séparateurs interdits. Les flèches « → » du pipeline actuel disparaissent (texte de l'issue avec virgules).
- `.nvmrc` reste à 24.
