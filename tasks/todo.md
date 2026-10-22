# #9 [BV-07] Nettoyage : suppression du snapshot `site/`

Branche : `feat/bv-07-nettoyage-snapshot` (déjà créée). PR `Closes #9` ouverte par l'orchestrateur.
Décision de Benoit du 22/10/2026 (commentaire de #9) : fait maintenant, sans attendre #8 ; le prérequis « #8 fermé » de la recette est ignoré.
Dépendances : #7 (bascule) mergé, `master` déploie `dist/`. Décision liée (#2) : D-2 (observation avant suppression, levée par la décision du 22/10). Décisions du 22/10 appliquées : HSTS posé par le serveur (absent de `public/.htaccess`, plus de passage à 31536000), pas d'environnement GitHub.
Tag annoté `snapshot-kirby` : **déjà créé et poussé** par l'orchestrateur sur `ff18679` (dernier commit de `master` contenant `site/`). Ne pas le recréer ni le déplacer.
Inchangés : `package.json`, lockfile, `.nvmrc` (24), `public/`, `src/`, secrets `DEPLOY_*`, cible et source rsync (`dist/`), job `test`, `scripts/import_kirby.py`.

## Critères d'acceptation (issue #9)

- [ ] Le tag `snapshot-kirby` existe sur le dépôt distant (fait : `git ls-remote --tags origin snapshot-kirby`)
- [ ] CI verte sans `site/`
- [ ] Supprimés : `site/`, `tests/test_parity.py`, `tests/parity-allowlist.json`
- [ ] README : retour arrière via le tag
- [ ] Demande de Benoit : CLAUDE.md à jour dans la même PR

## Tests (catalogue #10)

| ID | Action | Fichier |
|---|---|---|
| T-BV-CSS-01 | **retiré** (`test_css_01_static_identical`) | `tests/test_dist.py` |
| T-BV-PAR-00 à 04 | **retirés** (fichier supprimé) | `tests/test_parity.py` |
| T-BV-PAR-05 | **retiré** (`test_par_05_media_identical`) | `tests/test_dist.py` |
| T-BV-ART-03 | modifié : `.htaccess` versionné seulement dans `public/` (plus d'exception `site/.htaccess`) | `tests/test_repo.py` |
| T-BV-HTML-01 | contrôle « chaque règle à `off` de `.htmlvalidate.json` a une entrée `html-validate` justifiée » repris de `test_par_00` (qui le portait) dans `test_html_01_exceptions` ; même ID, pas de nouvel identifiant | `tests/test_repo.py` |
| T-BV-A11Y-02 | inchangé, lit `tests/exceptions.json` au lieu de `tests/parity-allowlist.json` | `tests/e2e/a11y.spec.ts` |
| T-BV-WF-04 | retirer la seule assertion `assertNotIn("site/", job)` (la source `dist/` reste exigée) | `tests/test_repo.py` |

Rien d'autre n'est retiré : les 48 autres tests de #10 restent verts.

## Fichiers

1. `git rm -r site/ tests/test_parity.py`.
2. `git mv tests/parity-allowlist.json tests/exceptions.json`, puis garder seulement les 4 entrées encore utiles :
   les 2 `html-validate` (`long-title`, `no-inline-style`) et les 2 `axe` (iframe YouTube de sigfox, fichier Google).
   Retirer les entrées `PAR-01`, `PAR-02` et `D-3` : elles déclaraient des écarts au snapshot, qui n'existe plus. Les corrections D-3 restent exigées par T-BV-A11Y-01 et T-BV-SPE-06, et la décision reste tracée dans #2.
   **Pourquoi ce choix :** `.htmlvalidate.json` n'accepte pas de commentaires (JSON) et les exceptions servent à deux outils (html-validate, axe) ; un seul petit fichier sous un nom neutre, au même format `{test, page, motif, pourquoi}`, est le plus court et garde chaque exception justifiée. Le renommage satisfait le scénario 2 (`git ls-files tests/parity-allowlist.json` vide).
3. `tests/e2e/a11y.spec.ts` : chemin `tests/parity-allowlist.json` → `tests/exceptions.json` (ligne 6) et le mot « allowlist » du commentaire/message si besoin (optionnel).
4. `tests/test_dist.py` : supprimer `assert_same_tree`, `test_css_01_static_identical`, `test_par_05_media_identical` et `import filecmp` (plus utilisé). Ne pas toucher `parse`, `norm`, `pages`, `refs` (utilisés par `test_links`, `test_a11y`, `test_budget`, CSP).
5. `tests/test_repo.py` :
   - ART-03 : `self.assertEqual(f, "public/.htaccess", f".htaccess versionné hors public/ : {f}")` ;
   - WF-04 : supprimer la ligne `assertNotIn("site/", job, ...)` ;
   - ajouter `test_html_01_exceptions` (≈ 6 lignes, reprises de `test_par_00`) : `tests/exceptions.json` est du JSON valide ; chaque entrée a `test`, `page`, `motif`, `pourquoi` non vides et `test` ∈ {`html-validate`, `axe`} ; ensemble des règles à `"off"` de `.htmlvalidate.json` = ensemble des `motif` des entrées `html-validate`. (Le sélecteur mort `axe` est déjà vérifié dans `a11y.spec.ts`.)
6. `README.md` : retirer la ligne `site/` ; réécrire « Rollback » (voir ci-dessous).
7. `CLAUDE.md` (seulement ces phrases) :
   - l. 7 « Aujourd'hui : `site/` est un snapshot… » → « `dist/`, construit par Astro, est servi par Apache. Chaque push sur `master` le déploie (`.github/workflows/deploy.yml`, rsync `--delete-after`) si le job `test` passe. L'ancien site Kirby n'existe plus que dans le tag `snapshot-kirby` : le retour arrière passe par ce tag (README). » ;
   - l. 13 « déployée à la place de `site/` après la bascule » → « déployée par rsync » ;
   - l. 45 « Tant que #7 n'est pas mergé, le job de déploiement doit continuer à publier `site/`. » → supprimée, sans remplacement (aucune règle ajoutée).
   - Rien d'autre (la ligne « En cours : migration… » et « Stack cible » restent).
8. `tasks/todo.md` (ce fichier).

## README : section « Rollback » (texte cible, à reprendre tel quel)

**Régression Astro (cas normal)** : inchangé, 3 étapes (`git revert <sha>` sur une branche, PR, merge quand `test` est vert, vérifier 200 sur `/`, une page projet, `/a-propos`).

**Retour à l'ancien site Kirby** (le snapshot n'est plus que dans le tag `snapshot-kirby`) :
1. Sur une branche partie de `master`, dans `.github/workflows/deploy.yml`, job `deploy`, remplacer la ligne `- run: npx astro build` par :
   `- run: git fetch --depth 1 origin tag snapshot-kirby && rm -rf dist && mkdir dist && git archive snapshot-kirby:site | tar -x -C dist`
2. PR vers `master`, merger quand `test` est vert : le job `deploy` publie le snapshot (mêmes garde-fous, même rsync). Le smoke peut être rouge (en-têtes et pages du snapshot différents de ceux attendus) : c'est attendu, le site est en ligne.
3. Vérifier 200 sur `/`, une page projet et `/a-propos`. Pour revenir à Astro : `git revert` de ce commit.

Pourquoi cette procédure et pas `git checkout snapshot-kirby -- site/` + source rsync `site/` :
- le commit taggé (`ff18679`) déploie déjà `dist/` : restaurer `site/` ne suffit pas, il faut changer ce que le job publie ;
- versionner à nouveau `site/` remet `site/.htaccess` dans le dépôt : T-BV-ART-03 devient rouge, le check `test` exigé par la protection de `master` bloque le merge ;
- changer la source rsync en `site/` casse T-BV-WF-04 (source `dist/` exigée) : même blocage.
  Remplir `dist/` depuis le tag dans le seul job `deploy` ne touche ni au dépôt ni aux tests, et garde rsync, garde-fous et cible inchangés.
- Vérifié en local le 22/10 (clone `--depth 1` jetable) : `git fetch --depth 1 origin tag snapshot-kirby` fonctionne sans identifiants (dépôt public, `persist-credentials: false`), `git archive` restitue les 14 `.html` + `.htaccess`, `predeploy_guard.sh dist` → OK (aucun lien symbolique ni `.php` dans le snapshot).

## Ordre des étapes

1. Suppressions et renommage (étapes 1-2), mise à jour des tests (3-5).
2. `npx astro build && python3 -I -m unittest discover -s tests -v && npx html-validate "dist/**/*.html" && npx playwright test` : tout vert.
3. README, CLAUDE.md.
4. Contrôle scénario 2 : `git ls-files site tests/test_parity.py tests/parity-allowlist.json` vide ; `grep -rn 'site/' .github tests README.md` → aucune ligne hors mentions du tag (`snapshot-kirby:site` ne contient pas `site/`).
5. Un commit : `chore: Supprime le snapshot Kirby site/ et les tests de parité` (ou deux : `chore` + `docs`).

## Recette (QA), à dérouler (scénarios 1 à 6, prérequis #8 ignoré)

1. `git ls-remote --tags origin snapshot-kirby` présent ; `git ls-tree snapshot-kirby site/ | head` non vide.
2. Voir étape 4 ci-dessus.
3. CI du ticket : `test` vert sur la PR ; après merge, `deploy` + smoke verts (orchestrateur).
4. `curl -sI https://benoitvinceneux.com/` : `Strict-Transport-Security` avec `max-age` ≥ 16000000.
5. Smoke complet (`BASE_URL=https://benoitvinceneux.com HSTS_MIN_AGE=16000000 bash tests/http_check.sh`) + 200 sur `/`, une page projet, `/a-propos`.
6. Rollback à blanc dans un **clone jetable** du scratchpad (`git clone` du dépôt, `git switch -c rollback-test` depuis la branche du ticket ; jamais dans le dépôt de travail : `git fetch --depth 1` y écrirait `.git/shallow`). Appliquer l'étape 1 du README telle qu'écrite, exécuter la commande `run:` remplacée, puis `bash tests/predeploy_guard.sh dist` et `python3 -I -m unittest discover -s tests -p test_repo.py` (WF-04 et ART-03 restent verts). Rien n'est poussé ; `rm -rf` du clone ensuite.

## Points d'attention

- Ne pas recréer/déplacer le tag ; ne pas toucher `DEPLOY_*`, la cible ni la source rsync.
- `tests/fixtures/kirby/site/` est une fixture de `test_import.py` (T-BV-IMP-04), pas le snapshot : **ne pas la supprimer**. `git rm -r site/` à la racine seulement.
- `scripts/import_kirby.py` garde `--site` par défaut `site` : script ponctuel (#5) hors périmètre du scénario 2 ; pour le relancer, extraire `site/` depuis le tag et passer `--site`. Non modifié pour garder le diff minimal.
- #10 cite encore `tests/parity-allowlist.json` comme fichier d'exceptions : le signaler dans la description de la PR (nouveau nom `tests/exceptions.json`, clés réservées `html-validate` et `axe` inchangées). Ne pas éditer #10 sans accord.
- Le job `deploy` après merge reste vert : `dist/` a 13 pages HTML ≥ 13 attendues par le garde-fou ; rien ne change dans ce job.
- Pas de nouvelle dépendance, pas de nouvel ID de test, pas de nouveau fichier hors renommage.

## Développement (22/10)

- Fait selon le plan, sans écart. `tests/exceptions.json` : 4 entrées (2 `html-validate`, 2 `axe`).
- Local : `npm ci`, `npx astro build`, unittest 47 tests OK (53 avant : -5 PAR-00 à 04, -2 CSS-01/PAR-05, +1 `test_html_01_exceptions`), `html-validate` OK, `http_check.sh` OK sur Apache local (port 8099 : le 8080 est pris sur ce poste), Playwright 14/14.
- Commande de retour arrière du README essayée dans un clone `--depth 1` jetable : 14 `.html`, `predeploy_guard.sh dist` OK.
