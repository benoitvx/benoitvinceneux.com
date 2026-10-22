# #6 [BV-04] Gabarits (layout, page projet, à propos, accueil) et parité

Branche : `feat/bv-04-gabarits-parite` (déjà créée). PR `Closes #6` ouverte par l'orchestrateur.
Décisions liées (#2, toutes validées) : D-3 (corrections hors parité déclarées dans `tests/parity-allowlist.json`), D-4 (accueil : `h1` puis `h3`, inchangé), D-BV2 (lien `/numerique-responsable` retiré), D-BV4 (aucune nouvelle dépendance).
`package.json`, lockfile, `.nvmrc` (24), `.github/workflows/deploy.yml` : **inchangés** (le déploiement publie toujours `site/`).
`tasks/lessons.md` (modifié, non commité) part avec le premier commit.

Principe : reproduire le HTML et les classes de `site/*.html` à l'identique. Pas de refonte, pas de modification de `public/static/master.css` (T-BV-CSS-01).

## Critères d'acceptation (issue #6)

- [ ] Inventaire complet : liste d'exclusion de `test_dist.py` vidée (fichier `tests/legacy-exclude.txt` supprimé), chaque URL `200` de `legacy-urls.txt` correspond à un fichier dans `dist/`
- [ ] `dist/sitemap.txt` liste `/`, `/a-propos` et les 11 projets
- [ ] Parité verte sur les 13 pages, chaque entrée de l'allowlist a un motif
- [ ] Nav dans l'ordre 1 à 12, `aria-current` sur l'élément actif
- [ ] Aucun lien interne en `.html`
- [ ] Tous les `href`, `src`, `srcset` internes se résolvent dans `dist/`
- [ ] Aucun hôte externe hors `allowed-hosts.txt`
- [ ] Aucun `id` en double
- [ ] Aucun `<script>` dans `dist/` (compatible `script-src 'none'`)

## Tests à livrer (catalogue #10)

Définition commune, dans `tests/test_dist.py` : **page** = chemin `200` de `legacy-urls.txt` sans `.` (13 pages) → fichier `dist/index.html` ou `dist/<slug>.html`. Fonction `pages()` + `norm(url, page)` (normalisation d'URL) + `parse(f)` (petit `HTMLParser` qui collecte balises/attributs/texte hors commentaires), réutilisées par les autres fichiers via `import test_dist as base` (import du **module**, pas des noms : sinon `TestDist` serait découvert deux fois). `discover -s tests` met `tests/` dans `sys.path`, même en `-I`.

| ID | Fichier | Contenu |
|---|---|---|
| T-BV-ART-04 | `tests/test_dist.py` | aucun `<script` (casse ignorée), aucun attribut `on\w+=`, aucune URL `javascript:` dans `dist/**/*.html` |
| T-BV-INV-01 | `tests/test_dist.py` | inchangé, mais `excluded()` renvoie `[]` si le fichier est absent → couvre les 13 pages |
| T-BV-INV-02 | `tests/test_dist.py` | retirer la dernière assertion (« legacy-exclude doit contenir les 13 pages », propre à #4) |
| T-BV-INV-03 | `tests/test_dist.py` | `tests/legacy-exclude.txt` absent ou vide |
| T-BV-SPE-05 | `tests/test_dist.py` | ajouter : ensemble des URL = `{DOMAIN + p for p in pages}` (13) |
| T-BV-CSP-01 | `tests/test_dist.py` | déjà sur toutes les pages (`rglob`) ; dette (b) : `url()` des CSS → `font-src` si extension `\.(woff2?\|ttf\|otf\|eot)`, sinon `img-src` (une regex) |
| T-BV-SEO-01 | `tests/test_dist.py` | pour les 13 pages : `<link rel="canonical">` = `https://benoitvinceneux.com/<slug>` (accueil : `…/`), `<meta name="description">` non vide, `<title>` unique entre les 13 |
| T-BV-LNK-01 | `tests/test_links.py` (nouveau) | chaque `href`/`src`/`srcset` interne de chaque `dist/**/*.html` (domaine absolu inclus) et chaque `url()` des CSS de `dist/` se résout (`p`, sinon `p.html`, `/` → `index.html`) ; `mailto:`/`tel:` ignorés ; `#ancre` → un `id` de la page |
| T-BV-LNK-02 | `tests/test_links.py` | aucun `href` interne finissant par `.html` |
| T-BV-HOST-01 | `tests/test_links.py` | hôte de chaque URL externe (`href`, `src`, `srcset`, `url()`) ∈ `tests/allowed-hosts.txt` |
| T-BV-A11Y-01 | `tests/test_a11y.py` (nouveau) | 13 pages + `404.html` : `<html lang="fr">`, un seul `<title>` non vide, `id` uniques, premier `<a href>` = lien d'évitement `href="#…"` dont la cible existe ; `aria-current="page"` dans la nav : exactement 1 sur les 12 pages de la nav, 0 sur l'accueil et la 404 ; chaque `<img>` a `alt` ; vignettes de l'accueil (`main img`) en `alt=""` ; chaque `<iframe>` a un `title` |
| T-BV-NAV-01 | `tests/test_a11y.py` | 13 pages + 404 : `href` de la nav = `/a-propos, /services-du-premier-ministre, /presidence-de-la-republique, /curated-adventures, /sigfox, /notresante, /ca-compte-pour-moi, /pierre-fabre, /groupama, /lepharmacien-fr, /toulouse-football-club, /yana-place` (liste en dur dans le test) |
| T-BV-PAR-00 | `tests/test_parity.py` (nouveau) | allowlist : JSON valide, chaque entrée a `test`, `page`, `motif`, `pourquoi` non vides ; chaque entrée sert (voir « Allowlist ») |
| T-BV-PAR-01 | `tests/test_parity.py` | texte visible (hors `script`/`style`/commentaires, `html.unescape`, espaces normalisés, NFC) identique `site/<page>.html` ↔ `dist/<page>.html`, 13 pages, après retrait des motifs de l'allowlist |
| T-BV-PAR-02 | `tests/test_parity.py` | ensemble des `href`/`src`/`srcset` normalisés identique (hors `mailto:`, `tel:`, `#…` seuls), après retrait des motifs |
| T-BV-PAR-03 | `tests/test_parity.py` | nombre d'`<img>` et d'`<iframe>` hors commentaires identique |
| T-BV-PAR-04 | `tests/test_parity.py` | `<title>` et meta description identiques (décodés) |
| T-BV-BUD-01 | `tests/test_budget.py` (nouveau) | chaque `.html` ≤ 50 Ko ; chaque image ≤ 700 Ko ; aucun fichier > 1 Mo ; total `dist/` ≤ 16 Mo ; total `dist/**/*.css` ≤ 100 Ko |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` | vert sur toutes les pages ; chaque règle à `off` dans `.htmlvalidate.json` a son entrée `html-validate` dans l'allowlist (contrôlé par PAR-00) |
| T-BV-A11Y-02 | `tests/e2e/a11y.spec.ts` | pages = 13 pages de `legacy-urls.txt` + `404.html` (même définition que Python, voir dette (a)) ; exclusions uniquement via les entrées `axe` de l'allowlist (`builder.exclude(motif)`) ; une seule : l'iframe YouTube de sigfox (violations dans le lecteur tiers) |
| T-BV-HTTP-01 à 06 | `tests/http_check.sh` | `excluded()` tolérant au fichier absent (`[ -f … ] && grep -qxF …`) → les 13 pages passent dans HTTP-01 et HTTP-02 ; rien d'autre à changer |

Message d'échec : chaque assertion nomme le fichier ou l'URL et la valeur attendue (convention #10). Scénarios négatifs de la recette (un mot changé dans un `.md`, un lien `/n-existe-pas`) : le message de PAR-01 / LNK-01 doit nommer la page et l'écart (pour PAR-01, afficher le premier fragment divergent, pas les deux textes entiers).

### Normalisation d'URL (`norm`, une seule fonction pour PAR-02, LNK-01, LNK-02)

`srcset` découpé sur `,` puis premier mot. Puis : `urljoin("https://benoitvinceneux.com/<page>", url)` ; si l'hôte est `benoitvinceneux.com` : garder le chemin, retirer query et fragment, `unquote`, NFC, retirer `.html` final, `/index` → `/`. Sinon URL externe (hôte en minuscules pour HOST-01). `mailto:`, `tel:` et `#ancre` seule : hors PAR-02. LNK-02 regarde le `href` **brut** (avant retrait de `.html`).

### Allowlist `tests/parity-allowlist.json`

Liste d'objets `{test, page, motif, pourquoi}`. `page` = slug (`index` pour l'accueil) ou `*`.
- `PAR-01` / `PAR-02` : `motif` = regex retirée du texte (PAR-01) ou des URL normalisées (PAR-02) des **deux** côtés avant comparaison. « Sert » = le motif a trouvé au moins une occurrence sur au moins une page concernée.
- `html-validate` : `motif` = id de règle ; « sert » = la règle est à `"off"` dans `.htmlvalidate.json`, et réciproquement chaque règle `off` a son entrée (bijection testée par PAR-00).
- `axe` : `motif` = sélecteur CSS exclu de l'analyse (`builder.exclude`), lu par `a11y.spec.ts` ; une entrée : l'iframe YouTube de sigfox (PAR-00 vérifie seulement ses champs).

Entrées attendues (à confirmer par les tests, ne rien pré-déclarer d'autre) :
1. `PAR-01`, `*`, `Aller au contenu`, « D-3 : lien d'évitement ajouté ».
2. `PAR-02`, `curated-adventures`, `^/numerique-responsable$`, « D-BV2 : lien vers une page non publiée retiré en #5 ».
3. Une entrée `html-validate` par règle désactivée (voir étape 6).

Écarts D-3 **non** déclarables parce qu'aucun test de parité ne les voit (une entrée serait morte et ferait échouer PAR-00) : `aria-current`, classes de l'élément actif, `alt=""` des vignettes (l'`alt` n'est pas du texte visible), CSS de focus, 404 (pas d'équivalent dans le snapshot). Ils sont couverts par A11Y-01 / A11Y-02. Le dire dans la PR. Coquilles : aucune correction prévue (ce n'est pas une refonte) ; si une est corrigée, entrée `PAR-01` dédiée.

## Fichiers

Modifier :
- `astro.config.mjs` : ajouter `markdown: { smartypants: false }` (sinon `'` → `’`, PAR-01 rouge) et `compressHTML: false` (sortie proche du snapshot, écarts lisibles ; poids sans enjeu).
- `src/layouts/Base.astro` : tout le gabarit commun (voir « Gabarits »). Props : `title`, `description`, `path` (canonical, absent sur la 404), `current` (slug actif ou rien), `noindex`. Constantes dans le frontmatter : tagline, réseaux, couleur `#0F4C81`, `DOMAIN`. Liste de nav = `a-propos` + `getCollection('projects')` triée par `order`.
- `src/pages/index.astro` : titre et description du snapshot, grille.
- `src/pages/404.astro` : passe dans Base avec la mise en page (pas de `current`, pas de canonical, `noindex`), contenu en français, `<title>` sur une ligne (lu par HTTP-04).
- `tests/test_dist.py` : `pages()`, `norm()`, `parse()`, `excluded()` tolérant, ART-04, INV-02 retouché, INV-03, SPE-05, CSP-01 (b), SEO-01.
- `tests/http_check.sh` : `excluded()` tolérant.
- `tests/e2e/a11y.spec.ts` : liste des pages lue dans `legacy-urls.txt` + `404.html`, entrées `axe` de l'allowlist → `disableRules` (supprime le nom Google en dur).
- `.htmlvalidate.json` : règles à `off` seulement si elles se déclenchent et ne se corrigent pas sans casser la parité.

Créer :
- `src/pages/[slug].astro` : `getStaticPaths` sur la collection, `render(entry)` (`import { render } from 'astro:content'`), 2 variantes.
- `src/pages/a-propos.astro` : porté à la main depuis `site/a-propos.html`.
- `tests/test_links.py`, `tests/test_a11y.py`, `tests/test_parity.py`, `tests/test_budget.py` (noms imposés par #10 ; `test_parity.py` est supprimé tel quel en #9).
- `tests/parity-allowlist.json`.
- `tests/allowed-hosts.txt` : les 19 hôtes externes du snapshot (un par ligne, triés) : `curatedadventures.club, dataforgood.fr, datalma.beta.gouv.fr, explore.data.gouv.fr, github.com, iscparis.com, laproductconf.com, projects.invisionapp.com, rsms.me, use.fontawesome.com, www.academie-nr.org, www.academy.thiga.co, www.eig.numerique.gouv.fr, www.lelaptop.com, www.linkedin.com, www.numerique.gouv.fr, www.youtube-nocookie.com, xpro.mit.edu, yana.place`.

Supprimer : `tests/legacy-exclude.txt` (INV-03 accepte « absent ou vide » ; lecteurs tolérants).

Ne pas toucher : `public/` (dont `master.css`, `.htaccess` : la CSP couvre déjà rsms, fontawesome, youtube-nocookie), `site/`, `src/content/`, `src/content.config.ts`, `src/pages/sitemap.txt.ts` (déjà 13 URL triées), `package.json`, lockfile, `.nvmrc`, `deploy.yml`.

## Gabarits (à reproduire depuis le snapshot)

`<head>` (ordre du snapshot) : `charset`, `<title>`, `viewport`, `<meta name="description">`, `<link rel="canonical" href="https://benoitvinceneux.com/<slug>">` (accueil : `…/` ; pas sur la 404), `noindex` sur la 404, `/static/master.css`, `https://rsms.me/inter/inter.css`, Font Awesome `https://use.fontawesome.com/releases/v5.12.1/css/brands.css` avec `integrity="sha384-…"` et `crossorigin="anonymous"`, puis le `<style>` `:root { --theme-highlight-text-color: #ffffff; --theme-highlight-background-color: #0F4C81; }` en **`<style is:inline media="screen">`** (un `<style>` normal est scopé et sorti dans `dist/_astro/*.css` → PAR-02 rouge, fichier en plus). Les règles du lien d'évitement et du focus visible (`a:focus-visible { outline: … }`, car `master.css` a `a { outline: 0 }`) vont dans ce même bloc inline.

- Titres : `Sigfox – Benoit Vinceneux` avec le caractère `–` littéral (Astro échappe `&` dans les expressions). Accueil : `Benoit Vinceneux – Senior Product Builder · AI × Data · Founder DNA. Passionné d'outdoor`, description `Senior Product Builder · AI × Data · Founder DNA Passionné d'outdoor 📍France`. Pages projet : description = front matter. À propos : titre et description du snapshot.
- SRI : calculer, ne pas recopier de mémoire : `curl -s <url FA> | openssl dgst -sha384 -binary | openssl base64 -A`, et vérifier que la réponse porte `access-control-allow-origin` (sinon la feuille et les icônes sautent). Pas d'`integrity` sur Inter (le ticket ne le demande pas, et rsms peut changer le fichier).
- `<body class="body lh4">`, premier enfant : `<a class="…" href="#contenu">Aller au contenu</a>`, masqué hors focus par le CSS inline. `<main id="contenu" class="main py05 sd-p05">`.
- En-tête : `<h1 class="p1"><a class="block h1 lh1 fw800" href="/">Benoit Vinceneux</a></h1>` (dans `<div class="py05 sd-p05">`), aside tagline (`<br>`), nav, aside réseaux (LinkedIn, GitHub, `title`, `fab` + `&#xf0e1;` / `&#xf09b;`, `span.hide`) : copier le markup du snapshot, liens en `/slug`.
- Nav : `<li class="px0125"><a class="inlineblock px0125 ul:hover color-link:hover" href="/slug"><span>Libellé</span></a></li>` ; élément actif : `a` sans `color-link:hover` + `aria-current="page"`, `span class="color-highlight bg-highlight bg-highlight-shadow"`. Libellés = `title` des projets (`🍿Curated Adventures` compris), « À propos » en tête. Accueil et 404 : aucun actif.
- Pied : `<footer class="py05 sd-p05"><div class="p1 copy"><p>(c) {new Date().getFullYear()}</p></div></footer>`.
- `[slug].astro`, variante `textposition === 'above'` (10 pages) : `<div class="">` > `span1 order9` > `p025` > `p075` h1 `h2 lh2 fw800` ; `<div class="ld-row">` > `span2` > `p075 copy lh4` > contenu ; colonne `span2` > `p1 copy copy--wide lh4` > `<figure class="image"><img alt="" height src srcset width></figure>` par image.
- Variante par défaut (yana-place, pas de `textposition`) : outer `ld-row`, h1 `h2 ld-h3 lh2 fw800`, inner `<div class="">` avec en plus un `span1` > `p075 copy lh4` > `<dl>` (`Role`, `Website` avec `<a class="ul" href>`) quand les champs existent (rendre client/role/date/website s'ils sont présents ; ordre du snapshot pour role puis website), figures dans `p1 copy lh4` (un bloc par image).
- `a-propos.astro` : contenu de `site/a-propos.html` copié, liens internes `services-du-premier-ministre.html` → `/services-du-premier-ministre` (etc.), `mailto:` obfusqué gardé tel quel, image `/media/…`. Les `·` et `—` du texte restent (parité ; la convention CLAUDE.md vaut pour les nouveaux textes : lien d'évitement et 404, sans séparateur).
- `index.astro` : `<div class="sd-grid2 ld-grid3">`, une carte `<article class="p1"><a class="block anchor" href="/slug"><figure><img class="block w100 maxw" src srcset alt=""></figure><h3 class="mt025 ul:hover">Titre</h3></a></article>` ; carte À propos en dur (chemins du snapshot) puis les 11 projets triés par `order` (`cover`). Pas de `h2` ajouté (D-4).
- Astro ajoute des `id` aux titres Markdown : normal, ne pas « corriger ». Vérifier qu'aucune URL nue du Markdown n'est transformée en lien par GFM (PAR-02 le dira).

## Étapes

1. Commit `docs:` : `tasks/lessons.md` + ce plan.
2. `astro.config.mjs`, `Base.astro`, `[slug].astro`, `a-propos.astro`, `index.astro`, `404.astro` ; `npx astro build` ; `grep -rli '<script' dist/` vide.
3. `tests/test_parity.py` + `parity-allowlist.json` d'abord (signal le plus rapide sur les vrais écarts) ; corriger les gabarits jusqu'au vert sans élargir l'allowlist au-delà des entrées attendues.
4. Supprimer `legacy-exclude.txt`, retoucher `test_dist.py` (helpers, ART-04, INV-02/03, SPE-05, CSP-01 b, SEO-01) et `http_check.sh`.
5. `test_links.py` + `allowed-hosts.txt`, `test_a11y.py`, `test_budget.py`. `python3 -I -m unittest discover -s tests -v` vert.
6. `npx html-validate "dist/**/*.html"` : lister ce qui sort. Corriger d'abord le markup quand c'est neutre pour la parité (ex. `frameborder="0"` de l'iframe sigfox → retirer et ajouter `border: 0` au `style` existant, dans le `.md`). Sinon `"règle": "off"` + entrée `html-validate` motivée. Attendus probables : `heading-level` (deux `h1` par page, `h1` → `h3` à l'accueil, D-4), `long-title` (titre de l'accueil, parité), `no-inline-style` (iframe responsive de sigfox). Peut-être `require-sri` pour Inter : préférer l'entrée allowlist à une `integrity` sur un fichier tiers mouvant.
7. `a11y.spec.ts` ; `npx playwright test` vert (0 serious/critical). Si axe signale `link-in-text-block` ou un contraste : corriger hors `master.css` seulement si trivial, sinon le noter (recette 9 : noté, pas corrigé).
8. Apache local (leçons #4 : `mod_autoindex`, port libre) : `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh` vert sur les 13 pages.
9. Contrôle visuel : `python3 -m http.server -d site 8001` et `python3 -m http.server -d dist 8002`, puis `npx playwright screenshot --viewport-size=1280,800 --full-page http://127.0.0.1:8001/<slug>.html <scratchpad>/snap-<slug>-1280.png` et pareil sur 8002 (`/<slug>.html`), en 1280 et 360 px, pour les 13 pages (au minimum accueil, sigfox, yana-place, a-propos en 360). Captures dans le scratchpad uniquement. Comparer : seule différence attendue = lien d'évitement invisible hors focus. Vérifier aussi l'absence de défilement horizontal à 360 px.
10. Recette locale : négatifs (mot changé dans un `.md` → PAR-01 rouge nommant la page ; `/n-existe-pas` dans `a-propos.astro` → LNK-01 rouge), restaurer.
11. Job complet : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html" && npx playwright test` + `http_check.sh`. `git status` : ni `dist/` ni capture versionnés.
12. Commit `feat: Gabarits Astro et tests de parité (BV-04)`.

## Points d'attention

- **Dette (a)** résolue par la définition de « page » : `a11y.spec.ts` teste les 13 pages de `legacy-urls.txt` + `404.html`, comme les tests Python. Le fichier Google n'est pas une page (une ligne de texte) : il n'est pas « exclu », il n'est simplement pas dans la liste, et son nom disparaît du code. Plafond : une future page HTML hors `legacy-urls.txt` ne serait pas auditée par axe ; elle doit de toute façon y être ajoutée (inventaire).
- **Dette (b)** : `master.css` n'a aucun `url()` aujourd'hui ; le tri par extension ne change rien au résultat, il évite seulement un faux rouge le jour où une image CSS apparaît.
- `aria-current` et l'`alt=""` des vignettes ne passent pas par l'allowlist (aucun test de parité ne les voit) : c'est A11Y-01 qui les verrouille.
- Pied de page : année du build. Égale au snapshot (2026) aujourd'hui ; si les tests de parité sont encore là au 1er janvier, PAR-01 rougira. Ils sont retirés en #9 : pas d'entrée d'allowlist (elle serait morte aujourd'hui).
- `import test_dist as base` (module) dans les nouveaux fichiers, jamais `from test_dist import TestDist` (double découverte).
- `dist/` absent : les tests échouent (pas de `skip`), comme les autres tests de `test_dist.py`.
- HTTP-04 lit `<title>` de `dist/404.html` par `sed` sur une ligne : garder `<title>…</title>` sur une seule ligne.
- Aucun `<script>` : pas d'îlot, pas de `client:*`, pas de `<script>` dans les `.astro` ; ART-04 le verrouille.
- Sécurité : aucun secret, aucun réglage GitHub, aucun accès serveur ; `deploy.yml` intact (publie `site/`) ; pas de `.php` ; aucun nom d'hôte ni chemin serveur dans le code, les commits ou la PR.
- Si `package.json` ou le lockfile bougent (ne devrait pas arriver) : leçon #3, régénérer depuis zéro et `npm ci --dry-run`.
