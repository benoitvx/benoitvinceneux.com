import filecmp
import hashlib
import os
import re
import tempfile
import unicodedata
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DOMAIN = "https://benoitvinceneux.com"
REFERENCE = """\
/	200
/a-propos	200
/groupama	200
/sigfox	200
/presidence-de-la-republique	200
/services-du-premier-ministre	200
/pierre-fabre	200
/notresante	200
/ca-compte-pour-moi	200
/curated-adventures	200
/lepharmacien-fr	200
/toulouse-football-club	200
/yana-place	200
/llms.txt	200
/llms-full.txt	200
/google48428a5b5297f7c9.html	200
/robots.txt	200
/sitemap.txt	200
/favicon.ico	200
/favicon.gif	200
/static/master.css	200
/home	301 /
/sitemap	301 /sitemap.txt
/x.php	403|404
/.htaccess	403
/media/	403
""".splitlines()
INLINE = {"a", "abbr", "b", "cite", "code", "em", "i", "mark", "q", "s", "small", "span", "strong", "sub", "sup", "u"}
CSS_URL = re.compile(r"""url\(\s*["']?([^"')]+)""")
ARTIFACT = re.compile(r"\.(php\d?|phtml|phar)$|^\.env|^\.DS_Store$|\.map$|^\.git$")


def legacy():
    return [line.split("\t", 1) for line in (ROOT / "tests/legacy-urls.txt").read_text().splitlines()]


def excluded():
    f = ROOT / "tests/legacy-exclude.txt"
    return f.read_text().split() if f.exists() else []


def ok_paths():
    return {p for p, want in legacy() if want == "200"}


def pages():
    """Slugs des 13 pages (entrées 200 sans point de legacy-urls.txt) ; l'accueil vaut 'index'."""
    return sorted(p.strip("/") or "index" for p in ok_paths() if "." not in p)


def norm(url, base="/"):
    """URL interne -> chemin normalisé (/slug, / pour l'accueil) ; URL externe -> URL sans query ni fragment, hôte en minuscules (#10)."""
    u = urlsplit(urljoin(DOMAIN + base, url.strip()))
    if u.netloc.lower() != "benoitvinceneux.com":
        return u._replace(netloc=u.netloc.lower(), query="", fragment="").geturl()
    path = re.sub(r"\.html$", "", unicodedata.normalize("NFC", unquote(u.path)))
    return "/" if path in ("", "/index") else path


class Doc(HTMLParser):
    """tags = [(balise, attributs, conteneurs ouverts parmi nav/main)], text = texte visible, title = textes des <title>."""
    def __init__(self):
        super().__init__()
        self.tags, self.text, self.title, self.open = [], [], [], []

    def handle_starttag(self, tag, attrs):
        if tag in ("nav", "main", "script", "style", "title"):
            self.open.append(tag)
        if tag == "title":
            self.title.append("")
        self.tags.append((tag, dict(attrs), set(self.open)))
        self.text.append("" if tag in INLINE else " ")  # bord de bloc = espace visible

    def handle_endtag(self, tag):
        self.text.append("" if tag in INLINE else " ")
        if tag in self.open:
            self.open.remove(tag)

    def handle_data(self, data):
        if "title" in self.open:
            self.title[-1] += data
        elif not {"script", "style"} & set(self.open):
            self.text.append(data)

    def refs(self):
        """(balise, attribut, valeur brute) de chaque href/src/srcset, srcset découpé."""
        for tag, a, _ in self.tags:
            for k in ("href", "src", "srcset"):
                for v in (a.get(k) or "").split(",") if k == "srcset" else [a.get(k) or ""]:
                    if v.strip():
                        yield tag, k, v.split()[0] if k == "srcset" else v.strip()


def parse(f):
    doc = Doc()
    doc.feed(Path(f).read_text())
    doc.close()
    return doc


