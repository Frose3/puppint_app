# PUPPINT

## Co je to PUPPINT?

Puppint je nástroj vytvořený za účelem sjednocení různých nástrojů pro OSINT analýzu a jednoduchou generaci klamavého účtu pomocí umělé inteligence Gemini. 
Vzhledem k tomu, že většina OSINT nástrojů je určena pro použití mimo EU, byl celý nástroj přizpůsoben českému prostředí.

V případě, že by nástroj měl být rozšířen pro evropské prostředí, 
bylo by zapotřebí přeložit vstupní parametry pro umělou inteligenci Gemini a také 
přeložit přední část webu.

Součástí nástroje jsou také seznamy českých jmen, příjmení a měst. 
Tyto seznamy se v nástroji nachází v případě, kdy by umělá inteligence nebyla funkční. 
Pro rozšíření by bylo nutné přidat jména, příjmení a města, které by odpovídali 
evropskému prostředí, do jednotlivých existujících seznamů.

## Použití

Nejdříve je nutné si samotný nástroj stáhnout pomocí příkazu `git clone https://github.com/Frose3/puppint_app.git`

Ke spuštění nástroje, je doporučeno využití Dockeru. Nástroj lze jednoduše spustit příkazem `docker compose up`. Při prvotním spuštěním bude uživatel vyzván k vytvoření super usera k přístupu do admin rozhraní. Po spuštění nástroje a vytvoření superuživatele je nutné přejít na adresu `http://localhost:8000`. Poté můžete nástroj jednoduše využít.

**Pro správné fungování všech nástrojů je potřeba, aby uživatel poskytl své API klíče jednotlivých služeb do souboru `api.env`.**

Výchozí přihlašovací údaje pro administrátorské rozhraní jsou `admin:admin`. Tyto údaje je možné změnit v souboru `docker-compose.yml` v sekci `environment`, kde jednotlivé údaje můžete změnit, dle potřeby. 

### Puppint
Tato část umožňuje využít unifikované nástroje, jako Shodan, Google Dork, FullHunt, a další, které jsou vypsané níže. Uživatel je zde schopen vypsat jednotlivé dotazy a také si vybrat, které z daných služeb chce využít. 

### Sock Puppet
Tento nástroj slouží k generování klamavého účtu pomocí umělé inteligence Google Gemini. V případě, že by funkce Gemini nebyla funkční, budou použity náhodně vybrané informace ze slovníků k jednotlivým vlastnostem klamavého účtu.

Po generaci se klamavý účet uloží do databáze, která je zobrazena  v administrátorském rozhraní, kde je uživatel schopen klamavý účet upravovat. V této databázi je možné uchovávat více klamavých účtů.

## Nástroje

### IPStack
**Popis:** IPstack je aplikace sloužící k získání geolokačních dat na základě veřejné IP adresy. 
Pomocí API lze získat informace o zemi, regionu, městě, souřadnicích daného 
místa a dalších.

- **Kde se zasílá požadavek:** Požadavek je posílán v souboru `osint_tootls/ipstack.py` ve funkci `ipstack()`. Této funkci je nutné předat veřejnou IP adresu, která je následně předána do dotazu
  - **Dotaz:** `response = requests.post(f"http://api.ipstack.com/{ip}?access_key={ipstack_api_key}")`
- **Zpracování výsledku:** Výsledky jsou zpracováné do proměnné `data`, která je typu slovník. Do toho jsou následně vloženy získané informace, jako je IP adresa, země, město a další.

**Použitá API dokumentace:** https://ipstack.com/documentation

### Shodan
**Popis:** Nástroj Shodan slouží k shromažďování informací o zařízeních připojených k internetu. Shodan oproti indexování webových stránek, např. Google, indexuje otevřené služby, porty a metadata z odpovědí jednotlivých síťových protokolů ze zařízení dostupných na adresách spojených s danou doménou.

