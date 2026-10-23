# benoitvinceneux.com - CLAUDE.md

## Projet

Site portfolio de Benoit Vinceneux : accueil, page « à propos », 11 pages projet, `llms.txt` (tenu à la main) et `llms-full.txt` (généré au build depuis les pages).

- **Aujourd'hui :** `dist/`, construit par Astro, est servi par Apache. Chaque push sur `master` le déploie (`.github/workflows/deploy.yml`, rsync `--delete-after`) si le job `test` passe. L'ancien site Kirby n'existe plus que dans le tag `snapshot-kirby` : le retour arrière passe par ce tag (README, section « Rollback »).
- **Migration Astro terminée** (bascule #7, nettoyage #9). Pilotage #1, décisions #2, catalogue des tests CI #10. **En cours :** milestone `M3 Contenus` (issues `[CONTENU]`, synthèse #23).

## Stack cible

- Astro, seule dépendance de `dependencies`. En `devDependencies`, seulement `@playwright/test`, `@axe-core/playwright` et `html-validate`, à des versions exactes (décision D-BV4). Toute autre dépendance : demander à Benoit.
- `build.format: 'file'`, sortie dans `dist/`, déployée par rsync.
- Tests : Python 3 stdlib (`unittest`, lancé en `python3 -I`) sur `dist/`, et Playwright pour l'accessibilité. Catalogue des tests : issue #10. Le déploiement n'a lieu que si le job `test` passe.
- Pas de Tailwind, pas d'intégration Astro, pas d'`astro:assets`. Les CSS et les URL du snapshot sont reprises telles quelles : ce n'est pas une refonte.

## Méthode de travail (sessions autonomes)

Un ticket = une issue GitHub = une branche `feat/bv-0x-description` = une PR qui contient `Closes #n`. Les tickets se traitent dans l'ordre des dépendances (#1). Pour chaque ticket, dispatcher des agents spécialisés, un workflow par ticket :

1. **Tech lead (planification) :**
   - lit l'issue, ses dépendances, les décisions de #2 et les tests du catalogue #10 qui la concernent ;
   - écrit le plan dans `tasks/todo.md` ;
   - s'arrête si une décision n'est pas tranchée.
2. **Développeur :** implémente le plan et les tests du catalogue liés au ticket, jusqu'à ce que le build et les tests passent en local.
3. **Relecteurs, en parallèle et indépendants,** chargés de trouver ce qui ne va pas :
   - conformité aux critères d'acceptation ;
   - simplicité : le moins de code et de fichiers possible ;
   - sécurité (skill `securite-developpement`) : en-têtes, `.htaccess`, secrets, workflow CI ;
   - pour les tickets de contenu : parité des URL et SEO.
4. **Correction et nouvelle revue,** 3 tours au plus. Au-delà : stop et rapport.
5. **QA :** déroule la section « Recette (QA) » de l'issue, coche ce qui est vérifiable en local et poste le résultat en commentaire de la PR.
6. **Intégration :** CI verte (`gh pr checks --watch`), squash-merge, puis vérification que le site en ligne répond toujours (200 sur `/`, une page projet et `/a-propos`). Mettre à jour la checklist de #1 et `tasks/lessons.md`.

## Garde-fous

S'arrêter et demander à Benoit avant :
- de merger le ticket de bascule (#7) ou tout ticket du milestone M2 : c'est la mise en production d'Astro ;
- tout réglage GitHub (secrets, environnements, protection de branche) ;
- toute action qui demande un secret, un accès au serveur ou un rsync manuel ;
- toute décision absente de #2.

Interdits :
- Ne jamais modifier les secrets `DEPLOY_*` ni la cible du rsync.
- Pas de `push --force`, pas de réécriture d'historique, pas de push sur le remote `framagit`.
- Dépôt public : ne jamais écrire dans le code, les commits, les PR ou les issues de nom d'hôte, d'utilisateur SSH, de chemin serveur ni de détail sur l'hébergement.
- Ne jamais versionner de fichier `.php` (le PHP est bloqué par le `.htaccess`).
- Sur cette machine, utiliser `env -u GH_TOKEN gh` pour toute commande `gh`.

## Conventions

- Commits : `type: Description en français` (feat, fix, docs, refactor, test, chore, style, content).
- Textes du site : pas de séparateurs décoratifs (« — », « · », « | ») ; attribution honnête des réalisations.
- Accessibilité : `alt` sur les images informatives, navigation clavier, `title` sur les iframes.
