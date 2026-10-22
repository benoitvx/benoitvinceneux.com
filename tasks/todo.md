# #11 [CONTENU] services-du-premier-ministre : cinq fronts, AI Product Lead, attribution MCP data.gouv

Branche : `feat/bv-11-services-premier-ministre` (déjà créée). PR `Closes #11` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Aucune décision de #2 en jeu (ticket de contenu, pas de dépendance ni de réglage).
Texte appliqué : version finale de #11, réponses de Benoit du 22/10/2026 incluses (AI Product Lead ; titre « Services du Premier ministre » ; ia.data.gouv.fr retiré ; « auteur » de etalab-ia/skills ; 30+ entretiens ; benchmark de transcription conservé).
`tasks/lessons.md` (leçons de #9) et ce plan : commités par le tech lead.

## Critères d'acceptation

- [ ] Titre de page inchangé : `Services du Premier ministre` (donc `<title>` inchangé).
- [ ] Chapeau : « Direction interministérielle du numérique, Services du Premier ministre 🇫🇷 », « *AI Product Lead : depuis janvier 2026* », puis le paragraphe IAE de l'issue.
- [ ] « Le contexte » : texte de l'issue (« ×2 par rapport à 2024 », « de gros consommateurs », citation avec deux-points), sans « — ».
- [ ] « La mission : cinq fronts » : les 5 puces de l'issue, mot pour mot.
- [ ] « L'approche : initialiser, prouver, transférer » : paragraphe actuel inchangé.
- [ ] Bloc « L'offre data : 3 piliers + 1 chantier » supprimé.
- [ ] « Réalisations » (et non plus « Réalisations clés ») : 4 blocs de l'issue, mot pour mot (100 questions, 8 catégories, +16 %, ~10 % d'erreur, 30+ entretiens, 3 POC, etalab-ia/skills « dont je suis l'auteur »).
- [ ] « Coordination de l'exposition des données » : MCP data.gouv.fr en coordination et suivi produit, 45 M de requêtes en 100 jours ; accompagnement avec la liste actuelle des administrations.
- [ ] Plus aucune trace de : « 3 millions de requêtes par semaine », « Buzz com », « 100 % retours positifs », ia.data.gouv.fr, « CPO MCP & Données », « Golden Dataset », la liste de skills tronquée.
- [ ] « Convictions portées » : 3 puces actuelles inchangées (*by design* en italique).
- [ ] Meta description = texte exact de l'issue.
- [ ] Aucun « — », « · », « | » dans le texte visible, le `<title>` et la meta description de la page.
- [ ] URL, slug, `order`, `cover`, `images` inchangés.
- [ ] `public/llms.txt` et `public/llms-full.txt` : passages Services du Premier ministre alignés (voir étape 2).

## Tests (catalogue #10)

Aucun test à ajouter (l'issue n'en demande pas). Tests existants qui doivent rester verts sans modification, et ceux que ce ticket touche :

| ID | Fichier | Lien avec #11 |
|---|---|---|
| T-BV-BUILD-01 | `npx astro build` + `tests/test_dist.py` | build de la page modifiée |
| T-BV-CONT-01, T-BV-CONT-02, T-BV-CONT-03 | `tests/test_content.py` | front matter (`description` non vide, `cover`/`images` existants), pas de KirbyText |
| T-BV-SPE-01 | `tests/test_dist.py` | toute URL `benoitvinceneux.com/...` des `llms*.txt` doit être une entrée 200 de `legacy-urls.txt` : ne garder que `/services-du-premier-ministre`, n'ajouter aucune URL du domaine |
| T-BV-SEO-01 | `tests/test_dist.py` | canonical, meta description non vide, `<title>` unique |
| T-BV-LNK-01, T-BV-LNK-02, T-BV-HOST-01 | `tests/test_links.py` | lien externe `github.com/etalab-ia/skills` déjà présent ; aucun nouvel hôte |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` (+ `tests/test_repo.py`) | HTML de la page |
| T-BV-HTTP-01 | `tests/http_check.sh` sur Apache local servant `dist/` | page et `llms*.txt` en 200, `text/markdown` |
| T-BV-A11Y-01, T-BV-A11Y-02 | `tests/e2e/a11y.spec.ts`, `tests/test_a11y.py` | axe sur la page |
| Autres (ART, INV, SPE-02..06, HTA, CSP, BUD, DEP, WF, GUARD, IMP) | `tests/*.py` | non concernés, doivent rester verts |

Commande unique : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html"`, puis Apache local + `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh`, puis `npx playwright test`.

## Fichiers modifiés (3, rien à créer)

1. `src/content/projects/services-du-premier-ministre.md` : front matter `description` + corps entier.
2. `public/llms.txt` : ligne 8 seulement.
3. `public/llms-full.txt` : section `## Services du Premier ministre — DINUM` seulement (lignes ~64 à 122).

Hors périmètre (ne pas toucher) : `src/pages/a-propos.astro` et le résumé d'en-tête des deux `llms*.txt` (« CPO MCP & Données », lignes 3, 22, 28 de llms-full.txt, ligne 3 de llms.txt) relèvent de #13 et #22. Gabarit, `<title>` « – Benoit Vinceneux » (tiret demi-cadratin, autorisé) : #14.

## Étapes

### 1. Page projet

Garder `title`, `order`, `textposition`, `cover`, `images` à l'octet. Remplacer `description` par :

```
description: "Direction interministérielle du numérique : IA dans l'État. Données publiques pour l'IA, code agentique souverain, évaluation des modèles, coaching produit."
```

Corps cible (conserver les conventions Markdown actuelles : `###` pour les sections, deux espaces en fin de ligne pour les retours à la ligne) :

```markdown
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

(paragraphe actuel, à l'octet)

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

(3 puces actuelles, à l'octet)
```

### 2. Fichiers LLM (mêmes faits que la page, aucun ajout)

- `public/llms.txt` ligne 8 : remplacer par l'entrée validée dans #22 (mêmes faits que la page) :
  `- [Services du Premier ministre](https://benoitvinceneux.com/services-du-premier-ministre): AI Product Lead à la DINUM depuis janvier 2026. Cinq fronts : données publiques pour l'IA (coordination du serveur MCP data.gouv.fr, 45 M de requêtes en 100 jours), stack de code agentique souveraine, évaluation LLM verticalisée (100 questions, +16 % de qualité), veille agentique, coaching produit.`
- `public/llms-full.txt` : réécrire la section entre `## Services du Premier ministre — DINUM` et le `---` qui précède `## Présidence de la République` comme transcription texte de la page (titre `## Services du Premier ministre : DINUM`, ligne URL inchangée, puis chapeau, Contexte, Mission : cinq fronts, Approche, Réalisations, Coordination de l'exposition des données, Convictions portées), sans « — » ni « · ». Supprimer « Offre data : 3 piliers + 1 chantier », l'ancien MCP data.gouv, ia.data.gouv.fr. Garder le style du fichier (pas de gras Markdown, puces `- `).

### 3. Vérification locale

1. `npx astro build`, puis les 4 commandes du tableau Tests.
2. Contrôle des séparateurs (« — », « · », « | ») :
   - `grep -nE '—|·|\|' dist/services-du-premier-ministre.html` : seuls résultats acceptables hors `<title>`, meta description et `<main>` (gabarit, #14) ;
   - `sed -n '8p' public/llms.txt | grep -E '—|·|\|'` : 0 résultat ;
   - `awk '/^## Services du Premier ministre/,/^## Présidence/' public/llms-full.txt | grep -nE '—|·|\|'` : 0 résultat.
3. `grep -n "3 millions\|Buzz\|ia.data.gouv\|CPO MCP\|Golden" dist/services-du-premier-ministre.html` : 0 résultat.
4. `git diff --stat` : seulement les 3 fichiers + `tasks/` ; front matter `cover`/`images` identiques.

### 4. Commit

`content: Services du Premier ministre, cinq fronts et intitulé AI Product Lead (#11)`. (`tasks/lessons.md` et ce plan sont déjà commités par le tech lead.)

## Points d'attention

- Attribution : le MCP data.gouv.fr est en **coordination et suivi produit**, jamais « construit » ni en tête des réalisations. Ne rien ajouter : pas de lien vers le benchmark de transcription (l'issue n'en donne pas), pas de lien MCP, pas de chiffre hors issue.
- Ne jamais citer ni nommer les « Sources » de l'issue (documents privés), ni la lettre de mission ou une doctrine non publiée.
- Le gabarit (`src/layouts/Base.astro`, `[slug].astro`) ou le pied de page peuvent contenir « · » ou « | » hors du contenu de la page : hors périmètre (#14). Le contrôle porte sur le `<title>`, la meta description et le contenu de `<main>`.
- `DILA / Légifrance` : la barre oblique n'est pas un séparateur interdit ; la liste reprend la page actuelle à l'identique.
- Placement de la liste des administrations (dans la puce « Accompagnement », avant les types d'aide, séparée par « ; ») : choix éditorial, l'issue dit seulement « inchangée » ; la phrase est figée ci-dessus.
- Première ligne du chapeau en gras, comme la page actuelle (seul le texte change).
- `.nvmrc` reste à 24.
