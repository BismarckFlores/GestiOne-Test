import os
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