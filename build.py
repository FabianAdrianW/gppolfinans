#!/usr/bin/env python3
"""Generates the Polfinans site: index + 6 insurance areas + claims help + privacy. Run: python3 build.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).parent

PHONE = "+48 509 064 464"; PHONE_TEL = "+48509064464"; PHONE_SHORT = "509 064 464"
MAIL = "gppolfinans@gmail.com"
ADDR1 = "ul. Metalowców 9, pok. 110"; ADDR2 = "54-156 Wrocław"
MAPS = "https://www.google.com/maps/search/?api=1&query=Metalowc%C3%B3w+9+54-156+Wroc%C5%82aw"
WEB3FORMS_KEY = "TODO_WEB3FORMS_KEY"   # TODO: klucz z web3forms.com założony na gppolfinans@gmail.com

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
def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in ICONS.items()) + "</svg>"

# ---------------- Areas ----------------
AREAS = [
 dict(slug="dom-i-majatek", icon="home", img="area-dom", name="Dom i majątek", topic="Dom i majątek",
   card="Mieszkanie, dom, wyposażenie i OC w życiu prywatnym.",
   title="Ubezpieczenie domu i mieszkania", seo="Ubezpieczenie domu i mieszkania, Wrocław",
   lead="Mury, wyposażenie, rzeczy, których nie da się łatwo odkupić, i odpowiedzialność wobec sąsiadów. Sprawdzimy, co obejmuje polisa i czy suma ubezpieczenia odpowiada dzisiejszej wartości domu.",
   alt="Otwarte drzwi wejściowe domu, na komodzie burgundowa teczka i klucze",
   when=["Kupujesz mieszkanie albo dom na kredyt, a bank wymaga polisy.",
         "Kończysz budowę lub remont i dom jest dziś wart więcej niż w dniu zawarcia umowy.",
         "Masz polisę od lat i nie pamiętasz, co dokładnie obejmuje.",
         "Wynajmujesz mieszkanie albo sam je komuś wynajmujesz."],
   qs=[("Co chcesz chronić?","Mury, stałe elementy, wyposażenie, ruchomości, budynki gospodarcze na działce."),
       ("Od jakich zdarzeń?","Lista nazwanych ryzyk albo formuła wszystkich ryzyk, z wyłączeniami zapisanymi w warunkach."),
       ("Jaka suma ubezpieczenia?","Wartość odtworzeniowa czy rzeczywista i ile kosztowałaby dziś odbudowa."),
       ("Czy potrzebujesz OC w życiu prywatnym?","Zalanie sąsiada, szkoda wyrządzona przez dziecko albo psa."),
       ("Jakiej pomocy potrzebujesz na miejscu?","Assistance domowe: hydraulik, elektryk, ślusarz.")],
   prep=["Adres, rok budowy, powierzchnia, rodzaj konstrukcji i dachu",
         "Obecna polisa, jeśli ją masz (zdjęcie lub PDF wystarczy)",
         "Przybliżona wartość wyposażenia i droższych rzeczy",
         "Informacja z banku, jeśli polisa ma być scedowana na kredyt",
         "Zabezpieczenia: drzwi, zamki, alarm, monitoring"],
   faq=[("Czym różni się wartość odtworzeniowa od rzeczywistej?","Wartość odtworzeniowa to koszt odbudowy albo zakupu nowej rzeczy tego samego rodzaju. Wartość rzeczywista uwzględnia zużycie, więc odszkodowanie może być niższe. W rozmowie sprawdzimy, jak liczy to konkretna oferta."),
        ("Czy polisa wymagana przez bank wystarczy?","Polisa do kredytu często chroni głównie mury, bo to one zabezpieczają bank. Wyposażenie i OC w życiu prywatnym zwykle trzeba dobrać osobno."),
        ("Czy da się ubezpieczyć dom w budowie?","Towarzystwa mają do tego osobne warunki. Zakres zależy od etapu prac i od tego, czy budynek jest już zamknięty.")]),
 dict(slug="samochod", icon="car", img="area-samochod", name="Samochód", topic="Samochód",
   card="OC, AC, assistance i to, jak naprawdę używasz auta.",
   title="Ubezpieczenie samochodu", seo="Ubezpieczenie samochodu OC i AC, Wrocław",
   lead="OC jest obowiązkowe, reszta zależy od tego, jak korzystasz z auta. Porównamy oferty kilku towarzystw przy tym samym zakresie, żeby ceny dało się uczciwie zestawić.",
   alt="Mężczyzna wkłada torbę do bagażnika samochodu przed domem",
   when=["Kupujesz samochód, nowy albo używany.",
         "Zbliża się koniec obecnej polisy OC lub AC.",
         "Auto jest w leasingu albo kupione na kredyt.",
         "Zmieniasz sposób używania auta, na przykład zaczynasz jeździć służbowo albo za granicę."],
   qs=[("Kto i jak jeździ?","Kierowcy, ich wiek, roczny przebieg, miejsce parkowania."),
       ("Czy AC ma sens przy tym aucie?","Wiek i wartość samochodu zestawione ze składką i udziałem własnym."),
       ("Jak będzie liczone odszkodowanie?","Wariant warsztatowy albo kosztorysowy, części oryginalne albo zamienniki."),
       ("Jakie assistance?","Holowanie, na jaki dystans, w kraju i za granicą, auto zastępcze."),
       ("Czy potrzebujesz dodatków?","NNW, szyby, ochrona zniżek. Warto wiedzieć, co dają, zanim się je dokupi.")],
   prep=["Dowód rejestracyjny: marka, model, rok produkcji, VIN",
         "Obecna polisa OC lub AC",
         "Data urodzenia i rok uzyskania prawa jazdy kierowców",
         "Szkody z ostatnich lat, jeśli były",
         "Przybliżony roczny przebieg"],
   faq=[("Czy OC przedłuża się automatycznie?","Tak. Jeśli nie wypowiesz umowy, OC zawarte na 12 miesięcy przedłuża się na kolejny rok. Dlatego dobrze jest porównać oferty przed końcem okresu."),
        ("Co z OC przy zakupie używanego auta?","Polisa poprzedniego właściciela przechodzi na Ciebie i obowiązuje do końca okresu. Możesz ją wypowiedzieć i zawrzeć własną."),
        ("Czym różni się wariant warsztatowy od kosztorysowego?","W wariancie warsztatowym auto jest naprawiane w serwisie, a towarzystwo płaci za faktury. W kosztorysowym dostajesz pieniądze według wyliczenia, zwykle niższe niż koszt naprawy w serwisie.")]),
 dict(slug="zycie", icon="heart", img="area-zycie", name="Życie", topic="Życie",
   card="Bliscy, kredyt i zobowiązania, które zostają na lata.",
   title="Ubezpieczenie na życie", seo="Ubezpieczenie na życie, Wrocław",
   lead="Ta polisa jest dla ludzi, którzy na Tobie polegają, i na zobowiązania, które zostają na lata. Pomożemy dobrać sumę i zakres do Twojej rodziny, kredytu i planów.",
   alt="Rodzina przygotowuje razem posiłek w kuchni",
   when=["Zakładasz rodzinę albo rodzi się dziecko.",
         "Bierzesz kredyt hipoteczny.",
         "Prowadzisz firmę, a bliscy zależą od Twoich dochodów.",
         "Masz polisę grupową z pracy i nie wiesz, czy wystarczy."],
   qs=[("Kogo ma chronić polisa?","Partnera, dzieci, wspólnika, bank."),
       ("Jaka suma ma sens?","Ile potrzebowaliby bliscy, żeby spłacić zobowiązania i utrzymać się przez kilka lat."),
       ("Jakie ryzyka oprócz śmierci?","Poważne zachorowanie, niezdolność do pracy, pobyt w szpitalu."),
       ("Na jak długo?","Do spłaty kredytu, do usamodzielnienia dzieci, do emerytury."),
       ("Polisa indywidualna czy grupowa?","Co daje ubezpieczenie z pracy i co się z nim dzieje przy zmianie pracodawcy.")],
   prep=["Wysokość i okres spłaty kredytów",
         "Osoby, które chcesz zabezpieczyć",
         "Obecne polisy, także grupowe z pracy",
         "Podstawowe informacje o zdrowiu, o które zapyta ankieta medyczna"],
   faq=[("Czym różni się polisa indywidualna od grupowej?","Grupowa jest zwykle związana z pracodawcą i może się skończyć razem z zatrudnieniem. Indywidualna należy do Ciebie, a warunki ustalasz bezpośrednio z towarzystwem."),
        ("Czy polisę można scedować na bank?","Tak, przy kredycie hipotecznym bank często o to prosi. W razie śmierci świadczenie w pierwszej kolejności spłaca wtedy kredyt."),
        ("Czy trzeba przechodzić badania?","To zależy od towarzystwa, wieku i sumy ubezpieczenia. Często wystarcza ankieta medyczna.")]),
 dict(slug="podroze", icon="plane", img="area-podroze", name="Podróże", topic="Podróże",
   card="Urlop, narty, praca za granicą. Leczenie, bagaż, rezygnacja.",
   title="Ubezpieczenie turystyczne", seo="Ubezpieczenie turystyczne na wyjazd, Wrocław",
   lead="Urlop, narty, praca za granicą. Ustalimy, dokąd jedziesz i co będziesz robić, i dobierzemy zakres, który zadziała na miejscu.",
   alt="Otwarte drzwi domu z widokiem na słoneczny ogród i wzgórza",
   when=["Planujesz urlop poza Polską.",
         "Jedziesz na narty, w wysokie góry albo nurkować.",
         "Wyjeżdżasz do pracy fizycznej za granicę.",
         "Podróżujesz kilka razy w roku i polisa roczna może wyjść taniej."],
   qs=[("Dokąd i na jak długo?","Europa, świat, kraje z wysokimi kosztami leczenia, takie jak USA."),
       ("Jaka suma kosztów leczenia?","Od niej zależy, czy polisa pokryje leczenie w szpitalu i transport do Polski."),
       ("Co będziesz robić?","Sporty zimowe, wysokogórskie i wodne często wymagają rozszerzenia."),
       ("Bagaż, OC i rezygnacja z wyjazdu","Dodatki, które warto omówić przy droższych wyjazdach."),
       ("Choroby przewlekłe","Czy polisa obejmie zaostrzenie choroby, którą już masz.")],
   prep=["Kraj oraz daty wyjazdu i powrotu",
         "Liczba i wiek podróżujących osób",
         "Planowane aktywności i sporty",
         "Koszt wyjazdu, jeśli chcesz ubezpieczyć rezygnację"],
   faq=[("Czy karta EKUZ wystarczy?","EKUZ daje dostęp do publicznej opieki zdrowotnej w krajach UE i EFTA na zasadach obowiązujących miejscowych. Nie pokrywa transportu do Polski ani leczenia w prywatnych placówkach, dlatego przyda się też polisa turystyczna."),
        ("Czy mogę kupić polisę, gdy jestem już za granicą?","Część towarzystw na to pozwala, zwykle z kilkudniową karencją. Łatwiej i pewniej jest załatwić to przed wyjazdem."),
        ("Kiedy ubezpieczyć rezygnację z wyjazdu?","Zwykle krótko po rezerwacji. Dokładny termin zależy od warunków konkretnego towarzystwa.")]),
 dict(slug="firma", icon="briefcase", img="area-firma", name="Firma", topic="Firma",
   card="Majątek, OC działalności i ciągłość pracy po szkodzie.",
   title="Ubezpieczenie firmy", seo="Ubezpieczenie firmy i OC działalności, Wrocław",
   lead="Majątek, ludzie, odpowiedzialność wobec klientów i to, co się dzieje, gdy firma musi stanąć. Zaczynamy od tego, czym się zajmujesz i gdzie są największe ryzyka.",
   alt="Dwoje rzemieślników ogląda drewnianą ramę w warsztacie",
   when=["Zakładasz działalność albo otwierasz nowe miejsce.",
         "Kontrahent albo przetarg wymaga od Ciebie OC.",
         "Kupujesz maszyny, sprzęt albo samochody firmowe.",
         "Firma urosła, a polisy zostały takie jak na początku."],
   qs=[("Co jest majątkiem firmy?","Lokal, maszyny, towar, sprzęt elektroniczny, gotówka."),
       ("Za co odpowiadasz wobec innych?","OC z tytułu prowadzenia działalności, OC za produkt, OC zawodowe."),
       ("Co, jeśli firma stanie?","Utracony zysk po pożarze lub zalaniu i stałe koszty, które trzeba płacić dalej."),
       ("Jak chronić pracowników?","Ubezpieczenia grupowe i NNW."),
       ("Czy masz flotę albo towar w drodze?","Pojazdy firmowe i ubezpieczenie przewożonych ładunków.")],
   prep=["Kod PKD i krótki opis działalności",
         "Wartość majątku: lokal, maszyny, towar",
         "Roczny obrót i liczba pracowników",
         "Obecne polisy i umowy, które wymagają ubezpieczenia",
         "Szkody z ostatnich lat, jeśli były"],
   faq=[("Czy OC działalności jest obowiązkowe?","W niektórych zawodach tak, na przykład u doradców podatkowych, biegłych rewidentów czy pośredników nieruchomości. W innych branżach to wybór, ale kontrahenci często go wymagają."),
        ("Co to jest ubezpieczenie utraty zysku?","Pokrywa zysk, którego firma nie osiągnęła, i stałe koszty po szkodzie, która zatrzymała działalność, na przykład po pożarze. Zwykle dokupuje się je do ubezpieczenia mienia."),
        ("Czy pracujecie z jednoosobowymi firmami?","Tak. Zakres dobieramy do skali, więc mała firma nie płaci za ochronę, której nie potrzebuje.")]),
 dict(slug="gospodarstwo", icon="wheat", img="area-gospodarstwo", name="Gospodarstwo", topic="Gospodarstwo",
   card="Budynki, maszyny, uprawy i obowiązkowe OC rolnika.",
   title="Ubezpieczenie gospodarstwa rolnego", seo="Ubezpieczenie gospodarstwa rolnego i OC rolnika",
   lead="Budynki, maszyny, zwierzęta i uprawy, do tego obowiązkowe OC rolnika. Uporządkujemy, co musisz mieć z mocy prawa, a co warto dobrać do skali gospodarstwa.",
   alt="Dwie osoby z planami budynku oglądają jasne wnętrze w remoncie",
   when=["Przejmujesz gospodarstwo albo kupujesz ziemię.",
         "Stawiasz nowy budynek albo kupujesz maszyny.",
         "Chcesz zabezpieczyć uprawy przed gradem, przymrozkiem lub suszą.",
         "Zbliża się termin obowiązkowych ubezpieczeń."],
   qs=[("Co jest obowiązkowe w Twoim przypadku?","OC rolnika i ubezpieczenie budynków rolniczych."),
       ("Jakie budynki i jakiej wartości?","Dom, budynki inwentarskie, magazyny, wiaty."),
       ("Jakie maszyny i sprzęt?","Ciągniki, kombajny, maszyny samobieżne i przyczepiane."),
       ("Uprawy i zwierzęta","Ryzyka pogodowe, choroby zwierząt, dopłaty do składek."),
       ("Czy prowadzisz działalność dodatkową?","Agroturystyka, sprzedaż bezpośrednia, przetwórstwo.")],
   prep=["Powierzchnia gospodarstwa",
         "Lista budynków z przybliżoną wartością",
         "Maszyny i pojazdy",
         "Rodzaj upraw i zwierząt",
         "Obecne polisy"],
   faq=[("Które ubezpieczenia rolnika są obowiązkowe?","OC rolnika z tytułu posiadania gospodarstwa rolnego oraz ubezpieczenie budynków wchodzących w skład gospodarstwa od ognia i innych zdarzeń losowych."),
        ("Kogo dotyczy obowiązek?","Właścicieli i posiadaczy gospodarstw o powierzchni ponad 1 ha przeliczeniowego. Przy przejęciu gospodarstwa polisa przechodzi na nowego właściciela."),
        ("Czy do ubezpieczenia upraw są dopłaty?","Do części upraw i zwierząt państwo dopłaca do składki. Zakres dopłat się zmienia, dlatego sprawdzamy go przy każdej ofercie.")]),
]
BY = {a["slug"]: a for a in AREAS}

CLAIMS = dict(slug="pomoc-przy-szkodzie", img="step-1", name="Pomoc przy szkodzie", topic="Szkoda",
   title="Pomoc przy szkodzie", seo="Pomoc przy zgłoszeniu szkody i likwidacji, Wrocław",
   lead="Szkoda to zły moment na czytanie warunków polisy. Zadzwoń, a pomożemy ustalić, co zgłosić, jakie dokumenty zebrać i jak rozmawiać z towarzystwem.",
   alt="Kobieta wypełnia dokument przy stole, obok burgundowa teczka",
   steps=[("Zadbaj o bezpieczeństwo","Ludzie i zwierzęta najpierw. Odetnij wodę lub prąd, przy wypadku wezwij pomoc."),
          ("Ogranicz szkodę","Zrób to, co rozsądne, żeby szkoda nie rosła. Warunki polis tego wymagają."),
          ("Zrób zdjęcia","Zanim cokolwiek naprawisz albo wyrzucisz. Ujęcia ogólne i szczegóły."),
          ("Zawiadom odpowiednie służby","Policję przy kradzieży, włamaniu lub wypadku z rannymi, administrację przy zalaniu."),
          ("Zadzwoń do nas","Powiemy, co dalej, i pomożemy zgłosić szkodę w terminie z warunków polisy.")],
   prep=["Numer polisy albo nazwa towarzystwa",
         "Data, miejsce i krótki opis zdarzenia",
         "Zdjęcia uszkodzeń",
         "Dane drugiej strony i oświadczenie sprawcy przy kolizji",
         "Numer notatki lub protokołu policji, jeśli była wzywana",
         "Rachunki i faktury za zniszczone rzeczy",
         "Numer konta do wypłaty odszkodowania"],
   faq=[("Ile mam czasu na zgłoszenie?","Termin podają ogólne warunki ubezpieczenia i bywa krótki, czasem to kilka dni od zdarzenia. Kradzież zgłasza się policji niezwłocznie. Dlatego lepiej zadzwonić od razu."),
        ("Co, jeśli nie zgadzam się z decyzją towarzystwa?","Możesz złożyć reklamację albo odwołanie. Pomożemy przygotować uzasadnienie i zebrać dokumenty. W sporze możesz też zwrócić się do Rzecznika Finansowego."),
        ("Czy z OC sprawcy należy mi się auto zastępcze?","Tak, jeśli Twoje auto nie nadaje się do jazdy albo jest w naprawie, a najem był uzasadniony. Warto ustalić to z nami przed wynajęciem.")])

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
<meta name="theme-color" content="#F7F4EF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121818" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="img/hero-dom.webp">
<link rel="canonical" href="https://gppolfinans.pl/{canonical}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%238B2E2E'/%3E%3Ctext x='16' y='23' font-family='Georgia,serif' font-size='21' text-anchor='middle' fill='%23F7F4EF'%3Ep%3C/text%3E%3C/svg%3E">
<link rel="preload" href="fonts/source-serif-4-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/source-sans-3-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
{extra}</head>
<body>
<a class="skip" href="#main">Przejdź do treści</a>
{SPRITE}
'''

LOGO = '<span class="logo__word">polf<i>i</i>nans</span><span class="logo__sub">Grupa Partnerska</span>'

def nav(home=True, current=None):
    p = "" if home else "index.html"
    items = [("obszary","Ubezpieczenia"),("proces","Jak pracujemy"),("szkoda","Szkoda"),("o-nas","O nas"),("kontakt","Kontakt")]
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
      <a class="nav__phone" href="tel:{PHONE_TEL}">{ic("phone")}<span>{PHONE_SHORT}</span></a>
      <a class="btn btn--primary nav__cta" href="#kontakt">Porozmawiajmy</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Otwórz menu"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="progress" aria-hidden="true"></div>
</header>
<nav class="drawer" id="drawer" aria-label="Menu">
  {drawer}
  <a class="btn btn--primary" href="#kontakt">Porozmawiajmy</a>
  <p class="drawer__phone">Albo zadzwoń: <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
</nav>
'''

def contact(topic=""):
    opts = '<option value="">Wybierz temat</option>' + "".join(f'<option{" selected" if t == topic else ""}>{t}</option>' for t in TOPICS)
    return f'''<section class="section contact tabbed" id="kontakt" aria-labelledby="contact-title">
  <div class="wrap contact__grid">
    <div>
      <span class="eyebrow">Kontakt</span>
      <h2 id="contact-title" style="margin-top:1.1rem">Porozmawiajmy o tym, co chcesz chronić</h2>
      <p class="contact__lead">Zadzwoń, napisz albo zostaw wiadomość w formularzu. Odezwiemy się, żeby umówić rozmowę w dogodnym dla Ciebie terminie.</p>
      <a class="bigphone" href="tel:{PHONE_TEL}"><small>{ic("phone")}Zadzwoń</small><span>{PHONE}</span></a>
      <ul class="lines">
        <li><a class="line" href="mailto:{MAIL}" data-copy="{MAIL}">{ic("mail")}<div><small>E-mail</small><span>{MAIL}</span></div><span class="line__go">{ic("arrow")}</span></a></li>
        <li><a class="line" href="{MAPS}" target="_blank" rel="noopener">{ic("pin")}<div><small>Biuro</small><span>{ADDR1}, {ADDR2}</span></div><span class="line__go">{ic("arrow")}</span></a></li>
      </ul>
    </div>
    <form class="form" id="form" novalidate data-key="{WEB3FORMS_KEY}" data-mail="{MAIL}">
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

def footer(home=True):
    p = "" if home else "index.html"
    areas = "".join(f'<li><a href="{a["slug"]}.html">{a["name"]}</a></li>' for a in AREAS)
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <a class="logo" href="{p or '#top'}" aria-label="Polfinans, strona główna">{LOGO}</a>
        <p>Multiagencja ubezpieczeniowa z Wrocławia. Jasne decyzje. Osobista opieka.</p>
        <!-- TODO: numer wpisu w rejestrze pośredników ubezpieczeniowych KNF (RPU) oraz NIP -->
      </div>
      <div><h3>Ubezpieczenia</h3><ul>{areas}<li><a href="pomoc-przy-szkodzie.html">Pomoc przy szkodzie</a></li></ul></div>
      <div><h3>Kontakt</h3><ul>
        <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
        <li><a href="mailto:{MAIL}">{MAIL}</a></li>
        <li><a href="{MAPS}" target="_blank" rel="noopener">{ADDR1}, {ADDR2}</a></li>
      </ul></div>
    </div>
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
<script src="main.js" defer></script>
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
      ("search","Analiza obecnych polis","Przynieś to, co już masz. Sprawdzimy zakres, sumy i wyłączenia, żeby było jasne, przed czym polisa chroni, a przed czym nie.","Analiza obecnych polis"),
      ("scale","Porównanie ofert","Zestawiamy warianty kilku towarzystw według tych samych kryteriów. Różnice w zakresie i cenie widzisz obok siebie.","Inne / jeszcze nie wiem"),
      ("pen","Pomoc przy zawarciu umowy","Przechodzimy razem przez dokumenty i warunki. Podpisujesz, kiedy wiesz, co podpisujesz.","Inne / jeszcze nie wiem"),
      ("buoy","Wsparcie przy szkodzie","Pomagamy zgłosić szkodę, skompletować dokumenty i doprowadzić likwidację do końca.","Szkoda"),
      ("refresh","Stała opieka","Wracamy do ustaleń, kiedy zmienia się Twoja sytuacja albo zbliża się odnowienie polisy.","Inne / jeszcze nie wiem"),
    ]
    rows_html = "".join(f'<li><a class="row" href="#kontakt" data-topic="{tp}"><span class="row__icon">{ic(icn)}</span><h3>{t}</h3><p>{d}</p><span class="row__go">{ic("arrow")}</span></a></li>' for icn, t, d, tp in rows)
    steps = [("Analiza potrzeb","Rozmawiamy o Twojej sytuacji i o tym, co chcesz chronić.","step-1","Rozmowa o sytuacji klienta przy stole"),
             ("Porównanie rozwiązań","Zestawiamy oferty i pokazujemy różnice w zakresie, wyłączeniach i cenie.","step-2","Dokumenty z porównaniem ofert rozłożone na stole"),
             ("Nasza propozycja","Rekomendujemy wariant i mówimy wprost, dlaczego właśnie ten.","step-3","Doradczyni omawia warianty przy tablicy z wydrukami"),
             ("Kolejne kroki","Pomagamy zawrzeć umowę i zostajemy w kontakcie przy zmianach i szkodzie.","step-4","Doradca wskazuje klientce miejsce na dokumencie")]
    steps_html = "".join(f'<li class="step{" is-active" if i == 0 else ""}"><button type="button" aria-controls="photos" aria-pressed="{"true" if i == 0 else "false"}"><span class="step__num" aria-hidden="true"></span><span class="step__t">{t}</span><span class="step__d">{d}</span><span class="step__bar" aria-hidden="true"></span></button><span class="unfold step__ph"><span class="unfold__in"><span class="reveal">{picture(img, alt).replace('sizes="(min-width:960px) 50vw, 100vw"', 'sizes="100vw"')}</span></span></span></li>' for i, (t, d, img, alt) in enumerate(steps))
    photos = "".join(picture(img, alt, cls="is-active" if i == 0 else "") for i, (_, _, img, alt) in enumerate(steps)).replace('loading="lazy" ', '')
    ld = {"@context":"https://schema.org","@type":"InsuranceAgency","name":"Polfinans Grupa Partnerska","url":"https://gppolfinans.pl/","telephone":PHONE,"email":MAIL,
          "address":{"@type":"PostalAddress","streetAddress":ADDR1,"postalCode":"54-156","addressLocality":"Wrocław","addressCountry":"PL"},"areaServed":"Wrocław"}
    extra = f'<link rel="preload" as="image" href="img/hero-dom-800.webp" imagesrcset="img/hero-dom-800.webp 800w, img/hero-dom.webp 1600w" imagesizes="(min-width:960px) 50vw, 100vw">\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    return head("Polfinans Grupa Partnerska | Doradztwo ubezpieczeniowe, Wrocław",
                "Multiagencja ubezpieczeniowa z Wrocławia. Porównujemy oferty kilku towarzystw, pomagamy zawrzeć umowę i przejść przez szkodę. Dom, samochód, życie, podróże, firma, gospodarstwo.",
                "", extra) + nav(True) + f'''
<main id="main">
<section class="hero" id="top" aria-labelledby="hero-title">
  <div class="hero__inner">
    <div>
      <span class="eyebrow" data-rise style="--i:0">Doradztwo ubezpieczeniowe we Wrocławiu</span>
      <h1 id="hero-title" data-rise style="--i:1">Jasne decyzje.<br>Osobista opieka.</h1>
      <p class="hero__lead" data-rise style="--i:2">Dom, rodzina, firma, plany. Za każdą polisą stoją konkretne sprawy. Pomagamy uporządkować informacje, zrozumieć zakres ochrony i świadomie wybrać dalszy krok.</p>
      <div class="hero__ctas" data-rise style="--i:3">
        <a class="btn btn--primary" href="#kontakt">Umów rozmowę {ic("arrow")}</a>
        <a class="btn btn--ghost" href="tel:{PHONE_TEL}">{ic("phone","i-phone")} {PHONE_SHORT}</a>
      </div>
      <ul class="creds" data-rise style="--i:4">
        <li>{ic("award")}Ponad 20 lat na rynku</li>
        <li>{ic("layers")}Oferty kilku towarzystw</li>
        <li>{ic("buoy")}Pomoc przy szkodzie</li>
      </ul>
    </div>
    <figure class="hero__media" id="heroMedia">
      <div class="hero__frame">{picture("hero-dom","Kobieta z zakupami i pies wchodzą do jasnego domu przez otwarte drzwi tarasowe", eager=True)}</div>
      <figcaption class="note"><strong>Najpierw zrozumieć.</strong><span>Potem rozmawiać o rozwiązaniu.</span></figcaption>
    </figure>
  </div>
</section>

<section class="section areas tabbed" id="obszary" aria-labelledby="areas-title">
  <div class="wrap">
    <div class="head head--split">
      <div style="display:grid;gap:1.1rem"><span class="eyebrow">Ubezpieczenia</span><h2 id="areas-title">Z czym możemy pomóc</h2></div>
      <p>Sześć obszarów ochrony. Wybierz ten, który Cię dotyczy. Na każdej stronie znajdziesz pytania, od których zaczniemy rozmowę, i listę rzeczy do przygotowania.</p>
    </div>
    <div class="areas__grid">
      <div>
        <ul class="idx" id="idx">{idx}</ul>
        <div class="areas__foot"><p>Nie widzisz swojej sprawy na liście? Napisz, czego dotyczy. Jeśli to nie nasz obszar, powiemy to wprost.</p><a class="link-more" href="#kontakt" data-topic="Inne / jeszcze nie wiem"><span>Opisz swoją sytuację</span>{ic("arrow")}</a></div>
      </div>
      <div class="frame" id="frame">{frame}{cards}</div>
    </div>
  </div>
</section>

<section class="section help" id="pomoc" aria-labelledby="help-title">
  <div class="wrap help__grid">
    <div class="help__side">
      <div class="head">
        <span class="eyebrow">Co robimy</span>
        <h2 id="help-title">Od pierwszej rozmowy do wypłaty odszkodowania</h2>
        <p>Jesteśmy multiagencją, więc pracujemy z kilkoma towarzystwami ubezpieczeniowymi i możemy porównać ich oferty. Sprawę prowadzi jedna osoba, do której możesz wrócić.</p>
      </div>
      <div class="ask"><svg class="ask__mark" aria-hidden="true" style="stroke-width:.6"><use href="#i-compass"/></svg><h3>Nie wiesz, od czego zacząć?</h3><p>Opisz krótko swoją sytuację, a zaproponujemy, od czego zacząć.</p><a class="btn btn--light" href="#kontakt" data-topic="Inne / jeszcze nie wiem">Napisz do nas {ic("arrow")}</a></div>
    </div>
    <ol class="rows" aria-label="Usługi" style="list-style:none">{rows_html}</ol>
  </div>
</section>

<section class="section process tabbed" id="proces" aria-labelledby="process-title">
  <div class="wrap">
    <div class="head head--split">
      <div style="display:grid;gap:1.1rem"><span class="eyebrow">Jak pracujemy</span><h2 id="process-title">Cztery kroki do decyzji, którą rozumiesz</h2></div>
      <p>Po rozmowie dostajesz podsumowanie: co sprawdziliśmy, z czego wynikają ustalenia i jaki jest następny krok. Możesz do niego wrócić przy kolejnym kontakcie.</p>
    </div>
    <div class="process__grid">
      <div class="ledger" id="ledger">
        <div class="ledger__title"><strong>Twoje ustalenia</strong><span>Krok po kroku</span></div>
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
      <p>Zadzwoń, zanim zaczniesz działać sam. Pomożemy ustalić, co zgłosić, jakie dokumenty zebrać i jak rozmawiać z towarzystwem.</p>
      <div class="claims__ctas">
        <a class="btn btn--primary" href="tel:{PHONE_TEL}">{ic("phone","i-phone")} {PHONE_SHORT}</a>
        <a class="btn btn--light" href="pomoc-przy-szkodzie.html">Co zrobić po szkodzie {ic("arrow")}</a>
      </div>
    </div>
    <div class="slip">
      <h3>Zaraz po zdarzeniu</h3>
      <ol>{"".join(f"<li><span><b>{t}</b>{d.split('.')[0]}.</span></li>" for t, d in CLAIMS["steps"][:4])}</ol>
      <a class="link-more" href="pomoc-przy-szkodzie.html"><span>Pełna lista i dokumenty</span>{ic("arrow")}</a>
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
      <h2 id="about-title">Polfinans Grupa Partnerska</h2>
      <p>Jesteśmy multiagencją ubezpieczeniową z Wrocławia. Od ponad 20 lat doradzamy klientom indywidualnym, firmom i instytucjom. Współpracujemy z wiodącymi towarzystwami ubezpieczeniowymi, dlatego porównujemy oferty zamiast proponować jedną.</p>
      <p>Pomagamy wybrać ubezpieczenie, zawrzeć umowę i przejść przez likwidację szkody. Każda sprawa ma u nas osobę, która ją prowadzi.</p>
      <ul class="values">
        <li class="value">{ic("search")}<div><strong>Jakość decyzji</strong><span>Wyjaśniamy, z czego wynika wybór, żebyś mógł go opisać własnymi słowami.</span></div></li>
        <li class="value">{ic("user")}<div><strong>Osobista odpowiedzialność</strong><span>Wiesz, kto prowadzi Twoją sprawę i jak się z nim skontaktować.</span></div></li>
        <li class="value">{ic("refresh")}<div><strong>Ciągłość</strong><span>Wracamy do ustaleń, gdy zmienia się Twoja sytuacja.</span></div></li>
        <li class="value">{ic("folder")}<div><strong>Porządek w dokumentach</strong><span>Ustalenia są zapisane. Wiesz, do czego wrócić.</span></div></li>
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
    <div class="cols__intro"><span class="eyebrow">Zaraz po zdarzeniu</span><h2 id="first-title">Co zrobić od razu</h2><p>Kolejność ma znaczenie. Te kroki pomagają ograniczyć szkodę i nie stracić prawa do odszkodowania.</p></div>
    <ol class="qs">{"".join(f"<li><div><strong>{t}</strong><span>{d}</span></div></li>" for t, d in a["steps"])}</ol>
  </div>
</section>'''
        prep_title, prep_lead = "Co przygotować do zgłoszenia", "Zaznacz to, co już masz. Lista zostaje tylko w Twojej przeglądarce."
        prep_left = f'<div class="cols__intro"><span class="eyebrow">Dokumenty</span><h2 id="prep-title">{prep_title}</h2><p>{prep_lead}</p></div>'
        prep_right = f'<div><ul class="checklist">{checklist(a["prep"])}</ul><div class="prep__meter"><span data-count>Gotowe: 0 z {len(a["prep"])}</span><b aria-hidden="true"></b></div></div>'
        prep_section = f'<section class="section prep tabbed" aria-labelledby="prep-title"><div class="wrap cols">{prep_left}{prep_right}</div></section>'
        band_t, band_p = "Szkoda się wydarzyła? Zadzwoń teraz", "Ustalimy, co zgłosić i w jakim terminie. Pomożemy zebrać dokumenty i przygotować zgłoszenie."
    else:
        first = f'''<section class="section sub sub--first" aria-labelledby="when-title">
  <div class="wrap cols">
    <div class="cols__intro"><span class="eyebrow">{a["name"]}</span><h2 id="when-title">Kiedy warto porozmawiać</h2><p>Najczęściej zgłaszają się do nas osoby w jednej z tych sytuacji.</p></div>
    <ul class="ticks">{"".join(f"<li>{ic('check')}<span>{t}</span></li>" for t in a["when"])}</ul>
  </div>
</section>'''
        prep_section = f'''<section class="section prep tabbed" aria-labelledby="qs-title">
  <div class="wrap cols">
    <div class="cols__intro"><span class="eyebrow">Przed rozmową</span><h2 id="qs-title">O co zapytamy</h2><p>Te pytania porządkują rozmowę. Nie musisz znać odpowiedzi na wszystkie, ustalimy je razem.</p>
      <div style="margin-top:1.5rem"><h3 style="font-size:1.35rem;margin-bottom:1rem">Co warto przygotować</h3><ul class="checklist">{checklist(a["prep"])}</ul><div class="prep__meter"><span data-count>Gotowe: 0 z {len(a["prep"])}</span><b aria-hidden="true"></b></div></div>
    </div>
    <ol class="qs">{"".join(f"<li><div><strong>{q}</strong><span>{d}</span></div></li>" for q, d in a["qs"])}</ol>
  </div>
</section>'''
        band_t, band_p = f"Porozmawiajmy o Twojej sprawie", "Przygotujemy porównanie i powiemy, który wariant polecamy i dlaczego."
    return head(f'{a["seo"]} | Polfinans', a["lead"][:155], f'{a["slug"]}.html') + nav(False, "szkoda" if claims else "obszary") + f'''
<main id="main">
<section class="hero page-hero" id="top" aria-labelledby="hero-title">
  <div class="hero__inner">
    <div>
      <ol class="crumbs" data-rise style="--i:0"><li><a href="index.html">Polfinans</a></li><li><a href="index.html#{"szkoda" if claims else "obszary"}">{"Pomoc" if claims else "Ubezpieczenia"}</a></li><li aria-current="page">{a["name"]}</li></ol>
      <h1 id="hero-title" data-rise style="--i:1">{a["title"]}</h1>
      <p class="hero__lead" data-rise style="--i:2">{a["lead"]}</p>
      <div class="hero__ctas" data-rise style="--i:3">
        <a class="btn btn--primary" href="{"tel:" + PHONE_TEL if claims else "#kontakt"}">{(ic("phone","i-phone") + " Zadzwoń: " + PHONE_SHORT) if claims else ("Umów rozmowę " + ic("arrow"))}</a>
        <a class="btn btn--ghost" href="{"#kontakt" if claims else "tel:" + PHONE_TEL}">{"Napisz do nas" if claims else ic("phone","i-phone") + " " + PHONE_SHORT}</a>
      </div>
    </div>
    <figure class="hero__media" id="heroMedia">
      <div class="hero__frame">{picture(a["img"], a["alt"], eager=True)}</div>
      <figcaption class="note"><strong>{"Spokojnie, krok po kroku." if claims else "Najpierw zrozumieć."}</strong><span>{"Powiemy, co zrobić w pierwszej kolejności." if claims else "Potem rozmawiać o rozwiązaniu."}</span></figcaption>
    </figure>
  </div>
</section>
{first}
{prep_section}
<section class="claims tabbed" aria-labelledby="band-title">
  <div class="claims__clip" aria-hidden="true"><svg class="claims__mark" style="stroke-width:.5"><use href="#i-{"buoy" if claims else a["icon"]}"/></svg></div>
  <div class="wrap claims__inner">
    <div><h2 id="band-title">{band_t}</h2><p>{band_p}</p></div>
    <div class="claims__ctas">
      <a class="btn btn--primary" href="tel:{PHONE_TEL}">{ic("phone","i-phone")} {PHONE_SHORT}</a>
      <a class="btn btn--light" href="#kontakt">Napisz wiadomość {ic("arrow")}</a>
    </div>
  </div>
</section>
<section class="section sub" aria-labelledby="faq-title">
  <div class="wrap cols">
    <div class="cols__intro"><span class="eyebrow">Pytania</span><h2 id="faq-title">Często pytacie</h2><p>Odpowiedzi są ogólne. Szczegóły zależą od warunków konkretnego towarzystwa i sprawdzamy je przy Twojej ofercie.</p></div>
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
    return head("Polityka prywatności | Polfinans", "Jak Polfinans przetwarza dane przesłane przez formularz kontaktowy.", "prywatnosc.html") + nav(False) + f'''
<main id="main">
<section class="section sub" style="padding-top:calc(var(--nav-h) + 4rem)">
  <div class="wrap legal">
    <span class="eyebrow">Prywatność</span>
    <h1 style="font-size:clamp(2.2rem,1.4rem + 3vw,3.6rem);margin-top:1rem">Polityka prywatności</h1>
    <!-- TODO: pełna nazwa administratora, forma prawna, NIP/REGON do uzupełnienia przez klienta -->
    <h2>Administrator danych</h2>
    <p>Administratorem danych podanych w formularzu jest Polfinans Grupa Partnerska, {ADDR1}, {ADDR2}. Kontakt w sprawie danych: <a href="mailto:{MAIL}">{MAIL}</a>, tel. {PHONE}.</p>
    <h2>Jakie dane i po co</h2>
    <p>Przetwarzamy dane, które sam wpiszesz w formularzu: imię i nazwisko, telefon lub e-mail i treść wiadomości. Używamy ich tylko po to, żeby odpowiedzieć i umówić rozmowę. Podstawą jest Twoja zgoda (art. 6 ust. 1 lit. a RODO) oraz działania przed zawarciem umowy na Twoje żądanie (art. 6 ust. 1 lit. b RODO).</p>
    <h2>Komu je przekazujemy</h2>
    <p>Wiadomość z formularza trafia na naszą skrzynkę przez usługę Web3Forms, która działa jako podmiot przetwarzający. Danych nie sprzedajemy i nie używamy do reklam.</p>
    <h2>Jak długo</h2>
    <p>Przechowujemy wiadomość tak długo, jak trwa rozmowa w Twojej sprawie, a jeśli dojdzie do współpracy, przez okres wymagany przepisami.</p>
    <h2>Twoje prawa</h2>
    <p>Masz prawo dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przeniesienia oraz cofnięcia zgody w dowolnym momencie. Możesz złożyć skargę do Prezesa Urzędu Ochrony Danych Osobowych.</p>
    <h2>Pliki cookie i statystyki</h2>
    <p>Strona nie używa plików cookie, analityki ani zewnętrznych czcionek. Lista „Co warto przygotować” działa tylko w Twojej przeglądarce i nie jest nigdzie wysyłana.</p>
  </div>
</section>
</main>
''' + footer(False)

def main():
    (ROOT / "index.html").write_text(index(), encoding="utf-8")
    for a in AREAS:
        (ROOT / f'{a["slug"]}.html').write_text(subpage(a), encoding="utf-8")
    (ROOT / f'{CLAIMS["slug"]}.html').write_text(subpage(CLAIMS, claims=True), encoding="utf-8")
    (ROOT / "prywatnosc.html").write_text(privacy(), encoding="utf-8")
    print("ok")

if __name__ == "__main__":
    main()
