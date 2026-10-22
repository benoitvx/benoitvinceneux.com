# #19 [CONTENU] groupama : année de mission, lien InVision

Branche : `feat/bv-19-groupama` (déjà créée). PR `Closes #19` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Aucune décision de #2 en jeu (contenu seul, ni dépendance, ni réglage, ni secret).
Texte appliqué : version finale de #19, réponses de Benoit du 22/10/2026 incluses :
- année **2020** confirmée ;
- lien InVision : le domaine `projects.invisionapp.com` ne répond plus, **lien supprimé** ;
- #23 ne contient rien de spécifique à Groupama (hors passe typographique transverse).

## Critères d'acceptation

- [ ] Titre de page inchangé : `Groupama` (donc `<title>` inchangé).
- [ ] Chapeau (1re ligne du corps) : « J'ai accompagné **Groupama** en 2020 sur la création d'un extranet à destination des courtiers. » Seul ajout : « en 2020 » après `**Groupama**` ; gras et saut de ligne Markdown final (deux espaces) conservés.
- [ ] Rôle : « Je suis intervenu sur ce projet en tant qu'**UX / UI Designer**. » (élision « qu' » et point final ajoutés ; gras conservé).
- [ ] Ligne `[Voir quelques écrans du produit](https://projects.invisionapp.com/share/MNWVV2MQT6A#/screens)` supprimée, avec la ligne vide qui la précède (le fichier finit sur la dernière tâche + saut de ligne).
- [ ] Reste du corps inchangé à l'octet : phrase plateforme, « **Nous sommes parvenus à valider et déployer le MVP en 2 mois.** », « Tâches réalisées » et ses 3 puces.
- [ ] Meta description réalignée (l'issue n'en donne pas ; seul fait modifié : l'année ; aucun séparateur présent) :
  `J'ai accompagné Groupama en 2020 sur la création d'un extranet à destination des courtiers. La plateforme permet aux courtiers de dématérialiser le suivi administratif…`
- [ ] Plus aucune trace sur la page de « InVision », « invisionapp », « Voir quelques écrans ».
- [ ] Aucun « — », « · », « | » dans le texte visible du `<main>` et la meta description de la page.
- [ ] URL, slug, `title`, `order`, `textposition`, `cover`, `images` inchangés. Aucun lien ajouté ; un seul lien externe retiré (demandé par l'issue).
- [ ] `public/llms.txt` et `public/llms-full.txt` : passages Groupama alignés (étape 2).

## Tests (catalogue #10)

Aucun test à ajouter (l'issue n'en demande pas). La page n'est référencée que par des listes d'URL (`tests/test_dist.py` l. 17, `tests/legacy-urls.txt` l. 3, `tests/test_a11y.py` l. 7, `tests/http_check.sh` l. 33). Tests qui doivent rester verts sans modification :

| ID | Fichier | Lien avec #19 |
|---|---|---|
| T-BV-BUILD-01 | `npx astro build` + `tests/test_dist.py` | build de la page modifiée |
| T-BV-CONT-01, T-BV-CONT-02, T-BV-CONT-03 | `tests/test_content.py` | front matter (`description` non vide, sur une seule ligne `description: "..."`), `cover`/`images` existants, pas de KirbyText |
| T-BV-SPE-01 | `tests/test_dist.py` | URL du domaine dans `llms*.txt` : `/groupama` déjà en 200, n'en ajouter aucune |
| T-BV-SEO-01 | `tests/test_dist.py` | canonical, meta description non vide, `<title>` unique |
| T-BV-LNK-01, T-BV-LNK-02, T-BV-HOST-01 | `tests/test_links.py` | aucun lien ni hôte nouveau ; HOST-01 ne vérifie que les hôtes présents, une entrée inutilisée de la liste ne casse rien |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` (+ `tests/test_repo.py`) | HTML de la page |
| T-BV-HTTP-01 | `tests/http_check.sh` sur Apache local servant `dist/` | `/groupama.html`, page et `llms*.txt` en 200 |
| T-BV-A11Y-01, T-BV-A11Y-02 | `tests/e2e/a11y.spec.ts`, `tests/test_a11y.py` | axe sur `/groupama` |
| Autres (ART, INV, SPE-02..06, HTA, CSP, BUD, DEP, WF, GUARD, IMP) | `tests/*.py` | non concernés, doivent rester verts |

Commande : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html"`, puis Apache local + `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh`, puis `npx playwright test`.

## Fichiers modifiés (3, rien à créer)

1. `src/content/projects/groupama.md` : `description`, chapeau, rôle, suppression du lien InVision.
2. `public/llms.txt` : ligne 15 seulement.
3. `public/llms-full.txt` : section `## Groupama` seulement (l. 373 à 389).

Hors périmètre (ne pas toucher) : `tests/allowed-hosts.txt` (l'issue n'impose pas d'y toucher ; `projects.invisionapp.com` y reste, inutilisé, sans effet sur les tests ; nettoyage possible plus tard sur demande) ; gabarit et format du `<title>` (#14) ; reste de `llms*.txt` (#22).

## Étapes

### 1. Page projet `src/content/projects/groupama.md`

- Front matter : remplacer seulement `description` par
  `description: "J'ai accompagné Groupama en 2020 sur la création d'un extranet à destination des courtiers. La plateforme permet aux courtiers de dématérialiser le suivi administratif…"`
- Corps, l. 1 : `J'ai accompagné **Groupama** en 2020 sur la création d'un extranet à destination des courtiers.  ` (deux espaces finaux conservés).
- Rôle : `Je suis intervenu sur ce projet en tant qu'**UX / UI Designer**.`
- Supprimer la ligne vide + la ligne `[Voir quelques écrans du produit](...)` en fin de fichier ; garder un saut de ligne final.

### 2. Fichiers LLM (mêmes faits, aucun ajout)

- `public/llms.txt` l. 15 :
  `- [Groupama](https://benoitvinceneux.com/groupama): UX/UI Designer (2020). Extranet courtiers : dématérialisation du suivi administratif, tarification en quelques clics. ~30 écrans, MVP validé et déployé en 2 mois.`
  (année ajoutée au format des autres lignes, « — » remplacé par « : » comme pour Sigfox en #18).
- `public/llms-full.txt`, section `## Groupama` :
  - l. 379 : `Accompagnement de Groupama en 2020 sur la création d'un extranet à destination des courtiers. La plateforme ...` (reste inchangé) ;
  - supprimer la ligne `Ressource : écrans produit sur InVision (https://projects.invisionapp.com/share/MNWVV2MQT6A).` et la ligne vide qui la précède, pour garder une seule ligne vide avant `---`.

### 3. Vérifications

- Build + tests (commande ci-dessus), tous verts.
- `grep -n -i invision src/ public/` : plus aucun résultat.
- `dist/groupama.html` : chapeau avec « en 2020 », « qu'UX / UI Designer. », pas de lien InVision, meta description à jour, aucun « — », « · », « | » dans `<main>` ni la meta.

## Points d'attention

- Ne rien ajouter qui ne soit dans l'issue : pas de rôle, résultat ni lien nouveau ; « MVP ... en 2 mois » conservé tel quel (formulation actuelle de la page).
- `description` reste sur une seule ligne entre guillemets doubles (T-BV-CONT).
- Ne pas citer la source de l'issue (CV) sur le site.
- Commit : `content: Groupama, année 2020, élision du rôle et suppression du lien InVision (#19)`.
