import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "src/content/projects"
REQUIRED = ("title", "order", "description", "cover", "images")


def front_matter(md):
    """Lignes du front matter (entre les deux premiers ---), sans parseur YAML."""
    lines = md.read_text().splitlines()
    return lines[1:lines.index("---", 1)]


class TestContent(unittest.TestCase):
    def test_cont_01_projects(self):
        legacy = [line.split("\t") for line in (ROOT / "tests/legacy-urls.txt").read_text().splitlines()]
        slugs = {p[1:] for p, want in legacy if want == "200" and "." not in p and p not in ("/", "/a-propos")}
        self.assertEqual({f.stem for f in PROJECTS.glob("*.md")}, slugs, "src/content/projects/*.md ≠ pages projet de legacy-urls.txt")
        orders = {}
        for md in sorted(PROJECTS.glob("*.md")):
            fm = front_matter(md)
            keys = {m[1] for line in fm if (m := re.match(r"^(\w+):", line))}
            for key in REQUIRED:
                self.assertIn(key, keys, f"{md.relative_to(ROOT)} : champ {key} absent")
            order = next(line.split(":")[1].strip() for line in fm if line.startswith("order:"))
            self.assertNotIn(order, orders, f"{md.relative_to(ROOT)} : order {order} déjà pris par {orders.get(order)}")
            orders[order] = md.name
            for path in re.findall(r"/media/[^\s\",]+", "\n".join(fm)):
                self.assertTrue((ROOT / "public" / path.lstrip("/")).is_file(), f"{md.relative_to(ROOT)} : public{path} absent")

    def test_cont_02_schema_required(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            shutil.copy(ROOT / "package.json", tmp)
            shutil.copytree(ROOT / "src", tmp / "src")
            (tmp / "node_modules").symlink_to(ROOT / "node_modules")
            # cacheDir interne : sinon le cache du content layer est celui du dépôt, via le lien node_modules
            config = (ROOT / "astro.config.mjs").read_text().replace("defineConfig({", "defineConfig({ cacheDir: './.cache',", 1)
            self.assertIn("cacheDir", config, "astro.config.mjs : defineConfig({ introuvable, cacheDir non injecté")
            (tmp / "astro.config.mjs").write_text(config)
            md = tmp / "src/content/projects/sigfox.md"
            md.write_text(re.sub(r"(?m)^description:.*\n", "", md.read_text(), count=1))
            r = subprocess.run(["npx", "astro", "sync"], cwd=tmp, capture_output=True, text=True, timeout=180)
        out = r.stdout + r.stderr
        self.assertNotEqual(r.returncode, 0, "astro sync accepte un projet sans description")
        self.assertIn("sigfox", out, f"astro sync ne nomme pas le projet fautif (sigfox) : {out[-500:]}")
        self.assertIn("description", out, f"astro sync ne nomme pas le champ description : {out[-500:]}")

    def test_cont_03_no_kirbytext(self):
        for md in sorted((ROOT / "src/content").rglob("*")):
            if md.is_file():
                for tag in re.findall(r"\((?:link|image|email|date):", md.read_text()):
                    self.fail(f"{md.relative_to(ROOT)} : Kirbytext {tag} non converti")


if __name__ == "__main__":
    unittest.main()
