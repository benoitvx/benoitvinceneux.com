"""T-BV-A11Y-01, NAV-01 : structure accessible et nav des 13 pages et de la 404."""
import unittest

import test_dist as base

NAV = ["/a-propos", "/services-du-premier-ministre", "/presidence-de-la-republique", "/curated-adventures", "/sigfox", "/notresante",
       "/ca-compte-pour-moi", "/pierre-fabre", "/groupama", "/lepharmacien-fr", "/toulouse-football-club", "/yana-place"]


def docs():
    for slug in base.pages() + ["404"]:
        yield slug, f"dist/{slug}.html", base.parse(base.DIST / f"{slug}.html")


class TestA11y(unittest.TestCase):
    def test_a11y_01_structure(self):
        for slug, rel, doc in docs():
            tags = doc.tags
            self.assertIn(("html", "fr"), [(t, a.get("lang")) for t, a, _ in tags], f'{rel} : <html lang="fr"> absent')
            self.assertEqual(len(doc.title), 1, f"{rel} : {len(doc.title)} <title>, attendu 1")
            self.assertTrue(doc.title[0].strip(), f"{rel} : <title> vide")
            ids = [a["id"] for _, a, _ in tags if a.get("id")]
            self.assertEqual(len(ids), len(set(ids)), f"{rel} : id en double {sorted({i for i in ids if ids.count(i) > 1})}")
            first = next(a["href"] for t, a, _ in tags if t == "a" and a.get("href"))
            self.assertTrue(first.startswith("#") and first[1:] in ids, f"{rel} : premier lien {first}, attendu un lien d'évitement vers un id existant")
            current = [a.get("href") for t, a, ctx in tags if t == "a" and "nav" in ctx and a.get("aria-current") == "page"]
            want = [] if slug in ("index", "404") else [f"/{slug}"]
            self.assertEqual(current, want, f'{rel} : aria-current="page" dans la nav sur {current}, attendu {want}')
            for t, a, ctx in tags:
                if t == "img":
                    self.assertIn("alt", a, f"{rel} : <img src={a.get('src')}> sans alt")
                    if slug == "index" and "main" in ctx:
                        self.assertEqual(a["alt"], "", f'{rel} : vignette {a.get("src")} alt={a["alt"]!r}, attendu alt=""')
                if t == "iframe":
                    self.assertTrue((a.get("title") or "").strip(), f"{rel} : <iframe src={a.get('src')}> sans title")

    def test_nav_01_order(self):
        for _, rel, doc in docs():
            hrefs = [a.get("href") for t, a, ctx in doc.tags if t == "a" and "nav" in ctx]
            self.assertEqual(hrefs, NAV, f"{rel} : ordre de la nav {hrefs}")


if __name__ == "__main__":
    unittest.main()
