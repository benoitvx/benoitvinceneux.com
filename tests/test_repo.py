import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = sorted((ROOT / ".github/workflows").glob("*.yml"))
DEV_ALLOWED = {"@playwright/test", "@axe-core/playwright", "html-validate"}  # D-BV4


class TestRepo(unittest.TestCase):
    def test_dep_01_dependencies(self):
        pkg = json.loads((ROOT / "package.json").read_text())
        deps, dev = pkg.get("dependencies", {}), pkg.get("devDependencies", {})
        self.assertEqual(set(deps), {"astro"}, "package.json: dependencies doit valoir {astro}")
        self.assertLessEqual(set(dev), DEV_ALLOWED, f"package.json: devDependencies hors D-BV4 {set(dev) - DEV_ALLOWED}")
        for name, version in {**deps, **dev}.items():
            self.assertRegex(version, r"^\d+\.\d+\.\d+$", f"package.json: version non exacte pour {name}")
        self.assertTrue((ROOT / "package-lock.json").is_file(), "package-lock.json absent")
        self.assertEqual((ROOT / ".nvmrc").read_text().strip(), "24", ".nvmrc doit valoir 24")

    def test_wf_01_actions_pinned_by_sha(self):
        self.assertTrue(WORKFLOWS, ".github/workflows/*.yml introuvable")
        for wf in WORKFLOWS:
            for n, line in enumerate(wf.read_text().splitlines(), 1):
                if m := re.match(r"\s*(?:-\s+)?uses:\s*(\S+)", line):
                    self.assertRegex(m[1], r"@[0-9a-f]{40}$", f"{wf.name}:{n} action non épinglée par SHA : {m[1]}")

    def test_wf_02_secrets_only_in_env(self):
        for wf in WORKFLOWS:
            lines = wf.read_text().splitlines()
            for n, line in enumerate(lines):
                if "secrets." not in line:
                    continue
                indent = len(line) - len(line.lstrip())
                parent = next((p for p in reversed(lines[:n]) if p.strip() and len(p) - len(p.lstrip()) < indent), "")
                self.assertEqual(parent.strip(), "env:", f"{wf.name}:{n + 1} secret hors d'un bloc env: : {line.strip()}")

    def test_wf_03_permissions_and_triggers(self):
        text = (ROOT / ".github/workflows/deploy.yml").read_text()
        for label, pattern in {
            "permissions: contents: read (racine)": r"^permissions:\s*\n\s+contents:\s*read\s*$",
            "push sur master": r"^\s+push:\s*\n\s+branches:\s*\[\s*master\s*\]",
            "pull_request": r"^\s+pull_request:",
            "workflow_dispatch": r"^\s+workflow_dispatch:",
            "job test": r"^  test:",
        }.items():
            self.assertRegex(text, re.compile(pattern, re.M), f"deploy.yml: {label} absent")

    def test_wf_04_deploy_job(self):
        text = (ROOT / ".github/workflows/deploy.yml").read_text()
        m = re.search(r"^  deploy:\n(?:(?!  \w).*\n?)*", text, re.M)
        self.assertTrue(m, "deploy.yml: job deploy absent")
        job = m[0]
        for label, pattern in {
            "needs: test": r"^\s+needs:\s*test\s*$",
            "if: exact du ticket": r"^\s+if: github\.event_name != 'pull_request' && github\.ref == 'refs/heads/master'$",
            "concurrency deploy sans annulation": r"^\s+concurrency:\n\s+group: deploy\n\s+cancel-in-progress: false$",
        }.items():
            self.assertRegex(job, re.compile(pattern, re.M), f"deploy.yml, job deploy : {label} absent")
        lines = job.splitlines()
        guard = next((i for i, l in enumerate(lines) if "predeploy_guard.sh" in l), None)
        rsync = next((i for i, l in enumerate(lines) if re.search(r"run:.*rsync ", l)), None)
        self.assertIsNotNone(guard, "deploy.yml, job deploy : predeploy_guard.sh absent")
        self.assertIsNotNone(rsync, "deploy.yml, job deploy : ligne run: rsync absente")
        self.assertLess(guard, rsync, "deploy.yml, job deploy : predeploy_guard.sh doit précéder rsync")
        self.assertIn("--delete-after --delay-updates", lines[rsync], "deploy.yml, rsync : --delete-after --delay-updates absent")
        self.assertIn(" dist/ ", lines[rsync], "deploy.yml, rsync : source dist/ absente")
        self.assertNotIn("site/", job, "deploy.yml, job deploy : publie encore site/")

    def test_art_03_no_php_in_git(self):
        files = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout.decode().split("\0")
        needle = b"<" + b"?php"  # jamais écrite en clair dans le dépôt
        for f in filter(None, files):
            self.assertNotRegex(f, r"\.php\d?$", f"fichier PHP versionné : {f}")
            if f.endswith(".htaccess"):
                self.assertIn(f, {"public/.htaccess", "site/.htaccess"}, f".htaccess versionné hors public/ et site/ : {f}")
            path = ROOT / f
            if path.is_file() and not path.is_symlink():
                self.assertNotIn(needle, path.read_bytes(), f"balise PHP dans le fichier versionné {f}")


if __name__ == "__main__":
    unittest.main()
