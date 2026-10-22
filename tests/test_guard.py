import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
GUARD = ROOT / "tests/predeploy_guard.sh"


class TestGuard(unittest.TestCase):
    """T-BV-GUARD-01 : predeploy_guard.sh sur des copies temporaires de dist/."""

    def run_guard(self, alter):
        self.assertTrue(DIST.is_dir(), "dist/ absent : lancer npx astro build")
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "dist"
            shutil.copytree(DIST, d, symlinks=True)
            alter(d)
            r = subprocess.run(["bash", GUARD, d], capture_output=True, text=True)
            return r.returncode, r.stdout + r.stderr

    def test_guard_01_dist_intact(self):
        code, out = self.run_guard(lambda d: None)
        self.assertEqual(code, 0, f"predeploy_guard.sh refuse dist/ intact : {out}")

    def test_guard_01_negatifs(self):
        def few_pages(d):
            for f in sorted(d.rglob("*.html"))[2:]:
                f.unlink()

        for name, alter, keyword in [
            (".htaccess supprimé", lambda d: (d / ".htaccess").unlink(), ".htaccess"),
            ("2 pages HTML seulement", few_pages, "pages"),
            ("x.php ajouté", lambda d: (d / "x.php").write_text("x"), ".php"),
            ("lien symbolique ajouté", lambda d: os.symlink("index.html", d / "lien.html"), "lien symbolique"),
        ]:
            with self.subTest(name):
                code, out = self.run_guard(alter)
                self.assertNotEqual(code, 0, f"predeploy_guard.sh accepte dist/ avec {name}")
                self.assertIn(keyword, out, f"predeploy_guard.sh ({name}) : « {keyword} » absent du message {out!r}")


if __name__ == "__main__":
    unittest.main()
