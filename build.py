#!/usr/bin/env python3
"""Generates the Polfinans site: index + 6 insurance areas + claims help + privacy. Run: python3 build.py"""
import json, pathlib, re
ROOT = pathlib.Path(__file__).parent

PHONE = "+48 504 031 330"; PHONE_TEL = "+48504031330"; PHONE_SHORT = "504 031 330"
MAIL = "biuro@gppolfinans.pl"
ADDR1 = "ul. Metalowców 9, pok. 110"; ADDR2 = "54-156 Wrocław"
MAPS = "https://www.google.com/maps/search/?api=1&query=Metalowc%C3%B3w+9+54-156+Wroc%C5%82aw"
FIRM = "Anna Wojda „POLFINANS”"; NIP = "898-132-68-85"; REGON = "020499082"; KNF_NO = "11200056/A"
KNF_URL = "https://rpu.knf.gov.pl/search/agent/11200056%2FA/353623"
FB = "https://www.facebook.com/Polfinans.ubezpieczenia"
L = "pl"   # current build language, set in main()

ICONS = {
 "home":'<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 "car":'<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
 "heart":'<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
 "plane":'<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
 "briefcase":'<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
 "wheat":'<path d="M2 22 16 8"/><path d="M3.47 12.53 5 11l1.53 1.53a3.5 3.5 0 0 1 0 4.94L5 19l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M7.47 8.53 9 7l1.53 1.53a3.5 3.5 0 0 1 0 4.94L9 15l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M11.47 4.53 13 3l1.53 1.53a3.5 3.5 0 0 1 0 4.94L13 11l-1.53-1.53a3.5 3.5 0 0 1 0-4.94Z"/><path d="M20 2h2v2a4 4 0 0 1-4 4h-2V6a4 4 0 0 1 4-4Z"/><path d="M11.47 17.47 13 19l-1.53 1.53a3.5 3.5 0 0 1-4.94 0L5 19l1.53-1.53a3.5 3.5 0 0 1 4.94 0Z"/><path d="M15.47 13.47 17 15l-1.53 1.53a3.5 3.5 0 0 1-4.94 0L9 15l1.53-1.53a3.5 3.5 0 0 1 4.94 0Z"/><path d="M19.47 9.47 21 11l-1.53 1.53a3.5 3.5 0 0 1-4.94 0L13 11l1.53-1.53a3.5 3.5 0 0 1 4.94 0Z"/>',
 "phone":'<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "mail":'<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
 "pin":'<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
 "arrow":'<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 "check":'<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
 "shield":'<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
 "search":'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><circle cx="11.5" cy="14.5" r="2.5"/><path d="M13.3 16.3 15 18"/>',
 "scale":'<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
 "pen":'<path d="M12 20h9"/><path d="M16.376 3.622a1 1 0 0 1 3.002 3.002L7.368 18.635a2 2 0 0 1-.855.506l-2.872.838a.5.5 0 0 1-.62-.62l.838-2.872a2 2 0 0 1 .506-.854z"/>',
 "buoy":'<circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/><circle cx="12" cy="12" r="4"/>',
 "refresh":'<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
 "compass":'<circle cx="12" cy="12" r="10"/><path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z"/>',
 "user":'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m16 11 2 2 4-4"/>',
 "award":'<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
 "layers":'<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
 "folder":'<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
 "copy":'<rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
}
FB_SVG = '<svg class="fb" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M24 12.07C24 5.41 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.89v2.26h3.32l-.53 3.5h-2.8V24C19.62 23.1 24 18.1 24 12.07"/></svg>'
def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in ICONS.items()) + "</svg>"

# ---------------- Areas ----------------
FAQ_LEAD = "Poniższe odpowiedzi mają charakter ogólny. Szczegółowe zasady postępowania zależą od warunków ubezpieczenia i rodzaju zdarzenia, dlatego każdą sytuację analizujemy indywidualnie."