def artifact_problems(root):
    root, problems = Path(root), []
    for d, dirs, files in os.walk(root):
        for name in dirs + files:
            p = Path(d) / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                problems.append(f"{rel} : lien symbolique")
            elif ARTIFACT.search(name) or (name == ".htaccess" and rel != ".htaccess"):
                problems.append(f"{rel} : fichier interdit")
    return problems


def csp():
    m = re.search(r'Content-Security-Policy "([^"]+)"', (DIST / ".htaccess").read_text())
    return m[1] if m else ""


class TestDist(unittest.TestCase):
    def test_build_01_index(self):
        self.assertTrue((DIST / "index.html").is_file(), "dist/index.html absent : lancer npx astro build")

    def assert_same_tree(self, name):
        src, out = ROOT / "site" / name, DIST / name
        files = lambda d: {p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file()}
        self.assertEqual(files(out), files(src), f"dist/{name}/ et site/{name}/ n'ont pas les mêmes fichiers")
        for rel in sorted(files(src)):
            self.assertTrue(filecmp.cmp(src / rel, out / rel, shallow=False), f"dist/{name}/{rel} diffère de site/{name}/{rel}")

    def test_css_01_static_identical(self):
        self.assert_same_tree("static")
        html = (DIST / "index.html").read_text()
        self.assertRegex(html, r'<link[^>]*href="/static/master\.css"', 'dist/index.html: <link href="/static/master.css"> absent')

    def test_par_05_media_identical(self):
        self.assert_same_tree("media")

    def test_art_01_dist_clean(self):
        self.assertEqual(artifact_problems(DIST), [], "dist/ contient des fichiers interdits")

    def test_art_02_detects_php_and_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "x.php").write_text("")
            (Path(d) / "lien").symlink_to("x.php")
            problems = artifact_problems(d)
        self.assertEqual(len(problems), 2, f"artifact_problems doit signaler x.php et lien : {problems}")
        self.assertTrue(any(p.startswith("x.php") for p in problems), f"x.php non signalé : {problems}")
        self.assertTrue(any(p.startswith("lien") for p in problems), f"lien symbolique non signalé : {problems}")

    def test_inv_01_files_exist(self):
        skip = set(excluded())
        for path in sorted(ok_paths() - skip):
            rel = "index.html" if path == "/" else path.lstrip("/")
            f = DIST / rel
            self.assertTrue(f.is_file() or (DIST / f"{rel}.html").is_file(), f"legacy-urls.txt {path} : ni dist/{rel} ni dist/{rel}.html")

    def test_inv_02_format_and_reference(self):
        lines = (ROOT / "tests/legacy-urls.txt").read_text().splitlines()
        for line in lines:
            self.assertRegex(line, r"^/\S*\t(200|301 /\S*|403\|404|403|404)$", f"legacy-urls.txt : ligne invalide {line!r}")
        paths = [line.split("\t")[0] for line in lines]
        self.assertEqual(len(paths), len(set(paths)), f"legacy-urls.txt : chemins en double {sorted({p for p in paths if paths.count(p) > 1})}")
        self.assertLessEqual(set(REFERENCE), set(lines), f"legacy-urls.txt : entrées de référence absentes {sorted(set(REFERENCE) - set(lines))}")

    def test_inv_03_no_exclusion(self):
        self.assertEqual(excluded(), [], "tests/legacy-exclude.txt doit être absent ou vide")

    def test_inv_04_redirect_targets(self):
        for path, want in legacy():
            if want.startswith("301 "):
                self.assertIn(want[4:], ok_paths(), f"legacy-urls.txt {path} : la cible {want[4:]} n'est pas une entrée 200")

    def test_spe_01_llms(self):
        for name in ("llms.txt", "llms-full.txt"):
            data = (DIST / name).read_bytes()
            self.assertTrue(data, f"dist/{name} vide")
            text = data.decode("utf-8")
            for m in re.finditer(re.escape(DOMAIN) + r"(/[\w./-]*)?", text):
                path = (m[1] or "/").rstrip(".") or "/"
                self.assertIn(path, ok_paths(), f"dist/{name} : {m[0]} n'est pas une entrée 200 de legacy-urls.txt")
        for f in DIST.rglob("*"):
            if f.is_file():
                self.assertNotIn(b"/societe-numerique", f.read_bytes(), f"{f.relative_to(ROOT)} contient /societe-numerique (D-BV2)")

    def test_spe_02_google(self):
        digest = hashlib.sha256((DIST / "google48428a5b5297f7c9.html").read_bytes()).hexdigest()
        self.assertEqual(digest, "f6c1d4827f5cbbe00470daddb685a61ec93567a69bb135a7360f208607204972", "dist/google48428a5b5297f7c9.html modifié")

    def test_spe_03_robots(self):
        lines = (DIST / "robots.txt").read_text().splitlines()
        for want in ("User-agent: *", "Allow: /", f"Sitemap: {DOMAIN}/sitemap.txt"):
            self.assertIn(want, lines, f"dist/robots.txt : ligne {want!r} absente")

    def test_spe_04_favicon(self):
        ico = (DIST / "favicon.ico").read_bytes()
        self.assertEqual(ico, (DIST / "favicon.gif").read_bytes(), "dist/favicon.ico diffère de dist/favicon.gif")
        self.assertTrue(ico.startswith(b"GIF8"), "dist/favicon.ico ne commence pas par GIF8")

    def test_spe_05_sitemap(self):
        lines = (DIST / "sitemap.txt").read_text().splitlines()
        for url in lines:
            self.assertRegex(url, re.escape(DOMAIN) + r"/\S*$", f"dist/sitemap.txt : URL invalide {url!r}")
            self.assertNotIn(".html", url, f"dist/sitemap.txt : {url} contient .html")
        self.assertEqual(len(lines), len(set(lines)), "dist/sitemap.txt : doublons")
        want = {f"{DOMAIN}/" + ("" if s == "index" else s) for s in pages()}
        self.assertEqual(set(lines), want, f"dist/sitemap.txt : en trop {sorted(set(lines) - want)}, manquant {sorted(want - set(lines))}")

    def test_spe_06_404(self):
        html = (DIST / "404.html").read_text()
        self.assertIn('<html lang="fr"', html, 'dist/404.html : <html lang="fr"> absent')
        self.assertIn('href="/"', html, 'dist/404.html : lien href="/" absent')
        self.assertIn('href="/static/', html, 'dist/404.html : asset href="/static/…" absent')
        self.assertNotRegex(html, r'(href|src)="static/', "dist/404.html : asset en chemin relatif static/")

    def test_hta_01_directives(self):
        hta = (DIST / ".htaccess").read_text()
        for label, pattern in {
            "Options -Indexes": r"^Options -Indexes$",
            "refus PHP": r'<FilesMatch "\\\.\(php[^"]*">\s*Require all denied',
            "Content-Type markdown llms": r'<FilesMatch "\^llms[^"]*">\s*Header set Content-Type "text/markdown',
            "ErrorDocument": r"^ErrorDocument 404 /404\.html$",
            "nosniff": r'X-Content-Type-Options "nosniff"',
            "Referrer-Policy": r'Referrer-Policy "strict-origin-when-cross-origin"',
            "HSTS": r'Strict-Transport-Security "max-age=300"',
            "301 home": r"^RewriteRule \^home/\?\$ (https://%\{HTTP_HOST\})?/ \[R=301,L\]$",
            "301 sitemap": r"^RewriteRule \^sitemap/\?\$ (https://%\{HTTP_HOST\})?/sitemap\.txt \[R=301,L\]$",
        }.items():
            self.assertRegex(hta, re.compile(pattern, re.M), f"dist/.htaccess : {label} absent")
        self.assertNotRegex(hta, r"includeSubDomains|preload", "dist/.htaccess : HSTS ne doit avoir ni includeSubDomains ni preload")

    def test_hta_02_no_html_redirect(self):
        for line in (DIST / ".htaccess").read_text().splitlines():
            if line.startswith("RewriteRule"):
                pattern = line.split()[1]
                self.assertNotRegex(pattern, r"\\\.html|index", f"dist/.htaccess : règle à risque de boucle {line!r}")

    def test_csp_01_hosts(self):
        dirs = {}
        for part in filter(str.strip, csp().split(";")):
            name, *values = part.split()
            dirs[name] = values
        for name, value in {"default-src": "'self'", "script-src": "'none'", "object-src": "'none'",
                            "base-uri": "'self'", "frame-ancestors": "'none'", "form-action": "'self'"}.items():
            self.assertEqual(dirs.get(name), [value], f"dist/.htaccess CSP : {name} {value} attendu")
        used = []  # (fichier, directive, url)
        directive = {"img": "img-src", "iframe": "frame-src"}
        for f in DIST.rglob("*.html"):
            doc = parse(f)
            used += [(f, "style-src", a.get("href") or "") for tag, a, _ in doc.tags
                     if tag == "link" and "stylesheet" in (a.get("rel") or "").split()]
            used += [(f, directive[tag], v) for tag, k, v in doc.refs() if tag in directive and k in ("src", "srcset")]
        for f in DIST.rglob("*.css"):
            css = f.read_text()
            imports = re.findall(r"""@import\s+(?:url\()?["']?([^"')\s;]+)""", css)
            used += [(f, "style-src", u) for u in imports]
            used += [(f, "font-src" if re.search(r"\.(woff2?|ttf|otf|eot)([?#]|$)", u) else "img-src", u)
                     for u in CSS_URL.findall(css) if u not in imports]
        for f, d, url in used:
            if url.startswith(("http://", "https://", "//")):
                origin = "https://" + urlsplit(url).netloc
                self.assertIn(origin, dirs.get(d, []), f"{f.relative_to(ROOT)} : {origin} non autorisé par {d}")
        self.assertIn("https://www.youtube-nocookie.com", dirs.get("frame-src", []), "dist/.htaccess CSP : frame-src youtube-nocookie absent")
        for host in ("https://use.fontawesome.com", "https://rsms.me"):
            self.assertIn(host, dirs.get("font-src", []), f"dist/.htaccess CSP : font-src {host} absent")

    def test_art_04_no_script(self):
        for f in DIST.rglob("*.html"):
            rel = f.relative_to(ROOT)
            self.assertNotRegex(f.read_text(), r"(?i)<script", f"{rel} : balise <script> (CSP script-src 'none')")
            for tag, a, _ in parse(f).tags:
                for k, v in a.items():
                    self.assertFalse(k.startswith("on"), f"{rel} : attribut {k} sur <{tag}>")
                    self.assertFalse((v or "").strip().lower().startswith("javascript:"), f"{rel} : URL javascript: dans {k} de <{tag}>")

    def test_seo_01_head(self):
        titles = {}
        for slug in pages():
            doc, rel = parse(DIST / f"{slug}.html"), f"dist/{slug}.html"
            want = f"{DOMAIN}/" + ("" if slug == "index" else slug)
            canon = [a.get("href") for t, a, _ in doc.tags if t == "link" and a.get("rel") == "canonical"]
            self.assertEqual(canon, [want], f"{rel} : canonical {canon}, attendu {want}")
            desc = [a.get("content") for t, a, _ in doc.tags if t == "meta" and a.get("name") == "description"]
            self.assertTrue(desc and desc[0].strip(), f"{rel} : meta description absente ou vide")
            title = "".join(doc.title)
            self.assertNotIn(title, titles, f"{rel} : <title> {title!r} déjà utilisé par {titles.get(title)}")
            titles[title] = rel


if __name__ == "__main__":
    unittest.main()
