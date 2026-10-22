"""Import des projets Kirby en Markdown (src/content/projects/<slug>.md).

Usage : python3 -I scripts/import_kirby.py <dossier_contenu> [--site site] [--out src/content/projects]

Lit seulement <contenu>/<n>_<slug>/project.txt (niveau racine, sans lien symbolique)
et le snapshot <site>/ (description, vignette, images). Aucun autre fichier n'est ouvert.
Le snapshot n'est plus dans le dépôt (#9) : l'extraire du tag avant usage,
par exemple `mkdir /tmp/site && git archive snapshot-kirby:site | tar -x -C /tmp/site`, puis `--site /tmp/site`.
"""
import argparse
import glob
import json
import os
import re
from html.parser import HTMLParser

DOMAIN = re.compile(r"^https?://(www\.)?benoitvinceneux\.com(?=/|$)")
FIELDS = ("role", "client", "date", "website", "textposition")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def fields(text):
    out = {}
    for part in re.split(r"^-{4}\s*$", text, flags=re.M):
        key, sep, value = part.partition(":")
        if sep:
            out[key.strip().lower()] = value.strip()
    return out


def link(m, slugs):
    url, text = m[1], m[2] or m[1]
    url = DOMAIN.sub("", url) or "/"
    if slugs is not None and url.startswith("/") and url.strip("/").split("/")[0] not in slugs | {"", "a-propos"}:
        return text  # page non publiée (D-BV2) : texte sans lien
    return f"[{text}]({url})"


def image(m, slug, site):
    name = m[1]
    stem, ext = os.path.splitext(name)
    for candidate in (f"{stem}-640x{ext}", name):
        found = sorted(glob.glob(os.path.join(glob.escape(site), "media/pages", glob.escape(slug), "*", glob.escape(candidate))))
        if found:
            return "![](/" + os.path.relpath(found[0], site).replace(os.sep, "/") + ")"
    raise SystemExit(f"{slug} : image {name} introuvable sous {site}/media/pages/{slug}/")


def convert(text, slug, site, slugs=None):
    """Kirbytext vers Markdown. slugs : pages publiées (None = pas de filtrage des liens internes)."""
    text = re.sub(r"\(link:\s*(\S+?)(?:\s+text:\s*([^)]*?))?\s*\)", lambda m: link(m, slugs), text)
    text = re.sub(r"\(email:\s*(\S+?)(?:\s+text:\s*([^)]*?))?\s*\)", lambda m: f"[{m[2] or m[1]}](mailto:{m[1]})", text)
    text = re.sub(r"\(image:\s*([^\s)]+)[^)]*\)", lambda m: image(m, slug, site), text)
    text = re.sub(r"^(#{1,6})(?=[^#\s])", r"\1 ", text, flags=re.M)
    lines, html = text.split("\n"), False
    for i, line in enumerate(lines):
        if not line.strip():
            html = False
        elif line.lstrip().startswith("<"):
            html = True  # bloc HTML brut jusqu'à la prochaine ligne vide (CommonMark type 6)
        if not html:
            line = line.rstrip()
            if line and i + 1 < len(lines) and lines[i + 1].strip():
                line += "  "  # saut de ligne dur (Kirby : markdown.breaks)
            lines[i] = line
    return "\n".join(lines)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.description, self.imgs, self.href = None, [], None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and a.get("name") == "description":
            self.description = a.get("content")
        elif tag == "a":
            self.href = a.get("href")
        elif tag == "img":
            self.imgs.append((self.href, a))

    def handle_endtag(self, tag):
        if tag == "a":
            self.href = None


def media(a):
    root = lambda s: re.sub(r"(^|,\s*)(?=media/)", r"\1/", s or "")
    return f'src: {json.dumps(root(a["src"]))}, srcset: {json.dumps(root(a.get("srcset")))}'


def projects(content):
    found = []
    for e in os.scandir(content):
        m = re.fullmatch(r"(\d+)_(.+)", e.name)
        txt = os.path.join(e.path, "project.txt")
        if m and m[2] != "a-propos" and not e.is_symlink() and e.is_dir() and os.path.isfile(txt) and not os.path.islink(txt):
            found.append((int(m[1]), m[2], txt))
    return sorted(found)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("content")
    p.add_argument("--site", default="site")
    p.add_argument("--out", default="src/content/projects")
    args = p.parse_args(argv)
    todo = projects(args.content)
    slugs = {slug for _, slug, _ in todo}
    grid = Page(read(os.path.join(args.site, "index.html"))).imgs
    os.makedirs(args.out, exist_ok=True)
    for order, slug, txt in todo:
        f = fields(read(txt))
        page = Page(read(os.path.join(args.site, f"{slug}.html")))
        cover = next((a for href, a in grid if href == f"{slug}.html"), None)
        if cover is None:
            raise SystemExit(f"{slug} : vignette absente de site/index.html")
        fm = [f"title: {json.dumps(f['title'], ensure_ascii=False)}", f"order: {order}",
              f"description: {json.dumps(page.description, ensure_ascii=False)}"]
        fm += [f"{k}: {json.dumps(f[k], ensure_ascii=False)}" for k in FIELDS if f.get(k)]
        fm += [f"cover: {{ {media(cover)} }}", "images:"]
        fm += [f'  - {{ {media(a)}, width: {int(a["width"])}, height: {int(a["height"])} }}' for _, a in page.imgs]
        body = convert(f.get("text", ""), slug, args.site, slugs)
        with open(os.path.join(args.out, f"{slug}.md"), "w", encoding="utf-8", newline="\n") as out:
            out.write("---\n" + "\n".join(fm) + "\n---\n" + body + "\n")


if __name__ == "__main__":
    main()