AREAS = [
 dict(slug="dom-i-majatek", icon="home", img="area-dom", name="Dom i majątek", topic="Dom i majątek",
   card="Mieszkanie, dom, wyposażenie i OC w życiu prywatnym.",
   title="Ubezpieczenie domu i mieszkania", seo="Ubezpieczenie domu i mieszkania, Wrocław",
   lead="Dom to nie tylko mury i wyposażenie, ale również przedmioty i wspomnienia, które mają dla Ciebie szczególną wartość. Pomożemy dobrać odpowiedni zakres ochrony, uwzględniając wartość nieruchomości, jej wyposażenia oraz odpowiedzialność cywilną wobec innych osób. Sprawdzimy również, czy suma ubezpieczenia odpowiada aktualnej wartości Twojego majątku.",
   note=("Wartość, którą budujesz. Ochrona, którą wybierasz.", "Zadbaj o właściwe zabezpieczenie swojego majątku."),
   when_lead="Zakup nieruchomości, wynajem, remont czy zmiana dotychczasowej polisy – każda z tych sytuacji to dobry moment, aby przyjrzeć się zakresowi ubezpieczenia i dopasować go do aktualnych potrzeb.",
   alt="Otwarte drzwi wejściowe domu, na komodzie burgundowa teczka i klucze",
   when=["Kupujesz mieszkanie albo dom na kredyt, a bank wymaga polisy.",
         "Zakończyłeś budowę, remont lub modernizację i chcesz zadbać o aktualną wartość ubezpieczenia nieruchomości.",
         "Masz polisę od lat i nie pamiętasz, co dokładnie obejmuje.",
         "Wynajmujesz mieszkanie lub udostępniasz swoją nieruchomość najemcom.",
         "Kończy się Twoje ubezpieczenie i chcesz porównać dostępne oferty."],
   qs_lead="Aby przygotować ofertę dopasowaną do Twojej nieruchomości, potrzebujemy kilku podstawowych informacji. Nie musisz znać wszystkich odpowiedzi – w razie potrzeby pomożemy Ci je ustalić.",
   qs=[("Co chcesz chronić?","Mury, elementy stałe, wyposażenie, ruchomości domowe oraz budynki gospodarcze znajdujące się na posesji."),
       ("Jak szeroka powinna być ochrona?","Rekomendujemy formułę ALL RISK, która zapewnia szeroki zakres ochrony od nagłych i nieprzewidzianych zdarzeń, z uwzględnieniem wyłączeń określonych w OWU."),
       ("Na jaką wartość ubezpieczyć nieruchomość?","Ustalimy odpowiednią sumę ubezpieczenia, uwzględniając wartość odtworzeniową lub rzeczywistą nieruchomości oraz aktualne koszty jej odbudowy."),
       ("Czy potrzebujesz OC w życiu prywatnym?","To dodatkowa ochrona na wypadek szkód wyrządzonych innym osobom, np. zalania mieszkania sąsiada czy szkody spowodowanej przez dziecko lub zwierzę domowe."),
       ("Z jakiej dodatkowej pomocy możesz skorzystać?","Rozbudowany Assistance to praktyczne wsparcie w codziennych i nagłych sytuacjach. Może obejmować m.in. pomoc hydraulika, elektryka czy ślusarza, wizyty lekarskie, konsultacje specjalistyczne oraz inne usługi – w zależności od oferty towarzystwa ubezpieczeniowego i wybranego wariantu.")],
   prep=["Adres nieruchomości, rok budowy, powierzchnię oraz rodzaj konstrukcji budynku i dachu.",
         "Obecną polisę, jeśli ją posiadasz – wystarczy zdjęcie lub plik PDF.",
         "Przybliżoną wartość wyposażenia i cenniejszych przedmiotów.",
         "Informacje dotyczące kredytu i banku, jeśli ubezpieczenie ma stanowić zabezpieczenie kredytu (cesja na bank).",
         "Rodzaj zastosowanych zabezpieczeń, np. drzwi antywłamaniowe, zamki, alarm czy monitoring.",
         "Dodatkowe instalacje, takie jak fotowoltaika, pompa ciepła czy klimatyzacja.",
         "Informację o zabudowaniach na posesji, np. garażu, budynku gospodarczym czy altanie.",
         "Sposób użytkowania nieruchomości – czy jest zamieszkana na stałe, wynajmowana, użytkowana sezonowo czy pozostaje niezamieszkana."],
   faq=[("Czym różni się wartość odtworzeniowa od rzeczywistej?","Wartość odtworzeniowa oznacza koszt odbudowy nieruchomości lub zakupu nowej rzeczy tego samego rodzaju i o podobnych parametrach. Wartość rzeczywista uwzględnia również stopień zużycia, co może oznaczać niższe odszkodowanie. Pomożemy Ci ustalić, która metoda wyceny będzie odpowiednia dla Twojej nieruchomości i wyposażenia."),
        ("Czy polisa wymagana przez bank wystarczy?","Niekoniecznie. Polisa wymagana przez bank zabezpiecza przede wszystkim interesy kredytodawcy i najczęściej obejmuje mury nieruchomości. Warto sprawdzić, czy zapewnia również ochronę wyposażenia, elementów stałych i OC w życiu prywatnym. W razie potrzeby pomożemy rozszerzyć zakres ubezpieczenia."),
        ("Czy da się ubezpieczyć dom w budowie?","Tak. Towarzystwa oferują ubezpieczenia przeznaczone dla nieruchomości w trakcie budowy. Zakres ochrony i warunki zawarcia polisy zależą m.in. od etapu prac, stanu zaawansowania budowy oraz zabezpieczenia obiektu.")]),
 dict(slug="samochod", icon="car", img="area-samochod", name="Samochód", topic="Samochód",
   card="OC, AC, assistance i to, jak naprawdę używasz auta.",
   title="Ubezpieczenie samochodu", seo="Ubezpieczenie samochodu OC i AC, Wrocław",
   lead="OC jest obowiązkowe, natomiast zakres ochrony może być znacznie szerszy – w zależności od Twoich potrzeb i sposobu użytkowania auta. Porównamy oferty kilku towarzystw, aby pomóc Ci wybrać najlepsze rozwiązanie.",
   note=("Właściwa ochrona zaczyna się od dobrego wyboru.", "Spokojna podróż. Bezpieczny powrót."),
   when_lead="Różne sytuacje na drodze wymagają różnego zakresu ochrony.",
   alt="Mężczyzna wkłada torbę do bagażnika samochodu przed domem",
   when=["Kupujesz samochód – nowy lub używany.",
         "Zbliża się termin zakończenia obecnej polisy OC lub AC.",
         "Finansujesz samochód leasingiem lub kredytem.",
         "Zmienia się sposób użytkowania auta, np. zaczynasz wykorzystywać je do celów służbowych lub częściej podróżujesz za granicę."],
   qs_lead="Aby przygotować odpowiednią ofertę, potrzebujemy kilku informacji, które pozwolą nam dopasować zakres ubezpieczenia do Twojego samochodu i sposobu jego użytkowania.",
   qs=[("Kto i w jaki sposób korzysta z samochodu?","Uwzględnimy wiek kierowców, przebieg oraz sposób użytkowania auta."),
       ("Czy warto rozszerzyć ochronę o AC?","Porównamy wartość i wiek samochodu z kosztem ubezpieczenia, zakresem ochrony oraz ewentualnym udziałem własnym w szkodzie."),
       ("Na jakich zasadach zostanie wypłacone odszkodowanie?","Sprawdzimy sposób likwidacji szkody – wariant serwisowy lub kosztorysowy, a także zasady stosowania części oryginalnych i zamiennych."),
       ("Jakiego Assistance potrzebujesz?","Ustalimy zakres pomocy na drodze, m.in. warunki i limit holowania w Polsce i za granicą oraz możliwość skorzystania z samochodu zastępczego."),
       ("Czy przydadzą Ci się dodatkowe ubezpieczenia?","NNW, ubezpieczenie szyb czy ochrona zniżek mogą stanowić wartościowe uzupełnienie polisy. Wyjaśnimy, co obejmują i kiedy warto z nich skorzystać.")],
   prep=["<strong>Dane właściciela pojazdu</strong> – imię, nazwisko, adres zamieszkania; podstawowe dane potrzebne do przygotowania kalkulacji.",
         "<strong>Dowód rejestracyjny</strong> – marka, model, rok produkcji i numer VIN. Najlepiej przygotować zdjęcie lub skan obu stron dokumentu.",
         "<strong>Obecną polisę OC lub AC</strong>, jeśli ją posiadasz.",
         "<strong>Datę urodzenia kierowcy oraz rok uzyskania prawa jazdy.</strong>",
         "<strong>Informacje o szkodach z ostatnich lat</strong>, jeśli występowały.",
         "<strong>Aktualny przebieg pojazdu.</strong>"],
   faq=[("Czy OC przedłuża się automatycznie?","Obowiązkowe OC zawarte na 12 miesięcy co do zasady przedłuża się automatycznie na kolejny rok, jeśli nie zostanie wypowiedziane najpóźniej na jeden dzień przed końcem umowy. Są jednak wyjątki, np. polisa poprzedniego właściciela kupionego samochodu nie przedłuża się automatycznie. Warto więc sprawdzić termin końca ochrony i porównać dostępne oferty."),
        ("Co z OC przy zakupie używanego auta?","Polisa OC poprzedniego właściciela przechodzi na nowego właściciela i obowiązuje do końca okresu, na jaki została zawarta. Możesz z niej korzystać albo ją wypowiedzieć i zawrzeć własną umowę. Pamiętaj, że ubezpieczyciel może dokonać ponownej kalkulacji składki."),
        ("Czym różni się wariant warsztatowy od kosztorysowego?","W wariancie warsztatowym naprawa rozliczana jest na podstawie faktur za wykonane prace i użyte części, zgodnie z warunkami polisy. W wariancie kosztorysowym ubezpieczyciel ustala wysokość odszkodowania na podstawie własnej wyceny, a środki otrzymujesz bezpośrednio na konto. Kwota może nie pokryć pełnego kosztu naprawy w wybranym serwisie.")]),
 dict(slug="zycie", icon="heart", img="area-zycie", name="Życie", topic="Życie",
   card="Bliscy, kredyt i zobowiązania, które zostają na lata.",
   title="Ubezpieczenie na życie", seo="Ubezpieczenie na życie, Wrocław",
   lead="To ochrona dla Ciebie i osób, które są dla Ciebie najważniejsze. Zapewnia finansowe wsparcie bliskim, pomaga zabezpieczyć zobowiązania i daje poczucie bezpieczeństwa na przyszłość.<br class='keep'><br class='keep'>Zakres polisy możemy rozszerzyć o dodatkowe pakiety chroniące m.in. na wypadek poważnego zachorowania, pobytu w szpitalu czy następstw nieszczęśliwych wypadków (NNW). Dostępne rozwiązania mogą obejmować również assistance, zapewniające praktyczną pomoc medyczną i organizacyjną w trudnych sytuacjach.<br class='keep'><br class='keep'>Dobierzemy sumę ubezpieczenia i zakres ochrony do Twojej sytuacji, potrzeb rodziny, zobowiązań finansowych i planów na przyszłość.<br class='keep'><br class='keep'><strong>Zadbaj o bezpieczeństwo swoje i tych, na których Ci zależy.</strong>",
   note=("Zabezpiecz dziś to, co ważne jutro.", "Z myślą o tych, którzy są dla Ciebie najważniejsi."),
   when_lead="W życiu pojawiają się momenty, w których warto pomyśleć o dodatkowym zabezpieczeniu.<br><br>Ubezpieczenie na życie warto rozważyć szczególnie wtedy, gdy:",
   alt="Rodzina przygotowuje razem posiłek w kuchni",
   when=["Masz rodzinę i chcesz zapewnić bliskim zabezpieczenie finansowe.",
         "Planujesz zakup mieszkania lub spłacasz kredyt hipoteczny.",
         "Twoje dochody stanowią ważną część domowego budżetu.",
         "Prowadzisz własną firmę i odpowiadasz nie tylko za siebie, ale również za jej zobowiązania.",
         "Zmieniasz pracę i tracisz dotychczasowe ubezpieczenie grupowe.",
         "Chcesz zabezpieczyć się finansowo na wypadek poważnej choroby lub długotrwałego leczenia.",
         "Masz już polisę, ale nie wiesz, czy jej suma i zakres nadal odpowiadają Twojej sytuacji."],
   qs_lead="Aby przygotować odpowiednią ofertę, potrzebujemy kilku informacji, które pozwolą nam dopasować sumę ubezpieczenia i zakres ochrony do Twojej sytuacji, potrzeb oraz planów na przyszłość.",
   qs=[("Kogo chcesz zabezpieczyć?","Partnera, dzieci, innych bliskich, a może również wspólnika lub firmę? Warto określić, kto powinien otrzymać wsparcie finansowe w razie Twojej śmierci."),
       ("Jaka suma ubezpieczenia będzie odpowiednia?","Powinna uwzględniać wysokość zobowiązań, potrzeby rodziny i środki, które pozwolą bliskim utrzymać dotychczasowy poziom życia przez określony czas."),
       ("Jakie sytuacje powinna obejmować ochrona?","Oprócz śmierci warto rozważyć poważne zachorowanie, niezdolność do pracy, trwały uszczerbek na zdrowiu czy pobyt w szpitalu."),
       ("Jak długo potrzebujesz ochrony?","Może to być okres spłaty kredytu, czas do usamodzielnienia się dzieci lub dłuższy okres, obejmujący również lata przed emeryturą."),
       ("Polisa indywidualna czy grupowa?","Ubezpieczenie grupowe z pracy może być dobrym rozwiązaniem, ale warto sprawdzić jego zakres, sumy ubezpieczenia i możliwość kontynuacji po zmianie pracodawcy. Polisę indywidualną można natomiast dopasować do własnych potrzeb i zobowiązań.")],
   prep=["Podstawowe dane osobowe, w tym wiek.",
         "Informacje o rodzinie i osobach, które chcesz zabezpieczyć finansowo.",
         "Wysokość kredytów i innych zobowiązań oraz okres pozostały do ich spłaty.",
         "Informacje o obecnych ubezpieczeniach na życie, również grupowych z pracy.",
         "Ogólne informacje o stanie zdrowia i historii leczenia – zgodnie z pytaniami w ankiecie medycznej ubezpieczyciela.",
         "Twoje oczekiwania – czy zależy Ci przede wszystkim na zabezpieczeniu bliskich, ochronie na wypadek poważnej choroby, czy również na dodatkowych świadczeniach."],
   faq=[("Czym różni się polisa indywidualna od grupowej?","Ubezpieczenie grupowe jest zazwyczaj oferowane przez pracodawcę i zapewnia ochronę na określonych warunkach. Może jednak wygasnąć po zakończeniu zatrudnienia. Polisa indywidualna jest zawierana bezpośrednio z ubezpieczycielem, a jej zakres i sumę ubezpieczenia można dopasować do własnych potrzeb."),
        ("Czy polisę można scedować na bank?","Tak. Przy kredycie hipotecznym bank może wymagać cesji praw z polisy na życie. Oznacza to, że w razie śmierci ubezpieczonego bank może otrzymać świadczenie do wysokości pozostałego zadłużenia, zgodnie z warunkami cesji. Ewentualna nadwyżka może przypaść uprawnionym osobom."),
        ("Czy przed zawarciem polisy trzeba przechodzić badania lekarskie?","Nie zawsze. W wielu przypadkach wystarczy wypełnienie ankiety medycznej dotyczącej stanu zdrowia i historii leczenia. Przy wyższych sumach ubezpieczenia, określonym wieku lub wskazaniach wynikających z ankiety ubezpieczyciel może jednak zlecić dodatkowe badania lub konsultacje.")]),
 dict(slug="podroze", icon="plane", img="area-podroze", name="Podróże", topic="Podróże",
   card="Urlop, narty, praca za granicą. Leczenie, bagaż, rezygnacja.",
   title="Ubezpieczenie turystyczne", seo="Ubezpieczenie turystyczne na wyjazd, Wrocław",
   lead="Urlop, wyjazd na narty, a może praca za granicą? Każda podróż wiąże się z innymi potrzebami. Pomożemy dobrać zakres ubezpieczenia do celu wyjazdu, planowanych aktywności i miejsca pobytu.",
   note=("Podróżuj, odkrywaj, doświadczaj.", "O ochronę zadbaj przed wyjazdem."),
   when_lead="Każda podróż jest inna. Niezależnie od jej celu, warto zadbać o odpowiednią ochronę.",
   alt="Słomkowy kapelusz, okulary, aparat, walizka, mapa i paszport na stole, w tle startujący samolot",
   when=["Planujesz urlop za granicą i chcesz zabezpieczyć się na wypadek kosztów leczenia lub nieprzewidzianych zdarzeń.",
         "Wybierasz się na narty, trekking w górach, nurkowanie lub uprawiasz inne aktywności wymagające rozszerzonej ochrony.",
         "Wyjeżdżasz za granicę do pracy, szczególnie fizycznej, i potrzebujesz zakresu uwzględniającego charakter wykonywanych obowiązków.",
         "Podróżujesz kilka razy w roku – ubezpieczenie roczne może okazać się korzystniejsze niż kupowanie osobnej polisy na każdy wyjazd.",
         "Podróżujesz z rodziną i chcesz zadbać o ochronę wszystkich uczestników wyjazdu.",
         "Organizujesz dłuższy wyjazd lub podróż do kraju, w którym koszty leczenia są szczególnie wysokie."],
   qs_lead="Aby przygotować odpowiednią ofertę, potrzebujemy kilku informacji, które pozwolą nam dopasować zakres ubezpieczenia do kierunku, czasu trwania i charakteru Twojego wyjazdu.",
   qs=[("Dokąd i na jak długo podróżujesz?","Znaczenie ma nie tylko kierunek wyjazdu, ale również czas pobytu. Innego zakresu ochrony możesz potrzebować podczas podróży po Europie, a innego w krajach, w których koszty leczenia są bardzo wysokie, np. w USA."),
       ("Jaka suma kosztów leczenia będzie odpowiednia?","Powinna uwzględniać koszty leczenia szpitalnego, wizyt lekarskich, zabiegów i transportu medycznego. Szczególnie ważne jest to podczas wyjazdów poza Europę."),
       ("Jakie aktywności planujesz?","Narty, wspinaczka wysokogórska, nurkowanie czy inne sporty mogą wymagać rozszerzenia ochrony. Ważne, aby zakres polisy odpowiadał rzeczywistemu charakterowi wyjazdu."),
       ("Czy potrzebujesz dodatkowej ochrony?","Ubezpieczenie bagażu, OC w życiu prywatnym, następstw nieszczęśliwych wypadków (NNW) czy kosztów rezygnacji z podróży mogą okazać się przydatne, szczególnie przy droższych wyjazdach."),
       ("Czy uwzględniono choroby przewlekłe?","Jeśli chorujesz przewlekle, sprawdź, czy polisa obejmuje zaostrzenie choroby lub nagłe pogorszenie stanu zdrowia podczas podróży. Niekiedy wymaga to dodatkowego rozszerzenia.")],
   prep=["Kraj, do którego podróżujesz, oraz datę wyjazdu i powrotu.",
         "Dane wszystkich uczestników wyjazdu.",
         "Cel podróży – wypoczynek, sport, praca czy inny rodzaj wyjazdu.",
         "Planowane aktywności, np. uprawiane sporty i dyscypliny podwyższonego ryzyka.",
         "Koszt podróży, jeśli chcesz objąć ochroną koszty rezygnacji lub przerwania wyjazdu."],
   faq=[("Czy karta EKUZ wystarczy?","EKUZ zapewnia dostęp do niezbędnej opieki zdrowotnej w publicznym systemie ochrony zdrowia krajów UE, EFTA i Szwajcarii, na zasadach obowiązujących osoby ubezpieczone w danym kraju. Nie pokrywa jednak wszystkich kosztów leczenia, transportu medycznego do Polski ani co do zasady leczenia w prywatnych placówkach. Dlatego warto uzupełnić ją o ubezpieczenie turystyczne."),
        ("Czy mogę kupić polisę, gdy jestem już za granicą?","Niektóre towarzystwa umożliwiają zakup ubezpieczenia już podczas podróży. Trzeba jednak sprawdzić warunki zawarcia umowy, ponieważ może obowiązywać karencja, a zakres ochrony może być ograniczony. Najbezpieczniej wykupić polisę jeszcze przed wyjazdem."),
        ("Kiedy ubezpieczyć koszty rezygnacji z wyjazdu?","Najlepiej zrobić to zaraz po dokonaniu rezerwacji lub zakupie wyjazdu. Ubezpieczyciele określają własne terminy zawarcia takiej umowy, dlatego warto sprawdzić je przed zakupem. Zbyt późne wykupienie polisy może oznaczać brak możliwości objęcia rezerwacji ochroną.")]),
 dict(slug="firma", icon="briefcase", img="area-firma", name="Firma", topic="Firma",
   card="Majątek, OC działalności i ciągłość pracy po szkodzie.",
   title="Ubezpieczenie firmy", seo="Ubezpieczenie firmy i OC działalności, Wrocław",
   lead="Majątek, pracownicy, odpowiedzialność wobec klientów i ciągłość działania – to obszary, które wymagają odpowiedniej ochrony. Zaczynamy od poznania Twojej działalności i oceny ryzyk, które mogą mieć największe znaczenie dla firmy.",
   note=("Chroń to, co budujesz każdego dnia.", "Zabezpiecz swoją firmę i skup się na jej rozwoju."),
   when_lead="<strong>Ubezpieczenie firmy warto rozważyć szczególnie wtedy, gdy:</strong>",
   alt="Dwoje rzemieślników ogląda drewnianą ramę w warsztacie",
   when=["Zakładasz działalność gospodarczą lub otwierasz nową lokalizację.",
         "Kontrahent lub warunki przetargu wymagają od Ciebie posiadania OC.",
         "Kupujesz maszyny, sprzęt lub samochody wykorzystywane w firmie.",
         "Zatrudniasz pracowników i chcesz zadbać o ochronę firmy oraz osób, które ją tworzą.",
         "Rozwijasz działalność, a dotychczasowe polisy nie uwzględniają już skali i charakteru Twojego biznesu."],
   qs_lead="Aby przygotować odpowiednią ofertę, potrzebujemy kilku informacji, które pozwolą nam dopasować zakres ubezpieczenia do rodzaju prowadzonej działalności, specyfiki Twojej firmy i związanych z nią ryzyk.",
   qs=[("Co obejmuje majątek Twojej firmy?","Lokal, maszyny, urządzenia, towar, sprzęt elektroniczny czy gotówka."),
       ("Za co odpowiadasz wobec innych?","OC z tytułu prowadzenia działalności, OC za produkt lub OC zawodowe – zależnie od charakteru firmy."),
       ("Co, jeśli działalność zostanie czasowo przerwana?","Ubezpieczenie utraty zysku po szkodzie, np. pożarze lub zalaniu, oraz stałych kosztów, które firma nadal musi ponosić."),
       ("Jak zadbać o ochronę pracowników?","Ubezpieczenia grupowe oraz NNW dla pracowników."),
       ("Czy Twoja firma korzysta z pojazdów lub przewozi towary?","Ubezpieczenie pojazdów firmowych oraz przewożonych ładunków.")],
   prep=["Kod PKD oraz krótki opis prowadzonej działalności.",
         "Informacje o majątku firmy, w tym wartość lokalu, maszyn, urządzeń i towaru.",
         "Przybliżony roczny obrót oraz liczbę zatrudnionych pracowników.",
         "Informacje o obecnych polisach oraz umowach lub wymaganiach kontrahentów, które wiążą się z koniecznością posiadania ubezpieczenia.",
         "Informacje o szkodach z ostatnich lat, jeśli wystąpiły."],
   faq=[("Czy OC działalności jest obowiązkowe?","W niektórych zawodach obowiązkowe jest ubezpieczenie odpowiedzialności cywilnej z tytułu wykonywania określonego zawodu, np. u doradców podatkowych, lekarzy czy pośredników nieruchomości. W pozostałych branżach OC działalności jest dobrowolne, ale jego posiadania mogą wymagać kontrahenci lub warunki przetargu."),
        ("Co to jest ubezpieczenie utraty zysku?","Chroni firmę przed skutkami finansowymi przerwy w działalności spowodowanej szkodą objętą ochroną, np. pożarem lub zalaniem. Może obejmować utracony zysk oraz stałe koszty, które firma nadal musi ponosić mimo przestoju. Ubezpieczenie to najczęściej zawierane jest jako rozszerzenie polisy majątkowej."),
        ("Czy ubezpieczacie również jednoosobowe działalności gospodarcze?","Tak. Zakres ubezpieczenia i sumy ochrony dopasowujemy do rodzaju oraz skali prowadzonej działalności, uwzględniając rzeczywiste potrzeby przedsiębiorcy.")]),
 dict(slug="gospodarstwo", icon="wheat", img="area-gospodarstwo", name="Gospodarstwo", topic="Gospodarstwo",
   card="Budynki, maszyny, uprawy i obowiązkowe OC rolnika.",
   title="Ubezpieczenie gospodarstwa rolnego", seo="Ubezpieczenie gospodarstwa rolnego i OC rolnika",
   lead="Budynki, maszyny, zwierzęta i uprawy, a także obowiązkowe OC rolnika.<br> Pomożemy Ci ustalić, jakie ubezpieczenia są wymagane przepisami, a jakie warto dobrać do specyfiki i skali prowadzonego gospodarstwa.",
   note=("Z myślą o Twojej pracy.", "Ochrona na każdą porę roku."),
   when_lead="Gospodarstwo ma swoją wartość.<br><strong>Budynki, maszyny, zwierzęta i uprawy.</strong><br>Zadbaj o ich ochronę.",
   alt="Pola uprawne w pasach, w tle budynki gospodarcze i silosy",
   when=["Przejmujesz gospodarstwo lub kupujesz grunty rolne.",
         "Budujesz nowy budynek gospodarczy albo inwestujesz w maszyny i sprzęt rolniczy.",
         "Chcesz zabezpieczyć uprawy przed skutkami gradu, przymrozków lub suszy.",
         "Zbliża się termin zawarcia obowiązkowych ubezpieczeń rolnych."],
   qs_lead="Aby przygotować odpowiednią ofertę, potrzebujemy kilku informacji, które pozwolą nam dopasować zakres ubezpieczenia do rodzaju prowadzonej działalności rolniczej, wielkości gospodarstwa i jego specyfiki.",
   qs=[("Jakie ubezpieczenia są obowiązkowe w Twoim przypadku?","OC rolnika oraz ubezpieczenie budynków wchodzących w skład gospodarstwa rolnego."),
       ("Jakie budynki wchodzą w skład gospodarstwa i ile są warte?","Dom mieszkalny, budynki inwentarskie, magazyny, stodoły i wiaty."),
       ("Jakie maszyny i sprzęt wykorzystujesz w gospodarstwie?","Ciągniki, kombajny, maszyny samobieżne i przyczepiane."),
       ("Jakie uprawy prowadzisz i jakie zwierzęta hodujesz?","Możliwości ubezpieczenia upraw od ryzyk pogodowych i zwierząt gospodarskich, a także dostępne dopłaty do składek."),
       ("Czy prowadzisz dodatkową działalność?","Agroturystykę, sprzedaż bezpośrednią lub przetwórstwo produktów rolnych.")],
   prep=["Powierzchnię gospodarstwa oraz areał gruntów rolnych.",
         "Wykaz budynków gospodarczych wraz z ich przybliżoną wartością.",
         "Informację o posiadanych maszynach i pojazdach rolniczych.",
         "Rodzaj prowadzonych upraw oraz gatunki i liczbę utrzymywanych zwierząt.",
         "Informację o obecnych polisach ubezpieczeniowych, jeśli je posiadasz."],
   faq=[("Które ubezpieczenia rolnika są obowiązkowe?","Obowiązkowe są dwa ubezpieczenia: OC rolnika z tytułu posiadania gospodarstwa rolnego oraz ubezpieczenie budynków wchodzących w skład gospodarstwa od ognia i innych zdarzeń losowych. Dodatkowo rolnicy otrzymujący dopłaty bezpośrednie mają obowiązek ubezpieczenia co najmniej 50% powierzchni upraw objętych dopłatami od przynajmniej jednego z wymaganych ryzyk."),
        ("Kogo dotyczy obowiązek ubezpieczenia OC i budynków?","Właścicieli i posiadaczy gospodarstw rolnych o powierzchni przekraczającej 1 ha użytków rolnych, podlegających opodatkowaniu podatkiem rolnym, a także osób prowadzących działy specjalne produkcji rolnej – niezależnie od powierzchni gospodarstwa. W przypadku zmiany posiadacza gospodarstwa prawa i obowiązki wynikające z zawartych umów ubezpieczenia przechodzą na nowego posiadacza."),
        ("Czy do ubezpieczenia upraw są dopłaty?","Tak. Państwo dofinansowuje składki ubezpieczenia wybranych upraw i zwierząt gospodarskich. Wysokość dopłat może sięgać 65% składki, a ich przyznanie zależy od rodzaju uprawy, zwierząt i zakresu ochrony określonego w aktualnych przepisach.")]),
]
BY = {a["slug"]: a for a in AREAS}

