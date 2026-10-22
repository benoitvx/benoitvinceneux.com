"""T-BV-BUD-01 : budget de poids de dist/."""
import unittest

import test_dist as base

KB = 1024
IMAGE = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg", ".ico"}


class TestBudget(unittest.TestCase):
    def test_bud_01_sizes(self):
        files = [f for f in base.DIST.rglob("*") if f.is_file()]
        for f in files:
            rel, size = f.relative_to(base.ROOT), f.stat().st_size
            self.assertLessEqual(size, 1024 * KB, f"{rel} : {size} o > 1 Mo")
            if f.suffix == ".html":
                self.assertLessEqual(size, 50 * KB, f"{rel} : {size} o > 50 Ko")
            if f.suffix.lower() in IMAGE:
                self.assertLessEqual(size, 700 * KB, f"{rel} : {size} o > 700 Ko")
        total = sum(f.stat().st_size for f in files)
        self.assertLessEqual(total, 16 * 1024 * KB, f"dist/ : {total} o > 16 Mo")
        css = sum(f.stat().st_size for f in files if f.suffix == ".css")
        self.assertLessEqual(css, 100 * KB, f"dist/**/*.css : {css} o > 100 Ko")


if __name__ == "__main__":
    unittest.main()
