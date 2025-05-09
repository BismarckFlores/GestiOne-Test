import csv
import os
import colorama
from colorama import Fore, Style
from tabulate import tabulate
from datetime import datetime, timedelta

# Inicializa colorama para colores en terminal
colorama.init(autoreset=True)

# Función para limpiar la consola solo cuando es necesario
def clear_console(force=False):
    if force:
        os.system('cls' if os.name == 'nt' else 'clear')

# Función para pausar después de mostrar información importante
def pause():
    input("\n🔄 Presiona Enter para continuar...")

# Archivos CSV para almacenar información
PRODUCTS_FILE = "GestiOne_cmd/products.csv"
SALES_FILE = "GestiOne_cmd/sales.csv"
SETTINGS_FILE = "GestiOne_cmd/settings.txt"

# Encabezado decorativo
def print_banner(title):
    border = "═" * (len(title) + 8)
    print(Fore.CYAN + f"\n╔{border}╗")
    print(Fore.CYAN + f"║    {title}    ║")
    print(Fore.CYAN + f"╚{border}╝\n")

# Mensaje de éxito
def success_message(message):
    print(Fore.GREEN + f"✅ {message}\n")

# Mensaje de error
def error_message(message):
    print(Fore.RED + f"❌ {message}\n")

# Inicializa los archivos si no existen
def init_files():
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

# Carga el nivel mínimo de stock desde el archivo de configuración
def get_min_stock_level():
    try:
        with open(SETTINGS_FILE, mode="r") as f:
            for line in f:
                if line.startswith("MIN_STOCK_LEVEL="):
                    return int(line.split("=")[1].strip())
    except FileNotFoundError:
        return 10  # Valor predeterminado si no existe el archivo

# Permite cambiar el nivel mínimo de stock
def set_min_stock_level():
    try:
        new_level = int(input(Fore.YELLOW + "🔧 Nuevo nivel mínimo de stock para alertas: ").strip())
        with open(SETTINGS_FILE, mode="w") as f:
            f.write(f"MIN_STOCK_LEVEL={new_level}\n")
        success_message(f"Nivel mínimo de stock actualizado a {new_level}.")
    except ValueError:
        error_message("El nivel mínimo de stock debe ser un número.")

# Verifica si algún producto está bajo el nivel mínimo de stock
def check_low_stock():
    min_stock_level = get_min_stock_level()
    low_stock_products = []

    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            product_id, name, price, quantity = row
            if int(quantity) <= min_stock_level:
                low_stock_products.append(row)

    if low_stock_products:
        print("\n⚠️  PRODUCTOS CON STOCK BAJO")
        print(tabulate(low_stock_products, headers=headers, tablefmt="fancy_grid"))
        print()

# Muestra todos los productos del inventario
def show_inventory():
    clear_console()
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        products = list(reader)
        
        # Verificar si el inventario está vacío
        if not products:
            print(Fore.YELLOW + "\n📦 Inventario vacío.\n")
        else:
            print(Fore.CYAN + "\n📦 INVENTARIO")
            print(tabulate(products, headers=headers, tablefmt="fancy_grid"))
    pause()

