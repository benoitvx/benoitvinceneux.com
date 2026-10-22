# Leçons de la migration Astro

## #3 Socle Astro (PR #24)
- Un `package-lock.json` produit sur macOS peut omettre des dépendances optionnelles d'autres plateformes (`@emnapi/*` des paquets wasm32) : `npm ci` échoue sur Linux. Régénérer le lockfile depuis zéro (`rm -rf node_modules package-lock.json && npm install`) et vérifier `npm ci --dry-run` avant de pousser.
- `python3 -I` n'empêche pas l'écriture des `.pyc` : `__pycache__/` doit être dans `.gitignore`.
- Ajouter le déclencheur `pull_request` impose de restreindre tout de suite le job de déploiement (`if:` sur `master` hors PR).
- `gh run list --branch master --limit 1` peut renvoyer un run Dependabot : filtrer avec `--workflow deploy.yml`.

## #4 .htaccess et fichiers statiques
- Apache local (macOS `/usr/sbin/httpd`) : charger `mod_autoindex`, sinon un dossier sans index répond 404 au lieu de 403 malgré `Options -Indexes` (Ubuntu l'active par défaut).
- Le port 8080 peut être occupé en local : prendre un autre port, `BASE_URL` suffit.

### Orchestration (#4, PR #32)
- Les 301 `RewriteRule ... / [R=301]` à cible relative prennent le schéma vu par Apache : derrière un proxy TLS, cela ajoute un saut `http://`. Cibles absolues `https://%{HTTP_HOST}/…`.
- La protection `.ht*` vient souvent de la conf globale du serveur : la poser aussi dans `public/.htaccess` pour ne pas en dépendre.

## #5 Import Kirby (PR #33)
- Les fichiers interdits au dépôt (`.php`, lien symbolique) de la fixture sont créés à la volée par le test : la fixture versionnée reste propre et T-BV-ART-03 passe.
- `python3 -I -m unittest tests.test_x` échoue (pas de paquet `tests`, `-I` retire le dossier courant) : utiliser `discover -s tests -p 'test_x.py'`.
- Regex de domaine : borner la fin d'hôte (`(?=/|$)`), sinon `benoitvinceneux.com.example.org` est réécrit.

## #6 Gabarits et parité
- Ajouter `crossorigin` + `integrity` à une ressource CDN que l'ancien site chargeait sans `crossorigin` casse le cache des visiteurs déjà venus : le CDN répond sans `Access-Control-Allow-Origin` ni `Vary: Origin` aux requêtes sans `Origin` (max-age 1 an), et le navigateur réutilise cette copie, qui échoue au contrôle CORS. Vérifier les en-têtes avec et sans `Origin` avant d'ajouter SRI ; une URL distincte (query string) évite la copie en cache.
- La comparaison visuelle snapshot/build se fait dans un contexte navigateur neuf par page, sinon le cache partagé fausse le résultat.
- html-validate (`unique-landmark`) exige un nom accessible sur chaque `<aside>` quand il y en a plusieurs : les `aria-label` sont nécessaires pour HTML-01.

### Orchestration (#6, PR #34)
- Le premier run sur `master` n'a pas de cache Playwright (les caches des branches de PR ne sont pas visibles depuis `master`) et `playwright install --with-deps` dépend d'`apt` : un miroir lent a bloqué le job plus de 10 min. Poser `timeout-minutes` sur les jobs pour ne pas attendre le plafond de 6 h.
