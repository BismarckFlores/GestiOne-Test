import csv
from tabulate import tabulate
from config import PRODUCTS_FILE, get_min_stock_level
from utils import clear_console, pause, success_message, error_message


def show_inventory():
    clear_console()
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        products = list(reader)

        if not products:
            error_message("Inventario vacío.")
        else:
            print("\n📦 INVENTARIO")
            print(tabulate(products, headers=headers, tablefmt="fancy_grid"))
    pause()


def save_inventory(products):
    sorted_products = sorted(products.values(), key=lambda p: int(p[0]))
    with open(PRODUCTS_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Price", "Quantity"])
        writer.writerows(sorted_products)
    success_message("Inventario actualizado correctamente.")
    # pause()


def add_product():
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        next(reader)
        products = {row[0]: row for row in reader}

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
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        next(reader)
        products = {row[0]: row for row in reader}

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
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        next(reader)
        products = list(reader)

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
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        products = {row[0]: row for row in reader}

    print("\n📦 INVENTARIO COMPLETO")
    print(tabulate(products.values(), headers=headers, tablefmt="fancy_grid"))

    # Espera a que el usuario vea el inventario y presione enter
    pause()  # <-- Añade una pausa para que vea la tabla

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
    min_stock_level = get_min_stock_level()
    low_stock_products = []

    if products is None:
        with open(PRODUCTS_FILE, mode="r") as f:
            reader = csv.reader(f)
            headers = next(reader)
            products = list(reader)
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