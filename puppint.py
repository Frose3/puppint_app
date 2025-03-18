import os
import subprocess
from time import sleep
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puppint.settings')

import django
django.setup()


from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from setup import is_virtualenv, run_command

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
"""
    print(banner)

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

    if not is_virtualenv():
        print("You are not using a virtual environment!")
        return

    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")

    check_superuser()

    run_command("python manage.py runserver")

if __name__ == "__main__":
    main()