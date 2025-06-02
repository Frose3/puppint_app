import email
import os

from google.genai.errors import ClientError, ServerError
from dotenv import load_dotenv
from osint_tools.tempmail import Tempmail
from google import genai
from unidecode import unidecode
import random
from app.models import SockPuppet
import configparser
from credit_card_info_generator import generate_credit_card


def generate_birth_num(gender, year_of_birth, month_of_birth, day_of_birth):
    year = str(year_of_birth)[-2:]
    month = str(month_of_birth)[-2:] if gender == 'male' else str(month_of_birth + 50)[-2:]
    day = str(day_of_birth)[-2:]

    while True:
        final_rand = generate_birth_number_ending()
        control = int(year + month + day + final_rand) % 11
        if control == 10:
            control = 0

        mod = int(year + month + day + final_rand + str(control)) % 11
        if mod == 0:
            return f"{year}{month}{day}/{final_rand}{control}"


def generate_birth_number_ending():
    while True:
        n1, n2, n3 = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)
        if n1 != 0 and n2 != 0 and n3 != 0:
            return f"{n1}{n2}{n3}"

def generate_email(first_name, surname, password):
    login_options = [
        unidecode(surname.lower()) + str(random.randint(0, 999)),
        unidecode(first_name) + str(random.randint(0, 999)),
        unidecode(surname[0].lower()) + unidecode(first_name) + str(random.randint(0, 999)),
        unidecode(first_name) + unidecode(surname[0].lower()) + str(random.randint(0, 999))
    ]
    login = random.choice(login_options)

    tm = Tempmail(login, password)
    email = tm.create_email()

    if email == 422:
        login = random.choice(login_options)
        tm = Tempmail(login, password)
        email = tm.create_email()

    return email

