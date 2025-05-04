# PUPPINT

## Co je to?

-------------

Puppint je nástroj, který vznikl za účelem sjednocení nástrojů 
pro OSINT analýzu a jednoduchou generaci Sock Puppeta pomocí umělé inteligence Gemini. 
Jelikož valná většina nástrojů OSINT je určena pro užití mimo EU celý nástroj byl 
přizpůsoben pro užití v ČR.

V případě, že by nástroj měl být rozšířen pro evropské prostředí, 
bylo by zapotřebí přeložit vstupní parametry pro umělou inteligenci Gemini a také 
přeložit přední část webu.

Součástí nástroje jsou také seznamy českých jmen, příjmení a měst. 
Tyto seznamy se v nástroji nachází v případě, kdy by umělá inteligence nebyla funkční. 
Pro rozšíření by bylo nutné přidat jména, příjmení a města, které by odpovídali 
evropskému prostředí, do jednotlivých existujících seznamů.

## Nástroje

------

### IPStack
**Popis:** IPstack je aplikace sloužící k získání geolokačních dat na základě veřejné IP adresy. 
Pomocí API lze získat informace o zemi, regionu, městě, souřadnicích daného 
místa a dalších.

- **Kde se zasílá požadavek:** Požadavek je posílán v souboru `osint_tootls/ipstack.py` ve funkci `ipstack()`. Této funkci je nutné předat veřejnou IP adresu, která je následně předána do dotazu:
  - **Dotaz:** `response = requests.post(f"http://api.ipstack.com/{ip}?access_key={ipstack_api_key}")`.
- **Zpracování výsledku:** Výsledky jsou zpracování do proměnné `data`, který je typu slovník. Do toho jsou následně nahrány získané informace, jako je IP adresa, země, město a další

**Použitá API dokumentace:** https://ipstack.com/documentation

### Shodan
**Popis:** Nástroj Shodan slouží k shromažďování informací o zařízeních připojených k internetu. Shodan oproti indexování webových stránek, jako to dělá Google, indexuje otevřené služby, porty a metadata získaná z odpovědí protokolů z těchto zařízení.

- **Kde se zasílá požadavek:** Požadavek je možno nalézt v souboru `osint_tootls/shodan_api.py` ve funkci `shodan_search()` a `shodan_host()`. Pro dotaz je využívána knihovna `shodan`. Před samotným dotazem je nutné předat API klíč třídě `Shodan` z knihovny `shodan`. Dále je možné volat funkci `search()` pro hledání domény nebo funkci `host()` pro hledaní za pomocí IP adreesy.  
  - **Dotazy:**
    - API klíč: `api = shodan.Shodan(shodan_api_key)`
    - Pro vyhledání domény: `results = api.search(user_request)`
    - Pro vyhledání IP adresy: `host = api.host(user_request)`
- **Zpracování výsledku:** 

**Použitá API dokumentace:** https://shodan.readthedocs.io/en/latest/

### FullHunt
**Popis:** FullHunt je nástroj, který automaticky mapuje a hlídá, jaké služby jsou veřejně 
dostupné z internetu v rámci organizace – jako jsou servery, webové aplikace nebo 
další služby – a pomáhá je chránit před útoky. Firmám tak umožňuje mít neustálý 
přehled o tom, jak vypadá jejich viditelná část pro potenciální útočníky.

- **Kde se zasílá požadavek:** Požadavek je zasílán v souboru `osint_tools/fullhunt.py` ve funkci `fullhunt()` pomocí knihovny `httpx`. Této funkci je nutné předat doménu, která je následně předána do dotazu společně s hlavičkou, do které se předává API klíč.
  - **Dotaz:** `response = httpx.get(response = httpx.get(f"https://fullhunt.io/api/v1/domain/{user_query}/details", headers=headers), headers=headers)`
- **Zpracování výsledku:** 

**Použitá API dokumentace:** https://api-docs.fullhunt.io/

### Google Reverse Image Search a Google Dorking
**Popis:** Tento nástroj slouží k hledání referencí na uživatelem vložený obrázek. API pro tuto službu poskytuje web *serpapi.com*. Puppint zpracuje uživatelem vloženou URL adresu obrázku, poskytne ji API, které vrátí nalezené reference k danému obrázku. Google Dork využívá stejného poskytovatele API, ale využívá jiný endpoint a to pro vyhledávání Google.

- **Kde se zasílá požadavek:**  Požadavek je zde zasílán v souboru `osint_tools/dorking.py` a `osint_tools/reverse.py` za pomocí serpapi knihovny, respektive za pomocí třídy GoogleSearch a následně funkce get_dict(). Do třídy GoogleSearch musí být nahrány parametry v podobě vybraného engine, dotazu a API klíče.
  - **Dotaz:**  
    - Pro předání parametrů třídě `GogleSearch`: `search = GoogleSearch(params)`
    - Pro vyhledání: `results = search.get_dict()`
- **Zpracování výsledku:** 

**Dokumentace k SerpAPI:** https://serpapi.com/google-reverse-image

