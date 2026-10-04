from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re
import sys
import json

ROOT = Path(__file__).resolve().parent
DOMAIN = "https://adam-jakubowski.com"
LANGS = ("pl", "en", "de")
FORM_FILES = {
    "pl/formularz-b2c.html", "pl/formularz-b2b.html",
    "en/b2c-form.html", "en/b2b-form.html",
    "de/b2c-formular.html", "de/b2b-formular.html",
}
PRIVACY_FILES = {
    "pl/polityka-prywatnosci.html", "en/privacy.html", "de/datenschutz.html"
}
FORBIDDEN_IMAGES = {"IMG_4679.JPG", "IMG_4685.JPG", "06-gotowy-bar.jpg", "07-montaz-siedziska.jpg", "IMG_4792"}
errors = []

class Doc(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]; self.assets=[]; self.forms=[]; self.canon=[]; self.alts=[]
        self.ids=[]; self.selects=[]; self.options=[]; self.metas=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag == "a" and a.get("href"): self.links.append(a["href"])
        if tag in {"img", "script"} and a.get("src"): self.assets.append(a["src"])
        if tag == "link" and a.get("href"):
            if a.get("rel") == "canonical": self.canon.append(a["href"])
            elif a.get("rel") == "alternate" and a.get("hreflang"): self.alts.append((a["hreflang"],a["href"]))
            elif a.get("rel") in {"stylesheet","icon"}: self.assets.append(a["href"])
            elif a.get("rel") == "describedby": self.links.append(a["href"])
        if tag == "form": self.forms.append(a)
        if tag == "select": self.selects.append(a)
        if tag == "option": self.options.append(a)
        if a.get("id"): self.ids.append(a["id"])
        if tag == "meta": self.metas.append(a)

def clean_path(value):
    parsed=urlsplit(value)
    if parsed.scheme in {"mailto","tel","http","https"} and not value.startswith(DOMAIN):
        return None
    path=unquote(parsed.path)
    if value.startswith(DOMAIN): path=unquote(urlsplit(value).path)
    if not path.startswith("/"): return None
    return path

def resolves(path):
    if path == "/": return (ROOT/"index.html").exists()
    target=ROOT/path.lstrip("/")
    candidates=[target]
    if path.endswith("/"): candidates.append(target/"index.html")
    elif not target.suffix: candidates += [target.with_suffix(".html"), target/"index.html"]
    return any(p.exists() and p.is_file() for p in candidates)

html_files=sorted(p for p in ROOT.rglob("*.html") if "node_modules" not in p.parts and ".wrangler" not in p.parts)
if len(html_files) != 65: errors.append(f"Expected 65 HTML files, found {len(html_files)}")

docs={}
for path in html_files:
    rel=path.relative_to(ROOT).as_posix()
    text=path.read_text(encoding="utf-8")
    doc=Doc(); doc.feed(text); docs[rel]=(text,doc)
    if text.count("<html") != 1 or text.count("</html>") != 1: errors.append(f"Malformed HTML shell: {rel}")
    if len(doc.ids) != len(set(doc.ids)): errors.append(f"Duplicate ids: {rel}")
    for ref in doc.links+doc.assets:
        local=clean_path(ref)
        if local and not resolves(local): errors.append(f"Broken local reference in {rel}: {ref}")
    for name in FORBIDDEN_IMAGES:
        if name.lower() in text.lower(): errors.append(f"Forbidden image reference in {rel}: {name}")
    if "formsubmit.co" in text.lower() or "github pages" in text.lower(): errors.append(f"Obsolete provider reference: {rel}")
    if "15%" in text or "2 200 zł" in text or "4 500 zł" in text: errors.append(f"Obsolete public B2B price: {rel}")
    if any(s in text for s in ("jeden punkt odpowiedzialności","single point of responsibility","ein einziger verantwortungspunkt")):
        errors.append(f"Forbidden responsibility promise: {rel}")

