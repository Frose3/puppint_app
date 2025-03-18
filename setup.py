import os, sys
import itertools
import subprocess
import threading
import time

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Chyba při spuštění příkazu '{command}': {e}")

def is_virtualenv():
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)


def setup():
    if not is_virtualenv():
        print("Program neběží ve virtuálním prostředí!")
        print("Vytvoř virtuální prostředí a aktivuj ho před spuštěním tohoto skriptu:\n")
        print("   python -m venv venv\n")
        print("   source venv/bin/activate  # Linux/macOS\n")
        print("   venv\\Scripts\\activate   # Windows\n")
        return

    print("Virtuální prostředí detekováno. Instalace balíčků...")

    run_command("pip install --upgrade pip")
    if os.path.exists("requirements.txt"):
        run_command("pip install -r requirements.txt")
    else:
        print("Soubor requirements.txt nebyl nalezen! Instalace základních balíčků...")
        run_command("pip install django django-bootstrap-v5 djangorestframework")

    print("Instalace dokončena!")


if __name__ == "__main__":
    setup()