def generate_sock():
    try:
        with open("osint_tools/wordlist_firstnames.txt", "r", encoding="utf-8") as f:
            names = f.readlines()
            name = random.choice(names).strip()
            first_name = name.lower().split(",")[1]
            gender = name.lower().split(",")[0]
    except FileNotFoundError:
        print("Wordlist nebyl nalezen.")
        return None

    try:
        load_dotenv(dotenv_path="api.env")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key == "":
            return False
    except configparser.NoOptionError:
        return False

    client = genai.Client(api_key=gemini_api_key)

    surname = ""
    try:
        surname_prompt = (f"Jednoslovně mi napiš dobré příjmení. Chci aby výsledek promptu byl čistě jedno příjmení, které tě napadne ke jménu {first_name.capitalize()}. Je to {gender}"
            f"Po tom co vybereš přijímení, tak chci, aby jsi nepsal za příjmením tečku.")
        surname_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f"{surname_prompt}"
        )
        surname = surname_response.text.strip()
    except (ClientError, ServerError) as e:
        print(e)
        if gender == 'male':
            try:
                with open("osint_tools/wordlist_lastnames_male.txt", "r", encoding="utf-8") as f:
                    last_names = f.readlines()
                    surname = random.choice(last_names).strip()
            except FileNotFoundError:
                print("Wordlist nebyl nalezen.")
                return None

        if gender == 'female':
            try:
                with open("osint_tools/wordlist_lastnames_female.txt", "r", encoding="utf-8") as f:
                    last_names = f.readlines()
                    surname = random.choice(last_names).strip()
            except FileNotFoundError:
                print("Wordlist nebyl nalezen.")
                return None

    age = random.randint(18, 40)

    try:
        height_prompt = (f"Napiš jakou výšku v centimetrech by mohla mít osoba se jménem {first_name.capitalize()} {surname} s věkem {age}."
            f"Rovnou napiš příslušné celé číslo a nic více k tomu nepiš. Nepiš za výškou tečku.")
        height_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f"{height_prompt}"
        )
        height = int(height_response.text.strip())
    except (ClientError, ServerError) as e:
        height = random.randint(156, 200)

    try:
        weight_prompt = (f"Napiš jakou váhu v kilogramech by mohla mít osoba se jménem {first_name.capitalize()} {surname}, s věkem {age} a s výškou {height}."
            f"Rovnou napiš příslušné celé číslo a nic více k tomu nepiš. Nepiš za váhu tečku.")
        weight_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f"{weight_prompt}"
        )
        weight = int(weight_response.text.strip())
    except (ClientError, ServerError) as e:
        weight = random.randint(60, 110)

    card = generate_credit_card('Visa')

    card_num = card['card_number']
    card_cvv = card['cvv']
    card_exp = card['expiry_date']

    year_of_birth = 2025 - age
    month_of_birth = random.randint(1, 12)
    if month_of_birth == 2:
        day_of_birth = random.randint(1, 28)
    else:
        day_of_birth = random.randint(1, 31)

    full_date = f"{day_of_birth}.{month_of_birth}.{year_of_birth}"

    birth_number = generate_birth_num(gender, year_of_birth, month_of_birth, day_of_birth)
    password = f"{first_name}{unidecode(surname)}{random.randint(0, 999)}"
    email = generate_email(first_name, surname, password)

    try:
        bio_prompt = (f"Vytvoř náhodnou biografii pro osobu se jménem {first_name.capitalize()} {surname} s věkem {age} let. Biografie by měla být uvěřitelná. Nesmí se jednat o osobu, která"
            f" by určitým způsobem mohla být známa veřejnosti. Aktuální zaměstnání by mělo odpovídat poskytnutému věku. Rovnou začni se samotnou biografií a nic více k tomu nepiš.")
        bio_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f"{bio_prompt}"
        )
        bio = bio_response.text
    except (ClientError, ServerError) as e:
        print(e)
        bio = ""

    try:
        city_prompt = (f"Na základě této biografie: {bio} mi napiš z ktrého města daná osoba pochází. Pokud město nepůjde jasně z biografie určit, použij náhodné město z oklí oblasti zmíněné v biografii."
                       f"Chci, aby výsledek v promptu byl čistě název daného města. Jakmile vypíšeš toto město nepiš za ním tečku.")
        city_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f"{city_prompt}"
        )
        city = city_response.text
    except (ClientError, ServerError) as e:
        print(e)
        try:
            with open("osint_tools/wordlist_cities.txt", "r", encoding="utf-8") as f:
                cities = f.readlines()
                city = random.choice(cities).strip()
        except FileNotFoundError:
            print("Wordlist nebyl nalezen.")
            return None

    try:
        street_address_prompt = (f"Na základě města {city} mi napiš náhodnou ulici, na které by bylo možno bydlet. Chci, aby výsledek promptu byl čistě název ulice."
                                 f"Jakmile vypíšeš tuto ulici, nepiš za ním tečku.")
        street_address_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f"{street_address_prompt}"
        )
        street = street_address_response.text
    except (ClientError, ServerError) as e:
        print(e)
        street = ""

    try:
        work_bio_prompt = (f"Na základě této biografie: {bio}, vytvoř profesní životopis. Profesní životopis by měl být uvěřitelný. Info o osobě: {email}, město: {city}, ulice: {street}"
            f"Celý životopis sepiš ve formátu Markdown. Vynechej část: \"<p>```markdown</p>\" a rovnou začni se samotný životopis a nic více k tomu nepiš.")
        work_bio_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f"{work_bio_prompt}"
        )
        work_bio = work_bio_response.text
    except (ClientError, ServerError) as e:
        print(e)
        work_bio = ""

    fullname = f"{first_name.capitalize()} {surname}"

    puppet = SockPuppet()

    data = {
        "fullname": fullname,
        "age": age,
        "height": height,
        "weight": weight,
        "date_of_birth": full_date,
        "birth_number": birth_number,
        "city": city,
        "street": street,
        "card_num": card_num,
        "card_cvv": card_cvv,
        "card_exp": card_exp,
        "bio": bio,
        "work_bio": work_bio,
        "additional_info": ""
    }

    if isinstance(email, str):
        data["email"] = email
        data["password"] = password
        puppet.email = email
        puppet.password = password

    puppet.name = fullname
    puppet.age = age
    puppet.height = height
    puppet.weight = weight
    puppet.date_of_birth = full_date
    puppet.birth_number = birth_number
    puppet.city = city
    puppet.street_address = street
    puppet.card_num = card_num
    puppet.card_cvv = card_cvv
    puppet.card_exp = card_exp
    puppet.bio = bio
    puppet.work_bio = work_bio
    puppet.additional_info = ""

    puppet.save()
    return data