CLAIMS = dict(slug="pomoc-przy-szkodzie", img="step-1", name="Pomoc przy szkodzie", topic="Szkoda",
   title="Pomoc przy szkodzie", seo="Pomoc przy zgłoszeniu szkody i likwidacji, Wrocław",
   lead="Szkoda to zły moment na czytanie warunków polisy. Zadzwoń do nas, a pomożemy Ci ustalić, jak zgłosić szkodę, jakie dokumenty przygotować i na co zwrócić uwagę w kontakcie z towarzystwem ubezpieczeniowym.",
   alt="Kobieta wypełnia dokument przy stole, obok burgundowa teczka",
   steps=[("Zadbaj o bezpieczeństwo","W pierwszej kolejności zadbaj o ludzi i zwierzęta. Jeśli to konieczne i bezpieczne, odetnij dopływ wody lub prądu. W razie zagrożenia życia lub zdrowia wezwij odpowiednie służby."),
          ("Ogranicz rozmiar szkody","Podejmij rozsądne działania, aby zapobiec dalszym zniszczeniom. Pamiętaj, że obowiązek ograniczania skutków szkody może wynikać z warunków ubezpieczenia."),
          ("Zadbaj o dokumentację","Zrób zdjęcia uszkodzeń – zarówno całego miejsca zdarzenia, jak i szczegółów. Jeśli to możliwe, udokumentuj szkodę przed rozpoczęciem napraw lub usuwaniem zniszczonych rzeczy."),
          ("Powiadom odpowiednie służby","W przypadku kradzieży lub włamania zgłoś zdarzenie policji. Jeśli są osoby ranne, wezwij pomoc. Przy zalaniu poinformuj administrację budynku lub zarządcę nieruchomości."),
          ("Skontaktuj się z nami","Podpowiemy, jakie kroki podjąć, pomożemy przygotować zgłoszenie i przypomnimy o terminach wynikających z warunków Twojej polisy.")],
   prep=["Numer polisy lub nazwę towarzystwa ubezpieczeniowego",
         "Datę, miejsce i krótki opis zdarzenia",
         "Zdjęcia dokumentujące uszkodzenia",
         "Dane drugiej strony oraz oświadczenie sprawcy – w przypadku kolizji",
         "Numer notatki lub protokołu policji – jeśli policja interweniowała",
         "Rachunki, faktury lub inne dokumenty potwierdzające wartość utraconych lub uszkodzonych rzeczy",
         "Numer rachunku bankowego do wypłaty odszkodowania"],
   faq=[("Ile mam czasu na zgłoszenie szkody?","Termin zależy od rodzaju ubezpieczenia i zapisów ogólnych warunków ubezpieczenia. W niektórych przypadkach na zgłoszenie jest niewiele czasu. Kradzież lub włamanie należy niezwłocznie zgłosić policji, zgodnie z wymaganiami polisy. Nie zwlekaj z kontaktem – pomożemy Ci ustalić, jakie terminy obowiązują w Twojej sytuacji."),
        ("Co zrobić, jeśli nie zgadzam się z decyzją towarzystwa ubezpieczeniowego?","Jeśli nie zgadzasz się z decyzją, możesz złożyć reklamację i przedstawić argumenty przemawiające za ponownym rozpatrzeniem sprawy. Pomożemy Ci przeanalizować decyzję, przygotować uzasadnienie i skompletować dokumenty. W przypadku sporu możesz również skorzystać z pomocy Rzecznika Finansowego."),
        ("Czy z OC sprawcy przysługuje mi samochód zastępczy?","Możesz ubiegać się o pokrycie kosztów wynajmu samochodu zastępczego, jeśli korzystanie z niego było uzasadnione i niezbędne na czas naprawy lub w okresie, w którym Twój samochód nie nadawał się do użytkowania.")])

