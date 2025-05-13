"""
sales.py

Módulo encargado de la gestión de ventas, historial, reportes y estadísticas.
"""

import csv
from datetime import datetime, timedelta
from tabulate import tabulate
from config import PRODUCTS_FILE, SALES_FILE
from utils import clear_console, pause, success_message, error_message, read_csv, write_csv, append_csv
from inventory import save_inventory


def register_ticket():
    """Registra una nueva venta, actualiza inventario y guarda la información en el archivo de ventas."""
    headers, rows = read_csv(PRODUCTS_FILE)
    products = {row[0]: row for row in rows}

    ticket = {}
    total_ticket = 0
    headers = ["ID", "Name", "Price", "Quantity"]

    while True:
        clear_console()
        print("\n🧾 NUEVO TICKET DE VENTA")
        print(tabulate(products.values(), headers=headers, tablefmt="fancy_grid"))

        product_id = input("ID del producto para añadir (o 'f' para finalizar): ").strip()
        if product_id.lower() == 'f':
            break

        if product_id in products:
            name = products[product_id][1]
            price = float(products[product_id][2])
            stock = int(products[product_id][3])

            try:
                quantity = int(input(f"Cantidad de {name} (disponible: {stock}): ").strip())
                if quantity > stock:
                    error_message("No hay suficiente stock. Intente de nuevo.")
                    continue
                if quantity <= 0:
                    error_message("Cantidad inválida. Debe ser mayor a 0.")
                    continue
            except ValueError:
                error_message("Entrada inválida. Debe ser un número.")
                continue

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
            success_message(f"{name} x{quantity} añadido al ticket.")
        else:
            error_message("Producto no encontrado. Intente de nuevo.")

    if not ticket:
        error_message("El ticket está vacío. No se registró ninguna venta.")
        return

    save_inventory(products)

    try:
        headers, sales = read_csv(SALES_FILE)
        sale_id = int(sales[-1][0]) + 1 if sales else 1
    except FileNotFoundError:
        sale_id = 1

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    append_csv(SALES_FILE, [[sale_id, pid, details["name"], details["quantity"], details["subtotal"], date] for pid, details in ticket.items()])

    success_message(f"Ticket registrado correctamente. Total: ${total_ticket:.2f}")
    pause()


def show_sales():
    """Muestra el historial completo de ventas agrupado por tickets."""
    clear_console()
    headers, sales = read_csv(SALES_FILE)

    if not sales:
        error_message("No hay ventas registradas.")
        pause()
        return

    grouped = {}
    for sale in sales:
        sale_id, pid, name, qty, subtotal, date = sale
        if sale_id not in grouped:
            grouped[sale_id] = {"date": date, "products": [], "total": 0}
        grouped[sale_id]["products"].append([pid, name, qty, subtotal])
        grouped[sale_id]["total"] += float(subtotal)

    ticket_ids = sorted(grouped.keys(), key=int)
    per_page = 5
    page = 0

    while True:
        clear_console()
        print("\n🧾 HISTORIAL DE VENTAS")
        start = page * per_page
        end = start + per_page
        for sid in ticket_ids[start:end]:
            print(f"\n🧾 Ticket #{sid} - Fecha: {grouped[sid]['date']}")
            print(tabulate(grouped[sid]["products"], headers=["ID Producto", "Nombre", "Cantidad", "Subtotal"], tablefmt="fancy_grid"))
            print(f"💵 Total: ${grouped[sid]['total']:.2f}")
            print("-" * 50)

        if end >= len(ticket_ids):
            break
        input("Presiona Enter para ver más ventas...")
        page += 1

    pause()


def sales_report_by_period():
    """Genera un reporte de ventas filtrado por periodo: diario, semanal o mensual."""
    period_options = {"diario": "daily", "semanal": "weekly", "mensual": "monthly"}
    period = input("Seleccione el periodo (diario, semanal, mensual): ").strip().lower()

    if period not in period_options:
        error_message("Opción inválida. Elija entre 'diario', 'semanal' o 'mensual'.")
        pause()
        return

    period_eng = period_options[period]
    headers, sales = read_csv(SALES_FILE)

    if not sales:
        error_message("No hay ventas registradas.")
        return

    now = datetime.now()
    filtered_sales = []
    for sale in sales:
        sale_date = datetime.strptime(sale[-1], "%Y-%m-%d %H:%M:%S")
        if (period_eng == "daily" and sale_date.date() == now.date()) or \
            (period_eng == "weekly" and sale_date >= now - timedelta(days=7)) or \
            (period_eng == "monthly" and sale_date.month == now.month and sale_date.year == now.year):
            filtered_sales.append(sale)

    if not filtered_sales:
        print(f"\n🧾 No hay ventas registradas para el periodo seleccionado ({period}).\n")
        pause()
        return

    grouped = {}
    for sale in filtered_sales:
        sale_id, pid, name, qty, subtotal, date = sale
        if sale_id not in grouped:
            grouped[sale_id] = {"date": date, "products": [], "total": 0}
        grouped[sale_id]["products"].append([pid, name, qty, subtotal])
        grouped[sale_id]["total"] += float(subtotal)

    print(f"\n🧾 Reporte de Ventas ({period.capitalize()})")
    for sid in sorted(grouped.keys(), key=int):
        print(f"\n🧾 Ticket #{sid} - Fecha: {grouped[sid]['date']}")
        print(tabulate(grouped[sid]["products"], headers=["ID Producto", "Nombre", "Cantidad", "Subtotal"], tablefmt="fancy_grid"))
        print(f"💵 Total: ${grouped[sid]['total']:.2f}")
        print("-" * 50)

    pause()


