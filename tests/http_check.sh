#!/usr/bin/env bash
# T-BV-HTTP-01 à 06 : comportement HTTP du site servi par Apache. Usage : BASE_URL=http://127.0.0.1:8080 bash tests/http_check.sh
# T-BV-SMK-01 (smoke, « tests/smoke.sh » de #7) : BASE_URL=https://benoitvinceneux.com HSTS_MIN_AGE=<seuil> (valeur dans deploy.yml), + redirection http -> https.
# HSTS posé par le serveur, jamais par dist/.htaccess (22/10/2026) : exigé avec max-age >= HSTS_MIN_AGE si fourni, absent sinon (Apache local).
set -u
BASE="${BASE_URL:?BASE_URL requis}"
DIR="$(dirname "$0")/.."
c() { curl -s --max-time 10 -H 'X-Forwarded-Proto: https' "$@"; }
fail() { echo "ÉCHEC $1 : obtenu « $2 », attendu « $3 »"; exit 1; }
excluded() { [ -f "$DIR/tests/legacy-exclude.txt" ] && grep -qxF "$1" "$DIR/tests/legacy-exclude.txt"; }

# HTTP-01 : statut attendu de chaque URL héritée
while IFS="$(printf '\t')" read -r path want; do
  excluded "$path" && continue
  got="$(c -o /dev/null -w '%{http_code} %{redirect_url}' "$BASE$path")"
  code="${got%% *}"
  case "$want" in
    "301 "*) loc="$(echo "${got#* }" | sed -E 's#^https?://[^/]+##')"
             [ "$code $loc" = "$want" ] || fail "$path" "$code $loc" "$want" ;;
    "403|404") [ "$code" = 403 ] || [ "$code" = 404 ] || fail "$path" "$code" "403 ou 404" ;;
    *) [ "$code" = "$want" ] || fail "$path" "$code" "$want" ;;
  esac
done < "$DIR/tests/legacy-urls.txt"

# HTTP-02 : variantes .html et slash final des pages, pas de boucle
for path in $(awk -F'\t' '$2 == "200" && $1 != "/" && $1 !~ /\./ { print $1 }' "$DIR/tests/legacy-urls.txt"); do
  excluded "$path" && continue
  for u in "$path.html" "$path/"; do
    code="$(c -o /dev/null -w '%{http_code}' "$BASE$u")"
    [ "$code" = 200 ] || [ "$code" = 301 ] || fail "$u" "$code" "200 ou 301"
  done
done
for u in / /index.html /groupama.html /a-propos/; do
  c -o /dev/null -L --max-redirs 3 "$BASE$u" || fail "$u" "curl code $?" "pas de boucle de redirection"
done

# HTTP-03 : PHP, .htaccess et listing de dossier refusés
code="$(c -o /dev/null -w '%{http_code}' "$BASE/x.php")"
[ "$code" = 403 ] || [ "$code" = 404 ] || fail /x.php "$code" "403 ou 404"
code="$(c -o /dev/null -w '%{http_code}' "$BASE/.htaccess")"
[ "$code" = 403 ] || fail /.htaccess "$code" 403
body="$(c -w '\n%{http_code}' "$BASE/media/")"
code="$(echo "$body" | tail -n1)"
[ "$code" = 403 ] || fail /media/ "$code" 403
case "$body" in *"Index of"*) fail /media/ "liste de fichiers" "pas de liste" ;; esac

# HTTP-04 : page 404
title="$(sed -n 's#.*<title>\([^<]*\)</title>.*#\1#p' "$DIR/dist/404.html")"
u="/n-existe-pas-$(date +%s)"
body="$(c -w '\n%{http_code}' "$BASE$u")"
code="$(echo "$body" | tail -n1)"
[ "$code" = 404 ] || fail "$u" "$code" 404
case "$body" in *"<title>$title</title>"*) ;; *) fail "$u" "corps sans le titre" "<title>$title</title>" ;; esac

# HTTP-05 : en-têtes de sécurité sur /
headers="$(c -I "$BASE/" | tr -d '\r')"
header() { echo "$headers" | grep -i "^$1:" | head -1 | sed -E 's/^[^:]+: ?//'; }
csp="$(sed -n 's/.*Content-Security-Policy "\([^"]*\)".*/\1/p' "$DIR/dist/.htaccess")"
[ "$(header X-Content-Type-Options)" = nosniff ] || fail "/ X-Content-Type-Options" "$(header X-Content-Type-Options)" nosniff
[ "$(header Referrer-Policy)" = strict-origin-when-cross-origin ] || fail "/ Referrer-Policy" "$(header Referrer-Policy)" strict-origin-when-cross-origin
hsts="$(header Strict-Transport-Security)"
if [ -n "${HSTS_MIN_AGE:-}" ]; then
  age="$(echo "$hsts" | sed -nE 's/.*max-age=([0-9]+).*/\1/p')"
  [ "${age:-0}" -ge "$HSTS_MIN_AGE" ] || fail "/ Strict-Transport-Security" "$hsts" "max-age >= $HSTS_MIN_AGE"
else
  [ -z "$hsts" ] || fail "/ Strict-Transport-Security" "$hsts" "absent (posé par le serveur, pas par dist/.htaccess)"
fi
[ "$(header Content-Security-Policy)" = "$csp" ] || fail "/ Content-Security-Policy" "$(header Content-Security-Policy)" "$csp"

# HTTP-06 : types de contenu
for u in /llms.txt:text/markdown /llms-full.txt:text/markdown /sitemap.txt:text/plain; do
  type="$(c -o /dev/null -w '%{content_type}' "$BASE${u%%:*}")"
  case "$type" in "${u#*:}"*) ;; *) fail "${u%%:*}" "$type" "${u#*:}" ;; esac
done

# SMK-01 : http:// redirige en 301 vers https:// (domaine public seulement)
case "$BASE" in https://*)
  got="$(curl -s --max-time 10 -o /dev/null -w '%{http_code} %{redirect_url}' "http://${BASE#https://}/")"
  [ "$got" = "301 $BASE/" ] || fail "http://${BASE#https://}/" "$got" "301 $BASE/" ;;
esac

echo "http_check : OK ($BASE)"
