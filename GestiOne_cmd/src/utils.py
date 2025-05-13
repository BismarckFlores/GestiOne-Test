"""
utils.py

Módulo utilitario con funciones generales como manejo de consola, mensajes y archivos CSV.
"""

import os
import csv
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)


def clear_console(force=False):
    """Limpia la consola según el sistema operativo."""
    if force:
        os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Realiza una pausa esperando a que el usuario presione Enter."""
    input("\n🔄 Presiona Enter para continuar...")


def print_banner(title):
    """Imprime un título decorativo con estilo."""
    border = "═" * (len(title) + 8)
    print(Fore.CYAN + f"\n╔{border}╗")
    print(Fore.CYAN + f"║    {title}    ║")
    print(Fore.CYAN + f"╚{border}╝\n")


def success_message(message):
    """Muestra un mensaje de éxito en color verde."""
    print(Fore.GREEN + f"✅ {message}\n")


def error_message(message):
    """Muestra un mensaje de error en color rojo."""
    print(Fore.RED + f"❌ {message}\n")


def read_csv(file_path):
    """Lee un CSV completo y devuelve headers y datos."""
    with open(file_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = list(reader)
    return headers, data


def write_csv(file_path, headers, data):
    """Sobrescribe un archivo CSV con encabezados y datos."""
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)


def append_csv(file_path, rows):
    """Agrega nuevas filas al final de un archivo CSV existente."""
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)