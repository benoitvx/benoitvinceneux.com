# Leçons de la migration Astro

## #3 Socle Astro (PR #24)
- Un `package-lock.json` produit sur macOS peut omettre des dépendances optionnelles d'autres plateformes (`@emnapi/*` des paquets wasm32) : `npm ci` échoue sur Linux. Régénérer le lockfile depuis zéro (`rm -rf node_modules package-lock.json && npm install`) et vérifier `npm ci --dry-run` avant de pousser.
- `python3 -I` n'empêche pas l'écriture des `.pyc` : `__pycache__/` doit être dans `.gitignore`.
- Ajouter le déclencheur `pull_request` impose de restreindre tout de suite le job de déploiement (`if:` sur `master` hors PR).
- `gh run list --branch master --limit 1` peut renvoyer un run Dependabot : filtrer avec `--workflow deploy.yml`.