TOPICS = [a["topic"] for a in AREAS] + ["Szkoda", "Analiza obecnych polis", "Inne / jeszcze nie wiem"]

# ---------------- Partials ----------------
def head(title, desc, canonical, extra=""):
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="only light">
<meta name="theme-color" content="#F7F4EF">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="img/hero-dom.webp">
<link rel="canonical" href="https://gppolfinans.pl/{"en/" if L == "en" else ""}{canonical}">
<link rel="alternate" hreflang="pl" href="https://gppolfinans.pl/{canonical}">
<link rel="alternate" hreflang="en" href="https://gppolfinans.pl/en/{canonical}">
<link rel="alternate" hreflang="x-default" href="https://gppolfinans.pl/{canonical}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%238B2E2E'/%3E%3Ctext x='16' y='23' font-family='Georgia,serif' font-size='21' text-anchor='middle' fill='%23F7F4EF'%3Ep%3C/text%3E%3C/svg%3E">
<link rel="preload" href="fonts/source-serif-4-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/source-sans-3-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css?v=1794229000">
{extra}</head>
<body>
<a class="skip" href="#main">Przejdź do treści</a>
{SPRITE}
'''

LOGO = '<span class="logo__word">polf<i>i</i>nans</span><span class="logo__sub">Grupa Partnerska</span>'

def nav(home=True, current=None, page=""):
    p = "" if home else "index.html"
    items = [("obszary","Ubezpieczenia"),("proces","Nasze podejście"),("szkoda","Szkoda"),("o-nas","O nas"),("kontakt","Kontakt")]
    def cur(k):
        if current == k: return ' aria-current="page"'
        return ""
    lis = "".join(f'<li><a href="{p}#{k}"{cur(k)}>{t}</a></li>' for k, t in items)
    drawer = "".join(f'<a href="{p}#{k}">{t}</a>' for k, t in items)
    return f'''<header class="nav" id="nav">
  <div class="nav__inner">
    <a class="logo" href="{'#top' if home else 'index.html'}" aria-label="Polfinans Grupa Partnerska, strona główna">{LOGO}</a>
    <ul class="nav__links" id="navLinks">{lis}<span class="nav__indicator" aria-hidden="true"></span></ul>
    <div class="nav__actions">
      {lang_switch(page)}
      <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Otwórz menu"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="progress" aria-hidden="true"></div>
