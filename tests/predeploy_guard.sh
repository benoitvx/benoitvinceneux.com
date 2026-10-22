#!/usr/bin/env bash
# Garde-fous avant rsync (#7, T-BV-GUARD-01). Usage : bash tests/predeploy_guard.sh dist
set -u
d="${1:?dossier requis}"
fail() { echo "ÉCHEC predeploy_guard : $1" >&2; exit 1; }
[ -d "$d" ] || fail "$d introuvable"
[ -f "$d/.htaccess" ] || fail "$d/.htaccess absent"
links="$(find "$d" -type l)"
[ -z "$links" ] || fail "lien symbolique : $links"
php="$(find "$d" -type f \( -iname '*.php' -o -iname '*.php[0-9]' -o -iname '*.phtml' -o -iname '*.phar' \))"
[ -z "$php" ] || fail "fichier .php : $php"
# Pages HTML attendues : entrées 200 de legacy-urls.txt sans extension ou en .html
want="$(awk -F'\t' '$2 == "200" && ($1 !~ /\./ || $1 ~ /\.html$/)' "$(dirname "$0")/legacy-urls.txt" | wc -l | tr -d ' ')"
got="$(find "$d" -type f -name '*.html' ! -name 404.html | wc -l | tr -d ' ')"
[ "$got" -ge "$want" ] || fail "$got pages HTML dans $d, au moins $want attendues"
echo "predeploy_guard : OK ($d)"