- **Kde se zasílá požadavek:** Požadavek je možno nalézt v souboru `osint_tootls/shodan_api.py` ve funkci `shodan_search()` a `shodan_host()`. Pro dotaz je využívána knihovna `shodan`. Před samotným dotazem je nutné předat API klíč třídě `Shodan` z knihovny `shodan`. Dále je možné volat funkci `search()` pro hledání domény nebo funkci `host()` pro hledaní za pomocí IP adreesy.  
  - **Dotazy:**
    - API klíč: `api = shodan.Shodan(shodan_api_key)`
    - Pro vyhledání domény: `results = api.search(user_request)`
    - Pro vyhledání IP adresy: `host = api.host(user_request)`
- **Zpracování výsledku:** Výsledky ze skenu jednotlivých domén jsou nahrané do proměnné `data`, která je typu slovník. Do této struktury jsou vkládány informace, jako název domény, IP adresa, SSL verze a další. Tato proměnná je následně přidána do proměnné `all_data`, která je typu list.

**Použitá API dokumentace:** https://shodan.readthedocs.io/en/latest/

### FullHunt
**Popis:** FullHunt je nástroj, který automaticky mapuje a hlídá, jaké služby jsou veřejně 
dostupné z internetu v rámci organizace – jako jsou servery, webové aplikace nebo 
další služby. Firmám tak umožňuje mít neustálý 
přehled o tom, jak vypadá jejich viditelná část pro potenciální útočníky.

- **Kde se zasílá požadavek:** Požadavek je zasílán v souboru `osint_tools/fullhunt.py` ve funkci `fullhunt()` pomocí knihovny `httpx`. Této funkci je nutné předat doménu, která je následně předána do dotazu společně s hlavičkou, do které se předává API klíč.
  - **Dotaz:** `response = httpx.get(response = httpx.get(f"https://fullhunt.io/api/v1/domain/{user_query}/details", headers=headers), headers=headers)`
- **Zpracování výsledku:** Všechny výsledky jsou nahrané do proměnné `data`, která je typu slovník. Do této struktury jsou vkládány informace, jako informace o DNS, informace o IP adresse, portech a další.

**Použitá API dokumentace:** https://api-docs.fullhunt.io/

### Google Reverse Image Search a Google Dorking
**Popis:** Tento nástroj slouží k hledání referencí na uživatelem vložený obrázek. API pro tuto službu poskytuje web *serpapi.com*. Puppint zpracuje uživatelem vloženou URL adresu obrázku, poskytne ji API, které vrátí nalezené reference k danému obrázku. Google Dork využívá stejného poskytovatele API, ale využívá jiný engine.

- **Kde se zasílá požadavek:** Požadavek je zde zasílán v souboru `osint_tools/dorking.py` a `osint_tools/reverse.py` za pomocí serpapi knihovny, respektive za pomocí třídy GoogleSearch a následně funkce get_dict(). Do třídy GoogleSearch musí být nahrány parametry v podobě vybraného engine, dotazu a API klíče.
  - **Dotaz:**  
    - Pro předání parametrů třídě `GogleSearch`: `search = GoogleSearch(params)`
    - Pro vyhledání: `results = search.get_dict()`
- **Zpracování výsledku:** Všechny výsledky jsou nahrané do proměnné `data`, která je typu slovník. Do této struktury jsou vkládány informace v podobě nadpisu, ikony a jednotlivých odkazů na zdroj.
  
**Dokumentace k SerpAPI:** https://serpapi.com/google-reverse-image

### Generace Sock Puppeta
**Popis:** Ke generaci Sock Puppeta je použit seznam jmen, umělá inteligence Gemini 2.0 Flash a služba Mail.tm pro vytvoření emailové adresy.
Umělá inteligence Gemini od společnosti Google byla vybrána z důvodu poskytování API bez jakýchkoliv poplatků. V nástroji generuje: příjmení, město, adresu a biografii. Nástroj umožňuje také stažení informací o Sock Puppetovi ve formátu JSON, případně i úpravu jednotlivých informací.
Služba Mail.tm umožňuje vytvořit bezplatně dočasnou jednorázovou anonymní emailovou adresu. Tato služba také poskytuje API, díky kterému můžeme vše vytvořit uvnitř nástroje.

