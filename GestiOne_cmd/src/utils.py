import os
import csv
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)


def clear_console(force=False):
    if force:
        os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("\n🔄 Presiona Enter para continuar...")


def print_banner(title):
    border = "═" * (len(title) + 8)
    print(Fore.CYAN + f"\n╔{border}╗")
    print(Fore.CYAN + f"║    {title}    ║")
    print(Fore.CYAN + f"╚{border}╝\n")


def success_message(message):
    print(Fore.GREEN + f"✅ {message}\n")


def error_message(message):
    print(Fore.RED + f"❌ {message}\n")

<<<<<<< HEAD

=======
>>>>>>> 711d7f2605a89b6fcd5611344707e44836f9d5ae
def read_csv(file_path):
    """Lee un CSV completo y devuelve headers y datos."""
    with open(file_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = list(reader)
    return headers, data

<<<<<<< HEAD

=======
>>>>>>> 711d7f2605a89b6fcd5611344707e44836f9d5ae
def write_csv(file_path, headers, data):
    """Escribe un CSV completo con headers y datos."""
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

<<<<<<< HEAD

=======
>>>>>>> 711d7f2605a89b6fcd5611344707e44836f9d5ae
def append_csv(file_path, rows):
    """Agrega filas a un CSV existente."""
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)