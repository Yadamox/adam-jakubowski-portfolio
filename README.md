# Strona Adam Jakubowski — v11

Statyczna, trójjęzyczna strona usługowa PL/EN/DE. Produkcja działa na Cloudflare Pages.

## Źródło i generowanie

- Główne źródło treści i szablonów: `build_v10.py`.
- Case study Landbyska Verket: trzy pliki `*/landbyska-verket.html`.
- Style i skrypty: `site-v10.css`, `site-v10.js`, `case-study.css`.
- Nie edytuj ręcznie stron generowanych — następny build je nadpisze.

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