- **Kde se zasílá požadavek:** Požadavek se zasílá v souboru `osint_tools/sockpuppet.py`. K zaslání požadavku se využívá knihovna `genai` od Google. Součástí knihovny je třída `Client`, které je předáván API klíč. Společně je potom třída s parametrem API klíče nahrána do proměnné `client`. Díky této proměnné poté můžeme zavolat funkci `generate_content()`, které se předávají parametry v podobě modelu umělé inteligence, kterou chceme využít (v aktuálním případě `gemini-2.0-flash`) a parametr `contents`, kterému je předáván samotný dotaz pro umělou inteligenci.
  - **Dotazy:** 
    - API klíč: `client = genai.Client(api_key=gemini_api_key)`
    - Dotaz pro AI: `response = client.models.generate_content(model="gemini-2.0-flash", contents=f"{prompt}")`
- **Zpracování výsledku:** Všechny výsledky jsou nahrané do proměnné `data`, která je typu slovník. Do této struktury jsou vkládány informace, jako jméno, příjmení, věk a další.

**Dokumentace k Google Gemini:** https://ai.google.dev/gemini-api/docs

#### TempMail
**Popis:** Ke generaci e-mailové adresy pro klamavý účet je využívána služba Mail.tm, která umožňuje generovat dočasné e-mailové služby.

- **Kde se zasílá požadavek:** Požadavky jsou zasílány v souboru `osint_tools/tempmail.py` a to ve funkcích `create_email()` a `get_domain()`. Tyto požadavky jsou zasílány pomocí knihovny `requests`. U požadavku ve funkci `create_email()` je nutno předat také parametry v podobě hlavičky JSON dat, které obsahují vygenerovaný login, heslo a získanou doménu z funkce `get_domain()`.
  - **Dotazy:** 
    - Pro získání domény ve funkci `get_domain()`: `response = requests.get(f"{self.api_domain}/domains?page=1")`
    - Pro vytvoření emialu ve funkci `create_email()`: `response = requests.post(f"{self.api_domain}/accounts", headers=headers, data=json.dumps(data))`
- **Zpracování výsledku:** Výsledkem je poté funkční e-mailová adresa, kterou lze pod daným heslem využít na stránce https://mail.tm.

**Dokumentace k mail.tm:** https://docs.mail.tm

## Právní rámec a limity legálního použití nástroje Puppint

Nástroj Puppint je určen výhradně pro etické a legální použití v oblasti kybernetické bezpečnosti, výzkumu a vzdělávání. Jakékoliv zneužití tohoto nástroje může být považováno za protiprávní činnost a může mít právní důsledky.

### Legální rámec využití
**Získávání informací**
- Nástroj slouží k získávání veřejně dostupných informací a vytváření klamavých účtů. Přístup k informacím z neveřejných nebo chráněných částí služeb (např. pomocí klamavých účtů), může být považováno za porušení práva.


- § 230 trestního zákoníku stanoví, že kdo překoná bezpečnostní opatření, a tím neoprávněně získá přístup k počítačovému systému nebo k jeho části, bude potrestán odnětím svobody až na dvě léta, zákazem činnosti nebo propadnutím věci.
  - Uživatel může porušit toto právní ustanovení v případě, že pomocí nástroje získá neoprávněný přístup k počítači nebo jeho části.
- § 231 trestního zákoníku pojednává o opatření a přechovávání přístupového zařízení a hesla k počítačovému systému a jiných takových dat. Tedy toto právní ustanovení poruší ten, kdo vyrobí, uvede do oběhu, doveze, vyveze, proveze, nabízí, zprostředkuje, prodá nebo jinak zpřístupní, sobě nebo jinému opatří nebo přechovává například počítačové heslo, přístupový kód, data, postup nebo jakýkoli jiný podobný prostředek, pomocí něhož lze získat přístup k počítačovému systému nebo jeho části.
  - Toto právní ustanovení může uživatel porušit v případě, že pomocí nástroje vyhledá a získá například heslo k počítačovému systému a uchová toto heslo pro budoucí použití nebo v případě, že se toto heslo rozhodne sdílet.
