# #5 [BV-03] Script d'import Kirby vers Markdown et collection `projects`

Branche : `feat/bv-03-import-kirby` (déjà créée). PR `Closes #5` ouverte par l'orchestrateur.
Décisions liées (#2, toutes validées) : D-BV1 (Markdown éditable), D-BV2 (aucun brouillon publié, liens vers pages non publiées retirés), D-BV4 (aucune nouvelle dépendance : `package.json` et lockfile ne changent pas ; si jamais ils changent, leçon #3 : régénérer depuis zéro et `npm ci --dry-run`).
`tasks/lessons.md` (modifié, non commité) part avec le premier commit.

## Critères d'acceptation (issue #5)

- [ ] 11 fichiers `.md`, ids égaux aux slugs de `legacy-urls.txt`
- [ ] Un champ obligatoire supprimé fait échouer `astro build` (et `astro sync`, T-BV-CONT-02)
- [ ] Tests verts : `(link:)`, `(email:)`, titres `##Titre` convertis
- [ ] Test vert : lien absolu vers le domaine rendu relatif
- [ ] Test vert : saut de ligne dur hors bloc HTML, pas à l'intérieur
- [ ] La fixture contient un faux `index.php`, un faux `.htaccess`, un dossier de brouillons à 2 profondeurs et un lien symbolique : aucun n'apparaît dans la sortie
- [ ] Aucun `.php` ni `.htaccess` versionné sous `src/` ou `public/`, hors `public/.htaccess`

## Tests à livrer (catalogue #10)

| ID | Fichier | Contenu |
|---|---|---|
| T-BV-CONT-01 | `tests/test_content.py` (nouveau) | 11 `src/content/projects/*.md` ; noms = slugs des pages projet de `legacy-urls.txt` (entrées `200` HTML moins `/` et `/a-propos`) ; front matter lu ligne par ligne (pas de YAML) : `title`, `order`, `description`, `cover`, `images` présents ; `order` uniques ; chaque chemin `/media/…` de `cover` et `images` (src et srcset) existe sous `public/` |
| T-BV-CONT-02 | `tests/test_content.py` | copie temporaire minimale (`package.json`, `astro.config.mjs`, `src/`) + symlink `node_modules`, ligne `description:` retirée d'un `.md`, `npx astro sync` : code ≠ 0, la sortie contient le nom du fichier et `description` |
| T-BV-CONT-03 | `tests/test_content.py` | aucun `(link:`, `(image:`, `(email:`, `(date:` sous `src/content/` |
| T-BV-IMP-01 | `tests/test_import.py` (nouveau) | 4 tests séparés : `(link: URL text: X)` → `[X](URL)` ; `(email: a@b text: X)` → `[X](mailto:a@b)` ; `##Titre` → `## Titre` ; `(image: x.jpg)` → `![](/media/…)` |
| T-BV-IMP-02 | `tests/test_import.py` | `https://benoitvinceneux.com/x` → `/x` ; `https://example.org/x` inchangé (2 tests) |
| T-BV-IMP-03 | `tests/test_import.py` | saut simple → saut dur hors HTML ; inchangé dans un `<div>…</div>` multiligne (2 tests) |
| T-BV-IMP-04 | `tests/test_import.py` | import de la fixture (copiée dans un dossier temporaire, parasites créés à la volée, voir plus bas) : seuls les projets valides sont écrits ; `builtins.open` patché pour lever sur tout chemin hors liste blanche |
| T-BV-IMP-05 | `tests/test_import.py` | deux exécutions sur la fixture : sorties identiques à l'octet |
| T-BV-IMP-06 | `tests/test_import.py` | `socket.socket` patché pour lever : l'import passe quand même |
| T-BV-PAR-05 | `tests/test_dist.py` | `dist/media/` identique à `site/media/` (même liste de fichiers + `filecmp.cmp(shallow=False)`) ; factoriser avec T-BV-CSS-01 en une petite fonction `assert_same_tree(src, out)` |

Les tests existants (`test_repo.py`, `test_dist.py`, `e2e/`) doivent rester verts, en particulier T-BV-ART-03 et T-BV-SPE-05.

## Fichiers

Créer :
- `scripts/import_kirby.py` : stdlib seule, `python3 -I scripts/import_kirby.py <dossier_contenu> [--site site] [--out src/content/projects]`. Le dossier de contenu est **toujours** un argument CLI : jamais de chemin d'archive écrit dans un fichier versionné.
- `src/content.config.ts` : collection `projects`, `glob({ pattern: '*.md', base: './src/content/projects' })` (id = nom de fichier = slug).
- `src/content/projects/<slug>.md` × 11 : sortie du script, commitée.
- `tests/test_import.py`, `tests/test_content.py`.
- `tests/fixtures/kirby/` (synthétique, minuscule, voir plus bas).

Modifier :
- `tests/test_dist.py` : T-BV-PAR-05 + helper partagé avec CSS-01.
- `src/pages/sitemap.txt.ts` : rien à changer dans la logique (elle liste déjà `getCollection('projects')`) ; retirer le commentaire « [] tant que #5… » et trier par `data.order` (`getCollection` rend l'ordre du système de fichiers : sitemap identique macOS/Linux). Le sitemap liste maintenant 13 URL.

Ne pas toucher : `public/media/` (déjà copié et identique à `site/media`, vérifié par `diff -rq` : T-BV-PAR-05 le garantit), `tests/legacy-exclude.txt` (les pages projet y restent : gabarit en #6), `package.json`, lockfile, `.nvmrc`, `deploy.yml`.

## Spécification du script

Lecture (liste blanche, aucune autre ouverture de fichier) :
- Dossier de contenu : `os.scandir` du **seul niveau racine**. Un dossier est un projet s'il matche `^(\d+)_(.+)$`, n'est pas un lien symbolique (`entry.is_symlink()`), contient un `project.txt` qui n'est pas un lien symbolique, et que son slug n'est pas `a-propos` (porté à la main en #6). `order` = le nombre du préfixe, `slug` = le reste.
- Aucune descente récursive : `_drafts`, `sandbox`, `error`, `home`, les sous-dossiers (dont `4_curated-adventures/4_curated-adventures/`) ne sont jamais parcourus. Si un `os.walk` est utilisé malgré tout : `followlinks=False` et élagage des dossiers commençant par `_`.
- `site.txt` : **non lu**. Seul usage : `(date: year)` du pied de page, qui relève du layout (#6). Ponytail : ajouter la lecture le jour où un champ de `site.txt` alimente une page projet.
- Snapshot `site/` (argument `--site`) : `<slug>.html` (meta description + `<img>` dans l'ordre) et `index.html` (vignette de la grille : `<img>` dans le lien `href="<slug>.html"`). Parsing avec `html.parser`, `html.unescape` sur la description (`&hellip;`, `&rsquo;`…).
- Toutes les lectures passent par `open(...)` builtin (pas `Path.read_text`, qui contourne le patch de T-BV-IMP-04).
- Jamais de `.php`, `.htaccess`, `*.png.txt` ni autre fichier ouvert, même pour inspection.

Parsing Kirby : `re.split(r"^-{4}\s*$", texte, flags=re.M)`, puis `Clé: valeur` (clé avant le premier `:`, en minuscules, valeur `strip()`). Champs utilisés : `title`, `text`, `textposition`, `client`, `role`, `date`, `website`. Champs vides omis du front matter.

Convertisseur Kirbytext → Markdown (fonction pure `convert(text, slug, media_dir)`, testée directement) :
1. `(link: URL text: X)` → `[X](URL)` ; `URL` commençant par `http(s)://(www.)?benoitvinceneux.com` rendue relative (`/x`, `/` si vide). Lien interne vers un slug non publié (ni projet importé ni `a-propos`, ex. `/numerique-responsable` dans curated-adventures) → texte seul, sans lien (D-BV2).
2. `(email: a@b text: X)` → `[X](mailto:a@b)` ; sans `text:`, le texte est l'adresse.
3. `(image: x.jpg)` → `![](/media/pages/<slug>/<hash>/x.jpg)` : chemin trouvé dans `<site>/media/pages/<slug>/*/` (variante `-640x` si elle existe, sinon le nom exact). Aucun usage dans le contenu réel, mais exigé par T-BV-IMP-01.
4. `^(#{1,6})(?=[^#\s])` → `\1 `.
5. Sauts de ligne : ajouter deux espaces en fin de ligne quand la ligne et la suivante sont non vides, **sauf** dans un bloc HTML brut. Bloc HTML = d'une ligne qui commence par `<` (après espaces) jusqu'à la prochaine ligne vide (règle CommonMark type 6). Deux espaces plutôt que `\` : en fin de bloc ou de liste, ils sont ignorés au lieu d'afficher un `\`. Attention aux lignes `---` (règle horizontale) : ne pas les coller à une ligne de texte (setext) ; dans le contenu réel elles sont précédées d'une ligne vide.
6. `(date: …)` : pas dans les `project.txt`, rien à convertir ; T-BV-CONT-03 garantit l'absence en sortie.

Front matter écrit à la main (pas de lib YAML), chaînes via `json.dumps(…, ensure_ascii=False)` (JSON ⊂ YAML), clés dans un ordre fixe, une image par ligne en mapping de flux :

```yaml
---
title: "Sigfox"
order: 5
description: "…"
textposition: "above"
cover: { src: "/media/pages/sigfox/…/sigfox-min-288x288.png", srcset: "…" }
images:
  - { src: "/media/pages/sigfox/…/sigfox-min-640x.png", srcset: "…", width: 640, height: 640 }
---
<corps converti>
```

- Chemins `media/…` du snapshot préfixés par `/` (la parité de #6 normalise les chemins relatifs) ; `srcset` repris tel quel, avec `/` devant chaque URL.
- `alt` non stocké : vide partout dans les pages projet du snapshot ; l'`alt` des vignettes est l'affaire de #6 (D-3).
- Sortie déterministe : projets triés par `order`, `\n` final, encodage UTF-8, aucun horodatage. Le script écrit seulement les fichiers des projets importés (pas de suppression dans `--out`).

Schéma `src/content.config.ts` (zod d'Astro, `import { z } from 'astro/zod'` ou `astro:content` selon la version 7.3.7) :
`title: string`, `order: number().int()`, `description: string().min(1)` (obligatoire), `role?`, `client?`, `date?`, `website?` (strings), `textposition?` (string), `cover: { src, srcset }`, `images: array({ src, srcset, width: number, height: number })`.

## Fixture `tests/fixtures/kirby/` (versionnée, synthétique)

```
tests/fixtures/kirby/
  content/
    2_projet-a/project.txt        # Title, Text avec (link:), (email:), ##Titre, <div> multiligne, Textposition, Role
    3_projet-b/project.txt        # second projet valide (ordre, champs vides omis)
    1_a-propos/project.txt        # ignoré (hors collection)
    4_sans-contenu/note.md        # dossier sans project.txt : ignoré (fichier hors liste blanche)
    _drafts/a/b/project.txt       # brouillon à 2 profondeurs : ignoré
    sandbox/sandbox.txt           # ignoré
  site/
    index.html                    # grille : un <a href="projet-a.html"><img src srcset></a> par projet
    projet-a.html, projet-b.html  # meta description + <img>
    media/pages/projet-a/h1/x-640x.jpg   # fichiers vides, pour (image:)
```

Créés **à la volée** par le test dans une copie temporaire (`shutil.copytree` puis écriture), jamais versionnés (garde-fou CLAUDE.md et T-BV-ART-03, qui n'admet `.htaccess` que dans `public/` et `site/`) :
- `content/2_projet-a/2_projet-a/index.php` (contenu inoffensif, ex. `# faux fichier`, sans balise PHP) ;
- `content/.htaccess` et `content/2_projet-a/.htaccess` ;
- `content/5_lien -> ../elsewhere` (lien symbolique vers un dossier hors fixture contenant un `project.txt`) et `content/3_projet-b/project.txt` doublé d'un lien symbolique `6_lien-fichier/project.txt -> …`.

Assertions T-BV-IMP-04 : la sortie contient exactement `projet-a.md` et `projet-b.md` ; aucun fichier ouvert hors `content/*/project.txt` (non-lien), `site/**` et le dossier de sortie (écriture). Un docstring en tête de `test_import.py` signale que les parasites sont générés : c'est ce que la recette (scénario 2) doit vérifier.

## Étapes

1. Commit `docs:` de `tasks/lessons.md` + ce plan.
2. `tests/test_import.py` + fixture (rouge), puis `scripts/import_kirby.py` jusqu'au vert : `python3 -I -m unittest tests.test_import -v`.
3. Lancer le script une fois sur l'archive locale (chemin passé en argument, jamais écrit dans le dépôt) : `python3 -I scripts/import_kirby.py <archive> --site site --out src/content/projects`. Relancer : `git status` vide (idempotence, scénario 8).
4. Relire les 11 `.md` contre le snapshot (au moins sigfox pour le HTML brut, curated-adventures pour le lien retiré, yana-place pour les 7 images). `grep -rn '(link:\|(image:\|(email:\|(date:' src/content` vide.
5. `src/content.config.ts`, retrait du commentaire dans `sitemap.txt.ts`, `npx astro build`.
6. `tests/test_content.py` et T-BV-PAR-05 dans `test_dist.py`.
7. Tout le job en local : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html"`, plus `http_check.sh` (Apache local, voir leçons #4) et `npx playwright test`.
8. `git ls-files | grep -E '\.php$|\.htaccess$'` → seulement `public/.htaccess` et `site/.htaccess`.
9. Commit `feat: Script d'import Kirby et collection projects (BV-03)`.

## Points d'attention

- Sécurité : l'archive contient des `.htaccess` et un `index.php` suspect. Ne jamais les ouvrir, lire, afficher, copier ou exécuter. Aucune copie de l'archive dans le dépôt ni dans `public/`. Aucun nom d'hôte, chemin serveur ou chemin local de l'archive dans un fichier versionné, un commit ou la PR.
- T-BV-CONT-02 : vérifier que `astro sync` échoue bien sur une erreur de schéma avec Astro 7.3.7 et que le message nomme fichier et champ. Si `sync` ne valide pas, le signaler (le catalogue impose `sync`) au lieu de basculer en silence sur `build`. Ne pas copier `site/`, `public/` ni `dist/` dans la copie temporaire (lent, inutile). Avec `node_modules` en lien symbolique, le cache du content layer (`node_modules/.astro/`) serait celui du vrai dépôt : passer un `cacheDir` interne au dossier temporaire (config de la copie) et vérifier qu'un `npx astro build` après la suite donne toujours 13 lignes de sitemap. Le message d'Astro nomme la collection et l'id (`sigfox`) plutôt que le chemin : asserter sur le slug et `description`, pas sur `sigfox.md`.
- T-BV-SPE-05 : le sitemap passe à 13 URL dont 11 pages pas encore construites (gabarit en #6) : attendu, les pages restent dans `legacy-exclude.txt`. Vérifier que `http_check.sh` et T-BV-INV-01 ne lisent pas le sitemap.
- `description` : présente et non vide dans les 11 pages du snapshot (vérifié), prise de la meta (tronquée avec `…` par Kirby) : c'est voulu, parité T-BV-PAR-04 en #6.
- Ordre : `order` = préfixe 2 à 12, cohérent avec l'ordre de la nav (T-BV-NAV-01).
- Lien `/numerique-responsable` (brouillon) dans curated-adventures : retiré en #5 (D-BV2) ; l'écart de parité sera déclaré dans `tests/parity-allowlist.json` en #6. À noter dans la PR.
- `__pycache__` déjà ignoré ; ne pas versionner de sortie de test.
- Pas de nouvelle dépendance, pas de `.php`, pas de `.htaccess` hors `public/`.
