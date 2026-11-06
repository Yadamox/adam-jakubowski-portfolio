# Strona Adam Jakubowski — v16

Statyczna witryna PL/EN/DE na Cloudflare Pages. Zewnętrzny PM całego
uzgodnionego projektu, wybranego etapu lub pakietu prac.

## Odtwarzalny build

- `build_v16.py` to produkcyjny punkt wejścia. Nie wymaga podglądów ani iCloud.
- `v16-source/` zawiera generatory, CSS/JS i `base-source.zip` z niezmiennym
  wejściem bazowym. Archiwum jest rozpakowywane wyłącznie do katalogu roboczego.
- `approved-v16-sha256.json`: 93 pliki zaakceptowanego podglądu. Przed konwersją
  produkcyjną każdy z nich musi odtworzyć się identycznie.
- Różnice produkcyjne: usunięte wyłącznie podglądowe noindex/nofollow,
  zachowane noindex podziękowań, publiczny robots/llms, parametr cache JS v16.
- Przywrócono wcześniejsze ograniczenia pominięte w podglądzie: brak
  automatycznego oferowania usług zagranicznych na stronie DE oraz
  odpowiedzialność za własny zakres i brak wyłączenia odpowiedzialności ustawowej.
- `built-v16-sha256.json` kontroluje wynik po konwersji. HTML nie edytuj ręcznie.
- Stare generatory i testy v13 są historyczne; nie służą do budowania v16.

## Testy i publikacja

```bash
npm install
npm run release
npx wrangler pages deploy ../.cloudflare-release --project-name adam-jakubowski --branch main
```

`npm run release` wykonuje build, testy 65 HTML, linków, języków, formularzy,
prywatności, cen, SEO, nagłówków i obrazów; pakiet publiczny trafia do
`../.cloudflare-release`. Źródła, archiwum bazowe i testy nie są publikowane.

Testy przeglądarkowe (Chrome i `puppeteer-core` dostępne lokalnie):

```bash
SITE_URL=https://adam-jakubowski.com node verification/test_browser.cjs
SITE_URL=https://adam-jakubowski.com node verification/test_contact.cjs
SITE_URL=https://adam-jakubowski.com node verification/test_followup.cjs
```

Raporty i zrzuty powstają pod `verification/`, bez włączania do Gita/pakietu.
`RESUME_MATRIX=1` służy wyłącznie do dokończenia przerwanego runnera po
pełnej zaliczonej macierzy; sprawdza kompletność raportu i wersję zdalnego JS.
Domyślnie wykonywana jest pełna macierz od początku.

Po publikacji: odczyt apex, www, Pages i konkretnego wdrożenia; porównanie
z pakietem, wszystkie trasy, formularze i zachowanie mobilne. Lighthouse
uruchamiaj osobno, po zakończeniu testów przeglądarkowych.

## Kontakt i ograniczenia

Formularze przygotowują lokalną wiadomość, pozwalają ją skopiować i wymagają
samodzielnego wysłania. Nie ma backendu wysyłającego ani zewnętrznego operatora.
Testy przechwytują mailto i nie wysyłają wiadomości.

- Bez materiałów poufnych i nieuprawnionego portfolio.
- Zakres doświadczenia STOLPIN nie oznacza portfolio nowej działalności.
- Bramka formalna pozostaje: wyłącznie niezobowiązujące zapytania, bez
  odpłatnych umów, płatności i rezerwacji do zamknięcia formalności.
- Ceny niezależnego doradztwa nie są cennikiem prowadzenia lub wykonania projektu.
