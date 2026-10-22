# #20 [CONTENU] yana-place : résultats et rôle

Branche : `feat/bv-20-yana-place` (déjà créée). PR `Closes #20` ouverte par l'orchestrateur.
Milestone M3. Dépendance : #9 (mergé). Aucune décision de #2 en jeu (contenu seul, ni dépendance, ni réglage, ni secret).
Texte appliqué : version finale de #20, réponses de Benoit du 22/10/2026 incluses :
- rénovation en **6 mois** ;
- montant **750 K€ de dette bancaire** publiable ;
- intitulé **« cofondateur »**.
#23 ne contient rien de spécifique à YANA.place (hors passe typographique transverse).

## Texte final à appliquer (issue #20, « Proposition »)

> En 2018, j'achète avec 2 associés un espace de 220 m² en plein cœur de l'hypercentre de Toulouse. Nous le rénovons entièrement en 6 mois pour proposer un nouveau produit sur le marché toulousain : des bureaux fermés pour 4 à 6 personnes, tout équipés, à louer pour un an minimum.
>
> **Rôle** : cofondateur, designer et gestionnaire
>
> **Résultats**
> - 40 postes de travail
> - 750 K€ de dette bancaire pour l'achat et la rénovation
> - Rentable dès la deuxième année
> - Exploité par une équipe locale depuis 2021
>
> **Site** : [yana.place](https://yana.place)

Meta description (donnée par l'issue, à appliquer telle quelle) :
`YANA.place : espace de bureaux de 220 m² à Toulouse, cofondé en 2018, rentable dès la deuxième année.`

## Critères d'acceptation

- [ ] Titre de page inchangé : `YANA.place` (donc `<title>` inchangé).
- [ ] Corps de la page = texte final ci-dessus, mot pour mot (« 220 m² », « cœur », « hypercentre », « 6 mois », « 4 à 6 personnes », « un an minimum »). Le gras actuel sur « un nouveau produit sur le marché toulousain » disparaît (absent de la proposition).
- [ ] Rôle affiché dans le corps : « **Rôle** : cofondateur, designer et gestionnaire » ; la coquille « Role » n'apparaît plus sur la page.
- [ ] Bloc « **Résultats** » avec exactement les 4 puces de l'issue, sans ajout.
- [ ] Lien « **Site** : [yana.place](https://yana.place) » dans le corps. URL cible inchangée (`https://yana.place`), seul le texte du lien passe de `https://yana.place` à `yana.place`. Aucun lien ajouté ni retiré.
- [ ] Meta description = celle de l'issue, telle quelle.
- [ ] Plus aucune trace sur la page de « 3 mois », « Co-fondateur », « 4 - 6 », « 220m2 », « coeur ».
- [ ] Aucun « — », « · », « | » dans le texte visible du `<main>` et la meta description de la page.
- [ ] URL, slug, `title`, `order`, `cover`, `images` inchangés.
- [ ] `public/llms.txt` et `public/llms-full.txt` : passages YANA.place alignés (étape 2).

## Tests (catalogue #10)

Aucun test à ajouter (l'issue n'en demande pas). La page n'est référencée que par des listes d'URL (`tests/test_dist.py` l. 27, `tests/legacy-urls.txt` l. 13, `tests/test_a11y.py` l. 7) et l'hôte `yana.place` est déjà dans `tests/allowed-hosts.txt` l. 19. Tests qui doivent rester verts sans modification :

| ID | Fichier | Lien avec #20 |
|---|---|---|
| T-BV-BUILD-01 | `npx astro build` + `tests/test_dist.py` | build de la page modifiée |
| T-BV-CONT-01, T-BV-CONT-02, T-BV-CONT-03 | `tests/test_content.py` | front matter (`description` non vide, sur une seule ligne `description: "..."`), `cover`/`images` existants, pas de KirbyText |
| T-BV-SPE-01 | `tests/test_dist.py` | URL du domaine dans `llms*.txt` : `/yana-place` déjà en 200, n'en ajouter aucune |
| T-BV-SEO-01 | `tests/test_dist.py` | canonical, meta description non vide, `<title>` unique |
| T-BV-LNK-01, T-BV-LNK-02, T-BV-HOST-01 | `tests/test_links.py` | lien `https://yana.place` conservé (déplacé du `<dl>` au corps), hôte déjà autorisé |
| T-BV-HTML-01 | `npx html-validate "dist/**/*.html"` (+ `tests/test_repo.py`) | HTML de la page (liste dans le corps) |
| T-BV-HTTP-01 | `tests/http_check.sh` sur Apache local servant `dist/` | `/yana-place.html`, page et `llms*.txt` en 200 |
| T-BV-A11Y-01, T-BV-A11Y-02 | `tests/e2e/a11y.spec.ts`, `tests/test_a11y.py` | axe sur `/yana-place` (nouvelle mise en page sans colonne `<dl>`) |
| Autres (ART, INV, SPE-02..06, HTA, CSP, BUD, DEP, WF, GUARD, IMP) | `tests/*.py` | non concernés, doivent rester verts |

Commande : `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html"`, puis Apache local + `BASE_URL=http://127.0.0.1:<port> bash tests/http_check.sh`, puis `npx playwright test`.

## Fichiers modifiés (3, rien à créer)

1. `src/content/projects/yana-place.md` : `description`, suppression de `role` et `website`, corps réécrit.
2. `public/llms.txt` : ligne 18 seulement.
3. `public/llms-full.txt` : section `## YANA.place` seulement (l. 407 à 414).

Hors périmètre (ne pas toucher) :
- `src/pages/[slug].astro` et `src/content.config.ts` : le bloc `<dl>` Role/Website et les champs `role`/`website` du schéma deviennent inutilisés (YANA.place était la seule page à s'en servir). Les laisser : diff limité au contenu, rendu des autres pages inchangé. Nettoyage possible plus tard sur demande.
- `src/pages/a-propos.astro` l. 31 (« founder, CEO ») et `public/llms-full.txt` l. 32 (parcours de l'à propos) : relèvent de #13 (en attente) et #22.
- Gabarit et format du `<title>` (#14), reste de `llms*.txt` (#22), `tests/allowed-hosts.txt`.

## Étapes

### 1. Page projet `src/content/projects/yana-place.md`

- Front matter :
  - `description: "YANA.place : espace de bureaux de 220 m² à Toulouse, cofondé en 2018, rentable dès la deuxième année."`
  - supprimer les lignes `role: ...` et `website: ...` (le rôle et le site passent dans le corps, comme dans la proposition ; sinon le lien et le rôle apparaîtraient deux fois, avec le libellé « Role » du gabarit) ;
  - `title`, `order`, `cover`, `images` inchangés ; pas de `textposition` (inchangé).
- Corps, remplacé intégralement par :

```
En 2018, j'achète avec 2 associés un espace de 220 m² en plein cœur de l'hypercentre de Toulouse. Nous le rénovons entièrement en 6 mois pour proposer un nouveau produit sur le marché toulousain : des bureaux fermés pour 4 à 6 personnes, tout équipés, à louer pour un an minimum.

**Rôle** : cofondateur, designer et gestionnaire

**Résultats**

- 40 postes de travail
- 750 K€ de dette bancaire pour l'achat et la rénovation
- Rentable dès la deuxième année
- Exploité par une équipe locale depuis 2021

**Site** : [yana.place](https://yana.place)
```

  (ligne vide entre « **Résultats** » et la liste pour un rendu Markdown sûr ; saut de ligne final.)

### 2. Fichiers LLM (mêmes faits, aucun ajout)

- `public/llms.txt` l. 18 :
  `- [YANA.place](https://benoitvinceneux.com/yana-place): Cofondateur, designer et gestionnaire (depuis 2018). Espace de 220 m² en hypercentre de Toulouse, rénové en 6 mois, bureaux fermés tout équipés (4 à 6 personnes, location d'un an minimum). 40 postes de travail, 750 K€ de dette bancaire pour l'achat et la rénovation, rentable dès la deuxième année, exploité par une équipe locale depuis 2021. https://yana.place`
- `public/llms-full.txt`, section `## YANA.place` (URL et Site inchangés) :
  - l. 412 : `Cofondateur, designer et gestionnaire (depuis 2018).`
  - l. 414 : `> « En 2018, j'achète avec 2 associés un espace de 220 m² en plein cœur de l'hypercentre de Toulouse. Nous le rénovons entièrement en 6 mois pour proposer un nouveau produit sur le marché toulousain : des bureaux fermés pour 4 à 6 personnes, tout équipés, à louer pour un an minimum. »`
  - ajouter après, séparé par une ligne vide :
    ```
    Résultats :
    - 40 postes de travail
    - 750 K€ de dette bancaire pour l'achat et la rénovation
    - Rentable dès la deuxième année
    - Exploité par une équipe locale depuis 2021
    ```
  - garder une seule ligne vide avant `---`.

### 3. Vérifications

- Build + tests (commande ci-dessus), tous verts.
- `dist/yana-place.html` : corps conforme au texte final, meta description de l'issue, lien `href="https://yana.place"` présent une seule fois, plus de `<dt>Role</dt>`, aucun « — », « · », « | » dans `<main>` ni la meta.
- `grep -n "3 mois\|Co-fondateur\|4 - 6" src/content/projects/yana-place.md public/llms.txt public/llms-full.txt` : aucun résultat.
- Vérifier visuellement la page (build local) : sans colonne `<dl>`, la mise en page `ld-row` garde le texte à gauche et les images à droite.

## Points d'attention

- Ne rien ajouter qui ne soit dans l'issue : pas de chiffre d'affaires, taux d'occupation ni nom d'associé ; « depuis 2018 » dans `llms*.txt` est repris de l'existant.
- `description` reste sur une seule ligne entre guillemets doubles (T-BV-CONT).
- Ne pas citer les sources de l'issue (CV, profil LinkedIn, liste d'expériences) sur le site.
- Commit : `content: YANA.place, rénovation en 6 mois, résultats et rôle de cofondateur (#20)`.
