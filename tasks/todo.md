# #4 [BV-02] `.htaccess` cible, fichiers statiques, 404, robots et sitemap

Branche : `feat/bv-02-htaccess-statiques` (déjà créée). PR `Closes #4` ouverte par l'orchestrateur.
Décisions liées (#2, toutes validées) : D-BV2 (retirer les liens vers les pages non publiées, `/societe-numerique` supprimée), D-BV3 (export Search Console du 22/10 : 7 pages indexées, toutes déjà dans la liste de référence, **aucune URL à ajouter**), D-3 (404 en français), D-BV4 (pas de nouvelle dépendance).
`package.json` ne change pas : ne pas toucher au lockfile (si jamais il change : leçon #3, régénérer depuis zéro et `npm ci --dry-run`).
Premier commit : inclure `tasks/lessons.md` (non versionné à ce jour).

## Critères d'acceptation (issue #4)

- [ ] Chaque URL de `legacy-urls.txt` hors liste d'exclusion temporaire (accueil, `/a-propos`, pages projet) correspond à un fichier dans `dist/`
- [ ] `dist/.htaccess` contient `ErrorDocument`, `Options -Indexes`, le refus PHP, le Content-Type markdown des `llms*.txt`, `nosniff`, `Content-Security-Policy`, `Strict-Transport-Security`
- [ ] `dist/sitemap.txt` liste `/`, `/a-propos` et chaque entrée de la collection `projects` (les 11 projets sont vérifiés dans #6)
- [ ] `dist/favicon.ico` identique à l'octet à `favicon.gif`
- [ ] Fichier de vérification Google identique à l'octet au snapshot
- [ ] Un fichier `.php` ajouté dans `public/` fait échouer le test
- [ ] Aucun fichier de `dist/` ne contient `/societe-numerique` (page supprimée, D-BV2), en particulier `llms.txt` et `llms-full.txt`
- [ ] Imposé par l'orchestrateur : job `deploy` strictement inchangé (publie toujours `site/`) ; aucun nom d'hébergeur, d'hôte, d'utilisateur ou de chemin serveur dans les fichiers

## Tests à livrer (catalogue #10)

| ID | Porté par | Contenu |
|---|---|---|
| T-BV-ART-01 | `tests/test_dist.py` | fonction `artifact_problems(root) -> list[str]` : fichiers `\.(php\d?\|phtml\|phar)$`, `.htaccess` hors racine, liens symboliques, `.env*`, `.DS_Store`, `*.map`, `.git` ; appelée sur `dist/` → liste vide |
| T-BV-ART-02 | `tests/test_dist.py` | même fonction sur un `tempfile.TemporaryDirectory` avec `x.php` + un symlink → la liste nomme les deux |
| T-BV-ART-03 | `tests/test_repo.py` | `git ls-files` (subprocess) : aucun `.php` ; `.htaccess` seulement `public/.htaccess` et `site/.htaccess` ; aucun fichier versionné ne contient la balise d'ouverture PHP (lecture en **octets** ; aiguille construite par concaténation, voir points d'attention) |
| T-BV-INV-01 | `tests/test_dist.py` | chaque entrée `200` hors `tests/legacy-exclude.txt` se résout dans `dist/` (`p` si fichier, sinon `p.html`, `/` → `index.html`) |
| T-BV-INV-02 | `tests/test_dist.py` | format `^/\S*\t(200\|301 /\S*\|403\|404\|403\|404)$`, chemins uniques, ⊇ les 26 chemins de référence (constante multiligne dans le test) ; + `legacy-exclude.txt` = exactement les 13 pages (accueil, `/a-propos`, 11 projets) |
| T-BV-INV-04 | `tests/test_dist.py` | chaque cible `301` est une entrée `200` |
| T-BV-SPE-01 | `tests/test_dist.py` | `llms*.txt` présents, non vides, UTF-8 ; chaque `https://benoitvinceneux.com(/…)?` cité (domaine nu → `/`) est une entrée `200` ; `/societe-numerique` absent de tous les fichiers de `dist/` (octets) |
| T-BV-SPE-02 | `tests/test_dist.py` | sha256 de `dist/google48428a5b5297f7c9.html` = `f6c1d4827f5cbbe00470daddb685a61ec93567a69bb135a7360f208607204972` (constante) |
| T-BV-SPE-03 | `tests/test_dist.py` | `robots.txt` : lignes `User-agent: *`, `Allow: /`, `Sitemap: https://benoitvinceneux.com/sitemap.txt` |
| T-BV-SPE-04 | `tests/test_dist.py` | `favicon.ico` == `favicon.gif` à l'octet, commence par `GIF8` |
| T-BV-SPE-05 | `tests/test_dist.py` | `sitemap.txt` : une URL `https://benoitvinceneux.com/…` par ligne, sans `.html`, sans doublon, contient `https://benoitvinceneux.com/` et `…/a-propos` (égalité aux 13 pages : #6) |
| T-BV-SPE-06 | `tests/test_dist.py` | `404.html` existe, `<html lang="fr">`, un `href="/"`, assets en chemins absolus (`href="/static/…"`, aucun `href="static/` relatif) |
| T-BV-HTA-01 | `tests/test_dist.py` | regex sur `dist/.htaccess` : `Options -Indexes`, `FilesMatch` PHP + `Require all denied`, `Content-Type "text/markdown` (llms), `ErrorDocument 404 /404.html`, `nosniff`, `Referrer-Policy`, `Strict-Transport-Security "max-age=300"`, pas de `includeSubDomains` ni `preload`, 301 `home` et `sitemap` |
| T-BV-HTA-02 | `tests/test_dist.py` | aucune `RewriteRule` dont le motif contient `\.html` ou `index` (la règle interne slug → `$1.html` du snapshot a `.html` dans la **cible**, pas dans le motif : elle passe) |
| T-BV-CSP-01 | `tests/test_dist.py` | CSP extraite du `.htaccess` : 6 directives fixes ; hôtes externes de `dist/**/*.html` (`<link rel=stylesheet>` → `style-src`, `<img>` → `img-src`, `<iframe>` → `frame-src`) et des CSS de `dist/` (`@import` → `style-src`, `url()` → `font-src`) couverts ; assertions littérales : `frame-src` contient `https://www.youtube-nocookie.com`, `font-src` contient `https://use.fontawesome.com` et `https://rsms.me` (sinon le scan est vide en #4). `html.parser` + `re` |
| T-BV-HTTP-01…06 | `tests/http_check.sh` + étape 6 du job | voir ci-dessous |
| (existants) BUILD-01, CSS-01, DEP-01, WF-01..03, HTML-01, A11Y-02 | inchangés | doivent rester verts ; A11Y-02 et HTML-01 couvrent `404.html` automatiquement (glob et `readdir` récursif : **pas d'ajout au spec**) |

`tests/http_check.sh` (bash 3.2 compatible : pas de `mapfile` ni tableau associatif ; `set -u` ; chaque curl avec `-H 'X-Forwarded-Proto: https'` ; `exit 1` au premier écart en affichant l'URL, l'obtenu et l'attendu ; chemins des fichiers lus via `$(dirname "$0")/..`) :
- HTTP-01 : pour chaque ligne de `tests/legacy-urls.txt` hors `tests/legacy-exclude.txt` : `curl -s -o /dev/null -w '%{http_code} %{redirect_url}'` ; `200` exact ; `301 <cible>` : code 301 et chemin de `redirect_url` (domaine retiré) == cible ; `403|404` : l'un des deux.
- HTTP-02 : pour chaque entrée `200` sans extension, hors exclusion et hors `/` : `/<slug>.html` et `/<slug>/` en 200 ou 301 (vide en #4, s'active en #6) ; `curl -s -o /dev/null -L --max-redirs 3` sur `/`, `/index.html`, `/groupama.html`, `/a-propos/` (liste du catalogue) : code retour curl 0 (sans `-f` : un 404 en #4 est acceptable, seule la boucle échoue).
- HTTP-03 : `/x.php` 403 ou 404 ; `/.htaccess` 403 ; `/media/` 403 et corps sans `Index of`.
- HTTP-04 : `/n-existe-pas-$(date +%s)` en 404, corps contient le `<title>` extrait de `dist/404.html`.
- HTTP-05 : `curl -sI /` : `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Strict-Transport-Security: max-age=${HSTS_MAX_AGE:-300}` (égalité exacte de la valeur), `Content-Security-Policy` == valeur extraite de `dist/.htaccess` (comparaison insensible à la casse sur le nom d'en-tête, `\r` retirés).
- HTTP-06 : `Content-Type` de `/llms.txt` et `/llms-full.txt` commence par `text/markdown`, de `/sitemap.txt` par `text/plain`.

## Fichiers

Créer :
- `public/.htaccess` (contenu ci-dessous)
- `public/llms.txt`, `public/llms-full.txt` : copies de `site/` ; dans `llms.txt` supprimer la ligne 15 (ANCT → `/societe-numerique`) ; dans `llms-full.txt` supprimer toute la section `## ANCT (Gouvernement 🇫🇷)` jusqu'au `---` suivant inclus (l. 377 à ~397). `grep -n -i 'societe-numerique\|anct' public/llms*.txt` vide. Aucune autre URL interne non publiée trouvée dans les `llms*.txt`.
- `public/google48428a5b5297f7c9.html` : `cp -p site/google48428a5b5297f7c9.html public/`
- `public/favicon.gif` : `git show b79225c:benoitvinceneux.com/content/favicon.gif > public/favicon.gif` (absent du snapshot ; source = contenu Kirby) ; `public/favicon.ico` : `cp public/favicon.gif public/favicon.ico`
- `public/robots.txt` : 3 lignes `User-agent: *` / `Allow: /` / `Sitemap: https://benoitvinceneux.com/sitemap.txt`
- `public/media/` : `cp -a site/media public/` (**avancé depuis #5**, voir points d'attention ; même blobs git, aucune croissance du dépôt)
- `src/pages/404.astro` : `<Base title="Page introuvable"><main><h1>Page introuvable</h1><p>La page demandée n'existe pas ou a été déplacée.</p><p><a href="/">Retour à l'accueil</a></p></main></Base>`
- `src/pages/sitemap.txt.ts` : vérifié dans le scratchpad (Astro 7.3.7) : sans collection, `getCollection` renvoie `[]` avec un simple WARN, le build passe.
  ```ts
  import { getCollection } from 'astro:content';
  export async function GET() {
    const projects = await getCollection('projects'); // [] tant que #5 n'a pas créé la collection
    const paths = ['/', '/a-propos', ...projects.map((p) => `/${p.id}`)];
    return new Response(paths.map((p) => `https://benoitvinceneux.com${p}`).join('\n') + '\n');
  }
  ```
- `tests/legacy-urls.txt` : exactement les 26 lignes de la liste de référence de #10 (séparateur tabulation), rien d'autre (D-BV3 n'ajoute rien)
- `tests/legacy-exclude.txt` : 13 chemins, un par ligne : `/`, `/a-propos`, `/groupama`, `/sigfox`, `/presidence-de-la-republique`, `/services-du-premier-ministre`, `/pierre-fabre`, `/notresante`, `/ca-compte-pour-moi`, `/curated-adventures`, `/lepharmacien-fr`, `/toulouse-football-club`, `/yana-place`
- `tests/http_check.sh`
- `.htmlvalidateignore` : `dist/google48428a5b5297f7c9.html` (fichier texte brut de Google, pas une page ; vérifier que la CLI l'honore avec le glob de l'étape 5, sinon exclure dans la commande)

Modifier :
- `src/layouts/Base.astro` : ajouter avant `master.css` les deux `<link rel="stylesheet">` du snapshot (`https://rsms.me/inter/inter.css`, `https://use.fontawesome.com/releases/v5.12.1/css/brands.css`) : mise en page du site sur la 404 (QA 8, 14), scan CSP-01 non vide
- `tests/test_dist.py` : ART-01/02, INV-01/02/04, SPE-01..06, HTA-01/02, CSP-01 (helpers partagés : lecture de `legacy-urls.txt`/`legacy-exclude.txt`, extraction CSP)
- `tests/test_repo.py` : ART-03
- `tests/e2e/a11y.spec.ts` : filtre d'une ligne excluant `google48428a5b5297f7c9.html` (sinon axe `html-has-lang`/`document-title` serious)
- `.github/workflows/deploy.yml` : **job `test` seulement**, étape 6 entre html-validate et l'étape `id: pw`. Job `deploy` : zéro octet modifié (`git diff` du bloc `deploy:` vide)

### `public/.htaccess`

Snapshot conservé (commentaire d'en-tête adapté), ordre : options/FilesMatch, en-têtes, ErrorDocument, rewrite HTTPS, 301, rewrite slug.
```apache
Options -Indexes
ErrorDocument 404 /404.html
<FilesMatch "\.(php[0-9]?|phtml|phar)$">
  Require all denied
</FilesMatch>
<FilesMatch "^llms(-full)?\.txt$">
  Header set Content-Type "text/markdown; charset=utf-8"
</FilesMatch>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Strict-Transport-Security "max-age=300"
Header always set Content-Security-Policy "default-src 'self'; script-src 'none'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'; style-src 'self' 'unsafe-inline' https://rsms.me https://use.fontawesome.com; font-src 'self' https://rsms.me https://use.fontawesome.com; img-src 'self' data:; frame-src https://www.youtube-nocookie.com"
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteCond %{HTTP:X-Forwarded-Proto} !https
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
RewriteRule ^home/?$ / [R=301,L]
RewriteRule ^sitemap/?$ /sitemap.txt [R=301,L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^(.+?)/?$ $1.html [L]
```
CDN relevés : `site/*.html` → `rsms.me` (Inter) et `use.fontawesome.com` (brands) en `<link>`, iframe `www.youtube-nocookie.com` (sigfox) ; `site/static/master.css` : aucun hôte externe. Aucune `<img>` externe. `'unsafe-inline'` en `style-src` : attributs `style=` du snapshot (sigfox). Pas de `'unsafe-inline'` en `font-src` (sans effet pour cette directive).

### Étape 6 du job `test`

```yaml
      - name: Apache local
        run: |
          command -v apache2 >/dev/null || { sudo apt-get update && sudo apt-get install -y apache2; }
          sudo cp -a dist /var/www/ci
          printf '%s\n' 'Listen 8080' '<VirtualHost *:8080>' '  DocumentRoot /var/www/ci' '  <Directory /var/www/ci>' '    AllowOverride All' '    Require all granted' '  </Directory>' '</VirtualHost>' | sudo tee /etc/apache2/sites-available/ci.conf
          sudo a2ensite ci
          sudo a2enmod rewrite headers
          sudo apachectl configtest
          sudo apachectl restart
      - run: bash tests/http_check.sh
        env:
          BASE_URL: http://127.0.0.1:8080
```
`apachectl restart` démarre Apache s'il est arrêté et recharge la conf s'il tourne (le `start` de #10 échouerait silencieusement si le service est déjà actif). Pas de `secrets.` ni de `uses:` ajouté : WF-01/02/03 inchangés.

## Ordre des étapes

1. Fichiers `public/` (copies, favicon, robots, media, `.htaccess`), `llms*.txt` nettoyés ; `Base.astro`, `404.astro`, `sitemap.txt.ts` ; `npx astro build`. Contrôles : `ls -a dist` (`.htaccess` copié), `cat dist/sitemap.txt`, `cmp dist/favicon.ico dist/favicon.gif`, `cmp dist/google48428a5b5297f7c9.html site/google48428a5b5297f7c9.html`, `grep -rl societe-numerique dist/` vide.
2. `tests/legacy-urls.txt`, `tests/legacy-exclude.txt`, `test_dist.py`, `test_repo.py` ; `python3 -I -m unittest discover -s tests -v` vert. Contre-épreuves : `public/x.php` → ART-01 rouge en nommant `x.php` (retirer) ; une ligne en trop dans `legacy-exclude.txt` → rouge ; `max-age=300; includeSubDomains` → HTA-01 rouge ; retirer `frame-src` → CSP-01 rouge.
3. `.htmlvalidateignore` ; `npx html-validate "dist/**/*.html"` vert (404 incluse). Filtre du spec ; `npx playwright test` vert (404 incluse, fichier Google exclu).
4. `tests/http_check.sh` en local : conf temporaire `${scratchpad}/httpd.conf` pour `/usr/sbin/httpd` : `ServerRoot "/usr"`, `Listen 127.0.0.1:8080`, `PidFile`/`ErrorLog` dans le scratchpad, `LoadModule` (depuis `/usr/libexec/apache2/`) `mpm_prefork`, `unixd`, `authz_core`, `dir`, `mime`, `rewrite`, `headers`, `log_config` ; `TypesConfig /private/etc/apache2/mime.types` ; `DirectoryIndex index.html` ; `DocumentRoot` = `dist/` du dépôt avec `<Directory>` `AllowOverride All` + `Require all granted` ; reproduire la règle globale d'Ubuntu `<FilesMatch "^\.ht"> Require all denied </FilesMatch>`. `httpd -f … -t` puis `httpd -f … -k start`, `BASE_URL=http://127.0.0.1:8080 bash tests/http_check.sh` vert, `-k stop`. Garder les sorties `curl -sI` de `/`, `/home`, `/sitemap`, `/n-existe-pas`, `/llms.txt` pour la QA. Contre-épreuve : casser la règle `home` → script rouge avec l'URL.
5. Étape 6 dans `deploy.yml` ; tests repo relancés ; `git diff master -- .github/workflows/deploy.yml` ne touche que le job `test`.
6. Relire `git diff master` (et `grep -niE 'ssh|/home/|/var/www/'`) : rien qui nomme un hôte, un utilisateur ou un chemin serveur (seul `/var/www/ci` du runner CI est permis).
7. Commits (types CLAUDE.md, en français) : `feat: Fichiers statiques, .htaccess cible, 404 et sitemap (BV-02)` (avec `tasks/lessons.md`), `test: Inventaire, fichiers spéciaux, .htaccess et CSP (BV-02)`, `chore: Étape Apache locale du job test (BV-02)`.

## Points d'attention

- **`/media/` avancé de #5** : HTTP-03 et la liste de référence exigent `/media/ 403`, impossible sans dossier `dist/media` (Apache répondrait 404) ; la liste d'exclusion est figée aux 13 pages. On copie donc `site/media` dans `public/media/` dès #4 (une commande, aucun code) ; #5 n'a plus qu'à constater la copie, PAR-05 reste dans #5. À signaler dans la PR et dans #5.
- **Balise d'ouverture PHP** : ne l'écrire littéralement dans aucun fichier versionné (ni test, ni plan) : dans `test_repo.py`, `needle = b"<" + b"?php"`. Lire en octets (`site/media`, `public/media` sont binaires). Vérifier que le dépôt actuel est propre (constaté : aucun fichier versionné ne la contient).
- **Fichier Google** : texte brut, ni doctype ni `lang` : exclu de html-validate (`.htmlvalidateignore`) et d'axe (filtre du spec) ; jamais lié (LNK-02, #6). Il reste compté par INV-01 et SPE-02. Si #6 exige que toute exclusion passe par l'allowlist, il y migrera.
- **`Header always`** pour les 4 en-têtes de sécurité : sinon absents des réponses 404 (ErrorDocument) et 301. Le `Header set Content-Type` des `llms` reste tel quel (snapshot).
- **Redirections 301** placées après la règle HTTPS et avant la règle slug → `.html`. Cible relative (`/`) : en production Apache construit l'URL avec le schéma de la requête ; HTTP-01 ne compare que le chemin. Pas de redirection `x.html` → `/x` ni `/index.html` → `/` (HTA-02, boucle).
- **Localement**, le `X-Forwarded-Proto: https` envoyé par le script neutralise la redirection HTTPS ; sans lui tout serait en 301.
- **`sitemap.txt.ts`** : pas de `src/content.config.ts` en #4 (il arrive en #5) ; le WARN `collection "projects" does not exist` au build est attendu. Pas de `site` dans `astro.config.mjs` : constante dans l'endpoint.
- **SPE-06** : `Base.astro` utilise déjà `/static/master.css` (absolu) ; les liens CDN sont absolus par nature.
- **HTTP-02** en #4 : la boucle par slug est vide (13 pages exclues) ; seuls les 4 `curl -L` tournent. Elle s'active en #6 quand l'exclusion est vidée.
- **Ne pas toucher** : job `deploy`, `.nvmrc` (24), `package.json`, `package-lock.json`, `site/`. Pas de PHP versionné.
- **Hors périmètre** : pages accueil/à propos/projets et leur nav (#6), collection et import (#5), allowlist (#6), `needs: test`, guard, smoke (#7), HSTS longue durée (#9).
- **QA hors local** : le scénario 13 (vidéo sigfox sous CSP) se fait sur l'Apache local avec `site/sigfox.html` copié dans le DocumentRoot temporaire (pas dans `public/`) ; les sorties `curl -sI` vont en commentaire de PR (orchestrateur).
