import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

class GestioneDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("GestiOne Desktop")
        self.root.geometry("1100x700")
        self.min_stock_level = 10
        
        # Configuración de archivos
        self.data_dir = "GestiOne_app/data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.products_file = os.path.join(self.data_dir, "products.csv")
        self.sales_file = os.path.join(self.data_dir, "sales.csv")
        self.settings_file = os.path.join(self.data_dir, "settings.txt")
        self.init_files()
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=('Helvetica', 10))
        self.style.configure("Accent.TButton", background="#4CAF50", foreground="white")
        self.style.configure("Warning.TButton", background="#FF9800", foreground="white")
        self.style.configure("Danger.TButton", background="#F44336", foreground="white")
        
        # Contenedor principal
        self.container = ttk.Frame(root)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        self.title = ttk.Label(
            self.container, 
            text="GestiOne Desktop", 
            font=('Helvetica', 20, 'bold'), 
            foreground="#555"
        )
        self.title.pack(pady=10)
        
        # Secciones
        self.setup_inventory_section()
        self.setup_sales_section()
        self.setup_settings_section()
        
        # Cargar datos
        self.load_inventory()
        self.load_sales()
        self.load_settings()

    def init_files(self):
        if not os.path.exists(self.products_file):
            with open(self.products_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Price", "Quantity"])
        
        if not os.path.exists(self.sales_file):
            with open(self.sales_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Sale ID", "Product ID", "Product Name", "Quantity", "Total", "Date"])
        
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, "w") as f:
                f.write("MIN_STOCK_LEVEL=10\n")

    def load_settings(self):
        try:
            with open(self.settings_file, "r") as f:
                for line in f:
                    if line.startswith("MIN_STOCK_LEVEL="):
                        self.min_stock_level = int(line.split("=")[1].strip())
        except:
            self.min_stock_level = 10

    def setup_inventory_section(self):
        frame = ttk.LabelFrame(self.container, text="📦 Inventario", padding=10)
        frame.pack(fill="both", expand=True, pady=10)
        
        # Filtros
        filters_frame = ttk.Frame(frame)
        filters_frame.pack(fill="x", pady=5)
        
        ttk.Label(filters_frame, text="ID:").pack(side="left", padx=5)
        self.inventory_id_filter = ttk.Entry(filters_frame, width=15)
        self.inventory_id_filter.pack(side="left", padx=5)
        
        ttk.Label(filters_frame, text="Nombre:").pack(side="left", padx=5)
        self.inventory_name_filter = ttk.Entry(filters_frame, width=15)
        self.inventory_name_filter.pack(side="left", padx=5)
        
        # Tabla
        self.tree_inventory = ttk.Treeview(
            frame, 
            columns=("ID", "Nombre", "Precio", "Cantidad"), 
            show="headings",
            height=10
        )
        self.tree_inventory.heading("ID", text="ID")
        self.tree_inventory.heading("Nombre", text="Nombre")
        self.tree_inventory.heading("Precio", text="Precio")
        self.tree_inventory.heading("Cantidad", text="Cantidad")
        self.tree_inventory.pack(fill="both", expand=True)
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Agregar Producto", 
            style="Accent.TButton",
            command=self.show_add_modal
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Editar", 
            command=self.show_edit_modal
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Restock", 
            style="Warning.TButton",
            command=self.show_restock_modal
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Eliminar", 
            style="Danger.TButton",
            command=self.delete_product
        ).pack(side="left", padx=5)

    def setup_sales_section(self):
        frame = ttk.LabelFrame(self.container, text="🧾 Historial de Ventas", padding=10)
        frame.pack(fill="both", expand=True, pady=10)
        
        self.tree_sales = ttk.Treeview(
            frame, 
            columns=("ID Venta", "ID Producto", "Producto", "Cantidad", "Total", "Fecha"), 
            show="headings",
            height=10
        )
        self.tree_sales.heading("ID Venta", text="ID Venta")
        self.tree_sales.heading("ID Producto", text="ID Producto")
        self.tree_sales.heading("Producto", text="Producto")
        self.tree_sales.heading("Cantidad", text="Cantidad")
        self.tree_sales.heading("Total", text="Total")
        self.tree_sales.heading("Fecha", text="Fecha")
        self.tree_sales.pack(fill="both", expand=True)
        
        ttk.Button(
            frame, 
            text="Registrar Venta", 
            style="Accent.TButton",
            command=self.show_sale_modal
        ).pack(pady=10)

    def setup_settings_section(self):
        frame = ttk.LabelFrame(self.container, text="⚙️ Ajustes", padding=10)
        frame.pack(fill="x", pady=10)
        
        self.toggle_settings_btn = ttk.Button(
            frame, 
            text="Mostrar Ajustes", 
            command=self.toggle_settings
        )
        self.toggle_settings_btn.pack()
        
        self.settings_frame = ttk.Frame(frame)
        
        # Configuración de stock mínimo
        ttk.Label(self.settings_frame, text="Nivel mínimo de stock:").pack()
        self.min_stock_entry = ttk.Entry(self.settings_frame)
        self.min_stock_entry.insert(0, str(self.min_stock_level))
        self.min_stock_entry.pack()
        
        ttk.Button(
            self.settings_frame, 
            text="Guardar", 
            style="Accent.TButton",
            command=self.save_min_stock
        ).pack(pady=5)
        
        # Botón de reset
        ttk.Button(
            self.settings_frame, 
            text="Resetear Datos", 
            style="Danger.TButton",
            command=self.confirm_reset
        ).pack(pady=5)

    def load_inventory(self):
        for item in self.tree_inventory.get_children():
            self.tree_inventory.delete(item)
        
        try:
            with open(self.products_file, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Saltar encabezado
                for row in reader:
                    if len(row) == 4:  # Validar formato
                        self.tree_inventory.insert("", "end", values=row)
                        # Resaltar productos con bajo stock
                        if int(row[3]) <= self.min_stock_level:
                            self.tree_inventory.tag_configure('lowstock', background='#ffcccc')
                            self.tree_inventory.item(self.tree_inventory.get_children()[-1], tags=('lowstock',))
        except FileNotFoundError:
            pass

    def load_sales(self):
        for item in self.tree_sales.get_children():
            self.tree_sales.delete(item)
        
        try:
            with open(self.sales_file, "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) == 6:  # Validar formato
                        self.tree_sales.insert("", "end", values=row)
        except FileNotFoundError:
            pass

    # ======================
    # MODALES Y FUNCIONALIDAD
    # ======================

    def show_add_modal(self):
        modal = tk.Toplevel(self.root)
        modal.title("Agregar Producto")
        modal.geometry("400x300")
        
        ttk.Label(modal, text="ID:").pack()
        id_entry = ttk.Entry(modal)
        id_entry.pack()
        
        ttk.Label(modal, text="Nombre:").pack()
        name_entry = ttk.Entry(modal)
        name_entry.pack()
        
        ttk.Label(modal, text="Precio:").pack()
        price_entry = ttk.Entry(modal)
        price_entry.pack()
        
        ttk.Label(modal, text="Cantidad:").pack()
        quantity_entry = ttk.Entry(modal)
        quantity_entry.pack()
        
        def save_product():
            try:
                product_id = id_entry.get().strip()
                name = name_entry.get().strip()
                price = float(price_entry.get())
                quantity = int(quantity_entry.get())
                
                if not product_id or not name:
                    raise ValueError("Nombre e ID son obligatorios")
                if price <= 0 or quantity < 0:
                    raise ValueError("Precio y cantidad deben ser positivos")
                
                # Verificar si el ID ya existe
                with open(self.products_file, "r") as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        if row[0] == product_id:
                            raise ValueError("ID ya existe")
                
                # Guardar nuevo producto
                with open(self.products_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([product_id, name, price, quantity])
                
                messagebox.showinfo("Éxito", "Producto agregado correctamente")
                modal.destroy()
                self.load_inventory()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        
        ttk.Button(modal, text="Guardar", command=save_product).pack(pady=10)

    def show_edit_modal(self):
        selected = self.tree_inventory.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un producto")
            return
        
        product_data = self.tree_inventory.item(selected[0])["values"]
        
        modal = tk.Toplevel(self.root)
        modal.title("Editar Producto")
        modal.geometry("400x250")
        
        ttk.Label(modal, text=f"Editando: {product_data[1]} (ID: {product_data[0]})").pack(pady=5)
        
        ttk.Label(modal, text="Nuevo nombre:").pack()
        name_entry = ttk.Entry(modal)
        name_entry.insert(0, product_data[1])
        name_entry.pack()
        
        ttk.Label(modal, text="Nuevo precio:").pack()
        price_entry = ttk.Entry(modal)
        price_entry.insert(0, product_data[2])
        price_entry.pack()
        
        def save_changes():
            try:
                new_name = name_entry.get().strip()
                new_price = float(price_entry.get())
                
                if not new_name:
                    raise ValueError("El nombre no puede estar vacío")
                if new_price <= 0:
                    raise ValueError("El precio debe ser positivo")
                
                # Actualizar el producto
                updated_products = []
                with open(self.products_file, "r") as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    for row in reader:
                        if row[0] == product_data[0]:
                            row[1] = new_name
                            row[2] = str(new_price)
                        updated_products.append(row)
                
                # Guardar cambios
                with open(self.products_file, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(updated_products)
                
                messagebox.showinfo("Éxito", "Producto actualizado")
                modal.destroy()
                self.load_inventory()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        
        ttk.Button(modal, text="Guardar Cambios", command=save_changes).pack(pady=10)

    def show_restock_modal(self):
        selected = self.tree_inventory.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un producto")
            return
        
        product_data = self.tree_inventory.item(selected[0])["values"]
        
        modal = tk.Toplevel(self.root)
        modal.title("Restock Producto")
        modal.geometry("400x200")
        
        ttk.Label(modal, text=f"Producto: {product_data[1]}").pack(pady=5)
        ttk.Label(modal, text=f"Stock actual: {product_data[3]}").pack()
        
        ttk.Label(modal, text="Cantidad a añadir:").pack()
        quantity_entry = ttk.Entry(modal)
        quantity_entry.pack()
        
        def process_restock():
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    raise ValueError("La cantidad debe ser positiva")
                
                # Actualizar stock
                updated_products = []
                with open(self.products_file, "r") as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    for row in reader:
                        if row[0] == product_data[0]:
                            row[3] = str(int(row[3]) + quantity)
                        updated_products.append(row)
                
                # Guardar cambios
                with open(self.products_file, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(updated_products)
                
                messagebox.showinfo("Éxito", f"Se añadieron {quantity} unidades")
                modal.destroy()
                self.load_inventory()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Dato inválido: {str(e)}")
        
        ttk.Button(modal, text="Aplicar Restock", command=process_restock).pack(pady=10)

    def show_sale_modal(self):
        modal = tk.Toplevel(self.root)
        modal.title("Registrar Venta")
        modal.geometry("600x400")
        
        # Obtener productos disponibles
        try:
            with open(self.products_file, "r") as f:
                products = list(csv.reader(f))[1:]  # Excluir encabezado
        except:
            products = []
        
        if not products:
            ttk.Label(modal, text="No hay productos disponibles").pack(pady=20)
            return
        
        # Widgets para cada producto
        self.sale_entries = {}
        frame = ttk.Frame(modal)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for product in products:
            product_frame = ttk.Frame(scrollable_frame)
            product_frame.pack(fill="x", pady=2)
            
            ttk.Label(product_frame, text=f"{product[1]} (Stock: {product[3]})").pack(side="left")
            entry = ttk.Entry(product_frame, width=5)
            entry.insert(0, "0")
            entry.pack(side="right", padx=5)
            self.sale_entries[product[0]] = entry
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def register_sale():
            try:
                sale_items = []
                total = 0.0
                
                # Validar cantidades y calcular total
                for product_id, entry in self.sale_entries.items():
                    quantity = int(entry.get())
                    if quantity > 0:
                        product = next(p for p in products if p[0] == product_id)
                        if quantity > int(product[3]):
                            raise ValueError(f"No hay suficiente stock de {product[1]}")
                        sale_items.append({
                            "id": product_id,
                            "name": product[1],
                            "price": float(product[2]),
                            "quantity": quantity
                        })
                        total += float(product[2]) * quantity
                
                if not sale_items:
                    raise ValueError("No se seleccionaron productos")
                
                # Generar ID de venta
                try:
                    with open(self.sales_file, "r") as f:
                        sales = list(csv.reader(f))
                    sale_id = int(sales[-1][0]) + 1 if len(sales) > 1 else 1
                except:
                    sale_id = 1
                
                # Registrar venta
                with open(self.sales_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    for item in sale_items:
                        writer.writerow([
                            sale_id,
                            item["id"],
                            item["name"],
                            item["quantity"],
                            item["price"] * item["quantity"],
                            date
                        ])
                
                # Actualizar inventario
                updated_products = []
                with open(self.products_file, "r") as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    for row in reader:
                        for item in sale_items:
                            if row[0] == item["id"]:
                                row[3] = str(int(row[3]) - item["quantity"])
                        updated_products.append(row)
                
                with open(self.products_file, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(updated_products)
                
                messagebox.showinfo("Éxito", f"Venta registrada\nTotal: ${total:.2f}")
                modal.destroy()
                self.load_inventory()
                self.load_sales()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(modal, text="Registrar Venta", command=register_sale).pack(pady=10)

    def delete_product(self):
        selected = self.tree_inventory.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un producto")
            return
        
        product_data = self.tree_inventory.item(selected[0])["values"]
        
        if not messagebox.askyesno("Confirmar", f"¿Eliminar {product_data[1]} (ID: {product_data[0]})?"):
            return
        
        # Eliminar producto
        remaining_products = []
        with open(self.products_file, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                if row[0] != product_data[0]:
                    remaining_products.append(row)
        
        with open(self.products_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(remaining_products)
        
        messagebox.showinfo("Éxito", "Producto eliminado")
        self.load_inventory()

    def toggle_settings(self):
        if self.settings_frame.winfo_ismapped():
            self.settings_frame.pack_forget()
            self.toggle_settings_btn.config(text="Mostrar Ajustes")
        else:
            self.settings_frame.pack(fill="x", pady=10)
            self.toggle_settings_btn.config(text="Ocultar Ajustes")

    def save_min_stock(self):
        try:
            new_level = int(self.min_stock_entry.get())
            if new_level <= 0:
                raise ValueError("El nivel debe ser positivo")
            
            with open(self.settings_file, "w") as f:
                f.write(f"MIN_STOCK_LEVEL={new_level}\n")
            
            self.min_stock_level = new_level
            messagebox.showinfo("Éxito", "Nivel mínimo actualizado")
            self.load_inventory()  # Para actualizar resaltado de bajo stock
            
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {str(e)}")

    def confirm_reset(self):
        if not messagebox.askyesno(
            "Confirmar", 
            "¿Resetear TODOS los datos?\n\nEsta acción borrará todos los productos y ventas registradas."
        ):
            return
        
        # Resetear productos
        with open(self.products_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Price", "Quantity"])
        
        # Resetear ventas
        with open(self.sales_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Sale ID", "Product ID", "Product Name", "Quantity", "Total", "Date"])
        
        # Resetear configuración
        with open(self.settings_file, "w") as f:
            f.write("MIN_STOCK_LEVEL=10\n")
        
        self.min_stock_level = 10
        self.min_stock_entry.delete(0, tk.END)
        self.min_stock_entry.insert(0, "10")
        
        messagebox.showinfo("Éxito", "Datos reseteados correctamente")
        self.load_inventory()
        self.load_sales()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestioneDesktop(root)
    root.mainloop()