# Primary generated pages: canonical, language equivalence and clean URLs.
for key, triplet in __import__('build_v10').PATHS.items():
    for idx,lang in enumerate(LANGS):
        rel=f"{lang}/{triplet[idx]}"
        path=ROOT/rel
        if not path.exists(): errors.append(f"Missing generated page: {rel}"); continue
        text,doc=docs[rel]
        expected=__import__('build_v10').url(key,lang)
        expected_canon=DOMAIN + expected
        if doc.canon != [expected_canon]: errors.append(f"Bad canonical in {rel}: {doc.canon} != {expected_canon}")
        if key == "thanks" and not any(m.get("name")=="robots" and "noindex" in m.get("content","") for m in doc.metas):
            errors.append(f"Thank-you page must be noindex: {rel}")
        if "/llms.txt" not in doc.links: errors.append(f"Missing llms.txt discovery link: {rel}")
        alt=dict(doc.alts)
        expected_alts={l: DOMAIN + __import__('build_v10').url(key,l) for l in LANGS}
        expected_alts["x-default"]=DOMAIN+"/pl/"
        if alt != expected_alts: errors.append(f"Bad hreflang set in {rel}: {alt}")
        for l in LANGS:
            if __import__('build_v10').url(key,l) not in doc.links: errors.append(f"Language switch loses route in {rel}: {l}")

# Case studies follow the same clean and contextual language rules.
for lang in LANGS:
    rel=f"{lang}/landbyska-verket.html"; text,doc=docs[rel]
    expected=f"{DOMAIN}/{lang}/landbyska-verket"
    if doc.canon != [expected]: errors.append(f"Bad case canonical: {rel}")
    for l in LANGS:
        if f"/{l}/landbyska-verket" not in doc.links: errors.append(f"Bad case language switch: {rel} -> {l}")
    if dict(doc.alts).get("x-default") != DOMAIN+"/pl/landbyska-verket": errors.append(f"Bad case x-default: {rel}")
    if "/site-v10.css?v=11" not in text or "/site-v10.js?v=11" not in text or "PROJECT DIRECTION" in text:
        errors.append(f"Case study not unified with v11: {rel}")
    if any(x in text for x in ("elementy konstrukcyjne sufitu","structural ceiling elements","konstruktive Deckenelemente","Jeden punkt koordynacji","One coordination point","Ein Koordinationspunkt")):
        errors.append(f"Case study overstates scope: {rel}")

# Lead forms do not send data through the site; they prepare an email locally.
for rel in FORM_FILES:
    text,doc=docs[rel]
    if len(doc.forms) != 1: errors.append(f"Expected one lead form: {rel}"); continue
    form=doc.forms[0]
    if form.get("action") != "mailto:info@adam-jakubowski.com" or "data-mailto-form" not in form:
        errors.append(f"Unsafe form transport: {rel}")
    if not any(s.get("name")=="service" and "required" in s for s in doc.selects): errors.append(f"Missing required service selector: {rel}")
    if len([o for o in doc.options if o.get("value")]) < 4: errors.append(f"Too few service options: {rel}")
    if "programie pocztowym" not in text and "email application" not in text and "E-Mail-Programm" not in text:
        errors.append(f"Missing local email explanation: {rel}")
    lang=rel[:2]
    if __import__('build_v10').T[lang]['availability_notice'] not in text: errors.append(f"Missing formal-gate notice: {rel}")
    if "b2b" in rel and not any(x in text for x in ("Nie wpisuj danych osób fizycznych","Do not enter personal","Keine personenbezogenen")):
        errors.append(f"Missing third-party data warning: {rel}")

for rel in PRIVACY_FILES:
    text,_=docs[rel]
    for required in ("Cloudflare", "info@adam-jakubowski.com"):
        if required not in text: errors.append(f"Privacy missing {required}: {rel}")
    low=text.lower()
    if not any(x.lower() in low for x in ("6 miesiącach","6 months","6 Monaten")): errors.append(f"Privacy missing retention: {rel}")
    if not any(x.lower() in low for x in ("poza EOG","outside the EEA","außerhalb des EWR")): errors.append(f"Privacy missing transfer notice: {rel}")
    if not any(x.lower() in low for x in ("podanie danych jest dobrowolne","providing data is voluntary","angabe von daten ist freiwillig")): errors.append(f"Privacy missing voluntary-data notice: {rel}")

