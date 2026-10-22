# #16 [CONTENU] notresante : dates et taille d'équipe

Branche : `feat/bv-16-notresante` (déjà créée). PR `Closes #16` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Aucune décision de #2 en jeu (contenu seul, ni dépendance, ni réglage, ni secret).
Texte appliqué : version finale de #16, réponses de Benoit du 22/10/2026 incluses (et #23) :
- période : **2016-2019** (écrite « 2016 à 2019 » dans le chapeau et la meta, comme la proposition) ;
- équipe : **1 PO, 1 designer, 3 développeurs** (ligne actuelle conservée ; pas de « 1 UX, 1 UI, 5 développeurs »).

## Critères d'acceptation

- [ ] Titre de page inchangé : `NotreSanté` (donc `<title>` inchangé).
- [ ] Chapeau, ligne 1 (gras conservé) : « NotreSanté : startup e-santé ».
- [ ] Chapeau, ligne 2 (italique conservé) : « Cofondateur, CPO : 2016 à 2019 ».
- [ ] Paragraphe d'intro, « Vision produit », « Ce qu'il en reste » : inchangés.
- [ ] « Périmètre », trois lignes données par l'issue :
  - « Management : 1 PO, 1 designer, 3 développeurs » (identique à l'actuelle) ;
  - « Levée de fonds, structuration juridique, constitution de l'équipe » (« recrutement » devient « constitution de l'équipe ») ;
  - « Hébergement de Données de Santé (HDS) : conformité de bout en bout » (« — » devient « : », « bout-en-bout » devient « de bout en bout »).
  Les trois autres puces (Produit end-to-end, Stratégie produit, Partenariats) sont inchangées.
