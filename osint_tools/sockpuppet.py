import datetime
import email
import os

from google.genai.errors import ClientError
from pyasn1_modules.rfc2459 import street_address

from osint_tools.tempmail import Tempmail
import requests
from google import genai
from unidecode import unidecode
from google.genai import types
# from PIL import Image
from io import BytesIO
import random
from app.models import SockPuppet
import configparser
from django.db import models


def generated_sock():
    try:
        with open("osint_tools/filtered_wordlist_names.txt", "r", encoding="utf-8") as f:
            names = f.readlines()
            name = random.choice(names).strip()
            name = name.lower().split(",")[1]
            gender = name.lower().split(",")[0]
    except FileNotFoundError:
        print("Wordlist file not found.")
        return

    config = configparser.ConfigParser()
    config.read("api.env")
    try:
        gemini_api_key = config.get("GEMINI", "GEMINI_API_KEY")
    except configparser.NoOptionError:
        return False

    client = genai.Client(api_key=gemini_api_key)
    try:
        surname_prompt = (f"Jednoslovně mi napiš dobré příjmení. Chci aby výsledek promptu byl čistě jedno příjmení, které tě napadne ke jménu {name.capitalize()}. Je to {gender}"
            f"Po tom co vybereš přijímení, tak chci, aby jsi nepsal za příjmením tečku.")
        surname_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f"{surname_prompt}"
        )
    except ClientError as e:
        return e

    age = random.randint(18, 45)

    surname = surname_response.text.strip()

    login_options = [
        surname.lower() + str(random.randint(0, 999)),
        name + str(random.randint(0, 999)),
        surname[0].lower() + name + str(random.randint(0, 999)),
        name + surname[0].lower() + str(random.randint(0, 999))
    ]

    login = random.choice(login_options)
    password = f"{name}{unidecode(surname)}{random.randint(0, 999)}"
    tm = Tempmail(login, password)
    email = tm.create_email()

    if email == 422:
        login = random.choice(login_options)
        tm = Tempmail(login, password)
        email = tm.create_email()

    year_of_birth = 2025 - age
    month_of_birth = random.randint(1, 12)
    if month_of_birth == 2:
        day_of_birth = random.randint(1, 28)
    else:
        day_of_birth = random.randint(1, 31)

    full_date = f"{day_of_birth}.{month_of_birth}.{year_of_birth}"
    # date_of_birth = datetime.datetime.strptime(full_date, "%d.%m.%Y").date()

    bio_prompt = (f"Vytvoř náhodnou biografii pro osobu se jménem {name.capitalize()} {surname} s věkem {age} let. Biografie by měla být uvěřitelná. Nesmí se jednat o osobu, která"
        f" by určitým způsobem mohla být známa veřejnosti. Aktuální zaměstnání by mělo odpovídat poskytnutému věku. Rovnou začni se samotnou biografií a nic více k tomu nepiš.")
    bio_response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{bio_prompt}"
    )
    bio = bio_response.text

    city_prompt = (f"Na základě této biografie: {bio} mi napiš z ktrého města daná osoba pochází. Chci, aby výsledek v promptu byl čistě název daného města. Jakmile vypíšeš toto město"
                   f"nepiš za ním tečku.")
    city_response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{city_prompt}"
    )
    city = city_response.text

    street_address_prompt = (f"Na základě města {city} mi napiš ulici, na které by mohla bydlet osoba s následující biografií: {bio}. Chci, aby výsledek promptu byl čistě název ulice."
                             f"Jakmile vypíšeš tuto ulici, nepiš za ním tečku.")
    street_address_response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{street_address_prompt}"
    )
    street = street_address_response.text

    # response = client.models.generate_images(
    #     model='imagen-3.0-generate-002',
    #     prompt=f'Osobu, která se jmenuje {name.capitalize()} {surname_response.text}, který má {age} let',
    #     config=types.GenerateImagesConfig(
    #         number_of_images=4,
    #     )
    # )
    # for generated_image in response.generated_images:
    #     image = Image.open(BytesIO(generated_image.image.image_bytes))
    #     image.save(f"{name.capitalize()}_{surname_response.text}.png")
    # print(f"Obrázek uložen jako {name.capitalize()}_{surname_response.text}.png")

    fullname = f"{name.capitalize()} {surname}"
    puppet = SockPuppet()

    if isinstance(email, str):
        data = {
            "fullname": fullname,
            "age": age,
            "date_of_birth": full_date,
            "city": city,
            "street": street,
            "email": email,
            "password": password,
            "bio": bio
        }
        puppet.name = fullname
        puppet.age = age
        puppet.date_of_birth = full_date
        puppet.city = city
        puppet.street_address = street
        puppet.email = email
        puppet.password = password
        puppet.bio = bio
        puppet.save()
    else:
        data = {
            "fullname": fullname,
            "age": age,
            "date_of_birth": full_date,
            "city": city,
            "street": street,
            "bio": bio,
        }
        puppet.name = fullname
        puppet.age = age
        puppet.date_of_birth = full_date
        puppet.city = city
        puppet.street_address = street
        puppet.bio = bio
        puppet.save()
    return data

    # file_path = "/puppet"
    # file_name = f"{unidecode(name.lower())}_{unidecode(surname.lower())}.txt"
    #
    # with open(os.path.join(file_path, file_name), "x", encoding="utf-8") as f:
    #     f.write(f"Jméno: {fullname}\n")
    #     f.write(f"Narozena: {int(datetime.date.today().strftime('%Y')) - age}\n\n")
    #     f.write(f"Věk: {age}\n\n")
    #     f.write(f"Příhlásit se můžete na: https://mail.tm/en/\n")
    #     # f.write(f"Emailová adresa: {email}\n")
    #     f.write(f"Heslo: {password}\n")
    #     f.write(f"Biografie: {bio}\n\n")