# #3 [BV-01] Socle Astro et job CI `test`

Branche : `feat/bv-01-socle-astro`. PR : `Closes #3` (ouverte par l'orchestrateur).
Décision liée : D-BV4 (#2, validée) : `dependencies` = `astro` seul ; `devDependencies` = `@playwright/test`, `@axe-core/playwright`, `html-validate`, versions exactes.

## Critères d'acceptation (issue #3)

- [ ] `package.json` : `dependencies` = `astro` seul (les `devDependencies` suivent D-BV4 ; la note CTO de #3 prime sur le scénario QA 8 « pas de devDependencies »)
- [ ] Une PR dont le build échoue a un check `test` rouge
- [ ] Un push sur `master` déploie toujours `site/`, sans changement visible (même commande rsync, même cible)
- [ ] Aucun `${{ secrets.* }}` dans une ligne `run:`
- [ ] Aucune action référencée par tag mobile (SHA de 40 caractères uniquement)
- [ ] Dependabot actif sur `npm` et `github-actions` (hebdomadaire)
- [ ] Projet Astro : `build.format: 'file'`, `trailingSlash: 'never'`, `.nvmrc` = `24`, `package-lock.json` versionné
- [ ] `site/static/` copié tel quel dans `public/static/` ; `master.css` chargé par `<link rel="stylesheet" href="/static/master.css">` dans `Base.astro` (pas d'import dans `src/`, pas d'URL `/_astro/…`)
- [ ] `permissions: contents: read` au niveau du workflow ; déclencheurs `push` (master), `pull_request`, `workflow_dispatch`

## Tests à livrer (catalogue #10)

| ID | Porté par | Contenu |
|---|---|---|
| T-BV-BUILD-01 | étape `npx astro build` du job `test` + assertion `dist/index.html` existe dans `tests/test_dist.py` | code retour 0, `dist/index.html` présent |
| T-BV-DEP-01 | `tests/test_repo.py` | `dependencies` == `{astro}` ; `devDependencies` ⊆ liste D-BV4 ; chaque version `^\d+\.\d+\.\d+$` ; `package-lock.json` présent ; `.nvmrc` (strip) == `24` |
| T-BV-WF-01 | `tests/test_repo.py` | chaque `uses:` de `.github/workflows/*.yml` finit par `@[0-9a-f]{40}` (commentaire `# vX` toléré après) |
| T-BV-WF-02 | `tests/test_repo.py` | toute ligne contenant `secrets.` : la ligne non vide précédente la plus proche d'indentation strictement inférieure vaut `env:` |
| T-BV-WF-03 | `tests/test_repo.py` | `permissions:` + `contents: read` au niveau racine ; `push` avec `branches: [master]`, `pull_request`, `workflow_dispatch` ; job `test:` présent (regex, pas de parseur YAML) |
| T-BV-CSS-01 | `tests/test_dist.py` | `dist/static/` identique à `site/static/` récursivement, comparaison du **contenu** ; `<link ... href="/static/master.css">` dans `dist/index.html` |
| T-BV-HTML-01 (outil) | `.htmlvalidate.json` + étape 5 du job | `{"extends": ["html-validate:recommended"]}`, vert sur `dist/index.html` |
| T-BV-A11Y-02 (harnais) | `playwright.config.ts` + `tests/e2e/a11y.spec.ts` + étape 7 du job | axe sur chaque `.html` de `dist/`, 1280 px, tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, échec sur `serious`/`critical` |

Total : 6 tests bloquants + 2 harnais (HTML-01, A11Y-02) verts sur la page actuelle.

## Fichiers

Créer :
- `.nvmrc` : `24` (n'existe pas encore ; ne pas mettre 25 malgré le Node local)
- `package.json`, `package-lock.json` (générés par npm, voir étape 1)
- `astro.config.mjs` : `defineConfig({ build: { format: 'file' }, trailingSlash: 'never' })`, rien d'autre
- `public/static/master.css` : `cp -a site/static public/` (copie à l'octet)
- `src/layouts/Base.astro` : `<!doctype html>`, `<html lang="fr">`, `<meta charset="utf-8">`, viewport, `<title>{title}</title>` (prop), `<link rel="stylesheet" href="/static/master.css">`, `<body><slot /></body>`. Le compilateur Astro fixe la forme des balises vides : vérifier `html-validate` sur le vrai `dist/index.html` et n'ajuster `.htmlvalidate.json` que si une règle se déclenche (toute règle désactivée devra avoir son entrée `html-validate` dans l'allowlist en #6).
- `src/pages/index.astro` : placeholder minimal utilisant `Base` (`<main><h1>Benoit Vinceneux</h1></main>`) ; remplacé par #4, jamais déployé avant #7.
- `tests/test_repo.py` : DEP-01, WF-01, WF-02, WF-03 (stdlib : `json`, `re`, `pathlib`, `unittest`)
- `tests/test_dist.py` : BUILD-01 (fichier), CSS-01
- `.htmlvalidate.json`
- `playwright.config.ts` : `testDir: 'tests/e2e'`, projet Chromium seul, `viewport 1280x800`, `webServer: { command: 'python3 -m http.server -d dist 4321', url: 'http://127.0.0.1:4321', reuseExistingServer: !process.env.CI }`, `use.baseURL`
- `tests/e2e/a11y.spec.ts` : liste récursive des `.html` de `dist/` (`fs`), un test par page, `AxeBuilder.withTags([...])`, filtre `impact in {serious, critical}` → `expect(...).toEqual([])` ; afficher les `moderate`/`minor` en `console.log`. Lecture de l'entrée `axe` de l'allowlist : hors périmètre (le fichier `tests/parity-allowlist.json` arrive avec #6).
- `.github/dependabot.yml` : `version: 2`, `npm` et `github-actions`, `directory: "/"`, `schedule.interval: weekly`

Modifier :
- `.github/workflows/deploy.yml` (voir ci-dessous)
- `.gitignore` : ajouter `test-results/`, `playwright-report/`

## Workflow cible (`.github/workflows/deploy.yml`)

```yaml
name: Deploy
on:
  push:
    branches: [master]
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  test:                       # pas de `name:` : le check doit s'appeler `test` (D-5)
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with: { persist-credentials: false }
      - uses: actions/setup-node@249970729cb0ef3589644e2896645e5dc5ba9c38 # v6
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - run: npx astro build                                   # T-BV-BUILD-01
      - run: python3 -I -m unittest discover -s tests -v       # stdlib
      - run: npx html-validate "dist/**/*.html"                # T-BV-HTML-01
      # étape 6 (Apache + tests/http_check.sh) : ajoutée par #4, qui livre le script
      - id: pw
        run: echo "version=$(npx playwright --version | awk '{print $2}')" >> "$GITHUB_OUTPUT"
      - uses: actions/cache@caa296126883cff596d87d8935842f9db880ef25 # v5
        with:
          path: ~/.cache/ms-playwright
          key: playwright-${{ runner.os }}-${{ steps.pw.outputs.version }}
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test                               # T-BV-A11Y-02
  deploy:
    if: github.event_name != 'pull_request' && github.ref == 'refs/heads/master'
    concurrency: { group: deploy, cancel-in-progress: false }
    runs-on: ubuntu-latest    # inchangé (#7 restructure ce job)
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with: { persist-credentials: false }
      - name: Configure SSH
        env:
          DEPLOY_SSH_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
          DEPLOY_KNOWN_HOSTS: ${{ secrets.DEPLOY_KNOWN_HOSTS }}
        run: |   # même logique, avec "$DEPLOY_SSH_KEY" / "$DEPLOY_KNOWN_HOSTS"
      - name: Deploy site/
        env:
          DEPLOY_TARGET: ${{ secrets.DEPLOY_TARGET }}
        run: rsync -rtlz --delete site/ "$DEPLOY_TARGET"
```

Forme en blocs YAML (pas d'objets `{ }` en ligne si cela gêne les regex de WF-03 ; les regex de `test_repo.py` doivent accepter la forme réellement écrite).

## Ordre des étapes

1. `.nvmrc` = 24 ; `npm init -y` puis nettoyer `package.json` (`"private": true`, `"type": "module"`, pas de `main`/`scripts` inutiles) ; `npm install --save-exact astro@7.3.7` ; `npm install --save-dev --save-exact @playwright/test@1.64.0 @axe-core/playwright@4.13.0 html-validate@11.16.2`. Vérifier qu'aucune version n'a de `^`/`~`.
2. `astro.config.mjs`, `cp -a site/static public/`, `Base.astro`, `index.astro` ; `npx astro build` → `dist/index.html`, `dist/static/master.css`, aucun `dist/_astro/`.
3. `tests/test_repo.py`, `tests/test_dist.py` ; `python3 -I -m unittest discover -s tests -v` vert. Vérifier qu'ils échouent bien : `dist/` absent → échec (pas `skip`) ; une ligne `uses: x@v4` → WF-01 rouge ; un `${{ secrets.X }}` dans `run:` → WF-02 rouge.
4. `.htmlvalidate.json`, `npx html-validate "dist/**/*.html"` vert.
5. `playwright.config.ts`, `tests/e2e/a11y.spec.ts` ; `npx playwright install chromium && npx playwright test` vert.
6. `deploy.yml`, `dependabot.yml`, `.gitignore` ; relancer les tests (WF-01/02/03 portent sur le nouveau workflow) ; `grep -nE 'run:.*secrets\.'` et `grep -nE 'uses: [^@]+@(v[0-9]|main|master)'` vides.
7. Commits en français, types de CLAUDE.md uniquement : `feat:` (socle Astro), `test:` (tests), `chore:` (workflow, Dependabot).

## Points d'attention

- **Écarts autorisés sur le job `deploy`, liste fermée** : (a) secrets via `env:` (#3) ; (b) `concurrency` sur le job (#3) ; (c) `if:` (imposé par l'ajout de `pull_request`) ; (d) checkout épinglé par SHA (#3, WF-01) ; (e) `persist-credentials: false` (sécurité, sans effet sur rsync) ; (f) étape renommée (CLAUDE.md, pas d'hébergeur). Rien d'autre : `runs-on: ubuntu-latest` reste.
- **Déploiement inchangé** : même `rsync -rtlz --delete site/ "$DEPLOY_TARGET"`, mêmes secrets `DEPLOY_*`, aucune nouvelle valeur. Pas de `needs: test` (#7). Le `concurrency` passe du niveau workflow au job `deploy` (sinon les runs de PR se sérialiseraient avec le déploiement). L'`if:` empêche tout déploiement depuis une PR ou un `workflow_dispatch` hors `master`.
- **Hébergement** : le nom de l'étape actuelle cite l'hébergeur ; la renommer `Deploy site/` (CLAUDE.md : aucun détail d'hébergement). Ne rien ajouter qui nomme hôte, utilisateur ou chemin. (Le README en parle déjà : hors périmètre, à signaler seulement.)
- **CSS-01** : `filecmp.dircmp` compare en `shallow` (taille + mtime) ; utiliser `filecmp.cmpfiles(..., shallow=False)` sur l'arborescence parcourue (ou `filecmp.cmp(shallow=False)` par fichier), et vérifier aussi les fichiers présents d'un seul côté.
- **Chemins** : les tests Python résolvent `dist/`, `site/`, `package.json`, `.nvmrc`, `.github/` depuis `ROOT = Path(__file__).resolve().parents[1]`, jamais depuis le cwd.
- **Tests stdlib** : tout test qui lit `dist/` échoue si `dist/` est absent ; chaque message d'échec nomme le fichier et la valeur attendue.
- **WF-02** : `env:` peut être au niveau step, job ou workflow ; l'algorithme « parent le plus proche d'indentation inférieure » couvre les trois.
- **unittest discover** : `tests/e2e/` ne contient que du TS, sans `__init__.py` : ignoré par `discover`. Playwright ne prend que `tests/e2e`.
- **Versions** : choisir des versions publiées depuis au moins 14 jours (chaîne d'approvisionnement) : astro 7.3.7 (7.4.2 sortie la veille), @playwright/test 1.64.0, @axe-core/playwright 4.13.0, html-validate 11.16.2. astro 7 exige Node ≥ 22.23.4 : OK avec 24. Lockfile généré avec npm 11 (Node 25 local), compatible avec `npm ci` sous Node 24.
- **Placeholder** `index.astro` : non déployé (le deploy publie `site/`), remplacé par la vraie accueil en #4.
- **Hors périmètre** : étape Apache (#4), allowlist (#6), `needs: test`, guard, smoke (#7), contenu. Ne pas créer `tests/parity-allowlist.json` vide.
- **QA hors local** (scénarios 3, 4, 5, 9 de la recette) : PR de contrôle et vérification Dependabot à faire par l'orchestrateur après push ; Dependabot peut nécessiter que la fonctionnalité soit active dans les réglages du dépôt (le fichier suffit pour les version updates).
