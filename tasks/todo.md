# #15 [CONTENU] ca-compte-pour-moi : cohérence des effectifs et de l'intitulé

Branche : `feat/bv-15-ca-compte-pour-moi` (déjà créée). PR `Closes #15` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Aucune décision de #2 en jeu (contenu seul, ni dépendance, ni réglage, ni secret).
Texte appliqué : version finale de #15, réponses de Benoit du 22/10/2026 incluses (et #23) :
- effectifs : on garde « 0 → 60 collaborateurs en 3 ans », on **retire** « 45 collaborateurs » de la ligne 2019 ;
- premiers collaborateurs : **COO, CMO, Head of Sales, CSM** ;
- période : **2014-2017** (écrite « 2014 à 2017 » dans le chapeau, comme la proposition).

## Critères d'acceptation

- [ ] Titre de page inchangé : `Ça Compte Pour Moi` (donc `<title>` inchangé).
- [ ] Chapeau, ligne 1 (gras conservé) : « Compagnie Fiduciaire : 25ᵉ cabinet d'expertise-comptable indépendant français (CA 30 M€, 400 collaborateurs) ».
- [ ] Chapeau, ligne 2 (italique conservé) : « Intrapreneur, Head of Product & GTM, premier profil produit : 2014 à 2017 ».
- [ ] Paragraphe d'intro et « Mission » : inchangés.
- [ ] « Périmètre », dernière puce : « Constitution et management des 10 premiers collaborateurs (COO, CMO, Head of Sales, CSM) » (le verbe change : « Recrutement » devient « Constitution »). Autres puces inchangées.
- [ ] « Résultats » : liste actuelle conservée (dont « 0 → 60 collaborateurs en 3 ans »), sauf « Début 2019 : 3 000 clients » (sans « 45 collaborateurs »).
- [ ] Titre de section : `### Distinctions : Trophées Les Echos 2015`.
- [ ] Puces des distinctions : « Or : Marketing digital », « Or : Stratégie de communication & Innovation de l'offre », « Prix spécial du jury » (seul « — » remplacé par « : », règle transverse de #23).
- [ ] Meta description (l'issue n'en donne pas, dérivée du nouveau chapeau) : `Compagnie Fiduciaire : 25ᵉ cabinet d'expertise-comptable indépendant français (CA 30 M€, 400 collaborateurs). Intrapreneur, Head of Product & GTM, premier profil produit : 2014 à 2017.`
- [ ] Plus aucune trace sur la page de : « 2014-2016 », « 45 collaborateurs », « Recrutement et management », « · ».
- [ ] Aucun « — », « · », « | » dans le texte visible du `<main>` et la meta description de la page.
- [ ] URL, slug, `title`, `order`, `textposition`, `cover`, `images` inchangés à l'octet. Aucun lien ajouté.
- [ ] `public/llms.txt` et `public/llms-full.txt` : passages Ça Compte Pour Moi alignés (étape 2).

## Tests (catalogue #10)

Aucun test à ajouter (l'issue n'en demande pas). Les seules références des tests à cette page sont des listes d'URL (`tests/test_dist.py` l. 23, `tests/test_a11y.py` l. 7). T-BV-CONT-01 / T-BV-SEO-01 ne vérifient que la présence et la non-vacuité de `description` (pas de limite de longueur). Tests qui doivent rester verts sans modification :

