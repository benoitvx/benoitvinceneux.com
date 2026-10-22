"""T-BV-IMP-01 à 06 : scripts/import_kirby.py sur la fixture tests/fixtures/kirby/.

Les parasites (faux index.php, .htaccess, liens symboliques) ne sont pas versionnés :
ils sont créés à la volée dans une copie temporaire par parasites() (garde-fou : aucun .php versionné).
"""
import builtins
import importlib.util
import shutil
import socket
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/kirby"
spec = importlib.util.spec_from_file_location("import_kirby", ROOT / "scripts/import_kirby.py")
kirby = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kirby)


def parasites(tmp):
    content = tmp / "content"
    (content / "2_projet-a/2_projet-a").mkdir()
    (content / "2_projet-a/2_projet-a/index.php").write_text("# faux fichier\n")
    for d in ("", "2_projet-a"):
        (content / d / ".htaccess").write_text("# faux fichier\n")
    (tmp / "elsewhere").mkdir()
    (tmp / "elsewhere/project.txt").write_text("Title: Lien\n")
    (content / "5_lien").symlink_to("../elsewhere")
    (content / "6_lien-fichier").mkdir()
    (content / "6_lien-fichier/project.txt").symlink_to("../3_projet-b/project.txt")


def run(out):
    """Copie la fixture, ajoute les parasites, importe vers out ; open() refusé hors liste blanche."""
    tmp = Path(tempfile.mkdtemp())
    shutil.copytree(FIXTURE, tmp, dirs_exist_ok=True)
    parasites(tmp)
    real_open = builtins.open

    def guarded(path, *a, **k):
        p = Path(path)
        allowed = (p.name == "project.txt" and p.parent.parent == tmp / "content" and not p.is_symlink()
                   and not p.parent.is_symlink()) or (tmp / "site") in p.parents or Path(out) in p.parents
        if not allowed:
            raise AssertionError(f"import_kirby a ouvert un fichier hors liste blanche : {path}")
        return real_open(path, *a, **k)

    try:
        with mock.patch("builtins.open", guarded):
            kirby.main([str(tmp / "content"), "--site", str(tmp / "site"), "--out", str(out)])
    finally:
        shutil.rmtree(tmp)
    return {f.name: f.read_bytes() for f in Path(out).iterdir()}


class TestImport(unittest.TestCase):
    def convert(self, text):
        return kirby.convert(text, "projet-a", str(FIXTURE / "site"))

    def test_imp_01_link(self):
        self.assertEqual(self.convert("(link: https://example.org text: X)"), "[X](https://example.org)")

    def test_imp_01_email(self):
        self.assertEqual(self.convert("(email: a@b.fr text: X)"), "[X](mailto:a@b.fr)")

    def test_imp_01_heading(self):
        self.assertEqual(self.convert("##Titre"), "## Titre")

    def test_imp_01_image(self):
        self.assertEqual(self.convert("(image: x.jpg)"), "![](/media/pages/projet-a/h1/x-640x.jpg)")

    def test_imp_02_own_domain_relative(self):
        self.assertEqual(self.convert("(link: https://benoitvinceneux.com/x text: X)"), "[X](/x)")

    def test_imp_02_other_domain_unchanged(self):
        self.assertEqual(self.convert("(link: https://example.org/x text: X)"), "[X](https://example.org/x)")

    def test_imp_03_hard_break_outside_html(self):
        self.assertEqual(self.convert("a\nb"), "a  \nb")

    def test_imp_03_unchanged_inside_html(self):
        html = "<div>\nligne 1\nligne 2\n</div>"
        self.assertEqual(self.convert(html), html)

    def test_imp_04_only_valid_projects(self):
        with tempfile.TemporaryDirectory() as out:
            files = run(out)
        self.assertEqual(sorted(files), ["projet-a.md", "projet-b.md"], f"sortie de l'import inattendue : {sorted(files)}")
        a = files["projet-a.md"].decode()
        for want in ('title: "Projet A"', "order: 2", 'description: "Description A…"', 'role: "Product Manager"',
                     "## Titre", "[le projet B](/projet-b)", "un brouillon.", "[moi](mailto:a@example.org)",
                     'src: "/media/pages/projet-a/h1/x-640x.jpg"', "width: 640, height: 640"):
            self.assertIn(want, a, f"projet-a.md : {want!r} absent")
        self.assertNotIn("client:", a, "projet-a.md : champ vide client: écrit")
        self.assertNotIn("/brouillon", a, "projet-a.md : lien vers une page non publiée conservé (D-BV2)")

    def test_imp_05_deterministic(self):
        with tempfile.TemporaryDirectory() as o1, tempfile.TemporaryDirectory() as o2:
            self.assertEqual(run(o1), run(o2), "deux imports de la fixture donnent des sorties différentes")

    def test_imp_06_offline(self):
        with mock.patch.object(socket, "socket", side_effect=OSError("réseau interdit")), tempfile.TemporaryDirectory() as out:
            self.assertEqual(sorted(run(out)), ["projet-a.md", "projet-b.md"], "import hors ligne incomplet")


if __name__ == "__main__":
    unittest.main()
