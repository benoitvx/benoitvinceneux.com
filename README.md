# benoitvinceneux.com

Site statique servi par Apache.

- `site/` : snapshot statique de l'ancien site Kirby (21/10/2026), en attendant la version Astro. L'ancien code Kirby reste dans l'historique git.
- Déploiement : chaque push sur `master` synchronise `site/` vers le serveur (`.github/workflows/deploy.yml`, rsync `--delete`).
- Secrets GitHub : `DEPLOY_SSH_KEY` (clé privée de déploiement), `DEPLOY_KNOWN_HOSTS` (empreinte du serveur), `DEPLOY_TARGET` (destination rsync `user@hôte:chemin/`).