| ID | Fichier | Lien avec #15 |
|---|---|---|
| T-BV-BUILD-01 | `npx astro build` + `tests/test_dist.py` | build de la page modifiée |
| T-BV-CONT-01, T-BV-CONT-02, T-BV-CONT-03 | `tests/test_content.py` | front matter (`description` non vide, `cover`/`images` existants), pas de KirbyText |
| T-BV-SPE-01 | `tests/test_dist.py` | URL `benoitvinceneux.com/...` des `llms*.txt` : `/ca-compte-pour-moi` est 200 dans `legacy-urls.txt` ; n'ajouter aucune URL du domaine |
| T-BV-SEO-01 | `tests/test_dist.py` | canonical, meta description non vide, `<title>` unique |
| T-BV-LNK-01, T-BV-LNK-02, T-BV-HOST-01 | `tests/test_links.py` | aucun lien ni hôte nouveau |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` (+ `tests/test_repo.py`) | HTML de la page |
| T-BV-HTTP-01 | `tests/http_check.sh` sur Apache local servant `dist/` | page et `llms*.txt` en 200 |
| T-BV-A11Y-01, T-BV-A11Y-02 | `tests/e2e/a11y.spec.ts`, `tests/test_a11y.py` | axe sur la page |
| Autres (ART, INV, SPE-02..06, HTA, CSP, BUD, DEP, WF, GUARD, IMP) | `tests/*.py` | non concernés, doivent rester verts |

Commande : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html"`, puis Apache local + `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh`, puis `npx playwright test`.

## Fichiers modifiés (3, rien à créer)

1. `src/content/projects/ca-compte-pour-moi.md` : front matter `description` + chapeau, dernière puce de Périmètre, ligne 2019, section Distinctions.
2. `public/llms.txt` : ligne 13 seulement.
3. `public/llms-full.txt` : section `## Ça Compte Pour Moi` seulement (lignes ~255 à 289, jusqu'au `---` qui précède `## Pierre Fabre`).

Hors périmètre (ne pas toucher) : `src/pages/a-propos.astro` et la ligne 37 de `public/llms-full.txt` (parcours À propos : « Ça Compte Pour Moi · intrapreneur · 2014 – 2016 ») relèvent de #13 et #22 ; l'écart de dates qui y subsiste est connu, ce n'est pas un oubli. Gabarit, séparateur du `<title>` : #14.

## Étapes

### 1. Page projet

Garder `title`, `order`, `textposition`, `cover`, `images` à l'octet. Remplacer `description` par :

```
description: "Compagnie Fiduciaire : 25ᵉ cabinet d'expertise-comptable indépendant français (CA 30 M€, 400 collaborateurs). Intrapreneur, Head of Product & GTM, premier profil produit : 2014 à 2017."
```

Corps cible (conventions actuelles conservées : deux espaces en fin de ligne dans les listes et le chapeau) :

```markdown
**Compagnie Fiduciaire : 25ᵉ cabinet d'expertise-comptable indépendant français (CA 30 M€, 400 collaborateurs)**  
*Intrapreneur, Head of Product & GTM, premier profil produit : 2014 à 2017*

Création de la première offre d'expertise-comptable 100 % digitale en France. De la page blanche au lancement, puis à la rentabilité.

### Mission

Lancer une spin-off digitale pour un acteur traditionnel de l'expertise-comptable. Mission complète : stratégie, marque, business plan, modèle économique, produit, GTM, RH.

### Périmètre

- Stratégie, positionnement, création de la marque, business plan, modèle économique  
- UX, wireframes, conception fonctionnelle de la plateforme  
- Pilotage d'un pool de partenaires (dev, webdesign, RP, achats médias)  
- Plan de lancement multi-canal et plan RH  
- Constitution et management des 10 premiers collaborateurs (COO, CMO, Head of Sales, CSM)

### Résultats

- Lancement février 2015 avec 2 collaborateurs et 0 client  
- 1 M€ d'ARR atteint un an après le lancement  
- Rentable 3 ans après le lancement  
- 0 → 60 collaborateurs en 3 ans  
- Début 2019 : 3 000 clients  
- Top 3 du marché après 4 ans

### Distinctions : Trophées Les Echos 2015

- Or : Marketing digital  
- Or : Stratégie de communication & Innovation de l'offre  
- Prix spécial du jury
```

### 2. Fichiers LLM (mêmes faits que la page, aucun ajout)

- `public/llms.txt` ligne 13 : seul l'intitulé et la période changent :
  `- [Ça Compte Pour Moi](https://benoitvinceneux.com/ca-compte-pour-moi): Intrapreneur, Head of Product & GTM, premier profil produit (2014-2017). Première offre d'expertise-comptable 100 % digitale en France pour la Compagnie Fiduciaire. 0 → 1 M€ ARR an 1, rentable an 3, 0 → 60 collaborateurs en 3 ans, top 3 du marché en 4 ans, 3 000 clients en 2019. 3 Trophées Les Echos 2015 (Or Marketing digital, Or Stratégie & Innovation, Prix spécial du jury).`
- `public/llms-full.txt`, section `## Ça Compte Pour Moi` (style du fichier : pas de gras, puces `- `, chapeau terminé par des points) :
  - l. 259 : `Compagnie Fiduciaire : 25ᵉ cabinet d'expertise-comptable indépendant français (CA 30 M€, 400 collaborateurs).`
  - l. 260 : `Intrapreneur, Head of Product & GTM, premier profil produit : 2014 à 2017.`
  - l. 274 : `- Constitution et management des 10 premiers collaborateurs (COO, CMO, Head of Sales, CSM)`
  - l. 282 : `- Début 2019 : 3 000 clients`
  - l. 284 : `### Distinctions : Trophées Les Echos 2015`
  - l. 286-287 : `- Or : Marketing digital`, `- Or : Stratégie de communication & Innovation de l'offre`
  - Le reste de la section est inchangé.

### 3. Vérification locale

1. `npx astro build`, puis les commandes du tableau Tests.
2. Séparateurs :
   - `grep -nE '—|·|\|' dist/ca-compte-pour-moi.html` : résultats acceptables seulement hors `<main>` et meta description (gabarit, #14) ;
   - `sed -n '13p' public/llms.txt | grep -E '—|·|\|'` : 0 résultat ;
   - `awk '/^## Ça Compte Pour Moi/,/^## Pierre Fabre/' public/llms-full.txt | grep -nE '—|·|\|'` : 0 résultat.
3. `grep -nE "2014-2016|45 collaborateurs|Recrutement et management" dist/ca-compte-pour-moi.html`, `sed -n '13p' public/llms.txt` et la section de `llms-full.txt` : 0 résultat.
4. `git diff --stat` : seulement les 3 fichiers + `tasks/todo.md` ; `cover`/`images` identiques.

### 4. Commit

`content: Ça Compte Pour Moi, effectifs, intitulé et période 2014-2017 (#15)` (inclut `tasks/todo.md`).

## Points d'attention

- Attribution : « premier profil produit » vient de l'issue ; ne rien ajouter d'autre (pas de CRO, pas de chiffre, pas d'explication de la baisse d'effectifs, pas de lien).
- Distinctions : l'issue ne donne que le nouveau titre ; les puces ne changent que par le remplacement de « — » par « : » (règle transverse), aucun mot modifié.
- « → » (flèche) n'est pas un séparateur interdit : conservé.
- Ne jamais citer ni nommer les « Sources » de l'issue (documents privés), ni de doctrine non publiée.
- Ne pas toucher au gabarit (`src/layouts/Base.astro`), ni à `.nvmrc` (24).
