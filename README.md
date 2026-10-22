# benoitvinceneux.com

Site portfolio statique construit avec Astro et servi par Apache.

- `src/`, `public/` : sources Astro. Le build produit `dist/`.
- `site/` : snapshot statique de l'ancien site Kirby, conservé jusqu'au nettoyage (#9).
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

Le smoke après déploiement (`tests/smoke.sh` dans #7) est `tests/http_check.sh` lancé sur le domaine public, avec `BASE_URL=https://benoitvinceneux.com`.

## Rollback

1. `git revert <sha du commit à annuler>` sur une branche, puis PR vers `master`.
2. Merger quand le job `test` est vert : le job `deploy` republie la version précédente.
3. Vérifier le run, puis le site : 200 sur `/`, une page projet et `/a-propos`.
