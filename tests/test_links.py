"""T-BV-LNK-01, LNK-02, HOST-01 : liens internes résolus, sans .html, hôtes externes connus."""
import re
import unittest
from urllib.parse import urlsplit

import test_dist as base

DIST = base.DIST


def sources():
    """(fichier relatif, chemin de base, [(attribut, valeur brute)], ids) pour chaque HTML et CSS de dist/."""
    for f in sorted(DIST.rglob("*.html")):
        doc = base.parse(f)
        ids = {a["id"] for _, a, _ in doc.tags if a.get("id")}
        yield f.relative_to(DIST).as_posix(), "/" + f.relative_to(DIST).as_posix(), [(k, v) for _, k, v in doc.refs()], ids
    for f in sorted(DIST.rglob("*.css")):
        found = re.findall(r"""url\(\s*["']?([^"')]+)""", f.read_text())
        yield f.relative_to(DIST).as_posix(), "/" + f.relative_to(DIST).as_posix(), [("url()", u) for u in found], set()


def resolves(path):
    rel = "index.html" if path == "/" else path.lstrip("/")
    return (DIST / rel).is_file() or (DIST / f"{rel}.html").is_file()


class TestLinks(unittest.TestCase):
    def test_lnk_01_internal_resolve(self):
        for name, b, refs, ids in sources():
            for k, v in refs:
                if v.startswith(("mailto:", "tel:", "data:")):
                    continue
                if v.startswith("#"):
                    self.assertIn(v[1:], ids, f"dist/{name} : ancre {v} sans id correspondant")
                    continue
                u = base.norm(v, b)
                if u.startswith("/"):
                    self.assertTrue(resolves(u), f"dist/{name} : {k}={v} ne se résout pas dans dist/ ({u})")

    def test_lnk_02_no_html_links(self):
        for name, b, refs, _ in sources():
            for k, v in refs:
                if k == "href" and base.norm(v, b).startswith("/"):
                    self.assertNotRegex(urlsplit(v).path, r"\.html$", f"dist/{name} : lien interne en .html {v}")

    def test_host_01_allowed(self):
        allowed = set((base.ROOT / "tests/allowed-hosts.txt").read_text().split())
        for name, b, refs, _ in sources():
            for k, v in refs:
                u = base.norm(v, b)
                if u.startswith(("http:", "https:")):
                    host = urlsplit(u).hostname
                    self.assertIn(host, allowed, f"dist/{name} : hôte {host} ({v}) absent de tests/allowed-hosts.txt")


if __name__ == "__main__":
    unittest.main()
