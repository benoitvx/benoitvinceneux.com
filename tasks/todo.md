# #17 [CONTENU] pierre-fabre : taux de connexion 80 %, dates 2014-2018

Branche : `feat/bv-17-pierre-fabre` (déjà créée). PR `Closes #17` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Aucune décision de #2 en jeu (contenu seul, ni dépendance, ni réglage, ni secret).
Texte appliqué : version finale de #17, réponses de Benoit du 22/10/2026 incluses (et #23) :
- taux de connexion : **80 %** (pas 75 %) ;
- période : **2014-2018**, écrite « 2014 à 2018 » comme la proposition ;
- chapeau : traduction fidèle annoncée par l'issue de « 80 % of all French pharmacies; 80 % of them log in at least once a week » ;
- règle : ne plus associer « 16 000 » à un pourcentage (le « 16 000 » disparaît de la page).

## Critères d'acceptation

- [ ] Titre de page inchangé : `Pierre Fabre` (donc `<title>` inchangé).
- [ ] Chapeau, ligne 1 (gras conservé) : « Laboratoires Pierre Fabre : Espace Pro B2B ».
- [ ] Chapeau, ligne 2 (italique conservé) : « 1ᵉʳ Product Manager B2B : 2014 à 2018 ».
- [ ] Chapeau, paragraphe : « Réinventer la relation entre le Laboratoire et les pharmacies clientes : **80 % des pharmacies françaises** ; **80 % d'entre elles se connectent au moins une fois par semaine**. » (gras comme l'issue).
- [ ] « Contexte », « Mission » et le contenu des 4 phases (Explorer, Concevoir, Réaliser, Grandir) : inchangés.
- [ ] Titre de section : « Périmètre : 4 phases » (« — » devient « : »).
- [ ] « Résultats », exactement deux puces :
  - « **3 heures gagnées** par semaine pour les pharmaciens utilisateurs » (identique) ;
  - « Une adoption B2B sur laquelle la stratégie digitale de Pierre Fabre s'est ensuite appuyée » (ajout de « Une » et « de »).
  La puce « 80 % des pharmaciens clients connectés… » est supprimée (le taux passe dans le chapeau).
