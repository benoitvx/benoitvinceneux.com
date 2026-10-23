# #13 [CONTENU] a-propos : tagline unique, poste actuel, parcours et engagements à jour

Branche : `feat/bv-13-a-propos` (déjà créée). PR `Closes #13` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Décision de #2 en jeu : D-BV2 (aucun lien vers une page non publiée ; `/societe-numerique` absent). Ni réglage GitHub, ni secret, ni accès serveur. Rien à trancher : blocker vide.

Texte appliqué : version finale de #13 = proposition + réponses cochées du 22/10/2026 + commentaire de Benoit du 23/10/2026 :
- H1 reste « À propos » ; la nouvelle tagline remplace l'ancienne en H2 (option b) ;
- Data for Good : lien conservé vers `https://dataforgood.fr/projets/qui-paie-le-prix-du-changement-climatique`, posé sur le nom du projet ;
- Pierre Fabre : 80 % (tranché, ne pas reposer) ; section Open source affichée avec les 5 dépôts.
- `<title>` au format tranché dans #14 : « Nom : Benoit Vinceneux ».

## Critères d'acceptation

- [ ] `<title>` = `À propos : Benoit Vinceneux`.
- [ ] Meta description = `Benoit Vinceneux, product builder spécialisé dans le 0→1 des produits IA et data : fondateur, freelance pendant 10 ans, puis intrapreneur d'État à la DINUM.`
- [ ] H1 `À propos` inchangé ; H2 = `Senior Product Builder, AI × Data, Founder DNA`.
- [ ] Blockquote, pitch (3 §), parcours (13 entrées, dans l'ordre), convictions (3), stack, Open source (5 dépôts, H3, nouvelle), Engagements & formations (12 entrées en `<ul>`, dans l'ordre) : mot pour mot selon le bloc ci-dessous.
- [ ] Liens « (lien conservé) » : même URL qu'aujourd'hui, posée sur le nom de l'organisme ou du programme ; la mention « (lien conservé) » n'apparaît pas. Meetup Claude Code Paris 02, EIG, Wilco, Surfrider : sans lien.
- [ ] Parcours : 7 liens internes conservés (mêmes slugs), aucun ajouté.
- [ ] Lien mailto final et `<figure>` image : inchangés (octet pour octet).
- [ ] Aucun « — », « · », « | », « – » (ni `&mdash;`, `&middot;`, `&ndash;`) dans le texte visible, le `<title>`, la meta description de la page et dans la section À propos de `llms-full.txt`.
- [ ] `public/llms-full.txt`, section `## À propos` réécrite (texte de la page) ; résumé d'en-tête des deux fichiers llms **inchangé** (#22).
- [ ] `public/llms.txt` ligne 7 : `Profil, parcours, convictions, stack quotidienne, projets open source, engagements et formations.` Rien d'autre.
- [ ] Tous les tests du catalogue #10 verts.

## Tests T-BV-* (aucun nouveau test)

Le catalogue #10 n'attache aucun test aux tickets de contenu ; les PR de contenu précédentes (#42 à #46) n'ont touché aucun fichier de test. On suit ce précédent. Doivent rester verts :

