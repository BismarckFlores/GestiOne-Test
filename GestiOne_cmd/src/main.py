"""
main.py

Módulo principal que maneja los menús de la aplicación y la interacción con el usuario.
"""

from utils import clear_console, print_banner, error_message
from utils import pause
from config import init_files, set_min_stock_level, reset_data, reset_min_stock_level
from inventory import show_inventory, add_product, edit_product, remove_product, restock_product, check_low_stock
from sales import register_ticket, show_sales, sales_report_by_period, top_selling_products, filter_sales_by_product, filter_sales_by_date_range


def inventory_menu():
    """Muestra el menú de gestión de inventario y gestiona la navegación del usuario."""
    while True:
        clear_console(True)
        print_banner("GESTIÓN DE INVENTARIO")
        print("1. 📦 Mostrar inventario")
        print("2. ➕ Agregar producto")
        print("3. ✏️  Editar producto")
        print("4. 🗑️  Eliminar producto")
        print("5. 🔄 Restock de producto")
        print("6. ⚠️ Ver productos con stock bajo")
        print("7. 🔙 Volver al menú principal")

        option = input("\nSeleccione una opción: ").strip()
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
                check_low_stock()
            case "7":
                break
            case _:
                error_message("Opción inválida. Intente de nuevo.")
                pause()


def sales_menu():
    """Muestra el menú de gestión de ventas y gestiona la navegación del usuario."""
    while True:
        clear_console(True)
        print_banner("GESTIÓN DE VENTAS")
        print("1. 🧾 Registrar Ticket de Venta")
        print("2. 📅 Ver historial de ventas")
        print("3. 📊 Reporte de ventas (Diario, Semanal, Mensual)")
        print("4. 🔝 Productos más vendidos")
        print("5. 📎 Reportes avanzados")
        print("6. 🔙 Volver al menú principal")

        option = input("\nSeleccione una opción: ").strip()
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
                advanced_sales_report()
            case "6":
                break
            case _:
                error_message("Opción inválida. Intente de nuevo.")
                pause()

def advanced_sales_report():
    """Muestra el menú de reportes avanzados permitiendo filtros por producto o fechas."""
    while True:
        clear_console(True)
        print_banner("REPORTES AVANZADOS")
        print("1. Filtrar por ID de Producto")
        print("2. Filtrar por Rango de Fechas")
        print("3. Volver")

        option = input("\nSeleccione una opción: ").strip()
        if option == "1":
            filter_sales_by_product()
        elif option == "2":
            filter_sales_by_date_range()
        elif option == "3":
            return
        else:
            error_message("Opción inválida. Intente de nuevo.")
        pause()

def config_menu():
    """Muestra el menú de configuración general y permite modificar opciones."""
    while True:
        clear_console(True)
        print_banner("CONFIGURACIÓN")
        print("1. ⚙️ Configurar nivel mínimo de stock")
        print("2. 🔁 Restablecer nivel mínimo a 10")
        print("3. 🗑️ Borrar todos los datos")
        print("4. 🔙 Volver al menú principal")

        option = input("\nSeleccione una opción: ").strip()
        match option:
            case "1":
                set_min_stock_level()
            case "2":
                reset_min_stock_level()
            case "3":
                reset_data()
            case "4":
                break
            case _:
                error_message("Opción inválida. Intente de nuevo.")
                pause()


def main():
    """Función principal que inicia la aplicación y muestra el menú principal."""
    init_files()
    while True:
        clear_console(True)
        print_banner("MENÚ PRINCIPAL")
        print("1. 📦 Gestión de Inventario")
        print("2. 🧾 Gestión de Ventas")
        print("3. ⚙️ Configuración")
        print("4. 🚪 Salir")

        option = input("\nSeleccione una opción: ").strip()
        match option:
            case "1":
                inventory_menu()
            case "2":
                sales_menu()
            case "3":
                config_menu()
            case "4":
                print("\n🎉 ¡Hasta luego! Gracias por usar GestiOne.\n")
                break
            case _:
                error_message("Opción inválida. Intente de nuevo.")
                pause()


if __name__ == "__main__":
    main()