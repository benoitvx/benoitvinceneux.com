# benoitvinceneux.com

Site portfolio statique construit avec Astro et servi par Apache.

- `src/`, `public/` : sources Astro. Le build produit `dist/`.
- Ancien site Kirby : supprimé du dépôt (#9), conservé dans le tag annoté `snapshot-kirby`.
- Déploiement (`.github/workflows/deploy.yml`) : chaque push sur `master` lance le job `test`, puis, s'il est vert, le job `deploy` reconstruit `dist/`, passe les garde-fous (`tests/predeploy_guard.sh`), le synchronise par rsync et lance le smoke.
- Secrets GitHub (au niveau du dépôt, sans environnement) : `DEPLOY_SSH_KEY`, `DEPLOY_KNOWN_HOSTS`, `DEPLOY_TARGET`. Le job `deploy` ne tourne que sur `master` hors PR, et `master` est protégée (PR obligatoire, check `test` exigé).
- HSTS : posé par la configuration du serveur, pas par `public/.htaccess`.

## Build local

```sh
npm ci
npx astro build
```

## Tests

```sh
python3 -I -m unittest discover -s tests -v
npx html-validate "dist/**/*.html"
BASE_URL=http://127.0.0.1:8080 bash tests/http_check.sh   # dist/ servi par un Apache local
npx playwright test
```

Le smoke après déploiement (`tests/smoke.sh` dans #7) est `tests/http_check.sh` lancé sur le domaine public : `BASE_URL=https://benoitvinceneux.com HSTS_MIN_AGE=16000000 bash tests/http_check.sh` (sans `HSTS_MIN_AGE`, le script exige l'absence de HSTS, ce qui ne vaut que pour l'Apache local).

## Rollback

Régression Astro (cas normal) :

1. `git revert <sha du commit à annuler>` sur une branche, puis PR vers `master`.
2. Merger quand le job `test` est vert : le job `deploy` republie la version précédente.
3. Vérifier le run, puis le site : 200 sur `/`, une page projet et `/a-propos`.

Retour à l'ancien site Kirby (le snapshot n'existe plus que dans le tag `snapshot-kirby`) :

1. Sur une branche partie de `master`, dans `.github/workflows/deploy.yml`, job `deploy` (pas le job `test`), remplacer la ligne `- run: npx astro build` par :
   `- run: git fetch --depth 1 origin tag snapshot-kirby && rm -rf dist && mkdir dist && git archive snapshot-kirby:site | tar -x -C dist`
2. PR vers `master`, merger quand `test` est vert : le job `deploy` publie le snapshot avec les mêmes garde-fous et le même rsync. Le smoke peut échouer (en-têtes et pages du snapshot différents de ceux attendus) : le site est quand même en ligne.
3. Vérifier 200 sur `/`, une page projet et `/a-propos`. Pour revenir à Astro : `git revert` de ce commit.