- § 232 trestního zákoníku pojednává o neoprávněném zásahu do počítačového systému nebo nosiče informací z nedbalosti, přičemž toto právní ustanovení stanoví, že kdo z hrubé nedbalosti porušením povinnosti vyplývající ze zaměstnání, povolání, postavení nebo funkce nebo uložené podle zákona nebo smluvně převzaté.
  - V případě, že by uživatel byl fyzická či právnická osoba, která vykonává zaměstnání, povolání, postavení nebo funkci, nebo má jiné povinnosti mu uložené podle zákona nebo smluvně převzaté, může toto právní ustanovení porušit. 

**Ochrana soukromí**
- Uživatel je odpovědný za užívání nástroje tak, aby dodržoval principy ochrany soukromí podle § 84 a § 86 občanského zákoníku.
  - § 84 občanského zákoníku stanoví, že zachytit jakýmkoli způsobem podobu člověka tak, aby podle zobrazení bylo možné určit jeho totožnost, je možné jen s jeho svolením.
    - Toto právní ustanovení může uživatel porušit v případě, že si uloží nebo analyzuje profilovou fotografii reálné osoby z veřejné sociální sítě bez jejího vědomí a souhlasu, aby ji použil pro vytvoření klamavého účtu.
  - § 85 občanského zákoníků, který stanoví, že rozšiřovat podobu člověka je možné jen s jeho svolením.
    - Právní ustanovení bude porušeno v případě, že uživatel použije fotografii reálné osoby k vytvoření falešného profilu a šíří ji v rámci OSINT vyšetřování nebo klamavých interakcí online, čímž šíří její podobu bez souhlasu.
  - § 86 občanského zákoníků poté vyjmenovává zakázaná jednání v rámci ochrany soukromí. Stanoví, že Nikdo nesmí zasáhnout do soukromí jiného, nemá-li k tomu zákonný důvod. Nelze bez svolení člověka narušit jeho soukromé prostory, sledovat jeho soukromý život nebo pořizovat o tom zvukový nebo obrazový záznam, využívat takové či jiné záznamy pořízené o soukromém životě člověka třetí osobou, nebo takové záznamy o jeho soukromém životě šířit.
    - V případě, že uživatel pomocí nástroje Puppint zjišťuje, kde se konkrétní osoba pohybuje (např. na základě metadat nebo IP adresy) a tato data ukládá nebo šíří bez jejího souhlasu, poruší tím toto právní ustanovení.
  - Uživatel by také měl vyhnout jakémukoliv pronásledování, jelikož může dojít k naplnění skutkové podstaty § 354 trestního zákoníku, který pojednává o nebezpečném pronásledování.

**Podvod**
- § 209 trestného zákoníku, který pojednává od podvodu může nabýt své skutkové podstaty v případě, že uživatel odcizí identitu s cílem oklamat jiného, tedy uvést jinou osobu v omyl s cílem se obohatit.
  - Uživatel poruší právní ustanovení tak, že vytvoří falešnou identitu s cílem vylákat od jiné osoby informace, služby nebo přístup k uzavřeným systémům, což naplňuje znaky podvodného jednání.  

**Osobní údaje**
- Uživatel je také povinen se řídit Nařízením (EU) 2016/679 (GDPR) a českým zákonem č. 110/2019 Sb. o zpracování osobních údajů.
  - Toto nařízení musí uživatel dodržovat, jelikož může zpracovávat osobní údaje získané přes nástroj Puppint (např. jména, e-maily, IP adresy, fotografie) bez právního základu (souhlasu, oprávněného zájmu, plnění smlouvy apod.), a porušil by tím GDPR i český zákon o zpracování osobních údajů.

### Vyloučení odpovědnosti
Autor ani Vysoké učení technické v Brně tohoto nástroje nenese žádnou odpovědnost za jakékoliv škody způsobené jeho používáním. Uživatel je plně zodpovědný za způsob používání nástroje a je také zodpovědný za způsob, jakým nakládá se zpracovanými daty.