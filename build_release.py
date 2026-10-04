from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / ".cloudflare-release"
PUBLIC_DIRS = ("pl", "en", "de", "assets", ".well-known")
PUBLIC_FILES = (
    "index.html", "kontakt.html", "o-mnie.html", "proces.html", "projekty.html", "zakres.html",
    "site-v10.css", "site-v10.js", "case-study.css", "sitemap.xml", "robots.txt", "llms.txt", "_headers", "_redirects",
)

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for name in PUBLIC_DIRS:
    shutil.copytree(ROOT / name, OUT / name)
for name in PUBLIC_FILES:
    src = ROOT / name
    if not src.is_file():
        raise SystemExit(f"Missing public file: {name}")
    shutil.copy2(src, OUT / name)

html = list(OUT.rglob("*.html"))
if len(html) != 65:
    raise SystemExit(f"Expected 65 HTML files, found {len(html)}")
for forbidden in (".git", ".wrangler", "node_modules", "build_v10.py", "test_site.py", "package.json"):
    if any(p.name == forbidden for p in OUT.rglob("*")):
        raise SystemExit(f"Forbidden release entry: {forbidden}")
print(f"Release ready: {OUT} | {len(list(OUT.rglob('*')))} files/dirs | 65 HTML")