| Test | Fichier |
|---|---|
| T-BV-BUILD-01, ART-01/02/04, INV-01..04, SPE-01..06, HTA-01/02, CSP-01, SEO-01 | `tests/test_dist.py` |
| T-BV-CONT-01/02/03 | `tests/test_content.py` |
| T-BV-LNK-01/02, T-BV-HOST-01 | `tests/test_links.py` |
| T-BV-A11Y-01 | `tests/test_a11y.py` |
| T-BV-BUD-01 | `tests/test_budget.py` |
| T-BV-ART-03, GUARD-01, IMP-* | `tests/test_repo.py`, `tests/test_guard.py`, `tests/test_import.py` |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` |
| T-BV-HTTP-* | `tests/http_check.sh` sur Apache local |
| T-BV-A11Y-02 | Playwright (`tests/e2e/`) |

SEO-01 vérifie l'unicité des `<title>` : « À propos : Benoit Vinceneux » n'entre en collision avec aucun.

## Fichiers

- Modifier `src/pages/a-propos.astro` (prop `title`, prop `description`, contenu entre le `<h2>` et le paragraphe mailto exclu).
- Modifier `public/llms-full.txt` (lignes 12 à 64, section `## À propos` seulement ; garder la ligne `---` qui la suit).
- Modifier `public/llms.txt` (ligne 7 seulement).
- Hors périmètre, ne pas toucher : `src/layouts/Base.astro` (la tagline de l'en-tête contient encore « · » : c'est #14), `.nvmrc` (reste 24), `tests/allowed-hosts.txt` (tous les hôtes utilisés y sont déjà : github.com, dataforgood.fr, www.linkedin.com, xpro.mit.edu, www.academy.thiga.co, www.academie-nr.org, laproductconf.com, www.lelaptop.com, iscparis.com ; à confirmer par test_links, ne rien ajouter par précaution).

## Contenu cible de `src/pages/a-propos.astro`

Props : `title="À propos : Benoit Vinceneux"`, `description="Benoit Vinceneux, product builder spécialisé dans le 0→1 des produits IA et data : fondateur, freelance pendant 10 ans, puis intrapreneur d'État à la DINUM."`.

Bloc qui remplace tout ce qui va du `<h2>` actuel au `</p>` de la liste des engagements (le `<p><a href="mailto:…">` qui suit reste tel quel) :

```html
<h2>Senior Product Builder, AI × Data, Founder DNA</h2>
<blockquote>
<p>Mi-builder, mi-hacker, mi-dealmaker : je fais passer la tech de l'idée à la production.</p>
</blockquote>
<p>Je suis Benoit Vinceneux, product builder spécialisé dans le 0→1, avec une ossature entrepreneuriale forte : fondateur, freelance pendant 10 ans, premier PM de plusieurs entreprises, puis intrapreneur d'État.</p>
<p>Aujourd'hui AI Product Lead à la Direction interministérielle du numérique (Services du Premier ministre), je pilote des initiatives IA pour l'État sur cinq fronts : l'ouverture des données publiques à l'IA, une stack de code agentique souveraine, les pratiques d'évaluation IA, la veille sur l'IA agentique, et le coaching produit des équipes de l'incubateur IA de l'État.</p>
<p>Je pense produit avec les yeux d'un fondateur (business case, adoption, go-to-market, partenariats), pas seulement roadmap et user stories. Je ne suis pas qu'un stratège : je prototype et je livre moi-même.</p>
<h3>Parcours</h3>
<ul>
<li><strong><a href="/services-du-premier-ministre">DINUM, Services du Premier ministre 🇫🇷</a></strong> : AI Product Lead ; depuis janvier 2026</li>
<li><strong><a href="/presidence-de-la-republique">Présidence de la République 🇫🇷</a></strong> : CPO Datalma ; octobre 2024 à décembre 2025 ; service pérennisé après 15 mois</li>
<li><strong>Freelance Product Lead</strong> : 2014 à 2024</li>
<li><strong><a href="/curated-adventures">🍿 Curated Adventures</a></strong> : fondateur ; 2021 à 2024</li>
<li><strong><a href="/yana-place">YANA.place</a></strong> : cofondateur ; depuis 2018</li>
<li><strong><a href="/sigfox">Sigfox</a></strong> : Product Manager ; 2016 et 2019-2020</li>
<li><strong><a href="/notresante">NotreSanté</a></strong> : cofondateur, CPO ; 2016 à 2019</li>
<li><strong>Résopharma / LePharmacien.fr</strong> : Product Manager &amp; GTM ; 2016 à 2018</li>
<li><strong>Laboratoires Pierre Fabre</strong> : 1ᵉʳ PM B2B ; 2014 à 2018 ; utilisé par 80 % des pharmacies françaises, dont 80 % se connectent au moins une fois par semaine</li>
<li><strong><a href="/ca-compte-pour-moi">Ça Compte Pour Moi</a></strong> : intrapreneur, premier profil produit ; 2014 à 2017 ; 1 M€ d'ARR un an après le lancement, 3 Trophées Les Echos</li>
<li><strong>Soregor / TGS France</strong> : Head of Product ; 2017 à 2019</li>
<li><strong>X-PRIME (aujourd'hui Mirum)</strong> : Project Director ; 2009 à 2014 ; portefeuille de 1,5 M€ par an, 40 % du CA de l'agence (Hermès, Inwi, PayPal, Airbus, The Kooples)</li>
<li><strong>Emakina</strong> : Project Manager ; 2008 à 2009 ; Libération, Panasonic, Havaianas, Novotel</li>
</ul>
<h3>Convictions</h3>
<ul>
<li>Les modèles se banalisent : le produit IA se gagne sur l'évaluation et la vitesse d'itération.</li>
<li>Livrer plutôt que pitcher : un prototype aligne mieux qu'un deck.</li>
<li>Un bon PM débloque le business, il ne gère pas seulement la roadmap.</li>
</ul>
<h3>Stack quotidienne</h3>
<p>Claude Code, OpenCode, MCP, Albert API, embeddings, LLM-as-a-judge, Python, React, Metabase, Dagster, dbt, Docker.</p>
<h3>Open source</h3>
<ul>
<li><a href="https://github.com/benoitvx/benoit-os">benoit-os</a> : mon OS d'agent personnel, avec skills, sous-agents, commandes, configurations MCP et installeur en une commande</li>
<li><a href="https://github.com/benoitvx/mcp-docs">mcp-docs</a> : serveur MCP pour Docs (La Suite numérique), 25 outils</li>
<li><a href="https://github.com/benoitvx/data-gouv-skill">data-gouv-skill</a> : skill Claude Code d'accès au catalogue de données ouvertes data.gouv.fr</li>
<li><a href="https://github.com/benoitvx/dvf-mcp-app">dvf-mcp-app</a> : MCP App qui affiche les prix immobiliers parisiens par arrondissement sur une carte (source DVF)</li>
<li><a href="https://github.com/benoitvx/dsfr-slides-template">dsfr-slides-template</a> : présentations web conformes au DSFR</li>
</ul>
<h3>Engagements &amp; formations</h3>
<ul>
<li>2026 : intervenant au meetup Claude Code Paris 02, <em>MCP Gateway for Open Government</em></li>
<li>2025 : Data for Good, saison 14, Product Lead du projet <em><a href="https://dataforgood.fr/projets/qui-paie-le-prix-du-changement-climatique">Qui paie le prix du changement climatique</a></em></li>
<li>2025 : <a href="https://www.linkedin.com/posts/aravind-srinivas-16051987_we-are-launching-a-perplexity-ai-business-activity-7294814157227315201-J51l/">Perplexity AI Fellowship</a>, sur sélection</li>
<li>Lauréat de la 7ᵉ promotion Entrepreneurs d'intérêt général</li>
<li>2024 : <a href="https://xpro.mit.edu/courses/course-v1:xPRO+AIPSx+R1/">MIT xPro</a>, <em>Designing and Building AI Products and Services</em></li>
<li>2023 : <a href="https://www.academy.thiga.co/en/training-lead-product">Thiga Academy</a>, <em>Lead Product Management</em></li>
<li>2023 : mentor de startups santé, Wilco</li>
<li>2020 : MOOC Numérique Responsable, <a href="https://www.academie-nr.org">Institut du Numérique Responsable</a></li>
<li>2019 à 2021 : <a href="https://laproductconf.com">La Product Conf</a>, co-organisateur de LPCx Toulouse</li>
<li>Depuis 2018 : bénévole Surfrider Foundation</li>
<li>2018 : <a href="https://www.lelaptop.com">Le Laptop</a>, méthodes de l'UX Design et du Design Thinking</li>
<li>2008 : <a href="https://iscparis.com">ISC Paris Business School</a>, Master Business &amp; IT</li>
</ul>
```

Les URL externes « (lien conservé) » sont copiées octet pour octet depuis la page actuelle (Perplexity : post linkedin.com ; Institut du Numérique Responsable : `https://www.academie-nr.org`, seul le libellé change ; ISC : ancre étendue au nom complet).

## Contenu cible de la section `## À propos` de `public/llms-full.txt`

Choix : texte de la page repris tel quel (1ʳᵉ personne), puisque #22 générera ce fichier depuis les pages. La ligne `---` qui suit la section est de la structure Markdown, pas un séparateur décoratif : on la garde.

```md
## À propos

URL : https://benoitvinceneux.com/a-propos

### Senior Product Builder, AI × Data, Founder DNA

Mi-builder, mi-hacker, mi-dealmaker : je fais passer la tech de l'idée à la production.

Je suis Benoit Vinceneux, product builder spécialisé dans le 0→1, avec une ossature entrepreneuriale forte : fondateur, freelance pendant 10 ans, premier PM de plusieurs entreprises, puis intrapreneur d'État.

Aujourd'hui AI Product Lead à la Direction interministérielle du numérique (Services du Premier ministre), je pilote des initiatives IA pour l'État sur cinq fronts : l'ouverture des données publiques à l'IA, une stack de code agentique souveraine, les pratiques d'évaluation IA, la veille sur l'IA agentique, et le coaching produit des équipes de l'incubateur IA de l'État.

Je pense produit avec les yeux d'un fondateur (business case, adoption, go-to-market, partenariats), pas seulement roadmap et user stories. Je ne suis pas qu'un stratège : je prototype et je livre moi-même.

### Parcours

- DINUM, Services du Premier ministre 🇫🇷 : AI Product Lead ; depuis janvier 2026
- Présidence de la République 🇫🇷 : CPO Datalma ; octobre 2024 à décembre 2025 ; service pérennisé après 15 mois
- Freelance Product Lead : 2014 à 2024
- 🍿 Curated Adventures : fondateur ; 2021 à 2024
- YANA.place : cofondateur ; depuis 2018
- Sigfox : Product Manager ; 2016 et 2019-2020
- NotreSanté : cofondateur, CPO ; 2016 à 2019
- Résopharma / LePharmacien.fr : Product Manager & GTM ; 2016 à 2018
- Laboratoires Pierre Fabre : 1ᵉʳ PM B2B ; 2014 à 2018 ; utilisé par 80 % des pharmacies françaises, dont 80 % se connectent au moins une fois par semaine
- Ça Compte Pour Moi : intrapreneur, premier profil produit ; 2014 à 2017 ; 1 M€ d'ARR un an après le lancement, 3 Trophées Les Echos
- Soregor / TGS France : Head of Product ; 2017 à 2019
- X-PRIME (aujourd'hui Mirum) : Project Director ; 2009 à 2014 ; portefeuille de 1,5 M€ par an, 40 % du CA de l'agence (Hermès, Inwi, PayPal, Airbus, The Kooples)
- Emakina : Project Manager ; 2008 à 2009 ; Libération, Panasonic, Havaianas, Novotel

### Convictions

- Les modèles se banalisent : le produit IA se gagne sur l'évaluation et la vitesse d'itération.
- Livrer plutôt que pitcher : un prototype aligne mieux qu'un deck.
- Un bon PM débloque le business, il ne gère pas seulement la roadmap.

### Stack quotidienne

Claude Code, OpenCode, MCP, Albert API, embeddings, LLM-as-a-judge, Python, React, Metabase, Dagster, dbt, Docker.

### Open source

- benoit-os (https://github.com/benoitvx/benoit-os) : mon OS d'agent personnel, avec skills, sous-agents, commandes, configurations MCP et installeur en une commande
- mcp-docs (https://github.com/benoitvx/mcp-docs) : serveur MCP pour Docs (La Suite numérique), 25 outils
- data-gouv-skill (https://github.com/benoitvx/data-gouv-skill) : skill Claude Code d'accès au catalogue de données ouvertes data.gouv.fr
- dvf-mcp-app (https://github.com/benoitvx/dvf-mcp-app) : MCP App qui affiche les prix immobiliers parisiens par arrondissement sur une carte (source DVF)
- dsfr-slides-template (https://github.com/benoitvx/dsfr-slides-template) : présentations web conformes au DSFR

### Engagements & formations

- 2026 : intervenant au meetup Claude Code Paris 02, « MCP Gateway for Open Government »
- 2025 : Data for Good, saison 14, Product Lead du projet « Qui paie le prix du changement climatique »
- 2025 : Perplexity AI Fellowship, sur sélection
- Lauréat de la 7ᵉ promotion Entrepreneurs d'intérêt général
- 2024 : MIT xPro, « Designing and Building AI Products and Services »
- 2023 : Thiga Academy, « Lead Product Management »
- 2023 : mentor de startups santé, Wilco
- 2020 : MOOC Numérique Responsable, Institut du Numérique Responsable
- 2019 à 2021 : La Product Conf, co-organisateur de LPCx Toulouse
- Depuis 2018 : bénévole Surfrider Foundation
- 2018 : Le Laptop, méthodes de l'UX Design et du Design Thinking
- 2008 : ISC Paris Business School, Master Business & IT
```

Les URL github.com ne sont pas des URL `https://benoitvinceneux.com/…` : SPE-01 ne les contrôle pas.

## Étapes

1. `src/pages/a-propos.astro` : props `title` et `description`, puis remplacement du bloc de contenu.
2. `public/llms-full.txt` : remplacement des lignes 12 à 64 (jusqu'à la ligne vide avant `---` exclue).
3. `public/llms.txt` : ligne 7.
4. `npm run build`.
5. `python3 -I -m unittest discover -s tests -p 'test_*.py'` puis `npx html-validate "dist/**/*.html"`.
6. `tests/http_check.sh` sur Apache local (port libre, `BASE_URL`).
7. `npx playwright test`.
8. Contrôles QA ci-dessous.

## Points d'attention

- Garder `&amp;` dans le HTML (« Engagements &amp; formations », « Product Manager &amp; GTM », « Master Business &amp; IT ») ; écrire le reste en UTF-8 brut (plus de `&eacute;`, `&Ccedil;`, `&mdash;`).
- Ponctuation du parcours copiée de l'issue : « : » puis « ; » ; trait d'union simple dans « 2019-2020 » ; ne pas normaliser en tiret demi-cadratin.
- Apostrophes droites, comme dans l'issue et la page actuelle.
- Présidence : « octobre 2024 » remplace « septembre 2024 » : voulu (aligné sur la page projet et `llms.txt`), pas une coquille.
- Ne rien ajouter qui ne figure pas dans l'issue ; ne jamais citer les « Sources » de l'issue.
- Ne pas toucher la tagline de `Base.astro` (#14) ni le résumé d'en-tête des fichiers llms (#22).

## QA (sur `dist/`)

- `grep -nE '—|–|·|\||&mdash;|&middot;|&ndash;' dist/a-propos.html` : 0 occurrence hors en-tête commun de `Base.astro` (aside « Présentation », traité par #14).
- Même grep sur la section `## À propos` de `dist/llms-full.txt` : 0 occurrence.
- Cohérence avec les pages projet (`public/llms.txt` lignes 8 à 18) : DINUM AI Product Lead depuis janvier 2026 ; Présidence octobre 2024 à décembre 2025 ; Curated Adventures 2021-2024 ; NotreSanté 2016-2019 ; Ça Compte Pour Moi 2014-2017 ; Pierre Fabre 2014-2018 et 80 % / 80 % ; LePharmacien.fr 2016-2018 ; YANA.place cofondateur depuis 2018 ; Sigfox 2016 et 2019-2020.
- Comparaison point par point du texte rendu avec l'issue : H1, H2, blockquote, 3 §, 13 entrées de parcours, 3 convictions, stack, 5 dépôts, 12 engagements en `<ul>`, mailto et `<figure>` inchangés, `<title>` et meta description.
