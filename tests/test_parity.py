"""T-BV-PAR-00 à 04 : parité dist/ ↔ site/ sur les 13 pages (retiré en #9)."""
import json
import re
import unicodedata
import unittest

import test_dist as base

ALLOW = base.ROOT / "tests/parity-allowlist.json"


def allow(test, slug=None):
    return [e["motif"] for e in json.loads(ALLOW.read_text()) if e["test"] == test and (slug is None or e["page"] in ("*", slug))]


def text(doc, slug):
    t = unicodedata.normalize("NFC", "".join(doc.text))
    for motif in allow("PAR-01", slug):
        t = re.sub(motif, " ", t)
    return " ".join(t.split())


def urls(doc, slug):
    out = {base.norm(v, f"/{slug}") for _, _, v in doc.refs()}
    return {u for u in out if not any(re.search(m, u) for m in allow("PAR-02", slug))}


def head(doc):
    desc = [a.get("content") for t, a, _ in doc.tags if t == "meta" and a.get("name") == "description"]
    return "".join(doc.title), desc


def both(slug):
    return base.parse(base.ROOT / "site" / f"{slug}.html"), base.parse(base.DIST / f"{slug}.html")


class TestParity(unittest.TestCase):
    def test_par_00_allowlist(self):
        entries = json.loads(ALLOW.read_text())
        rules = json.loads((base.ROOT / ".htmlvalidate.json").read_text()).get("rules", {})
        off = {r for r, v in rules.items() if v == "off"}
        self.assertEqual(off, set(allow("html-validate")), ".htmlvalidate.json : règles à off et entrées html-validate de l'allowlist diffèrent")
        for e in entries:
            for k in ("test", "page", "motif", "pourquoi"):
                self.assertTrue(str(e.get(k, "")).strip(), f"parity-allowlist.json : champ {k} vide dans {e}")
            slugs = base.pages() if e["page"] == "*" else [e["page"]]
            if e["test"] == "PAR-01":
                used = any(re.search(e["motif"], "".join(d.text)) for s in slugs for d in both(s))
            elif e["test"] == "PAR-02":
                used = any(re.search(e["motif"], base.norm(v, f"/{s}")) for s in slugs for d in both(s) for _, _, v in d.refs())
            else:  # html-validate : contrôlé avec .htmlvalidate.json ci-dessus ; axe : sélecteur vérifié dans a11y.spec.ts
                used = e["test"] in ("html-validate", "axe") and all((base.DIST / f"{s}.html").is_file() for s in slugs)
            self.assertTrue(used, f"parity-allowlist.json : entrée morte {e}")

    def test_par_01_text(self):
        for slug in base.pages():
            a, b = (text(d, slug) for d in both(slug))
            if a != b:
                i = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
                self.fail(f"{slug} : texte divergent, site « …{a[max(0, i - 30):i + 50]}… » / dist « …{b[max(0, i - 30):i + 50]}… »")

    def test_par_02_urls(self):
        for slug in base.pages():
            a, b = (urls(d, slug) for d in both(slug))
            self.assertEqual(a, b, f"{slug} : URL seulement dans site {sorted(a - b)}, seulement dans dist {sorted(b - a)}")

    def test_par_03_media_count(self):
        for slug in base.pages():
            for tag in ("img", "iframe"):
                a, b = (sum(t == tag for t, _, _ in d.tags) for d in both(slug))
                self.assertEqual(a, b, f"{slug} : {b} <{tag}> dans dist, {a} dans site")

    def test_par_04_head(self):
        for slug in base.pages():
            a, b = (head(d) for d in both(slug))
            self.assertEqual(a, b, f"{slug} : <title>/description site {a} ≠ dist {b}")


if __name__ == "__main__":
    unittest.main()
