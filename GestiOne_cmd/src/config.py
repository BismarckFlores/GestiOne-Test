"""
config.py

Módulo encargado de la configuración inicial del sistema y archivos base.
"""

import os
import csv
import sys
from utils import success_message, error_message

# Esto es para hacerlo ejecutable, si solo lo desea runear en el editor de codigo no dejalo como comentario
# def base_path():
#     if getattr(sys, 'frozen', False):
#         path = os.path.dirname(sys.executable)
#     else:
#         path = os.path.dirname(os.path.abspath(__file__))

#     os.makedirs(os.path.join(path, "storage"), exist_ok=True)
#     return path

# PRODUCTS_FILE = os.path.join(base_path(), "storage", "products.csv")
# SALES_FILE = os.path.join(base_path(), "storage", "sales.csv")
# SETTINGS_FILE = os.path.join(base_path(), "storage", "settings.txt")

PRODUCTS_FILE = "GestiOne_cmd/storage/products.csv"
SALES_FILE = "GestiOne_cmd/storage/sales.csv"
SETTINGS_FILE = "GestiOne_cmd/storage/settings.txt"


def init_files():
    """Inicializa los archivos de productos, ventas y configuración si no existen."""
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Price", "Quantity"])
        success_message("Archivo de productos creado correctamente.")

    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Sale ID", "Product ID", "Product Name", "Sales Quantity", "Total", "Date"])
        success_message("Archivo de ventas creado correctamente.")

    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, mode="w") as f:
            f.write("MIN_STOCK_LEVEL=10\n")
        success_message("Archivo de configuración creado correctamente.")


def get_min_stock_level():
    """Obtiene el nivel mínimo de stock configurado desde el archivo de configuración."""
    try:
        with open(SETTINGS_FILE, mode="r") as f:
            for line in f:
                if line.startswith("MIN_STOCK_LEVEL="):
                    return int(line.split("=")[1].strip())
    except FileNotFoundError:
        return 10


def set_min_stock_level():
    """Permite establecer un nuevo nivel mínimo de stock ingresado por el usuario."""
    try:
        new_level = int(input("🔧 Nuevo nivel mínimo de stock para alertas: ").strip())
        with open(SETTINGS_FILE, mode="w") as f:
            f.write(f"MIN_STOCK_LEVEL={new_level}\n")
        success_message(f"Nivel mínimo de stock actualizado a {new_level}.")
    except ValueError:
        error_message("El nivel mínimo de stock debe ser un número.")


def reset_min_stock_level():
    """Restablece el nivel mínimo de stock al valor predeterminado (10)."""
    with open(SETTINGS_FILE, "w") as f:
        f.write("MIN_STOCK_LEVEL=10\n")
    success_message("Nivel mínimo restablecido a 10.")


def reset_data():
    """Elimina todos los datos de inventario, ventas y restablece configuración."""
    confirmation = input("¿Estás seguro de que quieres borrar todo el inventario y las ventas? (s/n): ").strip().lower()
    if confirmation == "s":
        with open(PRODUCTS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Price", "Quantity"])
        with open(SALES_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Sale ID", "Product ID", "Product Name", "Sales Quantity", "Total", "Date"])
        reset_min_stock_level()
        success_message("Todos los datos han sido borrados correctamente.")
    else:
        error_message("Operación cancelada.")