pl_private=docs["pl/dla-klienta-prywatnego.html"][0]
for required in ("590 zł — cena końcowa","do 60 minut","3 dni roboczych","2 zł/km","24 godziny","50% ceny"):
    if required not in pl_private: errors.append(f"B2C terms missing: {required}")
if pl_private.count(__import__('build_v10').T['pl']['availability_notice']) < 4: errors.append("Formal-gate notice missing beside B2C prices")
if "kontrola instalacji ani zastępstwo odbioru przez uprawnionego specjalistę" not in pl_private: errors.append("Visible-scope handover boundary missing")
pl_business=docs["pl/dla-firm.html"][0]
for required in ("wartość netto faktycznie koordynowanych pakietów","minimalne wynagrodzenie","limit maksymalny"):
    if required not in pl_business.lower(): errors.append(f"B2B percentage rule missing: {required}")
for lang,home in (("pl","pl/index.html"),("en","en/index.html"),("de","de/index.html")):
    if __import__('build_v10').T[lang]['availability_notice'] not in docs[home][0]: errors.append(f"Formal-gate notice missing on home: {home}")
if __import__('build_v10').T['de']['territory_note'] not in docs['de/privatkunden.html'][0]: errors.append("German foreign-sales limitation missing")
if "ten opis nie wyłącza odpowiedzialności wymaganej prawem" not in pl_private: errors.append("Own-scope liability clarification missing")

# No public or canonical URL uses .html; sitemap excludes utility pages.
for rel,(text,doc) in docs.items():
    for value in doc.canon+[u for _,u in doc.alts]:
        if ".html" in urlsplit(value).path: errors.append(f"HTML extension in SEO URL: {rel}: {value}")
for rel,(text,doc) in docs.items():
    for href in doc.links:
        if href.startswith("/") and ".html" in urlsplit(href).path: errors.append(f"HTML extension in internal link: {rel}: {href}")
sitemap=(ROOT/"sitemap.xml").read_text(encoding="utf-8")
if ".html" in sitemap or "dziekujemy" in sitemap or "thank-you" in sitemap or "danke" in sitemap: errors.append("Sitemap contains extension or utility page")
if sitemap.count("<url>") != 45: errors.append(f"Expected 45 sitemap URLs, found {sitemap.count('<url>')}")

headers=(ROOT/"_headers").read_text(encoding="utf-8") if (ROOT/"_headers").exists() else ""
for h in ("Content-Security-Policy","Strict-Transport-Security","Permissions-Policy","X-Frame-Options","X-Content-Type-Options"):
    if h not in headers: errors.append(f"Missing security header: {h}")
redirects=(ROOT/"_redirects").read_text(encoding="utf-8") if (ROOT/"_redirects").exists() else ""
if "/pl/dla-firm.html /pl/dla-firm 301" not in redirects or "/en/privacy.html /en/privacy 301" not in redirects:
    errors.append("Missing explicit clean-URL redirects")

llms=(ROOT/"llms.txt").read_text(encoding="utf-8") if (ROOT/"llms.txt").exists() else ""
if not llms.startswith("# ") or "non-binding enquiries only" not in llms or "STOLPIN" not in llms:
    errors.append("llms.txt is missing required structure or scope limits")
try:
    catalog=json.loads((ROOT/".well-known/ai-catalog.json").read_text(encoding="utf-8"))
    if catalog.get("specVersion") != "1.0" or not isinstance(catalog.get("entries"),list): errors.append("Invalid AI catalog")
except Exception as exc:
    errors.append(f"Invalid AI catalog JSON: {exc}")

# All deployed web images must be metadata-free.
try:
    from PIL import Image
    for p in list((ROOT/"assets").glob("*.jpg"))+list((ROOT/"assets").glob("*.webp")):
        with Image.open(p) as im:
            if im.getexif(): errors.append(f"Image metadata present: {p.relative_to(ROOT)}")
except ImportError:
    errors.append("Pillow unavailable; image metadata check not executed")

if errors:
    print("FAIL")
    for e in errors: print("-",e)
    sys.exit(1)
print(f"PASS: {len(html_files)} HTML files; links, languages, forms, privacy, pricing, SEO, headers and image metadata verified")