</header>
<nav class="drawer" id="drawer" aria-label="Menu">
  {drawer}
</nav>
'''

def lang_switch(page):
    pl_href = ("../" + page) if L == "en" else "#top"
    en_href = "#top" if L == "en" else ("en/" + page)
    if L == "en" and not page: pl_href = "../"
    if L == "pl" and not page: en_href = "en/"
    cur_pl = ' aria-current="true"' if L == "pl" else ""
    cur_en = ' aria-current="true"' if L == "en" else ""
    return (f'<div class="lang{" lang--en" if L == "en" else ""}" role="group" aria-label="Język / Language">'
            f'<a class="lang__opt" href="{pl_href}" lang="pl" hreflang="pl"{cur_pl} title="Polski">PL</a>'
            f'<a class="lang__opt" href="{en_href}" lang="en" hreflang="en"{cur_en} title="English">EN</a>'
            '<span class="lang__pill" aria-hidden="true"></span></div>')

def contact(topic=""):
    opts = '<option value="">Wybierz temat</option>' + "".join(f'<option{" selected" if t == topic else ""}>{t}</option>' for t in TOPICS)
    return f'''<section class="section contact tabbed" id="kontakt" aria-labelledby="contact-title">
  <div class="wrap contact__grid">
    <div>
      <span class="eyebrow">Kontakt</span>
      <h2 id="contact-title" style="margin-top:1.1rem">Porozmawiajmy o tym, co chcesz chronić</h2>
      <p class="contact__lead">Zadzwoń, napisz lub zostaw wiadomość w formularzu. Skontaktujemy się z Tobą, aby porozmawiać o tym, jak możemy Ci pomóc.</p>
      <a class="bigphone" href="tel:{PHONE_TEL}"><small>{ic("phone")}Zadzwoń</small><span>{PHONE}</span></a>
      <ul class="lines">
        <li><a class="line" href="mailto:{MAIL}" data-copy="{MAIL}">{ic("mail")}<div><small>E-mail</small><span>{MAIL}</span></div><span class="line__go">{ic("arrow")}</span></a></li>
        <li><a class="line" href="{MAPS}" target="_blank" rel="noopener">{ic("pin")}<div><small>Biuro</small><span>{ADDR1}, {ADDR2}</span></div><span class="line__go">{ic("arrow")}</span></a></li>
      </ul>
    </div>
    <form class="form" id="form" novalidate data-mail="{MAIL}">
      <h3>Napisz do nas</h3>
      <div class="form__pair">
        <div class="field" id="f-name">
          <label for="name">Imię i nazwisko <i aria-hidden="true">*</i></label>
          <input id="name" name="name" autocomplete="name" required aria-describedby="name-err">
          <span class="field__error" id="name-err" aria-live="polite"></span>
        </div>
        <div class="field" id="f-reach">
          <label for="reach">Telefon lub e-mail</label>
          <input id="reach" name="reach" autocomplete="tel" inputmode="email" aria-describedby="reach-hint">
          <span class="form__note" id="reach-hint">Tak, żebyśmy mogli odpowiedzieć.</span>
        </div>
      </div>
      <div class="field">
        <label for="topic">Czego dotyczy sprawa?</label>
        <select id="topic" name="topic">{opts}</select>
      </div>
      <div class="field">
        <label for="msg">Wiadomość</label>
        <textarea id="msg" name="msg" placeholder="Np. kupuję mieszkanie i bank wymaga polisy"></textarea>
      </div>
      <input class="hp" type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div>
        <label class="consent"><input type="checkbox" id="consent" required aria-describedby="consent-err"> <span>Zgadzam się na przetwarzanie podanych danych w celu odpowiedzi na wiadomość. Więcej w <a href="prywatnosc.html">polityce prywatności</a>.</span></label>
        <span class="field__error" id="consent-err" aria-live="polite"></span>
      </div>
      <button class="btn btn--primary" type="submit">Wyślij wiadomość {ic("arrow")}</button>
      <p class="form__status" id="status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
'''

def footer(home=True, has_contact=True):
    p = "" if home else "index.html"
    k = "#kontakt" if has_contact else "index.html#kontakt"
    areas = "".join(f'<li><a href="{a["slug"]}.html">{a["name"]}</a></li>' for a in AREAS)
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer__cta">
      <p class="footer__ask">Sprawdź, czy Twoje ubezpieczenie naprawdę Cię chroni.</p>
      <a class="btn btn--primary" href="{k}" data-topic="Analiza obecnych polis">Porozmawiajmy {ic("arrow")}</a>
    </div>
    <div class="footer__grid">
      <div>
        <a class="logo" href="{p or '#top'}" aria-label="Polfinans, strona główna">{LOGO}</a>
        <p class="footer__motto">Bezpieczeństwo to kwestia wyboru.<br>Dobre decyzje to spokojna przyszłość.</p>
        <p class="footer__promise">{ic("shield")}<span>Twoje bezpieczeństwo to nasz priorytet.</span></p>
      </div>
      <div><h3>Ubezpieczenia</h3><ul>{areas}<li><a href="pomoc-przy-szkodzie.html">Pomoc przy szkodzie</a></li></ul></div>
      <div><h3>Kontakt</h3><ul>
        <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
        <li><a href="mailto:{MAIL}">{MAIL}</a></li>
        <li><a href="{MAPS}" target="_blank" rel="noopener">{ADDR1}, {ADDR2}</a></li>
        <li><a class="footer__fb" href="{FB}" target="_blank" rel="noopener">{FB_SVG}<span>Facebook</span></a></li>
      </ul></div>
    </div>
    <p class="footer__legal">{FIRM} · NIP {NIP} · REGON {REGON} · Agent ubezpieczeniowy wpisany do rejestru pośredników ubezpieczeniowych KNF pod nr <a href="{KNF_URL}" target="_blank" rel="noopener">{KNF_NO}</a></p>
    <div class="footer__bottom">
      <span>© 2026 Polfinans Grupa Partnerska</span>
      <span><a href="prywatnosc.html">Polityka prywatności</a></span>
      <!-- TODO: podpis "Strona: Adrian Wojtasik" do potwierdzenia z klientem -->
    </div>
  </div>
</footer>
<div class="callbar" id="callbar">
  <a class="btn btn--primary" href="tel:{PHONE_TEL}">{ic("phone","i-phone")} Zadzwoń</a>
  <a class="btn btn--ghost" href="#kontakt">Napisz</a>
</div>
<script src="main.js?v=1794229000" defer></script>
</body>
</html>
'''

