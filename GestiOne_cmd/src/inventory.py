"""
inventory.py

Módulo encargado de la gestión de inventario de productos.
"""

import csv
from tabulate import tabulate
from config import PRODUCTS_FILE, get_min_stock_level
from utils import clear_console, pause, success_message, error_message, read_csv, write_csv


def show_inventory():
    """Muestra el inventario actual en consola de manera tabulada."""
    clear_console()
    headers, products = read_csv(PRODUCTS_FILE)

    if not products:
        error_message("Inventario vacío.")
    else:
        print("\n📦 INVENTARIO")
        print(tabulate(products, headers=headers, tablefmt="fancy_grid"))
    pause()


def save_inventory(products):
    """
    Guarda el inventario en el archivo CSV ordenado por ID.

    Args:
        products (dict): Diccionario de productos con sus datos.
    """
    sorted_products = sorted(products.values(), key=lambda p: int(p[0]))
    write_csv(PRODUCTS_FILE, ["ID", "Name", "Price", "Quantity"], sorted_products)
    success_message("Inventario actualizado correctamente.")


def add_product():
    """Agrega un nuevo producto al inventario validando ID único, nombre, precio y cantidad."""
    headers, rows = read_csv(PRODUCTS_FILE)
    products = {row[0]: row for row in rows}

    while True:
        id_product = input("Product ID: ").strip()
        if not id_product.isdigit() or int(id_product) <= 0:
            error_message("ID debe ser un número positivo. Intente de nuevo.")
            pause()
        elif id_product in products:
            error_message("ID ya existe. Intente con otro.")
            pause()
        else:
            break

    name = input("Product Name: ").strip()
    while not name:
        error_message("El nombre no puede estar vacío. Intente de nuevo.")
        name = input("Product Name: ").strip()

    price = float(input("Product Price: ").strip())
    quantity = int(input("Product Quantity: ").strip())

    products[id_product] = [id_product, name, price, quantity]
    save_inventory(products)
    pause()


def edit_product():
    """Edita los datos de un producto existente en el inventario."""
    headers, rows = read_csv(PRODUCTS_FILE)
    products = {row[0]: row for row in rows}

    show_inventory()
    product_id = input("\nID del producto a editar: ").strip()

    if product_id not in products:
        error_message("Producto no encontrado. Intente de nuevo.")
        return

    current_product = products[product_id]
    print(f"\n📝 Editando {current_product[1]}")
    print(f"Nombre actual: {current_product[1]}")
    print(f"Precio actual: {current_product[2]}")

    new_name = input("Nuevo nombre (dejar en blanco para mantener actual): ").strip()
    new_price = input("Nuevo precio (dejar en blanco para mantener actual): ").strip()

    if new_name:
        current_product[1] = new_name
    if new_price:
        try:
            current_product[2] = str(float(new_price))
        except ValueError:
            error_message("Precio inválido. No se realizó el cambio.")
            pause()
            return

    save_inventory(products)
    pause()


def remove_product():
    """Elimina un producto del inventario según el ID proporcionado."""
    headers, products = read_csv(PRODUCTS_FILE)

    show_inventory()
    id_product = input("ID del producto a eliminar: ").strip()
    new_products = [p for p in products if p[0] != id_product]

    if len(new_products) == len(products):
        error_message("Producto no encontrado.")
        pause()
    else:
        save_inventory({p[0]: p for p in new_products})
        success_message(f"Producto con ID {id_product} eliminado correctamente.")
        pause()


def restock_product():
    """Agrega stock adicional a un producto existente en el inventario."""
    headers, rows = read_csv(PRODUCTS_FILE)
    products = {row[0]: row for row in rows}

    print("\n📦 INVENTARIO COMPLETO")
    print(tabulate(products.values(), headers=headers, tablefmt="fancy_grid"))

    pause()

    # Luego muestra productos con bajo stock si los hay
    check_low_stock(products, headers)

    product_id = input("\nID del producto para restock: ").strip()

    if product_id not in products:
        error_message("Producto no encontrado. Intente de nuevo.")
        pause()
        return

    try:
        restock_quantity = int(input(f"Cantidad para añadir al stock de {products[product_id][1]}: ").strip())
        if restock_quantity <= 0:
            error_message("La cantidad debe ser mayor a 0.")
            (pause)
            return
    except ValueError:
        error_message("Entrada inválida. Debe ser un número.")
        pause()
        return

    current_quantity = int(products[product_id][3])
    products[product_id][3] = str(current_quantity + restock_quantity)

    save_inventory(products)
    success_message(f"Stock de {products[product_id][1]} actualizado correctamente. Nuevo stock: {products[product_id][3]}")
    pause()


def check_low_stock(products=None, headers=None):
    """
    Muestra productos con stock por debajo del nivel mínimo configurado.

    Args:
        products (dict or list, optional): Productos a evaluar.
        headers (list, optional): Encabezados de las columnas.
    """
    min_stock_level = get_min_stock_level()
    low_stock_products = []

    if products is None:
        headers, products = read_csv(PRODUCTS_FILE)
    elif isinstance(products, dict):
        products = list(products.values())

    if headers is None:
        headers = ["ID", "Name", "Price", "Quantity"]

    for row in products:
        if int(row[3]) <= min_stock_level:
            low_stock_products.append(row)

    if low_stock_products:
        print("\n⚠️  PRODUCTOS CON STOCK BAJO")
        print(tabulate(low_stock_products, headers=headers, tablefmt="fancy_grid"))
    pause()