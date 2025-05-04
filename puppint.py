import os
import subprocess
from time import sleep

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puppint.settings')

import django
django.setup()
from django.contrib.auth.models import User

def print_banner():
    banner = r"""
██████╗ ██╗   ██╗██████╗ ██████╗ ██╗███╗   ██╗████████╗
██╔══██╗██║   ██║██╔══██╗██╔══██╗██║████╗  ██║╚══██╔══╝
██████╔╝██║   ██║██████╔╝██████╔╝██║██╔██╗ ██║   ██║   
██╔═══╝ ██║   ██║██╔═══╝ ██╔═══╝ ██║██║╚██╗██║   ██║   
██║     ╚██████╔╝██║     ██║     ██║██║ ╚████║   ██║   
╚═╝      ╚═════╝ ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝   

🔹 OSINT nástroj pro generování sock puppet identit a unifikaci OSINT nástrojů
🔹 Autor: [Filip Růžička]

🔹Tip: Nástroj vypnete zkratkou: Ctrl+C

!!!HAPPY HACKING!!!
"""
    print(banner)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Chyba při spuštění příkazu '{command}': {e}")

def check_superuser():
    if not User.objects.filter(is_superuser=True).exists():
        print("V databázi není žádný superuser!")
        create_superuser = input("Chceš ho vytvořit? (y/n): ").strip().lower()
        if create_superuser == "y":
            username = input("Zadej uživatelské jméno: ")
            email = input("Zadej e-mail: ")
            password = input("Zadej heslo: ")
            User.objects.create_superuser(username, email, password)

def main():

    print_banner()
    sleep(1)

    run_command("python manage.py makemigrations app")
    run_command("python manage.py migrate")

    check_superuser()

    run_command("python manage.py runserver 0.0.0.0:8000")

if __name__ == "__main__":
    main()