# Guarda el inventario actualizado sin eliminar productos agotados
def save_inventory(products):
    sorted_products = sorted(products.values(), key=lambda p: int(p[0]))
    with open(PRODUCTS_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Price", "Quantity"])
        writer.writerows(sorted_products)
    success_message("Inventario actualizado correctamente.")

# Permite agregar nuevos productos al inventario
def add_product():
    # Cargar todos los productos existentes
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        next(reader)
        products = {row[0]: row for row in reader}

    # Solicitar datos del nuevo producto
    while True:
        id_product = input("Product ID: ").strip()
        if not id_product.isdigit() or int(id_product) <= 0:
            print("❌ ID debe ser un número positivo. Intente de nuevo.\n")
        elif id_product in products:
            print("❌ ID ya existe. Intente con otro.\n")
        else:
            break
    
    name = input("Product Name: ").strip()
    while not name:
        print("❌ El nombre no puede estar vacío. Intente de nuevo.")
        name = input("Product Name: ").strip()

    price = float(input("Product Price: ").strip())
    quantity = int(input("Product Quantity: ").strip())

    # Añadir el nuevo producto
    products[id_product] = [id_product, name, price, quantity]
    save_inventory(products)

    print("✅ Producto agregado correctamente.\n")

# Permite editar solo el nombre y precio de un producto, no la cantidad
def edit_product():
    # Cargar productos del archivo
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        products = {row[0]: row for row in reader}

    # Mostrar inventario antes de editar
    show_inventory()

    # Solicitar el ID del producto a editar
    product_id = input("\nID del producto a editar: ").strip()

    # Verificar si el producto existe
    if product_id not in products:
        print("❌ Producto no encontrado. Intente de nuevo.\n")
        return

    # Mostrar los detalles actuales del producto
    current_product = products[product_id]
    print(f"\n📝 Editando {current_product[1]}")
    print(f"Nombre actual: {current_product[1]}")
    print(f"Precio actual: {current_product[2]}")

    # Solicitar los nuevos valores
    new_name = input("Nuevo nombre (dejar en blanco para mantener actual): ").strip()
    new_price = input("Nuevo precio (dejar en blanco para mantener actual): ").strip()

    # Actualizar solo los campos que se modificaron
    if new_name:
        current_product[1] = new_name
    if new_price:
        try:
            current_product[2] = str(float(new_price))
        except ValueError:
            print("❌ Precio inválido. No se realizó el cambio.\n")
            return

    # Guardar los cambios
    save_inventory(products)
    print(f"✅ Producto {current_product[1]} actualizado correctamente.\n")

# Permite restablecer el stock de productos con prioridad a los que necesitan restock urgente
def restock_product():
    # Cargar los productos desde el archivo
    min_stock_level = get_min_stock_level()
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        products = {row[0]: row for row in reader}

    # Filtrar productos con bajo stock
    low_stock_products = [p for p in products.values() if int(p[3]) <= min_stock_level]

    # Mostrar todos los productos para facilitar el restock
    print("\n📦 INVENTARIO COMPLETO")
    print(tabulate(products.values(), headers=headers, tablefmt="fancy_grid"))

    # Mostrar productos con bajo stock
    if low_stock_products:
        print("\n⚠️  PRODUCTOS CON STOCK BAJO")
        print(tabulate(low_stock_products, headers=headers, tablefmt="fancy_grid"))
    else:
        print("\n✅ No hay productos con stock bajo.\n")

    # Solicitar el ID del producto para restock
    product_id = input("\nID del producto para restock: ").strip()
    
    # Verificar si el producto existe
    if product_id not in products:
        print("❌ Producto no encontrado. Intente de nuevo.\n")
        return
    
    # Solicitar la cantidad a añadir
    try:
        restock_quantity = int(input(f"Cantidad para añadir al stock de {products[product_id][1]}: ").strip())
        if restock_quantity <= 0:
            print("❌ La cantidad debe ser mayor a 0.\n")
            return
    except ValueError:
        print("❌ Entrada inválida. Debe ser un número.\n")
        return
    
    # Actualizar el stock
    current_quantity = int(products[product_id][3])
    products[product_id][3] = str(current_quantity + restock_quantity)

    # Guardar los cambios
    save_inventory(products)
    print(f"✅ Stock de {products[product_id][1]} actualizado correctamente. Nuevo stock: {products[product_id][3]}\n")

# Permite eliminar un producto del inventario sin cambiar los IDs
def remove_product():
    # Cargar todos los productos del inventario
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        products = list(reader)
    
    # Mostrar inventario antes de eliminar
    show_inventory()
    id_product = input("ID del producto a eliminar: ").strip()
    
    # Filtrar el producto a eliminar
    new_products = [p for p in products if p[0] != id_product]
    
    if len(new_products) == len(products):
        print("❌ Producto no encontrado.\n")
    else:
        save_inventory({p[0]: p for p in new_products})
        print(f"✅ Producto con ID {id_product} eliminado correctamente.\n")

# Registra un nuevo ticket de venta con agrupación de productos
def register_ticket():
    # Cargar productos para verificar stock
    with open(PRODUCTS_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        products = {row[0]: row for row in reader}

    ticket = {}
    total_ticket = 0

    while True:
        show_inventory()
        product_id = input("ID del producto para añadir al ticket (o 'f' para finalizar): ").strip()
        
        if product_id.lower() == 'f':
            break
        
        if product_id in products:
            name = products[product_id][1]
            price = float(products[product_id][2])
            stock = int(products[product_id][3])

            while True:
                try:
                    quantity = int(input(f"Cantidad de {name} (disponible: {stock}): ").strip())
                    if quantity > stock:
                        print("❌ No hay suficiente stock. Intente de nuevo.")
                    elif quantity <= 0:
                        print("❌ Cantidad inválida. Debe ser mayor a 0.")
                    else:
                        break
                except ValueError:
                    print("❌ Entrada inválida. Debe ser un número.")

            if product_id in ticket:
                ticket[product_id]["quantity"] += quantity
                ticket[product_id]["subtotal"] += price * quantity
            else:
                ticket[product_id] = {
                    "name": name,
                    "price": price,
                    "quantity": quantity,
                    "subtotal": price * quantity
                }

            total_ticket += price * quantity
            products[product_id][3] = str(stock - quantity)

            print(f"✅ {name} x{quantity} añadido al ticket.\n")
        else:
            print("❌ Producto no encontrado. Intente de nuevo.\n")

    if not ticket:
        print("❌ El ticket está vacío. No se registró ninguna venta.\n")
        return

    # Guardar el inventario actualizado
    save_inventory(products)

    # Calcular el nuevo ID de venta
    try:
        with open(SALES_FILE, mode="r") as f:
            sales_reader = csv.reader(f)
            next(sales_reader)  # Saltar encabezado
            sales_data = list(sales_reader)
            sale_id = int(sales_data[-1][0]) + 1 if sales_data else 1
    except FileNotFoundError:
        sale_id = 1

    # Guardar el ticket en el archivo de ventas
    with open(SALES_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for pid, details in ticket.items():
            name = details["name"]
            quantity = details["quantity"]
            subtotal = details["subtotal"]
            writer.writerow([sale_id, pid, name, quantity, subtotal, date])

    print(f"✅ Ticket registrado correctamente. Total: ${total_ticket:.2f}\n")

# Muestra todas las ventas registradas
def show_sales():
    clear_console()
    with open(SALES_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        sales = list(reader)

    # Verificar si hay ventas
    if not sales:
        print("\n🧾 HISTORIAL DE VENTAS")
        print("No hay ventas registradas.\n")
    else:
        print("\n🧾 HISTORIAL DE VENTAS")
        print(tabulate(sales, headers=headers, tablefmt="fancy_grid"))
    
    pause()

# Genera reportes de ventas por día, semana o mes con validación en español
def sales_report_by_period():
    # Opciones válidas
    valid_periods = {
        "diario": "daily",
        "semanal": "weekly",
        "mensual": "monthly"
    }

    # Solicitar el periodo
    period = input("Seleccione el periodo (diario, semanal, mensual): ").strip().lower()
    
    if period not in valid_periods:
        print("❌ Opción inválida. Por favor, elija entre 'diario', 'semanal' o 'mensual'.\n")
        pause()
        return
    
    # Convertir el periodo a inglés para el cálculo
    period_eng = valid_periods[period]

    # Cargar las ventas
    with open(SALES_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        sales = list(reader)
    
    if not sales:
        print("\n🧾 No hay ventas registradas.\n")
        return
    
    # Filtrar ventas por periodo
    now = datetime.now()
    filtered_sales = []

    for sale in sales:
        sale_date = datetime.strptime(sale[-1], "%Y-%m-%d %H:%M:%S")
        
        if period_eng == "daily" and sale_date.date() == now.date():
            filtered_sales.append(sale)
        elif period_eng == "weekly" and sale_date >= now - timedelta(days=7):
            filtered_sales.append(sale)
        elif period_eng == "monthly" and sale_date.month == now.month and sale_date.year == now.year:
            filtered_sales.append(sale)

    # Mostrar resultados
    if filtered_sales:
        print(f"\n🧾 Reporte de Ventas ({period.capitalize()})")
        print(tabulate(filtered_sales, headers=headers, tablefmt="fancy_grid"))
    else:
        print(f"\n🧾 No hay ventas registradas para el periodo seleccionado ({period}).\n")
    pause()

# Genera un ranking de los productos más vendidos
def top_selling_products():
    # Cargar las ventas
    with open(SALES_FILE, mode="r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        sales = list(reader)
    
    if not sales:
        print("\n📈 No hay ventas registradas.\n")
        pause()
        return
    
    # Contar las ventas por producto
    product_sales = {}
    for sale in sales:
        product_id = sale[1]
        product_name = sale[2]
        quantity = int(sale[3])
        
        if product_id not in product_sales:
            product_sales[product_id] = {"name": product_name, "quantity": 0}
        
        product_sales[product_id]["quantity"] += quantity

    # Ordenar los productos más vendidos
    ranked_products = sorted(product_sales.values(), key=lambda p: p["quantity"], reverse=True)

    # Mostrar resultados
    print("\n🔝 Productos Más Vendidos")
    data = [[p["name"], p["quantity"]] for p in ranked_products]
    print(tabulate(data, headers=["Producto", "Cantidad Vendida"], tablefmt="fancy_grid"))
    pause()

# Resetea los archivos de datos
def reset_data():
    confirmation = input("¿Estás seguro de que quieres borrar todo el inventario y las ventas? (s/n): ").strip().lower()
    if confirmation == "s":
        # Reiniciar archivo de productos
        with open(PRODUCTS_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Price", "Quantity"])

        # Reiniciar archivo de ventas
        with open(SALES_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Sale ID", "Product ID", "Product Name", "Sales Quantity", "Total", "Date"])

        print("✅ Configuración de stock mínima creada con valor predeterminado de 10.\n")

        print("✅ Datos reseteados correctamente.\n")
    else:
        print("❌ Operación cancelada.\n")

# Submenú para gestión de inventario
def inventory_management():
    clear_console(True)
    while True:
        print_banner("GESTIÓN DE INVENTARIO")
        print(Fore.YELLOW + "1. 📦 Mostrar inventario")
        print(Fore.YELLOW + "2. ➕ Agregar producto")
        print(Fore.YELLOW + "3. ✏️  Editar producto")
        print(Fore.YELLOW + "4. 🗑️  Eliminar producto")
        print(Fore.YELLOW + "5. 🔄 Restock de producto")
        print(Fore.YELLOW + "6. 🔙 Volver al menú principal")
        
        option = input(Fore.YELLOW + "\nSeleccione una opción: ").strip()
        
        match option:
            case "1":
                show_inventory()
            case "2":
                add_product()
            case "3":
                edit_product()
            case "4":
                remove_product()
            case "5":
                restock_product()
            case "6":
                break
            case _:
                error_message("Opción inválida. Intente de nuevo.")

# Submenú para gestión de ventas
def sales_management():
    clear_console(True)
    while True:
        print_banner("GESTIÓN DE VENTAS")
        print(Fore.YELLOW + "1. 🧾 Registrar Ticket venta")
        print(Fore.YELLOW + "2. 📅 Ver historial de ventas")
        print(Fore.YELLOW + "3. 📊 Reporte de ventas (Diario, Semanal, Mensual)")
        print(Fore.YELLOW + "4. 🔝 Productos más vendidos")
        print(Fore.YELLOW + "5. 🔙 Volver al menú principal")
        option = input(Fore.YELLOW + "\nSeleccione una opción: ").strip()
        
        match option:
            case "1":
                register_ticket()
            case "2":
                show_sales()
            case "3":
                sales_report_by_period()
            case "4":
                top_selling_products()
            case "5":
                break
            case _:
                error_message("Opción inválida. Intente de nuevo.")

# Submenú para configuración
def settings_management():
    clear_console(True)
    while True:
        print_banner("CONFIGURACIÓN")
        print(Fore.YELLOW + "1. ⚙️ Configurar nivel mínimo de stock")
        print(Fore.YELLOW + "2. 🔄 Resetear datos")
        print(Fore.YELLOW + "3. 🔙 Volver al menú principal")
        option = input(Fore.YELLOW + "\nSeleccione una opción: ").strip()
        
        match option:
            case "1":
                stock_settings()
            case "2":
                reset_data()
            case "3":
                break
            case _:
                error_message("Opción inválida. Intente de nuevo.")

# Submenú para configuración de stock mínimo
def stock_settings():
    while True:
        clear_console()
        current_level = get_min_stock_level()
        print_banner("CONFIGURACIÓN DE STOCK MÍNIMO")
        print(Fore.BLUE + f"🔎 Nivel mínimo actual: {current_level}")
        print(Fore.BLUE + "\n1. ✏️ Cambiar nivel mínimo de stock")
        print(Fore.BLUE + "2. 🔄 Restablecer a valor predeterminado (10)")
        print(Fore.BLUE + "3. 🔙 Volver al menú anterior")
        
        option = input(Fore.BLUE + "\nSeleccione una opción: ").strip()

        match option:
            case "1":
                try:
                    new_level = int(input(Fore.BLUE + "\nNuevo nivel mínimo de stock: ").strip())
                    if new_level <= 0:
                        print("❌ El nivel mínimo debe ser mayor a 0.\n")
                    else:
                        with open(SETTINGS_FILE, mode="w") as f:
                            f.write(f"MIN_STOCK_LEVEL={new_level}\n")
                        print(f"\n✅ Nivel mínimo actualizado a {new_level}.\n")
                        pause()
                except ValueError:
                    print("❌ Entrada inválida. Debe ser un número.\n")
                    pause()

            case "2":
                with open(SETTINGS_FILE, mode="w") as f:
                    f.write("MIN_STOCK_LEVEL=10\n")
                print("\n✅ Nivel mínimo restablecido a 10.\n")
                pause()

            case "3":
                break

            case _:
                print("❌ Opción inválida. Intente de nuevo.\n")
                pause()


# Menú principal del sistema con submenús
def main():
    init_files()
    while True:
        clear_console(True)
        print_banner("MENÚ PRINCIPAL")
        print(Fore.GREEN + "1. 📦 Gestión de Inventario")
        print(Fore.GREEN + "2. 🧾 Gestión de Ventas")
        print(Fore.GREEN + "3. ⚙️ Configuración")
        print(Fore.GREEN + "4. 🚪 Salir")
        option = input(Fore.GREEN + "\nSeleccione una opción: ").strip()
        
        match option:
            case "1":
                inventory_management()
            case "2":
                sales_management()
            case "3":
                settings_management()
            case "4":
                print(Fore.CYAN + "\n🎉 ¡Hasta luego! Gracias por usar GestiOne.\n")
                break
            case _:
                error_message("Opción inválida. Intente de nuevo.")

# Ejecutar el programa
main()