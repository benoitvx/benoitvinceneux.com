# #22 [CONTENU] llms.txt et llms-full.txt

Branche : `feat/bv-22-llms` (déjà créée). PR `Closes #22` ouverte par l'orchestrateur.
Milestone M3. Dépendances : #9, #11 à #21 (tous mergés, dont #13 à propos et #14 gabarit). Décision de #2 en jeu : D-BV2 (`/societe-numerique` absente de tout `dist/`, déjà testé par T-BV-SPE-01). D-BV4 : aucune dépendance ajoutée. Ni réglage GitHub, ni secret, ni accès serveur : blocker vide.

Texte appliqué : version finale de #22 = proposition + réponses cochées du 22/10/2026 + commentaire de Benoit du 23/10/2026 (mention familiale « Père de famille » insérée avant « passionné d'outdoor ») + passe typographique transverse de #23 pour `lepharmacien-fr`.

## Critères d'acceptation

- [ ] Résumé d'en-tête, identique dans `public/llms.txt` et `dist/llms-full.txt`, en citation `> ` sur une seule ligne :
  `> Senior Product Builder, AI × Data, Founder DNA. Père de famille, passionné d'outdoor, 📍France. Product builder spécialisé dans le 0→1 des produits IA et data : fondateur, freelance pendant 10 ans, puis intrapreneur d'État. Aujourd'hui AI Product Lead à la DINUM (Services du Premier ministre) : données publiques pour l'IA, code agentique souverain, évaluation des modèles, coaching produit.`
  La phrase « Mi-builder, mi-hacker, mi-dealmaker… » disparaît du résumé de `llms.txt`.
