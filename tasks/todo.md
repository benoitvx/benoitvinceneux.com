# #7 [BV-05] Bascule : déploiement de `dist/` conditionné aux tests

> Remplacé en partie le 22/10/2026 (décisions de Benoit) : HSTS laissé au serveur (absent de `public/.htaccess`, smoke avec `HSTS_MIN_AGE=16000000`), pas d'environnement `production` (secrets au niveau du dépôt). Les mentions de `environment: production` et `HSTS_MAX_AGE=300` ci-dessous sont caduques.

Branche : `feat/bv-05-bascule` (déjà créée). PR `Closes #7` ouverte par l'orchestrateur, **non mergée** : M2 = mise en production, Benoit décide (CLAUDE.md, garde-fous).
Dépendances : #4 (BV-02) et #6 (BV-04) mergés. Décisions liées (#2) : D-1 (pas de préproduction : smoke + revert en moins de 5 min), D-5 (Environment `production` + protection de `master`, réglés par Benoit).
`tasks/lessons.md` (modifié, non commité) part avec le premier commit.
Inchangés : `package.json`, lockfile, `.nvmrc` (24), job `test` (sauf `timeout-minutes`), secrets `DEPLOY_*`, cible rsync.

## Critères d'acceptation (issue #7)

- [ ] Un test volontairement rouge sur une PR de contrôle empêche tout déploiement
- [ ] Un `workflow_dispatch` lancé depuis une autre branche ne déploie pas
- [ ] Le job échoue avant le rsync si `.htaccess` manque ou si `dist/` contient trop peu de pages
- [ ] Smoke vert après le premier déploiement
- [ ] Le README décrit le rollback en 3 étapes au plus

## Tests à livrer (catalogue #10)

| ID | Fichier | Contenu |
|---|---|---|
| T-BV-WF-04 | `tests/test_repo.py` (nouvelle méthode `test_wf_04_deploy_job`) | Lire `deploy.yml`, isoler le bloc du job (de `^  deploy:` à la fin ou au job suivant `^  \w`). Regex `re.M` : `^\s+needs:\s*test\s*$` ; ligne `if:` **exacte** `if: github.event_name != 'pull_request' && github.ref == 'refs/heads/master'` ; `concurrency:` suivi de `group: deploy` et `cancel-in-progress: false`. Index de la première ligne contenant `predeploy_guard.sh` < index de la première ligne qui matche `run:.*rsync ` ; cette même ligne contient `--delete-after --delay-updates` et ` dist/ ` comme source ; `assertNotIn("site/", bloc_deploy)`. Message d'échec nommant le critère manquant. |
| T-BV-GUARD-01 | `tests/test_guard.py` (nouveau) | 5 cas, `subprocess.run(["bash", ROOT/"tests/predeploy_guard.sh", tmp])` sur des copies de `dist/` dans `tempfile.TemporaryDirectory()` (`shutil.copytree(..., symlinks=True)`) : (1) copie intacte → code 0 ; (2) `.htaccess` supprimé ; (3) tous les `*.html` sauf 2 supprimés ; (4) `x.php` ajouté ; (5) lien symbolique ajouté (`os.symlink`). Cas 2 à 5 : code ≠ 0 **et** un mot-clé du message dans la sortie (le script écrit sur `>&2` : lancer avec `stderr=subprocess.STDOUT` ou lire `stderr`) (`.htaccess`, `pages`, `.php`, `lien symbolique`). `dist/` absent → échec (convention #10), pas de skip. |
| T-BV-SMK-01 | `tests/http_check.sh` (existant, + 1 bloc) | Joué dans le job `deploy` après rsync : `BASE_URL=https://benoitvinceneux.com HSTS_MAX_AGE=300 bash tests/http_check.sh`. Ajout : si `BASE_URL` commence par `https://`, `curl -s -o /dev/null -w '%{http_code} %{redirect_url}' "http://${BASE#https://}/"` (sans l'en-tête `X-Forwarded-Proto`) doit valoir `301 https://<hôte>/`. Sans effet sur le run Apache local (`http://127.0.0.1:8080`). Non bloquant pour la mise en ligne (voir points d'attention). |

Tout le reste du catalogue est déjà vert : rien à retirer.

## Fichiers

| Fichier | Action |
|---|---|
| `tests/predeploy_guard.sh` | **Créer** (~15 lignes bash, `set -u`). Usage `bash tests/predeploy_guard.sh <dir>`. Contrôles, chacun `echo "ÉCHEC predeploy_guard : …" >&2; exit 1` : `test -f "$d/.htaccess"` ; `find "$d" -type l` vide (« lien symbolique : <chemins> ») ; `find "$d" -type f \( -name '*.php' -o -name '*.php[0-9]' -o -name '*.phtml' -o -name '*.phar' \)` vide (même motif que T-BV-ART-01 et le `.htaccess`) ; `find "$d" -name '*.html' -type f \| wc -l` ≥ nombre d'entrées `200` de `legacy-urls.txt` qui sont des pages (sans `.`) ou finissent par `.html` (awk, 14 aujourd'hui : 13 pages + fichier Google ; `dist/` en a 15 avec `404.html`). Message : « N pages HTML dans <dir>, au moins M attendues ». `legacy-urls.txt` lu relativement au script (`$(dirname "$0")`). Fin : `echo "predeploy_guard : OK (<dir>)"`. |
| `tests/test_guard.py` | **Créer** (T-BV-GUARD-01). |
| `tests/test_repo.py` | **Modifier** : + `test_wf_04_deploy_job`. |
| `tests/http_check.sh` | **Modifier** : + bloc http→https (SMK-01), commentaire d'en-tête mis à jour. |
| `.github/workflows/deploy.yml` | **Modifier** le job `deploy` (voir ci-dessous) ; job `test` : seulement `timeout-minutes: 15`. |
| `README.md` | **Réécrire** (court) : ce que publie `master` (désormais `dist/`, plus `site/`), build local, tests, rollback. Retirer la description des secrets qui donne le format de la cible (`user@hôte:chemin/`) : garder seulement les noms `DEPLOY_SSH_KEY`, `DEPLOY_KNOWN_HOSTS`, `DEPLOY_TARGET`. Aucun détail d'hébergement (dépôt public). |
| `tests/smoke.sh` | **Ne pas créer** : la note CTO de #7 dit `smoke.sh` = `http_check.sh`. Une ligne dans le README : « le smoke post-déploiement (`tests/smoke.sh` dans #7) est `tests/http_check.sh` lancé sur le domaine public ». |

