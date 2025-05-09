from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super secret key"  # Required for flash messages (user feedback)

PRODUCTS_FILE = "GestiOne_web/data/products.csv"
SALES_FILE = "GestiOne_web/data/sales.csv"
SETTINGS_FILE = "GestiOne_web/data/settings.txt"

# --- Helper Functions (adapted from your script) ---
def init_files():
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Price", "Quantity"])

    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Sale ID", "Product ID", "Product Name", "Sales Quantity", "Total", "Date"])

    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, mode="w") as f:
            f.write("MIN_STOCK_LEVEL=10\n")

def get_min_stock_level():
    try:
        with open(SETTINGS_FILE, mode="r") as f:
            for line in f:
                if line.startswith("MIN_STOCK_LEVEL="):
                    return int(line.split("=")[1].strip())
    except FileNotFoundError:
        return 10

def save_inventory(products):
    with open(PRODUCTS_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Price", "Quantity"])
        writer.writerows(products.values())  # Save values, not the dict itself

def load_products():
    init_files()  # Ensure file exists
    products = {}
    try:
        with open(PRODUCTS_FILE, mode="r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                products[row[0]] = row
    except FileNotFoundError:
        pass  # Handle the case where the file doesn't exist yet
    return products

def load_sales():
    init_files()  # Ensure file exists
    sales = []
    try:
        with open(SALES_FILE, mode="r") as f:
            reader = csv.reader(f)
            next(reader)
            sales = list(reader)
    except FileNotFoundError:
        pass
    return sales

# --- Routes (Web Page Endpoints) ---
@app.route("/")
def index():
    products = load_products()
    sales = load_sales()
    min_stock_level = get_min_stock_level()
    return render_template("index.html", products=products.values(), sales=sales, min_stock_level=min_stock_level)

@app.route("/add_product", methods=["POST"])
def add_product():
    products = load_products()
    id_product = request.form["id_product"]
    name = request.form["name"]
    price = request.form["price"]
    quantity = request.form["quantity"]

    if id_product in products:
        flash("Product ID already exists.", "error")
    else:
        products[id_product] = [id_product, name, price, quantity]
        save_inventory(products)
        flash("Product added successfully!", "success")
    return redirect(url_for("index"))

@app.route("/edit_product/<id_product>", methods=["POST"])
def edit_product(id_product):
    products = load_products()
    if id_product not in products:
        flash("Product not found.", "error")
    else:
        if request.form["name"]:
            products[id_product][1] = request.form["name"]
        if request.form["price"]:
            products[id_product][2] = request.form["price"]
        save_inventory(products)
        flash("Product updated successfully!", "success")
    return redirect(url_for("index"))

@app.route("/delete_product/<id_product>")
def delete_product(id_product):
    products = load_products()
    if id_product not in products:
        flash("Product not found.", "error")
    else:
        del products[id_product]
        save_inventory(products)
        flash("Product deleted successfully!", "success")
    return redirect(url_for("index"))

@app.route("/restock_product/<id_product>", methods=["POST"])
def restock_product(id_product):
    products = load_products()
    if id_product not in products:
        flash("Product not found.", "error")
    else:
        try:
            restock_quantity = int(request.form["restock_quantity"])
            if restock_quantity <= 0:
                flash("Quantity must be greater than 0.", "error")
            else:
                products[id_product][3] = str(int(products[id_product][3]) + restock_quantity)
                save_inventory(products)
                flash("Product restocked successfully!", "success")
        except ValueError:
            flash("Invalid quantity.", "error")
    return redirect(url_for("index"))

@app.route("/register_sale", methods=["POST"])
def register_sale():
    products = load_products()
    sales = load_sales()
    sale_items = []
    total_amount = 0

    for product_id, quantity in request.form.items():
        if product_id != "submit":  # Avoid the submit button
            if product_id in products:
                try:
                    quantity = int(quantity)
                    if quantity > 0 and quantity <= int(products[product_id][3]):
                        sale_items.append({"product_id": product_id, "quantity": quantity})
                        products[product_id][3] = str(int(products[product_id][3]) - quantity)
                        total_amount += float(products[product_id][2]) * quantity
                    else:
                        flash(f"Invalid quantity for {products[product_id][1]}.", "error")
                        return redirect(url_for("index"))
                except ValueError:
                    flash(f"Invalid quantity for {products[product_id][1]}.", "error")
                    return redirect(url_for("index"))
            else:
                flash(f"Product with ID {product_id} not found.", "error")
                return redirect(url_for("index"))

    if sale_items:
        save_inventory(products)
        sale_id = len(sales) + 1 if sales else 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(SALES_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            for item in sale_items:
                writer.writerow([sale_id, item["product_id"], products[item["product_id"]][1], item["quantity"], float(products[item["product_id"]][2]) * item["quantity"], now])
        flash("Sale registered successfully!", "success")
    else:
        flash("No items to register.", "warning")
    return redirect(url_for("index"))

@app.route("/reset_data")
def reset_data():
    confirmation = request.args.get("confirm")
    if confirmation == "true":
        with open(PRODUCTS_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Price", "Quantity"])
        with open(SALES_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Sale ID", "Product ID", "Product Name", "Sales Quantity", "Total", "Date"])
        with open(SETTINGS_FILE, mode="w") as f:
            f.write("MIN_STOCK_LEVEL=10\n")
        flash("Data reset successfully!", "success")
    else:
        flash("Reset cancelled.", "info")
    return redirect(url_for("index"))

@app.route("/set_min_stock_level", methods=["POST"])
def set_min_stock_level():
    try:
        new_level = int(request.form["min_stock_level"])
        if new_level <= 0:
            flash("Minimum stock level must be greater than 0.", "error")
        else:
            with open(SETTINGS_FILE, mode="w") as f:
                f.write(f"MIN_STOCK_LEVEL={new_level}\n")
            flash("Minimum stock level updated!", "success")
    except ValueError:
        flash("Invalid input for minimum stock level.", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for development