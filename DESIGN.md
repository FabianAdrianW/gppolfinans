# Polfinans Grupa Partnerska — serwis (główna + 6 obszarów + szkoda + prywatność)

Cel: wizytówka i lead page. Styl bazuje na Silu (fixed navbar 80% skali na desktopie, sekcja z przenikaniem tła, formularz), kolory i fonty z Brand Book 7.0.
Wywołane skille: generator-wizytowek, ui-ux-pro-max, humanizer.
Odstępstwa od generator-wizytowek (jak w Silu, decyzja Fabiana i klientki): dużo hoverów i animacji navbaru, bez obrotów obiektów.

## Tokeny (źródło: Brand Book 7.0 / moodboard)
--btn/--wine #8B2E2E Burgund (akcja, 7,9:1 na papierze) · --ink #1E2929 Grafit · --muted #566462 · --paper #F7F4EF · --sand #EEE7DE · --surface #FFF. Tryb ciemny: paper #121818, akcent tekstowy #E3A29A.
Typografia: Source Serif 4 (500) nagłówki, Source Sans 3 (400/600) tekst. Lokalnie, latin + latin-ext (Fontsource, OFL).

## Sygnatura
Zakładka teczki: burgundowa teczka jest na każdym zdjęciu marki, więc krawędzie sekcji ciemnych/piaskowych mają kształt zakładki teczki (.tabbed, clip-path). Moduł "Twoje ustalenia" z moodboardu jako sekcja procesu.

## Ruch i hover
Start: sekwencja hero + osiadanie zdjęcia. Navbar: stała wysokość, linia/cień po scrollu, przesuwany wskaźnik (pigułka), pasek postępu, burger morph, menu mobilne clip-path + stagger.
Przyciski: wypełnienie rozchodzi się od miejsca wejścia kursora.
Hover/ruch: hero 3D tilt + nota w przeciwną stronę; obszary jako indeks z lepką ramką zdjęcia (wipe clip-path, na dotyku automatyczna zmiana); pomoc przy szkodzie jako wiersze z przeciągnięciem tła + ciemna karta pytania; proces "Twoje ustalenia" (auto-przewijanie, zmiana zdjęcia z wipe); pas deklaracji z lekko przechyloną kartką (.slip); o nas z cytatem nachodzącym na zdjęcie; kontakt z dużym numerem telefonu (.bigphone) i listą kanałów; FAQ (animowane), checklisty z licznikiem, linki "Inne obszary". Etykiety nad nagłówkami to pigułki, bez wersalików i kresek. prefers-reduced-motion wyłącza wszystko.

## Zdjęcia
Wszystkie z materiałów klientki (moodboard v7, WhatsApp 22:01:41–44). To ilustracje kierunku marki (generowane), nie zdjęcia zespołu ani biura — przy procesie podpis "Ilustracja kierunku marki". Pominięte: 22:01:45 (wygląda na zdjęcie stockowe z obcej strony), 22:01:46 (niska rozdzielczość).

## Do uzupełnienia (TODO w kodzie)
- Klucz Web3Forms (build.py: WEB3FORMS_KEY). Do tego czasu formularz otwiera program pocztowy (mailto).
- Nr wpisu w rejestrze pośredników KNF (RPU), NIP, pełna nazwa administratora danych (stopka, prywatnosc.html).
- Podpis "Strona: Adrian Wojtasik" w stopce — do potwierdzenia.
- Prawdziwe zdjęcia zespołu/biura, jeśli mają się pojawić.
- Stary telefon 504 031 330 i biuro@gppolfinans.pl nie są używane (wybrano dane z brand booka).
