# #50 [CONTENU] Services du Premier ministre : évaluation, code agentique et interventions

Branche : `feat/bv-50-spm-sections`. PR `Closes #50`.
Milestone M3. Dépendance : #23 (fermée). Ce qui fait foi : décision et réponses de Benoit du 24/10/2026 (commentaires de #50). Aucune nouvelle page ni URL, aucune dépendance ajoutée (D-BV4), ni réglage GitHub, ni secret, ni accès serveur.

## Critères d'acceptation

- [ ] `src/content/projects/services-du-premier-ministre.md` : `### Réalisations` remplacé par trois sections `### Évaluation des modèles d'IA`, `### Code agentique souverain`, `### Interventions` ; contexte, mission, approche, coordination des données et convictions inchangés.
- [ ] Évaluation : 100 questions, « un assistant juridique » sans nom de produit, aucun détail de méthode en plus, guide « rédigé », 10 % d'erreurs en moins par rapport au système actuel, auteur d'eval-ocr-htr, contributeur d'eval-transcript, aucun chantier en cours.
- [ ] Code agentique : éléments publics seulement, 30+ entretiens, « développé avec un agent de code », auteur d'etalab-ia/skills. Ni doctrine, ni document non publié, ni volumétrie, utilisateurs, bêta-testeurs, noms d'administrations, changement de socle.
- [ ] Interventions : Claude Code Paris 02 (février 2026, « MCP Leading the People », slides), atelier MCP ALLiaNCE du 20/01/2026 (slides), Sovereign Agents Blitz Hackathon 2026 (29/04/2026, sans lien), une phrase sur les talks dans l'administration (sans lieu ni date).
- [ ] Aucun lien hors de ceux de l'issue ; aucun « — », « · », « | ».
- [ ] `description` du front matter et entrée de `public/llms.txt` alignées sur la nouvelle page ; `dist/llms-full.txt` reprend la nouvelle version.

## Tests (catalogue #10)

- T-BV-HOST-01 : ajouter `guides.ia.numerique.gouv.fr` et `benoitvx.github.io` à `tests/allowed-hosts.txt`.
- Tous les autres (`tests/*`, html-validate, Playwright, BUD-01) restent verts.

## Fichiers

`src/content/projects/services-du-premier-ministre.md`, `public/llms.txt`, `tests/allowed-hosts.txt`, `tasks/todo.md`, `tasks/lessons.md`.

## Hors périmètre, à signaler

- `src/content/a-propos.md` l. 47 garde l'ancien titre *MCP Gateway for Open Government* (commande : tout va dans la page SPM).
- Paragraphe « supports / dsfr-slides-template » de la proposition non repris (absent du périmètre).
