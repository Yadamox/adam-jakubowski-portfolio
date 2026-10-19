# Strona Adam Jakubowski — v13

Statyczna, trójjęzyczna strona usługowa PL/EN/DE. Produkcja działa na Cloudflare Pages.

## Źródło i generowanie

- Punkt wejścia: `build_v13.py`; cały build jest samowystarczalny w tym repozytorium.
- Treści i bazowe szablony: `build_v10.py`; case study: `case-studies-source.json`.
- Warstwa układu v13: `transform_v13.py`; style i ruch: `site-v13.css`, `site-v13.js`.
- `nojs-v13.css` jest wczytywany wyłącznie przez `noscript`: pełna nawigacja bez JS, bez przeskoku strony przy wczytywaniu skryptu.
- `base_content.py` odczytuje definicje treści przez AST, bez ponownego generowania stron podczas testów.
- `approved-v13-sha256.json` i `test_v13.py` chronią zaakceptowany wygląd oraz treść; różnice techniczne: produkcyjne indeksowanie i wydzielenie fallbacku no-JS.
- Nie edytuj ręcznie stron generowanych — następny build je nadpisze.
- Podglądy v12/v13 i iCloud nie są zależnościami procesu publikacji.

## Testy

```bash
npm install
npm run verify
```

Test obejmuje 65 plików HTML, linki, odpowiedniki językowe, formularze, prywatność, ceny, SEO, nagłówki bezpieczeństwa i metadane zdjęć.

## Pakiet produkcyjny

```bash
npm run release
```

Pakiet powstaje w `../.cloudflare-release`. Zawiera wyłącznie pliki publiczne.

## Wdrożenie

```bash
npx wrangler pages deploy ../.cloudflare-release --project-name adam-jakubowski --branch main
```

Po wdrożeniu sprawdź domenę główną, `www`, adres Pages, routing bez `.html`, nagłówki i Lighthouse. Dane logowania Cloudflare nie mogą trafić do repozytorium.

## Formularze

Formularze nie przesyłają danych do zewnętrznego operatora. Skrypt przygotowuje wiadomość w lokalnym programie pocztowym użytkownika; użytkownik wysyła ją samodzielnie.

## Zasady publikacyjne

- Nie używaj materiałów poufnych ani plików wykluczonych.
- Nie rozszerzaj roli Adama ani STOLPIN ponad udokumentowany zakres.
- Nie usuwaj komunikatu o bramce formalnej, dopóki nie zostanie ona zamknięta.
- Każdą publikację poprzedzaj `npm run release` i kontrolą produkcji.