- [ ] « Distinctions » :
  - « 2019 : Trophée de la Citoyenneté et de la Solidarité, Conseil départemental de la Haute-Garonne » (« départemental » en minuscule, comme l'issue) ;
  - « 2018 : Prix de l'innovation, CCI Occitanie ».
- [ ] Meta description (donnée par l'issue, appliquée telle quelle) : `NotreSanté, startup e-santé : cofondateur et CPO, 2016 à 2019.`
- [ ] Plus aucune trace sur la page de : « 2017-2020 », « recrutement », « bout-en-bout », « Conseil Départemental ».
- [ ] Aucun « — », « · », « | » dans le texte visible du `<main>` et la meta description de la page.
- [ ] URL, slug, `title`, `order`, `textposition`, `cover`, `images` inchangés à l'octet. Aucun lien ajouté.
- [ ] `public/llms.txt` et `public/llms-full.txt` : passages NotreSanté alignés (étape 2).

## Tests (catalogue #10)

Aucun test à ajouter (l'issue n'en demande pas). Les tests ne référencent cette page que par des listes d'URL (`tests/test_dist.py` l. 22, `tests/legacy-urls.txt` l. 8, `tests/test_a11y.py` l. 6). Tests qui doivent rester verts sans modification :

| ID | Fichier | Lien avec #16 |
|---|---|---|
| T-BV-BUILD-01 | `npx astro build` + `tests/test_dist.py` | build de la page modifiée |
| T-BV-CONT-01, T-BV-CONT-02, T-BV-CONT-03 | `tests/test_content.py` | front matter (`description` non vide, `cover`/`images` existants), pas de KirbyText |
| T-BV-SPE-01 | `tests/test_dist.py` | URL `benoitvinceneux.com/...` des `llms*.txt` : `/notresante` est 200 dans `legacy-urls.txt` ; n'ajouter aucune URL du domaine |
| T-BV-SEO-01 | `tests/test_dist.py` | canonical, meta description non vide, `<title>` unique |
| T-BV-LNK-01, T-BV-LNK-02, T-BV-HOST-01 | `tests/test_links.py` | aucun lien ni hôte nouveau |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` (+ `tests/test_repo.py`) | HTML de la page |
| T-BV-HTTP-01 | `tests/http_check.sh` sur Apache local servant `dist/` | page et `llms*.txt` en 200 |
| T-BV-A11Y-01, T-BV-A11Y-02 | `tests/e2e/a11y.spec.ts`, `tests/test_a11y.py` | axe sur la page |
| Autres (ART, INV, SPE-02..06, HTA, CSP, BUD, DEP, WF, GUARD, IMP) | `tests/*.py` | non concernés, doivent rester verts |

Commande : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html"`, puis Apache local + `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh`, puis `npx playwright test`.

## Fichiers modifiés (3, rien à créer)

1. `src/content/projects/notresante.md` : front matter `description`, chapeau, 2 puces de Périmètre, 2 puces de Distinctions.
2. `public/llms.txt` : ligne 12 seulement.
3. `public/llms-full.txt` : section `## NotreSanté` seulement (l. 220 à 252, jusqu'au `---` qui précède `## Ça Compte Pour Moi`).

Hors périmètre (ne pas toucher) : `src/pages/a-propos.astro` l. 33 et `public/llms-full.txt` l. 34 (parcours À propos : « NotreSanté · cofondateur, CPO · 2017 – 2020 ») relèvent de #13 et #22 ; l'écart de dates qui y subsiste est connu, ce n'est pas un oubli (même choix que #15). Gabarit, séparateur du `<title>` : #14.

## Étapes

### 1. Page projet

Garder `title`, `order`, `textposition`, `cover`, `images` à l'octet. Remplacer `description` par :

```
description: "NotreSanté, startup e-santé : cofondateur et CPO, 2016 à 2019."
```

Corps cible (conventions actuelles conservées : deux espaces en fin de ligne dans le chapeau et les listes, sauf dernière puce) :

```markdown
**NotreSanté : startup e-santé**  
*Cofondateur, CPO : 2016 à 2019*

Application mobile iOS / Android pour la gestion de la santé des familles avec enfants en bas âge. Cible B2C : familles avec enfants de moins de 10 ans.

### Vision produit

(inchangé)

### Périmètre

- Produit end-to-end : discovery, conception, pilotage du dev, go-to-market  
- Stratégie produit, recherche utilisateurs, validation UX/UI  
- Management : 1 PO, 1 designer, 3 développeurs  
- Levée de fonds, structuration juridique, constitution de l'équipe  
- Hébergement de Données de Santé (HDS) : conformité de bout en bout  
- Partenariats laboratoires pharmaceutiques et pharmaciens

### Distinctions

- 2019 : Trophée de la Citoyenneté et de la Solidarité, Conseil départemental de la Haute-Garonne  
- 2018 : Prix de l'innovation, CCI Occitanie

### Ce qu'il en reste

(inchangé)
```

### 2. Fichiers LLM (mêmes faits que la page, aucun ajout)

- `public/llms.txt` ligne 12 : seule la période change, `(2017-2020)` devient `(2016-2019)` ; le reste de la ligne est inchangé (elle ne contient ni « — », ni « · », ni « | »).
- `public/llms-full.txt`, section `## NotreSanté` (style du fichier : pas de gras, puces `- `, chapeau terminé par des points) :
  - l. 224 : `NotreSanté : startup e-santé.`
  - l. 225 : `Cofondateur, CPO : 2016 à 2019.`
  - puce Levée de fonds : `- Levée de fonds, structuration juridique, constitution de l'équipe`
  - puce HDS : `- Hébergement de Données de Santé (HDS) : conformité de bout en bout`
  - distinctions : `- 2019 : Trophée de la Citoyenneté et de la Solidarité, Conseil départemental de la Haute-Garonne`, `- 2018 : Prix de l'innovation, CCI Occitanie`
  - Le reste de la section est inchangé.

### 3. Vérification locale

1. `npx astro build`, puis les commandes du tableau Tests.
2. Séparateurs :
   - `grep -nE '—|·|\|' dist/notresante.html` : résultats acceptables seulement hors `<main>` et meta description (gabarit, #14) ;
   - `sed -n '12p' public/llms.txt | grep -E '—|·|\|'` : 0 résultat ;
   - `awk '/^## NotreSanté/,/^## Ça Compte Pour Moi/' public/llms-full.txt | grep -nE '—|·|\|'` : 0 résultat.
3. `grep -niE "2017-2020|recrutement|bout-en-bout|Conseil Départemental" dist/notresante.html`, `sed -n '12p' public/llms.txt` et la section de `llms-full.txt` : 0 résultat.
4. `git diff --stat` : seulement les 3 fichiers + `tasks/todo.md` ; `cover`/`images` identiques.

### 4. Commit

`content: NotreSanté, période 2016-2019 et constitution de l'équipe (#16)` (inclut `tasks/todo.md`).

## Points d'attention

- Attribution : ne rien ajouter (pas l'équipe LinkedIn « 1 UX, 1 UI, 5 développeurs », pas de chiffre, pas de lien, pas de mention CV).
- « iOS / Android » (barre oblique), « × » et « end-to-end » ne sont pas des séparateurs interdits : conservés.
- Ne jamais citer ni nommer les « Sources » de l'issue (documents privés), ni de doctrine non publiée.
- Ne pas toucher au gabarit (`src/layouts/Base.astro`), ni à `.nvmrc` (24).