- [ ] `dist/llms-full.txt` est **généré au build** (`src/pages/llms-full.txt.ts`) ; `public/llms-full.txt` n'existe plus. Aucun fichier `llms-full` tenu à la main.
- [ ] Structure de `dist/llms-full.txt` : `# Benoit Vinceneux`, résumé, lignes `Site :`, `Email :`, `LinkedIn :`, `GitHub :` (valeurs actuelles), `---`, puis pour `/a-propos` puis chaque projet dans l'ordre `order` : `## <titre>`, `URL : https://benoitvinceneux.com/<slug>`, texte de la page.
- [ ] Texte d'un projet = `entry.body` sans les blocs HTML bruts (iframe de `sigfox.md`). Texte de `/a-propos` = la même source markdown que la page.
- [ ] `/a-propos` : le contenu du H2 tagline jusqu'aux engagements vit dans `src/content/a-propos.md` (hors collection), rendu par `a-propos.astro` et lu par l'endpoint. HTML équivalent à `master` : mêmes textes, mêmes liens, mêmes niveaux de titres ; H1, lien mailto et image restent dans `a-propos.astro`.
- [ ] `public/llms.txt` : entrées Services du Premier ministre et Présidence mot pour mot selon la proposition (vérifié : déjà le cas, ne pas toucher) ; autres entrées alignées sur les chapeaux des pages (textes ci-dessous) ; aucune entrée `/societe-numerique`.
- [ ] Aucun « — » ni « · » dans `public/llms.txt` ni dans `dist/llms-full.txt` (les « – » d'intervalle de dates et le « patient – pharmacien » de la page restent).
- [ ] `lepharmacien-fr.md` : « — » et « · » remplacés (l. 4, 10, 11, 28, 36), rien d'autre ne change.
- [ ] `Content-Type: text/markdown` toujours servi pour `/llms-full.txt` (FilesMatch `^llms(-full)?\.txt$` inchangé).
- [ ] Ligne de `CLAUDE.md` (l. 5) qui décrit `llms-full.txt` : préciser « généré au build ».
- [ ] Rien d'ajouté qui ne figure pas dans les pages ou l'issue ; aucune « Source » de l'issue citée.

## Tests à livrer (catalogue #10)

| ID | Fichier | Changement |
|---|---|---|
| T-BV-SPE-01 | `tests/test_dist.py` (`test_spe_01_llms`) | Garder l'existant. Ajouter : pour les deux fichiers, `"—"` et `"·"` absents ; pour `llms-full.txt`, `f"URL : {DOMAIN}/a-propos"` et `f"URL : {DOMAIN}/{slug}"` présents pour chaque `src/content/projects/*.md` (slug = stem), et `"<iframe"` absent. |
| T-BV-SPE-01 (source) | `tests/test_repo.py` | Nouveau `test_spe_01_llms_full_generated` : `public/llms-full.txt` n'existe pas (généré au build, #22). |
| T-BV-HTTP-06 | `tests/http_check.sh` | Inchangé : vérifie déjà `/llms-full.txt` en `text/markdown` (à faire passer sur Apache local). |
| T-BV-HTA-01 | `tests/test_dist.py` | Inchangé (FilesMatch llms). |
| Tous les autres | `tests/*`, html-validate, Playwright | Doivent rester verts (notamment LNK, HTML-01, A11Y sur `/a-propos`, BUD-01). |

Vérifié : `predeploy_guard.sh`, `README.md`, `legacy-urls.txt`, `test_content.py` (`rglob` sur `src/content` : `a-propos.md` ne contient pas de Kirbytext) ne supposent pas `public/llms-full.txt` ; rien à adapter hors CLAUDE.md l. 5.

## Fichiers

- Supprimer : `public/llms-full.txt`.
- Créer : `src/content/a-propos.md`, `src/pages/llms-full.txt.ts`.
- Modifier : `src/pages/a-propos.astro`, `public/llms.txt`, `src/content/projects/lepharmacien-fr.md`, `tests/test_dist.py`, `tests/test_repo.py`, `CLAUDE.md` (l. 5).

## Étapes

1. **lepharmacien-fr.md** (remplacements exacts, rien d'autre) :
   - l. 4 : `description: "Résopharma : LePharmacien.fr Product Manager & GTM, 2016 – 2018"`
   - l. 10 : `**Résopharma : LePharmacien.fr**  ` (garder les 2 espaces finaux)
   - l. 11 : `*Product Manager & GTM, 2016 – 2018*`
   - l. 28 : `### Périmètre : 4 phases` (même forme que pierre-fabre)
   - l. 36 : `- Analyse des flux de données : WebServices & API  `
2. **a-propos.md** : copier en markdown le contenu de `a-propos.astro` du `<h2>` jusqu'à la fin de la liste « Engagements & formations » (pas le paragraphe mailto). `## Senior Product Builder…`, `> Mi-builder…`, paragraphes, `### Parcours` etc. ; `<li><strong><a href="/x">T</a></strong> : …` devient `- **[T](/x)** : …` ; `<strong>T</strong>` devient `**T**` ; `<em><a href>…</a></em>` devient `*[…](…)*` ; `&amp;` devient `&`. Pas de front matter. Garder les apostrophes droites (smartypants est désactivé).
3. **a-propos.astro** : `import { Content } from '../content/a-propos.md';` et remplacer le HTML copié par `<Content />`, à la même place, avant le `<p><a href="mailto:…">` (garder l'obfuscation telle quelle).
4. **Endpoint** `src/pages/llms-full.txt.ts`, sur le modèle de `sitemap.txt.ts`. Une seule source pour le résumé : le lire dans `public/llms.txt` (`import llms from '../../public/llms.txt?raw'`, ligne `^> .*$`), pour qu'il ne puisse pas diverger. Esquisse :
   ```ts
   import { getCollection } from 'astro:content';
   import llms from '../../public/llms.txt?raw';
   import about from '../content/a-propos.md?raw';

   const SITE = 'https://benoitvinceneux.com';
   export async function GET() {
     const projects = (await getCollection('projects')).sort((a, b) => a.data.order - b.data.order);
     const pages = [{ title: 'À propos', slug: 'a-propos', body: about },
       ...projects.map((p) => ({ title: p.data.title, slug: p.id, body: p.body ?? '' }))];
     const head = `# Benoit Vinceneux\n\n${llms.match(/^> .*$/m)![0]}\n\nSite : ${SITE}\nEmail : benoitvinceneux@gmail.com\nLinkedIn : https://www.linkedin.com/in/benoitvinceneux/\nGitHub : https://github.com/benoitvx\n\n---`;
     const sections = pages.map((p) => `## ${p.title}\n\nURL : ${SITE}/${p.slug}\n\n${p.body.replace(/^<(\w+)[\s\S]*?<\/\1>$/gm, '').trim()}`);
     return new Response([head, ...sections].join('\n\n') + '\n');
   }
   ```
   Vérifier que le regex retire bien tout le bloc `<div>…</div>` de sigfox (aucun `<` résiduel) et rien d'autre. Si `?raw` sur `public/` pose problème au build, lire le fichier avec `node:fs` (pas de dépendance).
5. Supprimer `public/llms-full.txt` (`git rm`).
6. **public/llms.txt** : remplacer la ligne de résumé par le résumé validé. Ne pas toucher À propos, Services du Premier ministre, Présidence, Contact. Remplacer les autres entrées par (chapeau de la page d'abord, puis faits présents sur la page) :
   - `- [Curated Adventures](https://benoitvinceneux.com/curated-adventures): Fondateur, projet solo : 2021 à 2024. Guide pour trouver rapidement les meilleurs documentaires d'aventure outdoor (surf, escalade, snowboard, vélo) sur YouTube et Vimeo. Curation manuelle ; fin 2023, expérience reconstruite autour d'un GPT personnalisé ; des automatisations IA ont réduit de 80 % le temps passé sur les opérations quotidiennes. Démarche éco-responsable. https://curatedadventures.club`
   - `- [Sigfox](https://benoitvinceneux.com/sigfox): Sigfox : opérateur télécom 0G pour objets connectés. Product Manager. Sigfox Device Management System : 2019-2020, premier espace client B2B pour les grands comptes (~100 écrans, équipe de 2 à 10 développeurs, −50 % sur les délais de paiement clients, support facturation 10 min → 1 min). Sigfox Global Network Operation Center : 2016, data viz temps réel sur un mur de 12 écrans (−65 % de temps d'identification de l'origine d'une erreur réseau).`
   - `- [NotreSanté](https://benoitvinceneux.com/notresante): NotreSanté : startup e-santé. Cofondateur, CPO : 2016 à 2019. App iOS/Android pour familles avec enfants en bas âge, parcours croisés patient/professionnel de santé, hébergement HDS. 2019 : Trophée de la Citoyenneté et de la Solidarité, Conseil départemental de la Haute-Garonne ; 2018 : Prix de l'innovation, CCI Occitanie.`
   - `- [Ça Compte Pour Moi](https://benoitvinceneux.com/ca-compte-pour-moi): Compagnie Fiduciaire : 25ᵉ cabinet d'expertise-comptable indépendant français (CA 30 M€, 400 collaborateurs). Intrapreneur, Head of Product & GTM, premier profil produit : 2014 à 2017. Première offre d'expertise-comptable 100 % digitale en France. 1 M€ d'ARR un an après le lancement, rentable 3 ans après le lancement, 0 → 60 collaborateurs en 3 ans, 3 000 clients début 2019, top 3 du marché après 4 ans. Distinctions : Trophées Les Echos 2015 (Or Marketing digital, Or Stratégie de communication & Innovation de l'offre, Prix spécial du jury).`
   - `- [Pierre Fabre](https://benoitvinceneux.com/pierre-fabre): Laboratoires Pierre Fabre : Espace Pro B2B. 1ᵉʳ Product Manager B2B : 2014 à 2018. Réinventer la relation entre le Laboratoire et les pharmacies clientes : 80 % des pharmacies françaises ; 80 % d'entre elles se connectent au moins une fois par semaine. Centre névralgique relationnel (commande en ligne, gestion des factures, e-learning, e-merchandising, retours produits), premières fonctionnalités lancées en septembre 2015. 3 heures gagnées par semaine pour les pharmaciens utilisateurs.`
   - `- [Groupama](https://benoitvinceneux.com/groupama): J'ai accompagné Groupama en 2020 sur la création d'un extranet à destination des courtiers. UX / UI Designer. Dématérialisation du suivi administratif, tarifications en quelques clics ; environ 30 écrans, MVP validé et déployé en 2 mois.`
   - `- [LePharmacien.fr](https://benoitvinceneux.com/lepharmacien-fr): Résopharma : LePharmacien.fr. Product Manager & GTM, 2016 – 2018. Imaginer une plateforme de services pour simplifier la relation patient – pharmacien. Dispositif multi-canal (desktop, tablette et smartphone) : envoi d'ordonnance, Click & Collect, enrôlement des patients, pharmacie de garde partout en France 24h/24 et 7j/7. 10 ateliers de co-création, 250 wireframes réalisés, lancement en octobre 2018.`
   - `- [Toulouse Football Club](https://benoitvinceneux.com/toulouse-football-club): Je suis intervenu régulièrement auprès du club de Football de Toulouse entre 2014 & 2019. Pilotage opérationnel de la refonte du site institutionnel & de la boutique officielle, outil CRM sur mesure (site officiel, boutique, billetterie, réseaux sociaux), remise à plat des outils digitaux et des prestataires.`
   - `- [YANA.place](https://benoitvinceneux.com/yana-place): En 2018, j'achète avec 2 associés un espace de 220 m² en plein cœur de l'hypercentre de Toulouse, rénové entièrement en 6 mois : des bureaux fermés pour 4 à 6 personnes, tout équipés, à louer pour un an minimum. Rôle : cofondateur, designer et gestionnaire. 40 postes de travail, 750 K€ de dette bancaire pour l'achat et la rénovation, rentable dès la deuxième année, exploité par une équipe locale depuis 2021. https://yana.place`
   L'ordre des entrées reste celui d'aujourd'hui (navigation).
7. **CLAUDE.md** l. 5 : « …11 pages projet, `llms.txt` (tenu à la main) et `llms-full.txt` (généré au build depuis les pages). »
8. **Tests** : `test_dist.py` et `test_repo.py` comme dans le tableau.
9. **Vérification locale** : `npx astro build` ; `python3 -I -m unittest discover -s tests` ; `npx html-validate "dist/**/*.html"` ; Apache local + `BASE_URL=… bash tests/http_check.sh` (Content-Type de `/llms-full.txt`) ; `npx playwright test` ; `grep -c '[—·]' public/llms.txt dist/llms-full.txt` = 0.

## Points d'attention

- **Ids de titres** : le markdown rendu par Astro ajoute un `id` aux `<h2>`/`<h3>` de `/a-propos` (comme sur les pages projet). C'est la seule différence attendue avec `master` ; la QA la neutralise dans le diff. Tout autre écart (`&amp;` vs `&#x26;` compris, s'il apparaît, ce sont des entités équivalentes) est à justifier.
- **Hiérarchie dans llms-full** : le H2 tagline de `/a-propos` apparaît en `##` juste sous `## À propos`. Accepté (texte tel que la page) ; ne pas réécrire les niveaux.
- **Chemins relatifs** dans les corps (`/services-du-premier-ministre` dans a-propos.md) : laissés tels quels dans llms-full (SPE-01 ne vérifie que les URL absolues).
- `lepharmacien-fr` : la description change, donc la meta description et la carte d'accueil aussi : attendu (passe #23).
- Pas de nouvelle dépendance (D-BV4) ; `.nvmrc` reste `24`.
- Ne pas écrire de « Sources » de l'issue ni de détail d'hébergement.

## QA (à poster sur la PR)

1. Pour `/a-propos` et les 11 projets : texte visible du `<main>` de `dist/<page>.html` (balises retirées, sans H1, mailto ni `<dl>` Role/Website) comparé à la section de `dist/llms-full.txt` (markdown retiré), paragraphe par paragraphe ; lister tout écart (attendu : aucun hors iframe sigfox).
2. `<main>` de `dist/a-propos.html` vs celui de `master` (build de master dans un dossier temporaire), normalisé (espaces, attributs `id` des titres, entités) : aucun écart de texte, de lien ni de niveau de titre.
3. `dist/llms-full.txt` : 12 lignes `URL :`, ordre = navigation, résumé identique à celui de `llms.txt`, 0 « — », 0 « · », 0 `/societe-numerique`.
4. `curl -sI <apache local>/llms-full.txt` : `Content-Type: text/markdown; charset=utf-8`.