### Job `deploy` cible

```yaml
  deploy:
    needs: test
    if: github.event_name != 'pull_request' && github.ref == 'refs/heads/master'
    concurrency:
      group: deploy
      cancel-in-progress: false
    runs-on: ubuntu-24.04
    environment: production
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@<même SHA> # v6
        with:
          persist-credentials: false
      - uses: actions/setup-node@<même SHA> # v6
        with:
          node-version-file: .nvmrc
          cache: npm
      - run: npm ci
      - run: npx astro build
      - name: Garde-fous avant mise en ligne
        run: bash tests/predeploy_guard.sh dist
      - name: Configure SSH        # inchangé (secrets via env:)
        ...
      - name: Deploy dist/
        env:
          DEPLOY_TARGET: ${{ secrets.DEPLOY_TARGET }}
        run: rsync -rtlz --delete-after --delay-updates dist/ "$DEPLOY_TARGET"
      - name: Smoke après mise en ligne (T-BV-SMK-01, non bloquant pour la mise en ligne)
        run: bash tests/http_check.sh
        env:
          BASE_URL: https://benoitvinceneux.com
          HSTS_MAX_AGE: 300
```

## Ordre des étapes

1. Commit `chore: Leçons de #6` avec `tasks/lessons.md` (et ce `tasks/todo.md`).
2. `tests/predeploy_guard.sh` + `tests/test_guard.py` ; vérifier les 5 cas.
3. `test_wf_04` dans `tests/test_repo.py` : le lancer, il doit être **rouge** sur le workflow actuel.
4. `deploy.yml` (job `deploy` + `timeout-minutes` sur `test`) : WF-01 à 04 verts.
5. Bloc http→https dans `http_check.sh` ; rejouer `http_check.sh` sur l'Apache local (le bloc ne doit pas s'exécuter en `http://`).
6. README.
7. Vérification locale complète : `npx astro build`, `python3 -I -m unittest discover -s tests -v`, `npx html-validate "dist/**/*.html"`, `http_check.sh` sur Apache local, `npx playwright test`.
8. Commits `type: Description en français`, pas de push (orchestrateur).