def picture(name, alt, w=1600, h=1067, eager=False, cls=""):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="img/{name}.webp" srcset="img/{name}-800.webp 800w, img/{name}.webp 1600w" sizes="(min-width:960px) 50vw, 100vw" width="{w}" height="{h}" alt="{alt}" {load}>'

# ---------------- Index ----------------
def index():
    idx = "".join(f'''<li><a class="idx__item{" is-active" if i == 0 else ""}" href="{a["slug"]}.html"><span class="idx__icon">{ic(a["icon"])}</span><span class="idx__name">{a["name"]}</span><span class="idx__go">{ic("arrow")}</span><span class="idx__desc"><span><span>{a["card"]}</span></span></span><span class="unfold idx__ph" aria-hidden="true"><span class="unfold__in"><span class="reveal"><img src="img/{a["img"]}-800.webp" width="800" height="533" alt="" loading="lazy" decoding="async"></span></span></span></a></li>''' for i, a in enumerate(AREAS))
    frame = "".join(f'<img class="{"is-active" if i == 0 else ""}" src="img/{a["img"]}-800.webp" data-full="img/{a["img"]}.webp" width="800" height="533" alt="" decoding="async">' for i, a in enumerate(AREAS))
    cards = "".join(f'<a class="frame__cap{" is-active" if i == 0 else ""}" href="{a["slug"]}.html"{"" if i == 0 else ' tabindex="-1" aria-hidden="true"'}><span class="frame__ic">{ic(a["icon"])}</span><span class="frame__txt"><strong>{a["name"]}</strong><span>{a["card"]}</span></span><span class="frame__more">Szczegóły {ic("arrow")}</span></a>' for i, a in enumerate(AREAS))
    rows = [
      ("search","Analiza obecnych polis","Sprawdzimy zakres ochrony, sumy ubezpieczenia i wyłączenia odpowiedzialności.","Analiza obecnych polis"),
      ("scale","Porównanie ofert","Porównamy oferty kilku towarzystw ubezpieczeniowych, zwracając uwagę na zakres ochrony, warunki i cenę.","Inne / jeszcze nie wiem"),
      ("pen","Pomoc przy zawarciu umowy","Wyjaśnimy warunki ubezpieczenia i pomożemy dopełnić formalności, abyś wiedział, co obejmuje polisa i na jakich zasadach działa.","Inne / jeszcze nie wiem"),
      ("buoy","Wsparcie przy szkodzie","Pomożemy zgłosić szkodę, skompletować dokumentację i przejść przez kolejne etapy jej likwidacji.","Szkoda"),
      ("refresh","Stała opieka","Przypomnimy o zbliżających się terminach wznowienia polis i pomożemy ocenić, czy dotychczasowy zakres ochrony nadal odpowiada Twojej sytuacji i potrzebom.","Inne / jeszcze nie wiem"),
    ]
    rows_html = "".join(f'<li><a class="row" href="#kontakt" data-topic="{tp}"><span class="row__icon">{ic(icn)}</span><h3>{t}</h3><p>{d}</p><span class="row__go">{ic("arrow")}</span></a></li>' for icn, t, d, tp in rows)
    steps = [("Analiza potrzeb","Rozmawiamy o Twojej sytuacji, oczekiwaniach i tym, co jest dla Ciebie najważniejsze.","step-1","Rozmowa o sytuacji klienta przy stole"),
             ("Porównujemy dostępne oferty","Porównujemy oferty różnych towarzystw ubezpieczeniowych, zwracając uwagę na zakres ochrony, wyłączenia odpowiedzialności i wysokość składki.","step-2","Dokumenty z porównaniem ofert rozłożone na stole"),
             ("Przedstawiamy rekomendację","Proponujemy rozwiązanie dopasowane do Twoich potrzeb i wyjaśniamy, dlaczego właśnie ten wariant warto rozważyć.","step-3","Doradczyni omawia warianty przy tablicy z wydrukami"),
             ("Zawarcie ubezpieczenia i dalsze wsparcie","Pomagamy w zawarciu umowy i pozostajemy do Twojej dyspozycji również po zakupie polisy – przy aktualizacji ochrony i w przypadku szkody.","step-4","Doradca wskazuje klientce miejsce na dokumencie")]
    steps_html = "".join(f'<li class="step{" is-active" if i == 0 else ""}"><button type="button" aria-controls="photos" aria-pressed="{"true" if i == 0 else "false"}"><span class="step__num" aria-hidden="true"></span><span class="step__t">{t}</span><span class="step__d">{d}</span><span class="step__bar" aria-hidden="true"></span></button><span class="unfold step__ph"><span class="unfold__in"><span class="reveal">{picture(img, alt).replace('sizes="(min-width:960px) 50vw, 100vw"', 'sizes="100vw"')}</span></span></span></li>' for i, (t, d, img, alt) in enumerate(steps))
    photos = "".join(picture(img, alt, cls="is-active" if i == 0 else "") for i, (_, _, img, alt) in enumerate(steps)).replace('loading="lazy" ', '')
    ld = {"@context":"https://schema.org","@type":"InsuranceAgency","name":"Polfinans Grupa Partnerska","url":"https://gppolfinans.pl/","telephone":PHONE,"email":MAIL,
          "address":{"@type":"PostalAddress","streetAddress":ADDR1,"postalCode":"54-156","addressLocality":"Wrocław","addressCountry":"PL"},
          "hasMap":MAPS,"areaServed":"Wrocław","legalName":"Anna Wojda POLFINANS","vatID":"PL"+NIP.replace("-",""),"sameAs":[FB],
          "image":"https://gppolfinans.pl/img/hero-dom.webp","inLanguage":["pl","en"]}
    extra = f'<link rel="preload" as="image" href="img/hero-dom-800.webp" imagesrcset="img/hero-dom-800.webp 800w, img/hero-dom.webp 1600w" imagesizes="(min-width:960px) 50vw, 100vw">\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    return head("Polfinans Grupa Partnerska | Doradztwo ubezpieczeniowe, Wrocław",
                "Multiagencja ubezpieczeniowa z Wrocławia. Porównujemy oferty kilku towarzystw, pomagamy zawrzeć umowę i przejść przez szkodę. Dom, samochód, życie, podróże, firma, gospodarstwo.",
                "", extra) + nav(True, page="") + f'''
<main id="main">
<section class="hero" id="top" aria-labelledby="hero-title">
  <div class="hero__inner">
    <div>
      <h1 id="hero-title" class="h1--long" data-rise style="--i:0">Doradztwo i pośrednictwo ubezpieczeniowe oparte na wiedzy, analizie i&nbsp;doświadczeniu</h1>
      <p class="hero__lead" data-rise style="--i:1">Każdy Klient i jego potrzeby są inne, dlatego do ubezpieczeń podchodzimy indywidualnie. Pomagamy dobrać odpowiedni zakres ochrony, przedstawiamy dostępne rozwiązania i wspieramy w podejmowaniu świadomych decyzji. Bo dobre ubezpieczenie to coś więcej niż dokument i suma gwarancyjna – to przemyślana ochrona, poczucie bezpieczeństwa oraz pewność, że w ważnych momentach możesz liczyć na nasze wsparcie.</p>
      <ul class="creds" data-rise style="--i:2">
        <li>{ic("award")}30 lat na rynku</li>
        <li>{ic("layers")}Szeroki wybór ubezpieczeń</li>
        <li>{ic("user")}Indywidualne podejście</li>
        <li>{ic("buoy")}Wsparcie przy szkodzie</li>
      </ul>
    </div>
    <figure class="hero__media" id="heroMedia">
      <div class="hero__frame">{picture("hero-dom","Kobieta z zakupami i pies wchodzą do jasnego domu przez otwarte drzwi tarasowe", eager=True)}</div>
      <figcaption class="note"><strong>Z myślą o tym, co ważne.</strong><span>Dobre decyzje zaczynają się tutaj.</span></figcaption>
    </figure>
  </div>
</section>

<section class="section areas tabbed" id="obszary" aria-labelledby="areas-title">
  <div class="wrap">
    <div class="head head--split">
      <div style="display:grid;gap:1.1rem"><span class="eyebrow">Ubezpieczenia</span><h2 id="areas-title">Znajdź ochronę dopasowaną do swoich potrzeb</h2></div>
      <p>Oferujemy ubezpieczenia w różnych obszarach życia i działalności. Wybierz kategorię, która Cię interesuje, poznaj dostępne możliwości i sprawdź, jakich informacji potrzebujemy, aby przygotować odpowiednią ofertę dla Ciebie.</p>
    </div>
    <div class="areas__grid">
      <div>
        <ul class="idx" id="idx">{idx}</ul>
        <div class="areas__foot"><p><strong>Nie znalazłeś rozwiązania, którego szukasz?</strong> Opowiedz nam, czego potrzebujesz. Przyjrzymy się Twojej sytuacji i sprawdzimy, co możemy Ci zaproponować.</p><a class="link-more" href="#kontakt" data-topic="Inne / jeszcze nie wiem"><span>Napisz do nas</span>{ic("arrow")}</a></div>
      </div>
      <div class="frame" id="frame">{frame}{cards}</div>
    </div>
  </div>
</section>

<section class="section help" id="pomoc" aria-labelledby="help-title">
  <div class="wrap help__grid">
    <div class="help__side">
      <div class="head">
        <span class="eyebrow">Jak pracujemy</span>
        <h2 id="help-title">Więcej niż ubezpieczenie</h2>
        <p>Jako multiagencja współpracujemy z wieloma towarzystwami ubezpieczeniowymi, dzięki czemu możemy porównać ich oferty i pomóc Ci wybrać odpowiednią polisę. Nasza rola nie kończy się jednak na jej zawarciu. Pozostajemy do Twojej dyspozycji również wtedy, gdy potrzebujesz wsparcia przy zgłoszeniu i likwidacji szkody, chcesz przeanalizować swoje dotychczasowe ubezpieczenia lub rozszerzyć ochronę na kolejne obszary swojego życia.</p>
        <p>Stawiamy na bezpośredni kontakt i indywidualne podejście. Nie jesteś dla nas numerem polisy – zależy nam na relacjach opartych na zaufaniu, zaangażowaniu i partnerskiej współpracy.</p>
      </div>
      <div class="ask"><svg class="ask__mark" aria-hidden="true" style="stroke-width:.6"><use href="#i-compass"/></svg><h3>Nie wiesz, od czego zacząć? Porozmawiajmy.</h3><p>Niezależnie od tego, czy szukasz konkretnej polisy, czy dopiero rozważasz możliwości – pomożemy Ci określić, czego potrzebujesz i znaleźć polisę, która zapewni Ci odpowiednią ochronę.</p><a class="btn btn--light" href="#kontakt" data-topic="Inne / jeszcze nie wiem">Napisz do nas {ic("arrow")}</a></div>
    </div>
    <ol class="rows" aria-label="Usługi" style="list-style:none">{rows_html}</ol>
  </div>
</section>

<section class="section process tabbed" id="proces" aria-labelledby="process-title">
  <div class="wrap">
    <div class="head head--split">
      <div style="display:grid;gap:1.1rem"><span class="eyebrow">Nasze podejście</span><h2 id="process-title">Twoje potrzeby. Nasze doświadczenie. Wspólny wybór.</h2></div>
      <p>Każdą współpracę opieramy na rozmowie, analizie potrzeb i dopasowaniu odpowiednich rozwiązań. Dbamy o to, aby wszystkie ustalenia były jasne i zrozumiałe, a Ty wiedział, jakie możliwości masz do wyboru i na co warto zwrócić uwagę.</p>
    </div>
    <div class="process__grid">
      <div class="ledger" id="ledger">
        <div class="ledger__title"><strong>Nasza współpraca</strong><span>Krok po kroku</span></div>
        <ol class="steps">{steps_html}</ol>
      </div>
      <div class="photos" id="photos" aria-live="off">{photos}</div>
    </div>
  </div>
</section>

<section class="claims claims--slip tabbed" id="szkoda" aria-labelledby="claims-title">
  <div class="claims__clip" aria-hidden="true"><svg class="claims__mark" style="stroke-width:.5"><use href="#i-buoy"/></svg></div>
  <div class="wrap claims__inner">
    <div>
      <span class="eyebrow">Pomoc przy szkodzie</span>
      <h2 id="claims-title" style="margin-top:1.1rem">Szkoda to zły moment na czytanie warunków polisy</h2>
      <p>Zadzwoń do nas, a pomożemy Ci ustalić, jak zgłosić szkodę, jakie dokumenty przygotować i na co zwrócić uwagę w kontakcie z towarzystwem ubezpieczeniowym.</p>
      <div class="claims__ctas">
        <a class="btn btn--primary" href="#kontakt" data-topic="Szkoda">Potrzebujesz pomocy? Skontaktuj się z nami. {ic("arrow")}</a>
        <a class="btn btn--light" href="tel:{PHONE_TEL}">{ic("phone","i-phone")} {PHONE_SHORT}</a>
      </div>
    </div>
    <div class="slip">
      <h3>Zaraz po zdarzeniu</h3>
      <ol>{"".join(f"<li><span><b>{t}</b>{d.split('.')[0]}.</span></li>" for t, d in CLAIMS["steps"][:4])}</ol>
      <a class="link-more" href="pomoc-przy-szkodzie.html"><span>Pierwsze kroki po szkodzie</span>{ic("arrow")}</a>
    </div>
  </div>
</section>

<section class="section about after-slip" id="o-nas" aria-labelledby="about-title">
  <div class="wrap about__grid">
    <figure class="portrait">
      <div class="portrait__frame">{picture("about","Burgundowa teczka z dokumentami na kamiennym parapecie w słońcu", 1600, 1067)}</div>
      <blockquote class="quote"><p>To, co ważne, wymaga dobrego partnera.</p></blockquote>
    </figure>
    <div class="about__text">
      <span class="eyebrow">O nas</span>
      <h2 id="about-title" class="about__logo"><span class="sr-only">Polfinans Grupa Partnerska</span><span class="logo" aria-hidden="true">{LOGO}</span></h2>
      <p><strong>Polfinans – Grupa Partnerska</strong> to multiagencja ubezpieczeniowa z Wrocławia, która łączy wieloletnie doświadczenie, profesjonalne doradztwo i indywidualne podejście do klienta. Od 30 lat działamy na polskim rynku, współpracując z wiodącymi towarzystwami ubezpieczeniowymi. Dzięki temu możemy porównywać szeroki wybór ofert i proponować rozwiązania dopasowane do potrzeb klientów indywidualnych, firm i instytucji.</p>
      <p>Zapewniamy wsparcie na każdym etapie współpracy – od analizy potrzeb i wyboru odpowiedniego ubezpieczenia, przez zawarcie umowy, aż po pomoc w przypadku wystąpienia szkody i jej likwidacji. Dbamy o to, aby proponowane rozwiązania były zrozumiałe, odpowiednio dobrane i odpowiadały rzeczywistym potrzebom naszych klientów.</p>
      <p>Stawiamy na rzetelność, wysoką jakość obsługi i partnerskie relacje. Wierzymy, że dobre ubezpieczenie to coś więcej niż polisa – to przemyślana ochrona, poczucie bezpieczeństwa i pewność, że w ważnych momentach można liczyć na nasze wsparcie.</p>
      <ul class="values">
        <li class="value">{ic("search")}<div><strong>Świadome decyzje</strong><span>Wyjaśniamy różnice między ofertami i uzasadniamy nasze rekomendacje, abyś wiedział, co wybierasz i dlaczego.</span></div></li>
        <li class="value">{ic("user")}<div><strong>Indywidualne podejście</strong><span>Wiesz, kto zajmuje się Twoją sprawą i do kogo możesz zwrócić się z pytaniami.</span></div></li>
        <li class="value">{ic("buoy")}<div><strong>Stałe wsparcie</strong><span>Pozostajemy do Twojej dyspozycji również wtedy, gdy wystąpi szkoda, zmienią się Twoje potrzeby lub sytuacja życiowa.</span></div></li>
        <li class="value">{ic("refresh")}<div><strong>Ciągłość ochrony</strong><span>Pamiętamy o kończących się polisach i przypominamy o wznowieniach, pomagając Ci zachować ciągłość ochrony.</span></div></li>
      </ul>
    </div>
  </div>
</section>
{contact()}
</main>
''' + footer(True)

