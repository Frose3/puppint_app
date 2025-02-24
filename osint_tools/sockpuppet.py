from tempMail import Tempmail
import requests
from google import genai
from unidecode import unidecode
from google.genai import types
# from PIL import Image
from io import BytesIO

def custom_sock():
    name = input("Zadejte jméno: ")
    surname = input("Zadejte přijmení: ")
    age = input("Zadejte věk: ")
    email = input("Zadejte váš email: ")
    pw = input("Zadejte heslo: ")
    phone = input("Zadejte telefonní číslo: ")
    bio = input("Zadejte biografii: ")

    f = open("sockpuppet.txt", "a")
    f.write(f"Jméno: {name}\n"
            f"Příjmení {surname}\n"
            f"Věk: {age}\n"
            f"Emailová adresa: {email}\n"
            f"Heslo: {pw}\n"
            f"Mobilní telefon: {phone}\n\n"
            f"Biografie: {bio}\n")
    f.close()


def generated_sock():
    import random

    try:
        with open("wordlist_names.txt", "r", encoding="utf-8") as f:
            names = f.readlines()
            name = random.choice(names).strip()
            name = name.lower().split(",")[1]
    except FileNotFoundError:
        print("Wordlist file not found.")
        return

    GEMINI_API_KEY = "AIzaSyCx3LZGg8pJep8NTS-tQbdzsVdy8MmvMC0"

    client = genai.Client(api_key=GEMINI_API_KEY)
    surname_prompt = (f"Jednoslovně mi napiš dobré příjmení. Chci aby výsledek promptu byl čistě jedno příjmení, které tě napadne ke jménu {name.capitalize()}. "
                      f"Po tom co vybereš přijímení, tak chci, aby jsi nepsal za příjmením tečku.")
    surname_response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{surname_prompt}"
    )

    age = random.randint(18, 45)

    surname = surname_response.strip()

    login = name + surname[0] + str(age)
    password = f"{name}{unidecode(surname)}{random.randint(0, 500)}"
    tm = Tempmail(login, password)
    email = tm.create_email()

    bio_prompt = (f"Vytvoř náhodnou biografii pro osobu se jménem {name.capitalize()} {surname}, kterému je {age} let. Biografie by měla být uvěřitelná. Nesmí se jednat o osobu, která"
                  f" by určitým způsobem mohla být známa veřejnosti. Rovnou začni se samotnou biografií a nic více k tomu nepiš.")
    bio_response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{bio_prompt}"
    )

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



    # with open("generated_sockpuppet.txt", "a", encoding="utf-8") as f:
    #     f.write(f"Jméno: {name.capitalize()} {surname_response.text}\n")
    #     f.write(f"Věk: {age}\n")
    #     f.write(f"Emailová adresa: {email}\n")
    #     f.write(f"Heslo: {password}\n")
    #     f.write(f"Biografie: {bio_response.text}\n\n")

    return {
        "name": f"{name.capitalize()} {surname}",
        "age": age,
        "email": email,
        "password": password,
        "bio": bio_response.text
    }