- [ ] Meta description (l'issue n'en donne pas ; réalignée sur le chapeau sans rien ajouter, même forme que #16) :
  `Laboratoires Pierre Fabre, Espace Pro B2B : 1ᵉʳ Product Manager B2B, 2014 à 2018.`
- [ ] Plus aucune trace sur la page de : « 2011 », « 2017 », « 16 000 », « 1× », « 75 % ».
- [ ] Aucun « — », « · », « | » dans le texte visible du `<main>` et la meta description de la page.
- [ ] URL, slug, `title`, `order`, `textposition`, `cover`, `images` inchangés à l'octet. Aucun lien ajouté.
- [ ] `public/llms.txt` et `public/llms-full.txt` : passages Pierre Fabre alignés (étape 2).

## Tests (catalogue #10)

Aucun test à ajouter (l'issue n'en demande pas). Les tests ne référencent cette page que par des listes d'URL (`tests/test_dist.py` l. 21, `tests/legacy-urls.txt` l. 7, `tests/test_a11y.py` l. 7). Tests qui doivent rester verts sans modification :

| ID | Fichier | Lien avec #17 |
|---|---|---|
| T-BV-BUILD-01 | `npx astro build` + `tests/test_dist.py` | build de la page modifiée |
| T-BV-CONT-01, T-BV-CONT-02, T-BV-CONT-03 | `tests/test_content.py` | front matter (`description` non vide, `cover`/`images` existants), pas de KirbyText |
| T-BV-SPE-01 | `tests/test_dist.py` | URL `benoitvinceneux.com/...` des `llms*.txt` : `/pierre-fabre` est 200 dans `legacy-urls.txt` ; n'ajouter aucune URL du domaine |
| T-BV-SEO-01 | `tests/test_dist.py` | canonical, meta description non vide, `<title>` unique |
| T-BV-LNK-01, T-BV-LNK-02, T-BV-HOST-01 | `tests/test_links.py` | aucun lien ni hôte nouveau |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` (+ `tests/test_repo.py`) | HTML de la page |
| T-BV-HTTP-01 | `tests/http_check.sh` sur Apache local servant `dist/` | page et `llms*.txt` en 200 |
| T-BV-A11Y-01, T-BV-A11Y-02 | `tests/e2e/a11y.spec.ts`, `tests/test_a11y.py` | axe sur la page |
| Autres (ART, INV, SPE-02..06, HTA, CSP, BUD, DEP, WF, GUARD, IMP) | `tests/*.py` | non concernés, doivent rester verts |

Commande : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html"`, puis Apache local + `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh`, puis `npx playwright test`.

## Fichiers modifiés (3, rien à créer)

1. `src/content/projects/pierre-fabre.md` : front matter `description`, chapeau (3 lignes), titre « Périmètre », section « Résultats ».
2. `public/llms.txt` : ligne 14 seulement.
3. `public/llms-full.txt` : section `## Pierre Fabre` seulement (l. 293 à 325, jusqu'au `---` qui précède `## LePharmacien.fr`).

Hors périmètre (ne pas toucher) : `src/pages/a-propos.astro` l. 35 et `public/llms-full.txt` l. 36 (parcours À propos : « Laboratoires Pierre Fabre · 1ᵉʳ PM B2B · 2011 – 2017 (16 000 pharmaciens, 80 % connectés ≥ 1×/semaine) ») relèvent de #13 et #22 ; l'écart qui y subsiste (dates, 16 000 associé à un pourcentage) est connu, ce n'est pas un oubli (même choix que #15 et #16). Gabarit, séparateur du `<title>` : #14.

## Étapes

### 1. Page projet

Garder `title`, `order`, `textposition`, `cover`, `images` à l'octet. Remplacer `description` par :

```
description: "Laboratoires Pierre Fabre, Espace Pro B2B : 1ᵉʳ Product Manager B2B, 2014 à 2018."
```

Modifications du corps (conventions actuelles conservées : deux espaces en fin de ligne dans le chapeau et les listes, sauf dernière puce) :

```markdown
**Laboratoires Pierre Fabre : Espace Pro B2B**  
*1ᵉʳ Product Manager B2B : 2014 à 2018*

Réinventer la relation entre le Laboratoire et les pharmacies clientes : **80 % des pharmacies françaises** ; **80 % d'entre elles se connectent au moins une fois par semaine**.
```

```markdown
### Périmètre : 4 phases
```

```markdown
### Résultats

- **3 heures gagnées** par semaine pour les pharmaciens utilisateurs  
- Une adoption B2B sur laquelle la stratégie digitale de Pierre Fabre s'est ensuite appuyée
```

Tout le reste du corps (Contexte, Mission, Explorer, Concevoir, Réaliser, Grandir) reste à l'octet.

### 2. Fichiers pour les LLM (mêmes faits, aucun ajout)

`public/llms.txt` l. 14, remplacer par :

```
- [Pierre Fabre](https://benoitvinceneux.com/pierre-fabre): 1ᵉʳ Product Manager B2B (2014-2018). Espace Pro B2B des Laboratoires Pierre Fabre : centre névralgique relationnel avec les pharmacies clientes (commande en ligne, gestion des factures, e-learning, e-merchandising, retours produits). Lancement septembre 2015. 80 % des pharmacies françaises ; 80 % d'entre elles se connectent au moins une fois par semaine. 3 heures gagnées par semaine pour les pharmaciens utilisateurs.
```

`public/llms-full.txt`, section `## Pierre Fabre` :

- l. 297-298 : `Laboratoires Pierre Fabre : Espace Pro B2B.` puis `1ᵉʳ Product Manager B2B : 2014 à 2018.`
- l. 300 : `Mission : réinventer la relation entre le Laboratoire et les pharmacies clientes : 80 % des pharmacies françaises ; 80 % d'entre elles se connectent au moins une fois par semaine.`
- `### Périmètre — 4 phases` devient `### Périmètre : 4 phases`.
- `### Résultats` : deux puces seulement :
  - `- 3 heures gagnées par semaine pour les pharmaciens utilisateurs`
  - `- Une adoption B2B sur laquelle la stratégie digitale de Pierre Fabre s'est ensuite appuyée`
- Contexte, Objectifs de mission, puces des 4 phases : inchangés.

### 3. Vérifications

- Build + tests (commande ci-dessus), Apache local + `http_check.sh`, Playwright.
- `grep -nE '—|·|\|' src/content/projects/pierre-fabre.md` : aucune ligne hors front matter `cover`/`images` (les `,` des srcset ne sont pas concernés ; vérifier qu'il n'y a rien).
- `grep -nE '2011|2017|16 000|1×|75 %' src/content/projects/pierre-fabre.md` et dans la section Pierre Fabre de `llms.txt` / `llms-full.txt` (hors l. 36 du parcours, #13/#22) : aucun résultat.
- `git diff` : seulement les 3 fichiers listés (+ `tasks/todo.md`).

## Points d'attention

- Ne pas réintroduire « 16 000 » nulle part sur la page ni dans les passages Pierre Fabre des `llms*.txt` (règle de l'issue).
- « Laboratoire » garde sa majuscule (texte actuel et issue).
- L'espace avant « ; » et « % » suit l'issue (« françaises** ; ** », « 80 % ») : reproduire tel quel ; ne pas inventer d'espace insécable spécial si le fichier n'en utilise pas.
- Ne rien ajouter : pas de lien, pas de chiffre (pas de « 75 % », pas de « 16 000 »), pas de reformulation du Contexte ni des phases.
- Les sources de l'issue (CV, liste d'expériences) ne sont jamais citées sur le site.