# ---------------- Subpage ----------------
def others(skip):
    items = [a for a in AREAS if a["slug"] != skip][:5]
    return "".join(f'<li><a class="other" href="{a["slug"]}.html">{picture(a["img"], "", 800, 533)}<span>{a["name"]} {ic("arrow")}</span></a></li>' for a in items)

def faq_html(faq):
    return "".join(f'<details><summary>{q}</summary><div class="faq__a"><p>{a}</p></div></details>' for q, a in faq)

def checklist(items):
    return "".join(f'<li><label><input type="checkbox"><span>{t}</span></label></li>' for t in items)

def subpage(a, claims=False):
    eyebrow = "Pomoc" if claims else a["name"]
    when_block = ""
    if claims:
        first = f'''<section class="section sub sub--first" aria-labelledby="first-title">
  <div class="wrap cols">
    <div class="cols__intro"><span class="eyebrow">Zaraz po zdarzeniu</span><h2 id="first-title">Pierwsze kroki po szkodzie</h2><p>Kolejność działań ma znaczenie. Odpowiednie postępowanie może pomóc ograniczyć rozmiar szkody i sprawniej przejść przez proces jej zgłoszenia oraz likwidacji.</p></div>
    <ol class="qs">{"".join(f"<li><div><strong>{t}</strong><span>{d}</span></div></li>" for t, d in a["steps"])}</ol>
  </div>
</section>'''
        prep_title, prep_lead = "Co warto przygotować do zgłoszenia szkody?", "Zanim zgłosisz szkodę, przygotuj dostępne informacje i dokumenty. Nie musisz mieć wszystkiego od razu – w zależności od rodzaju zdarzenia i wymagań towarzystwa ubezpieczeniowego lista może się różnić."
        prep_left = f'<div class="cols__intro"><span class="eyebrow">Dokumenty</span><h2 id="prep-title">{prep_title}</h2><p>{prep_lead}</p></div>'
        prep_right = f'<div><p class="checklist__hint">Sprawdź, które informacje i dokumenty masz już przygotowane</p><ul class="checklist">{checklist(a["prep"])}</ul><div class="prep__meter"><span data-count>Gotowe: 0 z {len(a["prep"])}</span><b aria-hidden="true"></b></div></div>'
        prep_section = f'<section class="section prep tabbed" aria-labelledby="prep-title"><div class="wrap cols">{prep_left}{prep_right}</div></section>'
        band_t, band_p = "Potrzebujesz wsparcia? Skontaktuj się z nami.", "Pomożemy Ci ustalić, co i w jakim terminie należy zgłosić. Podpowiemy, jakie dokumenty przygotować i wesprzemy Cię w procesie zgłoszenia szkody."
    else:
        first = f'''<section class="section sub sub--first" aria-labelledby="when-title">
  <div class="wrap cols">
    <div class="cols__intro"><span class="eyebrow">{a["name"]}</span><h2 id="when-title">Dobrze dobrana ochrona zaczyna się od potrzeb</h2><p>{a.get("when_lead","Najczęściej zgłaszają się do nas osoby w jednej z tych sytuacji.")}</p></div>
    <ul class="ticks">{"".join(f"<li>{ic('check')}<span>{t}</span></li>" for t in a["when"])}</ul>
  </div>
</section>'''
        prep_section = f'''<section class="section prep tabbed" aria-labelledby="qs-title">
  <div class="wrap cols">
    <div class="cols__intro"><span class="eyebrow">Przed rozmową</span><h2 id="qs-title">Kilka pytań na początek</h2><p>{a["qs_lead"]}</p>
      <div style="margin-top:1.5rem"><h3 style="font-size:1.35rem;margin-bottom:1rem">Co warto przygotować</h3><ul class="checklist">{checklist(a["prep"])}</ul><div class="prep__meter"><span data-count>Gotowe: 0 z {len(a["prep"])}</span><b aria-hidden="true"></b></div></div>
    </div>
    <ol class="qs">{"".join(f"<li><div><strong>{q}</strong><span>{d}</span></div></li>" for q, d in a["qs"])}</ol>
  </div>
</section>'''
    band_html = f'''<section class="claims tabbed" aria-labelledby="band-title">
  <div class="claims__clip" aria-hidden="true"><svg class="claims__mark" style="stroke-width:.5"><use href="#i-buoy"/></svg></div>
  <div class="wrap claims__inner">
    <div><h2 id="band-title">{band_t}</h2><p>{band_p}</p></div>
    <div class="claims__ctas">
      <a class="btn btn--primary" href="tel:{PHONE_TEL}">{ic("phone","i-phone")} {PHONE_SHORT}</a>
      <a class="btn btn--light" href="#kontakt">Napisz wiadomość {ic("arrow")}</a>
    </div>
  </div>
</section>''' if claims else ""
    hero_ctas = f'''<div class="hero__ctas" data-rise style="--i:3">
        <a class="btn btn--primary" href="tel:{PHONE_TEL}">{ic("phone","i-phone")} Zadzwoń: {PHONE_SHORT}</a>
        <a class="btn btn--ghost" href="#kontakt">Napisz do nas</a>
      </div>''' if claims else ""
    lead_txt = re.sub(r"<[^>]+>", " ", a["lead"]); lead_txt = re.sub(r"\s+", " ", lead_txt).strip()
    note_t, note_s = ("Spokojnie, krok po kroku.", "Powiemy, co zrobić w pierwszej kolejności.") if claims else a["note"]
    note_html = f'<strong>{note_t}</strong>' + (f'<span>{note_s}</span>' if note_s else "")
    return head(f'{a["seo"]} | Polfinans', lead_txt[:155], f'{a["slug"]}.html') + nav(False, "szkoda" if claims else "obszary", page=f'{a["slug"]}.html') + f'''
<main id="main">
<section class="hero page-hero" id="top" aria-labelledby="hero-title">
  <div class="hero__inner">
    <div>
      <ol class="crumbs" data-rise style="--i:0"><li><a href="index.html">Polfinans</a></li><li><a href="index.html#{"szkoda" if claims else "obszary"}">{"Pomoc" if claims else "Ubezpieczenia"}</a></li><li aria-current="page">{a["name"]}</li></ol>
      <h1 id="hero-title" data-rise style="--i:1">{a["title"]}</h1>
      <p class="hero__lead" data-rise style="--i:2">{a["lead"]}</p>
      {hero_ctas}
    </div>
    <figure class="hero__media" id="heroMedia">
      <div class="hero__frame">{picture(a["img"], a["alt"], eager=True)}</div>
      <figcaption class="note">{note_html}</figcaption>
    </figure>
  </div>
</section>
{first}
{prep_section}
{band_html}
<section class="section sub" aria-labelledby="faq-title">
  <div class="wrap cols">
    <div class="cols__intro"><span class="eyebrow">Pytania</span><h2 id="faq-title">Często zadawane pytania</h2><p>{FAQ_LEAD}</p></div>
    <div class="faq">{faq_html(a["faq"])}</div>
  </div>
</section>
<section class="section sub" style="padding-top:0" aria-labelledby="others-title">
  <div class="wrap">
    <div class="head" style="margin-bottom:2rem"><h2 id="others-title" style="font-size:clamp(1.6rem,1.2rem + 1.4vw,2.3rem)">{"Ubezpieczenia, z którymi pomagamy" if claims else "Inne obszary"}</h2></div>
    <ul class="others">{others(a.get("slug") if not claims else "")}</ul>
  </div>
</section>
{contact(a["topic"])}
</main>
''' + footer(False)