## Points d'attention

- **Ne jamais toucher** les noms `DEPLOY_SSH_KEY`, `DEPLOY_KNOWN_HOSTS`, `DEPLOY_TARGET` ni `"$DEPLOY_TARGET"` (CLAUDE.md). Les secrets restent sous `env:` (T-BV-WF-02).
- **Avant le merge** de cette PR, `master` publie toujours `site/` : ne rien changer sur `master` hors de cette branche.
- `if:` à recopier **à l'octet près** (WF-04 compare la ligne exacte).
- `environment: production` (D-5) : si l'environnement n'existe pas encore, GitHub le crée sans règle au premier run et les secrets du dépôt restent lus ; il devient indispensable dès que Benoit y déplace les `DEPLOY_*`. Prérequis de merge (case D-5 de #2 non cochée) : Benoit crée l'environnement restreint à `master`, y déplace les secrets et protège `master` (check `test` exigé). Ce n'est pas un bloqueur d'implémentation.
- Smoke non bloquant (« équivalent » de `continue-on-error` retenu) : c'est la **dernière** étape du job, après le rsync. S'il échoue, le site est déjà en ligne et le job passe au rouge (signal visible), sans rollback automatique (hors périmètre). Pas de `continue-on-error` : il masquerait l'échec (job vert). Le rollback reste le revert manuel du README.
- `http_check.sh` lit `dist/404.html` et `dist/.htaccess` : c'est pourquoi le smoke tourne dans le job `deploy`, après le build.
- `--delete-after` supprime côté serveur tout ce qui n'est pas dans `dist/` : `llms-full.txt` et `google48428a5b5297f7c9.html` doivent être dans `public/` (c'est le cas, couvert par T-BV-SPE-01/02 et scénario QA 9).
- Le seuil du garde-fou suit le texte de #7 (« URL HTML de `legacy-urls.txt` ») : pages sans `.` + entrées `.html`. Lire strictement « URL 200 en `.html` » de #10 donnerait 1 seul fichier, ce qui ne protège rien contre un `dist/` partiel.
- `timeout-minutes` (leçon #6) : `test` 15 (cible 4 min, marge pour un premier run sans cache Playwright), `deploy` 10.
- `python3 -I` : `test_guard.py` importe seulement la stdlib (et au besoin `test_dist` comme module, convention #6).
- README, commits, PR : aucun nom d'hôte, utilisateur SSH, chemin serveur ni détail d'hébergement. Le domaine public `benoitvinceneux.com` est déjà dans le dépôt : autorisé.

### Rollback (README, 3 étapes)

1. `git revert <sha du commit de bascule>` sur une branche, PR vers `master`.
2. Merger quand `test` est vert : le job `deploy` republie `site/` (tant que `site/` existe, c'est-à-dire jusqu'à #9).
3. Vérifier le run et le site (200 sur `/`, une page projet, `/a-propos`).

## Recette (QA) : répartition

| Scénario | Qui |
|---|---|
| 1 Lecture du workflow | local (QA) |
| 2 PR de contrôle rouge | à faire (orchestrateur ou Benoit) |
| 3 `workflow_dispatch` depuis une autre branche | à faire (orchestrateur ou Benoit) |
| 4 Garde-fous en négatif | local : `predeploy_guard.sh` sur copies de `dist/` sans `.htaccess`, avec 2 pages, avec `x.php`, avec un lien symbolique → code ≠ 0, aucun rsync (aussi T-BV-GUARD-01) |
| 5 Bascule (merge) | à faire (Benoit) |
| 6 Smoke manuel `curl -sI` en production | à faire (après bascule) |
| 7 Régression navigateur | à faire (après bascule) |
| 8 Rollback à blanc | local : branche jetable, commit de la bascule, `git revert HEAD`, vérifier que le diff restaure `rsync … site/`, puis supprimer la branche |
| 9 Fichiers hors build servis | à faire (après bascule) |