### Generace Sock Puppeta
**Popis:** Ke generaci Sock Puppeta je použit seznam jmen, umělá inteligence Gemini 2.0 Flash a služba Mail.tm pro vytvoření emailové adresy.
Umělá inteligence Gemini od společnosti Google byla vybrána z důvodu poskytování API bez jakýchkoliv poplatků. V nástroji generuje: příjmení, město, adresu a biografii. Nástroj umožňuje také stažení informací o Sock Puppetovi ve formátu JSON, případně i úpravu jednotlivých informací.
Služba Mail.tm umožňuje vytvořit bezplatně dočasnou jednorázovou anonymní emailovou adresu. Tato služba také poskytuje API, díky kterému můžeme vše vytvořit uvnitř nástroje.

- **Kde se zasílá požadavek:** Požadavek se zasílá v souboru `osint_tools/sockpuppet.py`. K zaslání požadavku se využívá knihovna genai od Google. Součástí knihovny je třída `Client`, které je předáván API klíč. Společně je potom třída s parametrem API klíče nahrána do proměnné `client`. Díky této proměnné poté můžeme zavolat funkci `generate_content()`, které se předávají parametry v podobě modelu umělé inteligence, kterou chceme využít (v aktuálním případě `gemini-2.0-flash`) a parametr `contents`, kterému je předáván samotný dotaz pro umělou inteligneci
  - **Dotazy:** 
    - API klíč: `client = genai.Client(api_key=gemini_api_key)`
    - Dotaz pro AI: `response = client.models.generate_content(model="gemini-2.0-flash", contents=f"{prompt}")`
- **Zpracování výsledku:** Všechny výsledky jsou nahrané do proměnné `data`, která je typu slovník. Této proměnné jsou předávány informace, jako jmeno, příjmení, věk a další

**Dokumentace k Google Gemini:** https://ai.google.dev/gemini-api/docs

#### TempMail
**Popis:** Ke generaci e-mailové adresy pro klamavý účet je využívána také služba Mail.tm, která umožňuje generovat dočasné e-mailové služby.

- **Kde se zasílá požadavek:**  Požadavky je zasílány v souboru `osint_tools/tempmail.py` a to v funkcích `create_email()` a `get_domain()`. Tyto požadavky jsou zasílány pomocí knihovny `requests`. U požadavku ve funkci `create_email()` je nutno předat také parametry v podobě hlavičky JSON dat, které obsahují vygenerovaný login, heslo a získanou doménu z funkce `get_domain()`.
  - **Dotazy:** 
    - Pro získání domény ve funkci `get_domain()`: `response = requests.get(f"{self.api_domain}/domains?page=1")`
    - Pro vytvoření emialu ve funkci `create_email()`: `response = requests.post(f"{self.api_domain}/accounts", headers=headers, data=json.dumps(data))`
- **Zpracování výsledku:** Výsledkem je poté funkční e-mailová adresa, kterou lze pod daným heslem využít na stránce https://mail.tm

**Dokumentace k mail.tm:**  https://docs.mail.tm

## Právní rámec a limity legálního použití nástroje Puppint

-----------

Nástroj Puppint je určen výhradně pro etické a legální použití v oblasti kybernetické bezpečnosti, výzkumu a vzdělávání. Jakékoliv zneužití tohoto nástroje může být považováno za protiprávní činnost a může mít právní důsledky.

### Legální rámec využití
**Získávání informací**
- Nástroj slouží k získávání veřejně dostupných informací a vytváření klamavých účtů. Přístup k informacím z neveřejných nebo chráněných částí služeb (např. pomocí klamavých účtů), může být považováno za porušení občanského či trestního práva.

**Ochrana soukormí**
- Uživatel je odpovědný za užívání nástroje tak, aby dodržoval pravidla ochrany soukormí podle § 84 a §86 občanského zákoníku.
  - § 84 občanského zákoníku stanoví, že~zachytit jakýmkoli způsobem podobu člověka tak, aby~podle zobrazení bylo možné určit jeho totožnost, je možné jen s jeho svolením.
  - § 85 občanského zákoníků, který stanoví, že rozšiřovat podobu člověka je možné jen s jeho svolením
  - § 86 občanského zákoníků poté vyjmenovává zakázaná jednání v rámci ochrany soukromí. Stanoví, že Nikdo nesmí zasáhnout do soukromí jiného, nemá-li k tomu zákonný důvod. Nelze bez svolení člověka narušit jeho soukromé prostory, sledovat jeho soukromý život nebo pořizovat o tom zvukový nebo obrazový záznam, využívat takové či jiné záznamy pořízené o soukromém životě člověka třetí osobou, nebo takové záznamy o jeho soukromém životě šířit
  - Uživatel by také měl vyhnout jakémukoliv pronásledování, jelikož může dojít k naplnění skutkové podstaty § 354 trestního zákoníku, který pojednává o nebezpečném pronásledování

**Podvod**
- § 209 trestného zákoníku, který pojednává od podvodu může nabýt své skutkové podstaty v případě, že uživatel odcizí identitu s cílem oklamat jiného, tedy vyvolat v oběti omyl s cílem obohatit se, mohlo by takové jednání být posouzeno i dle

**Osobní údaje**
- Uživatel je také povinen se řídit Nařízením (EU) 2016/679 (GDPR) a českým zákonem č. 110/2019 Sb. o zpracování osobních údajů.

### Vyloučení odpovědnosti
Autor tohoto nástroje nenese žádnou odpovědnost za jakékoliv škody způsobené jeho používáním. Uživatel je plně zodpovědný za způsob používání nástroje a je také zodpovědný za způsob, jakým nakládá se zpracovanými daty.