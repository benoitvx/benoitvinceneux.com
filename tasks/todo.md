# #18 [CONTENU] sigfox : date du GNOC, note de rédaction en ligne

Branche : `feat/bv-18-sigfox` (déjà créée). PR `Closes #18` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Aucune décision de #2 en jeu (contenu seul, ni dépendance, ni réglage, ni secret).
Texte appliqué : version finale de #18, réponse de Benoit du 22/10/2026 incluse :
- InVision : le domaine ne répond plus, **la ligne « Ressource » est supprimée** ;
- GNOC : **2016** (pas 2018), cohérent avec l'À propos (« 2016 et 2019-2020 ») ;
- #23 ne contient rien de spécifique à Sigfox.

## Critères d'acceptation

- [ ] Titre de page inchangé : `Sigfox` (donc `<title>` inchangé).
- [ ] Chapeau ajouté en tête du corps, paragraphe simple, texte exact : « Sigfox : opérateur télécom 0G pour objets connectés. »
- [ ] Titre de mission 1 : « Sigfox Device Management System : 2019-2020 » (`###` conservé, « — » devient « : »).
- [ ] Titre de mission 2 : « Sigfox Global Network Operation Center : 2016 » (`###` conservé, 2018 devient 2016).
- [ ] La ligne « **Ressource** : 100 écrans produits sur InVision *(lien existant)* » est supprimée (et la ligne vide qui la précède, pour ne pas laisser deux lignes vides).
- [ ] Meta description, telle quelle (donnée par l'issue) :
  `Sigfox : Product Manager du premier espace client B2B (2019-2020) et d'un outil de data visualisation temps réel pour le centre d'opérations réseau (2016).`
- [ ] Tout le reste du corps inchangé à l'octet : rôles *Product Manager*, descriptions, Périmètre, Résultats, `---` entre les missions, bloc iframe YouTube (style en ligne, `src`, `title`).
- [ ] Plus aucune trace sur la page de : « 2018 », « InVision », « lien existant ».
- [ ] Aucun « — », « · », « | » dans le texte visible du `<main>` et la meta description de la page.
- [ ] URL, slug, `title`, `order`, `textposition`, `cover`, `images`, URL de la vidéo inchangés. Aucun lien ajouté.
- [ ] `public/llms.txt` et `public/llms-full.txt` : passages Sigfox alignés (étape 2).

## Tests (catalogue #10)

Aucun test à ajouter (l'issue n'en demande pas). La page n'est référencée que par des listes d'URL (`tests/test_dist.py` l. 18, `tests/legacy-urls.txt` l. 4, `tests/test_a11y.py` l. 6) et par T-BV-CONT (test_content.py l. 46, retire `description` de sigfox.md dans une copie : le champ doit rester sur une seule ligne `description: "..."`). Tests qui doivent rester verts sans modification :

| ID | Fichier | Lien avec #18 |
|---|---|---|
| T-BV-BUILD-01 | `npx astro build` + `tests/test_dist.py` | build de la page modifiée |
| T-BV-CONT-01, T-BV-CONT-02, T-BV-CONT-03 | `tests/test_content.py` | front matter (`description` non vide, une ligne), `cover`/`images` existants, pas de KirbyText |
| T-BV-SPE-01 | `tests/test_dist.py` | URL du domaine dans `llms*.txt` : `/sigfox` déjà en 200, n'en ajouter aucune |
| T-BV-SEO-01 | `tests/test_dist.py` | canonical, meta description non vide, `<title>` unique |
| T-BV-LNK-01, T-BV-LNK-02, T-BV-HOST-01 | `tests/test_links.py` | aucun lien ni hôte nouveau (youtube-nocookie déjà autorisé) |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` (+ `tests/test_repo.py`) | HTML de la page ; exception `no-inline-style` de `tests/exceptions.json` intacte |
| T-BV-HTTP-01 | `tests/http_check.sh` sur Apache local servant `dist/` | page et `llms*.txt` en 200 |
| T-BV-A11Y-01, T-BV-A11Y-02 | `tests/e2e/a11y.spec.ts`, `tests/test_a11y.py` | axe sur la page ; exception iframe YouTube de `tests/exceptions.json` intacte |
| Autres (ART, INV, SPE-02..06, HTA, CSP, BUD, DEP, WF, GUARD, IMP) | `tests/*.py` | non concernés, doivent rester verts |

Commande : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html"`, puis Apache local + `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh`, puis `npx playwright test`.

## Fichiers modifiés (3, rien à créer)

1. `src/content/projects/sigfox.md` : front matter `description`, chapeau, 2 titres `###`, suppression de la ligne Ressource.
2. `public/llms.txt` : ligne 11 seulement.
3. `public/llms-full.txt` : section `## Sigfox` seulement (l. 185 à 217).

Hors périmètre (ne pas toucher) : `public/llms-full.txt` l. 33 (parcours À propos « Sigfox · Product Manager · 2016 et 2019-2020 », dates déjà justes, séparateurs : #13/#22) ; `tests/exceptions.json` ; gabarit et format du `<title>` (#14).

## Étapes

### 1. Page projet

Garder `title`, `order`, `textposition`, `cover`, `images` à l'octet. Remplacer `description` par :

```
description: "Sigfox : Product Manager du premier espace client B2B (2019-2020) et d'un outil de data visualisation temps réel pour le centre d'opérations réseau (2016)."
```

Début du corps :

```markdown
Sigfox : opérateur télécom 0G pour objets connectés.

### Sigfox Device Management System : 2019-2020
```

Fin de la mission 1 : la section se termine par les Résultats (`- Temps passé en support sur les factures : 10 min → 1 min`), puis ligne vide, `---`. Supprimer la ligne `**Ressource** : …` et une des lignes vides qui l'entourent.

```markdown
### Sigfox Global Network Operation Center : 2016
```

Rien d'autre ne change (iframe comprise).

### 2. Fichiers pour les LLM (mêmes faits, aucun ajout)

`public/llms.txt` l. 11, remplacer par :

```
- [Sigfox](https://benoitvinceneux.com/sigfox): Opérateur télécom 0G pour objets connectés. Product Manager. DMS (2019-2020) : espace client B2B grands comptes (~100 écrans, équipe 2-10 devs, −50 % délais de paiement, support facturation 10 min → 1 min). GNOC (2016) : data viz temps réel sur mur de 12 écrans (−65 % temps d'identification d'erreur réseau).
```

`public/llms-full.txt`, section `## Sigfox` :

- après `URL : https://benoitvinceneux.com/sigfox` et sa ligne vide, ajouter `Sigfox : opérateur télécom 0G pour objets connectés.` suivi d'une ligne vide ;
- `### Sigfox Device Management System — 2019-2020` devient `### Sigfox Device Management System : 2019-2020` ;
- supprimer `Ressource : 100 écrans produits sur InVision.` et la ligne vide qui suit ;
- `### Sigfox Global Network Operation Center — 2018` devient `### Sigfox Global Network Operation Center : 2016` ;
- le reste inchangé.

### 3. Vérifications

- Build + tests (commande ci-dessus), Apache local + `http_check.sh`, Playwright.
- `grep -nE '—|·|\|' src/content/projects/sigfox.md` : aucune ligne.
- `grep -nE '2018|InVision|lien existant' src/content/projects/sigfox.md` et dans les passages Sigfox de `llms.txt` / `llms-full.txt` : aucun résultat.
- `dist/sigfox.html` : meta description identique à l'issue ; iframe présente avec `title` et le même `src`.
- `git diff` : seulement les 3 fichiers listés (+ `tasks/todo.md`).

## Points d'attention

- Ne pas toucher au bloc `<div style=…><iframe …>` : les exceptions html-validate (`no-inline-style`) et axe (iframe youtube-nocookie) en dépendent.
- Garder le séparateur Markdown `---` entre les missions (filet `<hr>`, pas un séparateur de texte).
- « ~100 écrans » dans Périmètre reste (fait de conception UX/UI, pas la ressource InVision).
- Ne rien ajouter : pas de lien de remplacement pour InVision, pas de chiffre, pas de reformulation des Périmètres ni Résultats.
- Les sources de l'issue (documents privés de Benoit) ne sont jamais citées sur le site.
