# #14 [CONTENU] accueil et gabarit : tagline sans séparateurs, `<title>` et page 404

Branche : `feat/bv-14-gabarit` (déjà créée). PR `Closes #14` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Aucune décision de #2 en jeu au-delà de la parité des URL (aucune URL ne change). Ni réglage GitHub, ni secret, ni accès serveur. Rien à trancher : blocker vide.

Texte appliqué : version finale de #14 = proposition + réponses cochées du 22/10/2026 + commentaire de Benoit du 23/10/2026 :
- `<title>` des autres pages et de la 404 : option (a), « Nom : Benoit Vinceneux », sans tagline. Seul l'accueil porte la tagline.
- Ajout au périmètre : coquille de `toulouse-football-club` (« effectué » devient « effectuées »).
- Ordre de navigation et de la grille : inchangé.

## Critères d'acceptation

- [ ] Tagline de l'en-tête commun (`src/layouts/Base.astro`), mêmes `<br>` qu'aujourd'hui :
  `Senior Product Builder, AI × Data, Founder DNA<br>` / `Passionné d'outdoor<br>` / `📍France`
- [ ] Accueil, `<title>` = `Benoit Vinceneux : Senior Product Builder, AI × Data, Founder DNA`
- [ ] Accueil, meta description = `Product builder spécialisé dans le 0→1 des produits IA et data. Fondateur, freelance pendant 10 ans, aujourd'hui intrapreneur d'État à la DINUM.` (telle quelle)
- [ ] Pages projet : `<title>` = `${title} : Benoit Vinceneux` (ex. `Groupama : Benoit Vinceneux`)
- [ ] 404 : `<title>` = `Page introuvable : Benoit Vinceneux`
- [ ] `/a-propos` : `<title>` déjà `À propos : Benoit Vinceneux` (#13), ne pas toucher
- [ ] Aucun « · », « – », « — », « | » dans la tagline commune ni dans aucun `<title>` de `dist/` ; chaque titre unique
- [ ] `src/content/projects/toulouse-football-club.md` : `missions que j'ai effectué` devient `missions que j'ai effectuées` ; rien d'autre dans ce fichier
- [ ] Ordre de la nav et de la grille inchangé (T-BV-NAV-01 vert sans modification)
- [ ] `llms.txt` / `llms-full.txt` : non modifiés (vérifié : le résumé d'en-tête relève de #22 ; aucun passage ne reprend la tagline à points médians, l'ancien `<title>`/description de l'accueil ni la phrase Toulouse ; `llms-full.txt` l.16 porte déjà la nouvelle tagline)

## Tests T-BV-* à garder verts (aucun nouveau test au catalogue pour ce ticket)

| Test | Fichier | Pourquoi il concerne #14 |
|------|---------|--------------------------|
| T-BV-BUILD-01 | `npx astro build` | gabarits modifiés |
| T-BV-SEO-01 | `tests/test_dist.py` (`test_seo_01_head`) | titres uniques, meta description non vide, canonical |
| T-BV-A11Y-01 | `tests/test_a11y.py` | titres |
| T-BV-NAV-01 | `tests/test_a11y.py` | ordre nav inchangé |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` | balisage de l'en-tête |
| T-BV-HTTP-04 | `tests/http_check.sh` | lit dynamiquement le `<title>` de `dist/404.html` (sed `[^<]*`, compatible avec « : ») |
| T-BV-CONT-01/03 | `tests/test_content.py` | fichier projet modifié |
| T-BV-SPE-01 | `tests/test_dist.py` | llms inchangés |
| Playwright / axe | `tests/e2e/` | accessibilité |
| suite complète | `python3 -I -m unittest discover -s tests` | non-régression |

Vérifié : aucun test ne code en dur l'ancien format « – Benoit Vinceneux » ni la tagline (grep sur `tests/`). Rien à adapter.
Pas de test ajouté pour l'absence de séparateurs : hors catalogue #10 ; la QA le vérifie dans `dist/` (commande ci-dessous).

## Fichiers à modifier (4, aucun à créer)

1. `src/layouts/Base.astro` : ligne de tagline `Senior Product Builder · AI × Data · Founder DNA<br>` devient `Senior Product Builder, AI × Data, Founder DNA<br>`. Les deux lignes suivantes inchangées.
2. `src/pages/index.astro` : attributs `title` et `description` de `<Base>` remplacés par les textes ci-dessus (rien d'autre).
3. `src/pages/[slug].astro` : `` title={`${title} – Benoit Vinceneux`} `` devient `` title={`${title} : Benoit Vinceneux`} ``.
4. `src/pages/404.astro` : `title="Page introuvable – Benoit Vinceneux"` devient `title="Page introuvable : Benoit Vinceneux"`.
5. `src/content/projects/toulouse-football-club.md` l.12 : `effectué` devient `effectuées` (garder les deux espaces finaux du saut dur `:  `).

## Étapes

1. Appliquer les 5 modifications ci-dessus.
2. `npx astro build`.
3. `python3 -I -m unittest discover -s tests` ; `npx html-validate "dist/**/*.html"`.
4. Apache local (port libre, voir lessons #4) puis `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh`.
5. `npx playwright test`.
6. Contrôle QA des titres et de la tagline :
   ```sh
   for f in $(find dist -name '*.html' | sort); do printf '%s\t' "$f"; sed -n 's#.*<title>\([^<]*\)</title>.*#\1#p' "$f"; done
   grep -h -o '<title>[^<]*</title>' dist/*.html | grep '[·–—|]'   # doit ne rien renvoyer
   grep -c 'Senior Product Builder, AI × Data, Founder DNA<br>' dist/*.html
   ```
   Attendu : 15 fichiers HTML (index, a-propos, 11 projets, 404, fichier Google sans `<title>` de gabarit), titres uniques au format attendu.

## Points d'attention

- Le « × » (U+00D7) de la tagline est à garder tel quel ; « 0→1 » (U+2192) dans la description aussi.
- Ne pas toucher au `<title>` de `/a-propos` ni au H2 de #13.
- Des « – » subsistent dans le corps de `lepharmacien-fr` (« patient – pharmacien ») et dans `llms*.txt` : hors périmètre (corps de page, pas `<title>` ni tagline). Le `grep` de QA porte donc sur les `<title>` et la tagline, pas sur tout le HTML.
- Apostrophe de `Passionné d'outdoor` et `d'État` : apostrophe droite `'`, comme aujourd'hui et dans l'issue.
- `.nvmrc` reste `24`. Aucune dépendance ajoutée.
- Ne citer aucune « Source » de l'issue dans le code, le commit ou la PR.
- Commit : `content: Accueil et gabarit, tagline sans séparateurs, titres « Nom : Benoit Vinceneux » et coquille Toulouse (#14)`.
