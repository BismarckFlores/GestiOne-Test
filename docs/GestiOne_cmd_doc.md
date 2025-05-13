# Documentación Técnica - GestiOne_cmd

## Módulos

### config.py
Módulo encargado de la configuración inicial del sistema y archivos base.

#### Funciones
- **init_files()**: Inicializa los archivos de productos, ventas y configuración si no existen.
- **get_min_stock_level()**: Obtiene el nivel mínimo de stock configurado desde el archivo de configuración.
- **set_min_stock_level()**: Permite establecer un nuevo nivel mínimo de stock ingresado por el usuario.
- **reset_min_stock_level()**: Restablece el nivel mínimo de stock al valor predeterminado (10).
- **reset_data()**: Elimina todos los datos de inventario, ventas y restablece configuración.


### inventory.py
Módulo encargado de la gestión de inventario de productos.

#### Funciones
- **show_inventory()**: Muestra el inventario actual en consola de manera tabulada.
- **save_inventory(products)**: Guarda el inventario en el archivo CSV ordenado por ID.
- **add_product()**: Agrega un nuevo producto al inventario validando ID único, nombre, precio y cantidad.
- **edit_product()**: Edita los datos de un producto existente en el inventario.
- **remove_product()**: Elimina un producto del inventario según el ID proporcionado.
- **restock_product()**: Agrega stock adicional a un producto existente en el inventario.
- **check_low_stock(products=None, headers=None)**: Muestra productos con stock por debajo del nivel mínimo configurado.


### main.py
Módulo principal que maneja los menús de la aplicación y la interacción con el usuario.

#### Funciones
- **inventory_menu()**: Muestra el menú de gestión de inventario y gestiona la navegación del usuario.
- **sales_menu()**: Muestra el menú de gestión de ventas y gestiona la navegación del usuario.
- **advanced_sales_report()**: Muestra el menú de reportes avanzados permitiendo filtros por producto o fechas.
- **config_menu()**: Muestra el menú de configuración general y permite modificar opciones.
- **main()**: Función principal que inicia la aplicación y muestra el menú principal.


### sales.py
Módulo encargado de la gestión de ventas, historial, reportes y estadísticas.

#### Funciones
- **register_ticket()**: Registra una nueva venta, actualiza inventario y guarda la información en el archivo de ventas.
- **show_sales()**: Muestra el historial completo de ventas agrupado por tickets.
- **sales_report_by_period()**: Genera un reporte de ventas filtrado por periodo: diario, semanal o mensual.
- **top_selling_products()**: Muestra el top 5 de productos más vendidos.
- **filter_sales_by_product()**: Filtra las ventas realizadas de un producto específico por su ID.
- **filter_sales_by_date_range()**: Filtra las ventas dentro de un rango de fechas especificado.


### utils.py
Módulo utilitario con funciones generales como manejo de consola, mensajes y archivos CSV.

#### Funciones
- **clear_console(force=False)**: Limpia la consola según el sistema operativo.
- **pause()**: Realiza una pausa esperando a que el usuario presione Enter.
- **print_banner(title)**: Imprime un título decorativo con estilo.
- **success_message(message)**: Muestra un mensaje de éxito en color verde.
- **error_message(message)**: Muestra un mensaje de error en color rojo.
- **read_csv(file_path)**: Lee un archivo CSV completo y devuelve encabezados y datos.
- **write_csv(file_path, headers, data)**: Sobrescribe un archivo CSV con encabezados y datos.
- **append_csv(file_path, rows)**: Agrega nuevas filas al final de un archivo CSV existente.