def privacy():
    return head("Polityka prywatności | Polfinans", "Jak Polfinans przetwarza dane przesłane przez formularz kontaktowy.", "prywatnosc.html") + nav(False, page="prywatnosc.html") + f'''
<main id="main">
<section class="section sub" style="padding-top:calc(var(--nav-h) + 4rem)">
  <div class="wrap legal">
    <span class="eyebrow">Prywatność</span>
    <h1 style="font-size:clamp(2.2rem,1.4rem + 3vw,3.6rem);margin-top:1rem">Polityka prywatności</h1>
    <h2>Administrator danych</h2>
    <p>Administratorem danych podanych w formularzu jest {FIRM} (Polfinans Grupa Partnerska), {ADDR1}, {ADDR2}, NIP {NIP}, REGON {REGON}, agent ubezpieczeniowy wpisany do rejestru pośredników ubezpieczeniowych KNF pod nr {KNF_NO}. Kontakt w sprawie danych: <a href="mailto:{MAIL}">{MAIL}</a>, tel. {PHONE}.</p>
    <h2>Jakie dane i po co</h2>
    <p>Przetwarzamy dane, które sam wpiszesz w formularzu: imię i nazwisko, telefon lub e-mail i treść wiadomości. Używamy ich tylko po to, żeby odpowiedzieć i umówić rozmowę. Podstawą jest Twoja zgoda (art. 6 ust. 1 lit. a RODO) oraz działania przed zawarciem umowy na Twoje żądanie (art. 6 ust. 1 lit. b RODO).</p>
    <h2>Komu je przekazujemy</h2>
    <p>Wiadomość z formularza trafia na naszą skrzynkę przez usługę FormSubmit (formsubmit.co), która działa jako podmiot przetwarzający. Danych nie sprzedajemy i nie używamy do reklam.</p>
    <h2>Jak długo</h2>
    <p>Przechowujemy wiadomość tak długo, jak trwa rozmowa w Twojej sprawie, a jeśli dojdzie do współpracy, przez okres wymagany przepisami.</p>
    <h2>Twoje prawa</h2>
    <p>Masz prawo dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przeniesienia oraz cofnięcia zgody w dowolnym momencie. Możesz złożyć skargę do Prezesa Urzędu Ochrony Danych Osobowych.</p>
    <h2>Pliki cookie i statystyki</h2>
    <p>Strona nie używa plików cookie, analityki ani zewnętrznych czcionek. Lista „Co warto przygotować” działa tylko w Twojej przeglądarce i nie jest nigdzie wysyłana.</p>
  </div>
</section>
</main>
''' + footer(False, has_contact=False)

def pages():
    yield "index.html", index()
    for a in AREAS:
        yield f'{a["slug"]}.html', subpage(a)
    yield f'{CLAIMS["slug"]}.html', subpage(CLAIMS, claims=True)
    yield "prywatnosc.html", privacy()

ASSET = re.compile(r'(?<=["\s,])(img/|fonts/|styles\.css|main\.js)')
def to_en(html):
    import content_en as E
    for k in sorted(E.UI, key=len, reverse=True):
        html = html.replace(k, E.UI[k])
    return ASSET.sub(r"../\1", html)

def main():
    global L, AREAS, CLAIMS, TOPICS, FAQ_LEAD
    for name, html in pages():
        (ROOT / name).write_text(html, encoding="utf-8")
    import content_en as E
    L = "en"
    AREAS = [{**a, **E.AREAS[a["slug"]]} for a in AREAS]
    CLAIMS = {**CLAIMS, **E.CLAIMS}; TOPICS = E.TOPICS; FAQ_LEAD = E.FAQ_LEAD
    (ROOT / "en").mkdir(exist_ok=True)
    for name, html in pages():
        (ROOT / "en" / name).write_text(to_en(html), encoding="utf-8")
    print("ok")

if __name__ == "__main__":
    main()