def top_selling_products():
    """Muestra el top 5 de productos más vendidos."""
    headers, sales = read_csv(SALES_FILE)

    if not sales:
        error_message("No hay ventas registradas.")
        pause()
        return

    product_sales = {}
    for sale in sales:
        product_id, name, quantity = sale[1], sale[2], int(sale[3])
        if product_id not in product_sales:
            product_sales[product_id] = {"name": name, "quantity": 0}
        product_sales[product_id]["quantity"] += quantity

    ranked = sorted(product_sales.values(), key=lambda p: p["quantity"], reverse=True)[:5]
    print("\n🔝 Top 5 Productos Más Vendidos")
    print(tabulate(
        [[i + 1, p["name"], p["quantity"]] for i, p in enumerate(ranked)],
        headers=["Top", "Producto", "Cantidad Vendida"],
        tablefmt="fancy_grid"
    ))
    pause()


def filter_sales_by_product():
    """Filtra las ventas realizadas de un producto específico por su ID."""
    product_id = input("Ingrese el ID del producto a consultar: ").strip()

    headers, data = read_csv(SALES_FILE)
    sales = [sale for sale in data if sale[1] == product_id]

    if not sales:
        error_message("No hay ventas registradas para ese producto.")
        return

    grouped = {}
    for sale in sales:
        sale_id, pid, name, qty, subtotal, date = sale
        if sale_id not in grouped:
            grouped[sale_id] = {"date": date, "products": [], "total": 0}
        grouped[sale_id]["products"].append([pid, name, qty, subtotal])
        grouped[sale_id]["total"] += float(subtotal)

    for sid in sorted(grouped.keys(), key=int):
        print(f"\n🧾 Ticket #{sid} - Fecha: {grouped[sid]['date']}")
        print(tabulate(grouped[sid]["products"], headers=["ID Producto", "Nombre", "Cantidad", "Subtotal"], tablefmt="fancy_grid"))
        print(f"💵 Total: ${grouped[sid]['total']:.2f}")
        print("-" * 50)


def filter_sales_by_date_range():
    """Filtra las ventas dentro de un rango de fechas especificado."""
    try:
        date_start = input("Ingrese la fecha inicial (YYYY-MM-DD): ").strip()
        date_end = input("Ingrese la fecha final (YYYY-MM-DD): ").strip()
        start_dt = datetime.strptime(date_start, "%Y-%m-%d")
        end_dt = datetime.strptime(date_end, "%Y-%m-%d")
    except ValueError:
        error_message("Formato de fecha inválido.")
        return

    headers, sales = read_csv(SALES_FILE)

    filtered = []
    for sale in sales:
        sale_dt = datetime.strptime(sale[-1], "%Y-%m-%d %H:%M:%S")
        if start_dt <= sale_dt <= end_dt:
            filtered.append(sale)

    if not filtered:
        error_message("No hay ventas en ese rango de fechas.")
        return

    grouped = {}
    for sale in filtered:
        sale_id, pid, name, qty, subtotal, date = sale
        if sale_id not in grouped:
            grouped[sale_id] = {"date": date, "products": [], "total": 0}
        grouped[sale_id]["products"].append([pid, name, qty, subtotal])
        grouped[sale_id]["total"] += float(subtotal)

    for sid in sorted(grouped.keys(), key=int):
        print(f"\n🧾 Ticket #{sid} - Fecha: {grouped[sid]['date']}")
        print(tabulate(grouped[sid]["products"], headers=["ID Producto", "Nombre", "Cantidad", "Subtotal"], tablefmt="fancy_grid"))
        print(f"💵 Total: ${grouped[sid]['total']:.2f}")
        print("-" * 50)