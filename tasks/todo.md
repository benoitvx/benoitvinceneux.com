# #21 [CONTENU] curated-adventures : virage IA, lien vers page absente

Branche : `feat/bv-21-curated-adventures` (déjà créée). PR `Closes #21` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Décision de #2 en jeu : D-BV2 (liens vers des pages non publiées : retirer), déjà appliquée à l'import (#5). Ni dépendance, ni réglage, ni secret.
Texte appliqué : version finale de #21, réponses de Benoit du 22/10/2026 incluses :
- période **2021 à 2024** (confirmée aussi par #23, questions transverses) ;
- GPT personnalisé **plus en ligne** : aucun lien, paragraphe au passé (la proposition l'est déjà) ;
- lien `/numerique-responsable` : **supprimé**.

## Texte final à appliquer

Corps de `src/content/projects/curated-adventures.md`, dans cet ordre (seuls changements : ligne de contexte, nouveau paragraphe, coquilles ; tout le reste mot pour mot, y compris « amis…. », « passionné & pratiquant », « YouTube, Viméo, etc. », les deux liens `https://curatedadventures.club` et le lien `https://curatedadventures.club/about`) :

```md
*Fondateur, projet solo : 2021 à 2024*

Parce que j’en avais marre de passer des heures à chercher un documentaire d’aventure sympa, j’ai créé un **guide des meilleurs documentaires** pour trouver rapidement celui que je voulais regarder, en fonction du sport, du genre ou de la durée.  
Mes amis m’ont demandé de leur partager cette liste, puis les amis de mes amis…. Et c’est comme ça que [🍿Curated Adventures](https://curatedadventures.club) est né.

Fin 2023, dès le lancement des GPTs par OpenAI, j’ai reconstruit l’expérience autour d’un GPT personnalisé : on décrivait l’envie du moment, il proposait le bon documentaire. Côté coulisses, des automatisations IA ont réduit de 80 % le temps passé sur les opérations quotidiennes.

Étant passionné & pratiquant, ce projet fait la part belle aux sports outdoor (surf, escalade, snowboard, vélo, etc.). Vous y trouverez des documentaires connus et moins connus à découvrir !

Je sélectionne manuellement tous les documentaires référencés. Ils sont à regarder sur une plateforme de vidéo en ligne (YouTube, Viméo, etc.).

Sensible aux questions environnementales, je sais que la lecture de vidéos en ligne est une partie du problème. Pour y remédier et pour apporter ma pierre à l’édifice, j’essaye de faire en sorte que le site [🍿Curated Adventures](https://curatedadventures.club) soit le plus responsable possible.  
Je précise toute cette démarche dans [cet article](https://curatedadventures.club/about).
```

Lectures retenues :
- Ligne de contexte « sous le titre » = première ligne du corps, en italique, comme les pages déjà traitées (NotreSanté, Pierre Fabre, Ça Compte Pour Moi : `*Rôle : période*`). Texte exact : « Fondateur, projet solo : 2021 à 2024 ».
- Apostrophes : le nouveau paragraphe prend les « ’ » typographiques du reste de la page (normalisation, pas de changement de contenu).
- Paragraphe « après « …est né. » » : nouveau paragraphe inséré juste après cette phrase, donc le premier paragraphe actuel est coupé en deux (« Étant passionné… » devient un paragraphe à part). Le hard break (deux espaces) en fin de ligne « est né. » disparaît.
- Coquille « docu » (pluriel) : le bloc cité par l'issue commence à « […] celui que je voulais regarder », donc après la première occurrence (« guide des meilleurs docu »), qui n'y apparaît pas corrigée. Le constat vise le mot « docu » en général : il est corrigé aux deux endroits du corps (« des meilleurs documentaires », « des documentaires connus ») et dans la meta description. « tout cette démarche » devient « toute cette démarche ».
- Lien `/numerique-responsable` : déjà retiré à l'import (#5, D-BV2) ; le texte « Sensible aux questions environnementales… » est conservé sans lien. Rien à faire sauf vérifier.

Meta description (l'issue n'en donne pas ; réalignée sur la coquille corrigée, rien d'autre) :
`Parce que j’en avais marre de passer des heures à chercher un documentaire d’aventure sympa, j’ai créé un guide des meilleurs documentaires pour trouver rapidement celui…`

## Critères d'acceptation

- [ ] Titre inchangé : `🍿Curated Adventures` (nav et `<title>` inchangés).
- [ ] Ligne de contexte « Fondateur, projet solo : 2021 à 2024 » en tête du corps, sous le `<h1>`.
- [ ] Paragraphe GPT présent mot pour mot (« Fin 2023 », « GPTs par OpenAI », « GPT personnalisé », « 80 % », « opérations quotidiennes »), placé après « …est né. », sans lien.
- [ ] Plus de « docu » isolé ni de « tout cette démarche » sur la page ; « toute cette démarche » présent.
- [ ] Aucun lien vers `/numerique-responsable` dans `dist/curated-adventures.html` ; liens existants conservés (`https://curatedadventures.club` ×2, `https://curatedadventures.club/about`), aucun lien ajouté.
- [ ] Rien d'autre ne change dans le texte (pas de « IA dès 2021 », pas de chiffre ni de rôle ajouté).
- [ ] Aucun « — », « · », « | » dans le texte visible du `<main>` et la meta description de la page.
- [ ] URL, slug, `title`, `order`, `textposition`, `cover`, `images` inchangés.
- [ ] `public/llms.txt` et `public/llms-full.txt` : passages Curated Adventures alignés (étape 2), y compris la période de la l. 31 de `llms-full.txt`.

## Tests (catalogue #10)

Aucun test à ajouter (l'issue n'en demande pas). Hôte `curatedadventures.club` déjà dans `tests/allowed-hosts.txt` l. 1 ; page listée dans `tests/test_dist.py` l. 24, `tests/legacy-urls.txt` l. 10, `tests/test_a11y.py` l. 6. Tests qui doivent rester verts sans modification :

| ID | Fichier | Lien avec #21 |
|---|---|---|
| T-BV-BUILD-01 | `npx astro build` + `tests/test_dist.py` | build de la page modifiée |
| T-BV-CONT-01, T-BV-CONT-02, T-BV-CONT-03 | `tests/test_content.py` | front matter (`description` non vide, sur une seule ligne `description: "..."`), `cover`/`images` existants, pas de KirbyText |
| T-BV-SPE-01 | `tests/test_dist.py` | URL du domaine dans `llms*.txt` : `/curated-adventures` déjà en 200, n'en ajouter aucune |
| T-BV-SEO-01 | `tests/test_dist.py` | canonical, meta description non vide, `<title>` unique |
| T-BV-LNK-01, T-BV-LNK-02, T-BV-HOST-01 | `tests/test_links.py` | liens internes valides, hôte externe déjà autorisé |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` (+ `tests/test_repo.py`) | HTML de la page |
| T-BV-HTTP-01 | `tests/http_check.sh` sur Apache local servant `dist/` | `/curated-adventures.html` et `llms*.txt` en 200 |
| T-BV-A11Y-01, T-BV-A11Y-02 | `tests/e2e/a11y.spec.ts`, `tests/test_a11y.py` | axe sur `/curated-adventures` |
| Autres (ART, INV, SPE-02..06, HTA, CSP, BUD, DEP, WF, GUARD, IMP) | `tests/*.py` | non concernés, doivent rester verts |

Commande : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html"`, puis Apache local + `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh`, puis `npx playwright test`.

## Fichiers modifiés (3, rien à créer)

1. `src/content/projects/curated-adventures.md` : `description` (« docu » → « documentaires ») et corps.
2. `public/llms.txt` : ligne 10 seulement.
3. `public/llms-full.txt` : section `## 🍿 Curated Adventures` (l. 162 à 181) et, l. 31, la seule période `2021 – 2023` → `2021 – 2024`.

Hors périmètre (ne pas toucher) :
- `public/llms-full.txt` l. 31 : seule la date change (`2023` → `2024`, période tranchée par Benoit dans #21 et #23, sinon contradiction avec la section réécrite dans le même fichier). « solopreneur » et le « · » restent pour #13/#22 (écart assumé avec #20, où l. 32 portait un intitulé et non une date). `src/pages/a-propos.astro` (période de l'à propos) : #13, en attente.
- Gabarit, format du `<title>` (#14), `src/pages/[slug].astro`, `src/content.config.ts`, `tests/allowed-hosts.txt`, reste de `llms*.txt` (#22).

## Étapes

1. **Page** : appliquer le front matter et le corps ci-dessus dans `src/content/projects/curated-adventures.md` (apostrophes typographiques « ’ » partout, y compris dans le nouveau paragraphe).
2. **llms** (mêmes faits, aucun ajout) :
   - `public/llms.txt` l. 10 :
     `- [Curated Adventures](https://benoitvinceneux.com/curated-adventures): Fondateur, projet solo (2021-2024). Guide pour trouver rapidement les meilleurs documentaires d'aventure outdoor (surf, escalade, snowboard, vélo) sur YouTube et Vimeo. Curation manuelle ; fin 2023, expérience reconstruite autour d'un GPT personnalisé ; automatisations IA : 80 % de temps en moins sur les opérations quotidiennes. Démarche éco-responsable. https://curatedadventures.club`
   - `public/llms-full.txt`, section Curated Adventures : « Solopreneur. » devient « Fondateur, projet solo : 2021 à 2024. » ; ajouter après le paragraphe « L'envie a démarré… » une sous-section `### Virage IA` reprenant le paragraphe de la page (fin 2023, GPT personnalisé lancé dès les GPTs d'OpenAI, l'utilisateur décrivait son envie et le GPT proposait le documentaire ; automatisations IA, 80 % de temps en moins sur les opérations quotidiennes ; ne pas écrire que le GPT n'est plus en ligne, absent de la page) ; l. 31 : `2021 – 2023` → `2021 – 2024` (rien d'autre sur la ligne) ; retirer les séparateurs de la section : « Sports outdoor — surf… » → « Sports outdoor : surf… », « « le plus responsable possible » — détaillé » → « « le plus responsable possible », détaillé ».
3. Build + tests (commande ci-dessus), puis contrôles QA :
   - `grep -c numerique-responsable dist/curated-adventures.html` → 0 ;
   - texte du `<main>` et meta description sans « — », « · », « | » ;
   - `grep -E '\bdocu\b|tout cette' dist/curated-adventures.html` → rien.
4. Commit : `content: Curated Adventures, virage IA, période 2021-2024 et coquilles (#21)`.

## Points d'attention

- Ne jamais citer les « Sources » de l'issue (CV, liste d'expériences, profil LinkedIn) ni écrire « IA dès 2021 ».
- Aucun lien vers le GPT (plus en ligne), aucun lien ajouté ou retiré par ailleurs.
- Ne pas toucher au titre à emoji (nav, `<title>`).
- `description` reste sur une seule ligne entre guillemets doubles (T-BV-CONT-01) ; elle contient des « ’ », pas de `"` à échapper.
- Node local 25, CI 24 : ne pas modifier `.nvmrc`.
