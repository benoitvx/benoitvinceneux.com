import filecmp
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


class TestDist(unittest.TestCase):
    def test_build_01_index(self):
        self.assertTrue((DIST / "index.html").is_file(), "dist/index.html absent : lancer npx astro build")

    def test_css_01_static_identical(self):
        src, out = ROOT / "site/static", DIST / "static"
        files = lambda d: {p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file()}
        self.assertEqual(files(out), files(src), "dist/static/ et site/static/ n'ont pas les mêmes fichiers")
        for rel in sorted(files(src)):
            self.assertTrue(filecmp.cmp(src / rel, out / rel, shallow=False), f"dist/static/{rel} diffère de site/static/{rel}")
        html = (DIST / "index.html").read_text()
        self.assertRegex(html, r'<link[^>]*href="/static/master\.css"', 'dist/index.html: <link href="/static/master.css"> absent')


if __name__ == "__main__":
    unittest.main()
