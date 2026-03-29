import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


DB_NAME = "durian_pos.db"


def get_conn():
    return sqlite3.connect(DB_NAME)


def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    for col in columns:
        if col[1] == column_name:
            return True
    return False


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_time TEXT NOT NULL,
            customer_name TEXT,
            payment_method TEXT,
            subtotal REAL NOT NULL DEFAULT 0,
            discount REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL DEFAULT 0,
            cash_received REAL NOT NULL DEFAULT 0,
            balance REAL NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            qty INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id)
        )
    """)

    if not column_exists(cursor, "sales", "customer_name"):
        cursor.execute("ALTER TABLE sales ADD COLUMN customer_name TEXT")

    if not column_exists(cursor, "sales", "payment_method"):
        cursor.execute("ALTER TABLE sales ADD COLUMN payment_method TEXT")

    if not column_exists(cursor, "sales", "subtotal"):
        cursor.execute("ALTER TABLE sales ADD COLUMN subtotal REAL NOT NULL DEFAULT 0")

    if not column_exists(cursor, "sales", "discount"):
        cursor.execute("ALTER TABLE sales ADD COLUMN discount REAL NOT NULL DEFAULT 0")

    if not column_exists(cursor, "sales", "cash_received"):
        cursor.execute("ALTER TABLE sales ADD COLUMN cash_received REAL NOT NULL DEFAULT 0")

    if not column_exists(cursor, "sales", "balance"):
        cursor.execute("ALTER TABLE sales ADD COLUMN balance REAL NOT NULL DEFAULT 0")

    conn.commit()
    conn.close()
    seed_products()


def seed_products():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_products = [
            ("Musang King", 65.0),
            ("D24", 38.0),
            ("XO", 28.0),
            ("Black Thorn", 75.0),
            ("Red Prawn", 45.0),
            ("Udang Merah", 42.0),
        ]
        cursor.executemany(
            "INSERT INTO products (name, price) VALUES (?, ?)",
            sample_products
        )
        conn.commit()

    conn.close()


def get_products_db(search_text=""):
    conn = get_conn()
    cursor = conn.cursor()

    if search_text.strip():
        cursor.execute(
            "SELECT id, name, price FROM products WHERE name LIKE ? ORDER BY name ASC",
            (f"%{search_text.strip()}%",)
        )
    else:
        cursor.execute("SELECT id, name, price FROM products ORDER BY name ASC")

    rows = cursor.fetchall()
    conn.close()
    return rows


def add_product_db(name, price):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()


def update_product_db(product_id, name, price):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE products SET name = ?, price = ? WHERE id = ?",
        (name, price, product_id)
    )
    conn.commit()
    conn.close()


def delete_product_db(product_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


def get_sales_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, sale_time, customer_name, payment_method, total
        FROM sales
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_sale_items_db(sale_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_name, price, qty, subtotal
        FROM sale_items
        WHERE sale_id = ?
        ORDER BY id ASC
    """, (sale_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_sale_main_db(sale_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sale_time, customer_name, payment_method,
               subtotal, discount, total, cash_received, balance
        FROM sales
        WHERE id = ?
    """, (sale_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def save_sale_db(cart, customer_name, payment_method, discount, cash_received):
    conn = get_conn()
    cursor = conn.cursor()

    subtotal = 0.0
    for item in cart.values():
        subtotal += item["price"] * item["qty"]

    total = subtotal - discount
    if total < 0:
        total = 0.0

    balance = cash_received - total
    sale_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO sales (
            sale_time, customer_name, payment_method,
            subtotal, discount, total, cash_received, balance
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sale_time,
        customer_name,
        payment_method,
        subtotal,
        discount,
        total,
        cash_received,
        balance
    ))
    sale_id = cursor.lastrowid

    for item in cart.values():
        item_subtotal = item["price"] * item["qty"]
        cursor.execute("""
            INSERT INTO sale_items (sale_id, product_name, price, qty, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (
            sale_id,
            item["name"],
            item["price"],
            item["qty"],
            item_subtotal
        ))

    conn.commit()
    conn.close()

    return sale_id, sale_time, subtotal, total, balance


def get_today_total_db():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT IFNULL(SUM(total), 0)
        FROM sales
        WHERE sale_time LIKE ?
    """, (f"{today}%",))
    total = cursor.fetchone()[0]
    conn.close()
    return total


class DurianPOSLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(10), spacing=dp(8), **kwargs)

        init_db()
        self.cart = {}

        self.build_ui()
        self.load_products()
        self.refresh_cart()

    def build_ui(self):
        header = Label(
            text="Durian POS",
            font_size="24sp",
            bold=True,
            size_hint=(1, None),
            height=dp(40)
        )
        self.add_widget(header)

        self.today_total_label = Label(
            text=f"Today Sales: RM {get_today_total_db():.2f}",
            font_size="16sp",
            size_hint=(1, None),
            height=dp(28)
        )
        self.add_widget(self.today_total_label)

        search_row = BoxLayout(orientation="horizontal", spacing=dp(6), size_hint=(1, None), height=dp(45))
        self.search_input = TextInput(
            multiline=False,
            hint_text="Search product",
            font_size="16sp"
        )
        search_btn = Button(text="Search", size_hint=(None, 1), width=dp(90))
        search_btn.bind(on_press=self.search_products)

        all_btn = Button(text="All", size_hint=(None, 1), width=dp(70))
        all_btn.bind(on_press=self.show_all_products)

        search_row.add_widget(self.search_input)
        search_row.add_widget(search_btn)
        search_row.add_widget(all_btn)
        self.add_widget(search_row)

        customer_row = BoxLayout(orientation="horizontal", spacing=dp(6), size_hint=(1, None), height=dp(45))
        self.customer_input = TextInput(multiline=False, hint_text="Customer", font_size="16sp")
        self.payment_input = TextInput(multiline=False, hint_text="Payment: Cash / QR / Card", font_size="16sp")
        customer_row.add_widget(self.customer_input)
        customer_row.add_widget(self.payment_input)
        self.add_widget(customer_row)

        payment_row = BoxLayout(orientation="horizontal", spacing=dp(6), size_hint=(1, None), height=dp(45))
        self.discount_input = TextInput(multiline=False, hint_text="Discount", input_filter="float", font_size="16sp")
        self.cash_input = TextInput(multiline=False, hint_text="Cash Received", input_filter="float", font_size="16sp")
        payment_row.add_widget(self.discount_input)
        payment_row.add_widget(self.cash_input)
        self.add_widget(payment_row)

        products_title = Label(
            text="Products",
            font_size="20sp",
            size_hint=(1, None),
            height=dp(30)
        )
        self.add_widget(products_title)

        product_scroll = ScrollView(size_hint=(1, 0.36))
        self.product_grid = GridLayout(cols=2, spacing=dp(8), padding=dp(4), size_hint_y=None)
        self.product_grid.bind(minimum_height=self.product_grid.setter("height"))
        product_scroll.add_widget(self.product_grid)
        self.add_widget(product_scroll)

        cart_title = Label(
            text="Cart",
            font_size="20sp",
            size_hint=(1, None),
            height=dp(30)
        )
        self.add_widget(cart_title)

        cart_scroll = ScrollView(size_hint=(1, 0.22))
        self.cart_layout = GridLayout(cols=1, spacing=dp(6), padding=dp(4), size_hint_y=None)
        self.cart_layout.bind(minimum_height=self.cart_layout.setter("height"))
        cart_scroll.add_widget(self.cart_layout)
        self.add_widget(cart_scroll)

        summary_box = BoxLayout(orientation="vertical", spacing=dp(3), size_hint=(1, None), height=dp(110))

        self.subtotal_label = Label(text="Subtotal: RM 0.00", font_size="16sp", halign="left")
        self.discount_label = Label(text="Discount: RM 0.00", font_size="16sp", halign="left")
        self.total_label = Label(text="Total: RM 0.00", font_size="20sp", bold=True, halign="left")
        self.balance_label = Label(text="Balance: RM 0.00", font_size="16sp", halign="left")

        for lbl in [self.subtotal_label, self.discount_label, self.total_label, self.balance_label]:
            lbl.size_hint = (1, None)
            lbl.height = dp(24)
            summary_box.add_widget(lbl)

        self.add_widget(summary_box)

        button_row_1 = BoxLayout(orientation="horizontal", spacing=dp(6), size_hint=(1, None), height=dp(50))
        calc_btn = Button(text="Calculate", font_size="16sp")
        calc_btn.bind(on_press=self.calculate_payment)

        clear_btn = Button(text="Clear Cart", font_size="16sp")
        clear_btn.bind(on_press=self.clear_cart)

        button_row_1.add_widget(calc_btn)
        button_row_1.add_widget(clear_btn)
        self.add_widget(button_row_1)

        button_row_2 = BoxLayout(orientation="horizontal", spacing=dp(6), size_hint=(1, None), height=dp(55))
        checkout_btn = Button(text="Checkout", font_size="18sp")
        checkout_btn.bind(on_press=self.checkout)

        remove_last_btn = Button(text="Remove Last", font_size="16sp")
        remove_last_btn.bind(on_press=self.remove_last_item)

        button_row_2.add_widget(checkout_btn)
        button_row_2.add_widget(remove_last_btn)
        self.add_widget(button_row_2)

        manage_row = BoxLayout(orientation="horizontal", spacing=dp(6), size_hint=(1, None), height=dp(48))
        manage_btn = Button(text="Manage Products", font_size="15sp")
        manage_btn.bind(on_press=self.open_manage_products)

        history_btn = Button(text="Sales History", font_size="15sp")
        history_btn.bind(on_press=self.open_sales_history)

        manage_row.add_widget(manage_btn)
        manage_row.add_widget(history_btn)
        self.add_widget(manage_row)

        self.status_label = Label(
            text="Ready",
            font_size="15sp",
            size_hint=(1, None),
            height=dp(26)
        )
        self.add_widget(self.status_label)

    def load_products(self, search_text=""):
        self.product_grid.clear_widgets()
        products = get_products_db(search_text)

        if not products:
            self.product_grid.add_widget(Label(
                text="No products found",
                font_size="16sp",
                size_hint_y=None,
                height=dp(50)
            ))
            return

        for product_id, name, price in products:
            btn = Button(
                text=f"{name}\nRM {price:.2f}",
                font_size="18sp",
                size_hint_y=None,
                height=dp(90)
            )
            btn.bind(on_press=lambda instance, pid=product_id, pname=name, pprice=price: self.add_to_cart(pid, pname, pprice))
            self.product_grid.add_widget(btn)

    def search_products(self, instance):
        text = self.search_input.text.strip()
        self.load_products(text)
        self.status_label.text = f"Search: {text}" if text else "Search cleared"

    def show_all_products(self, instance):
        self.search_input.text = ""
        self.load_products()
        self.status_label.text = "Showing all products"

    def add_to_cart(self, product_id, name, price):
        if product_id in self.cart:
            self.cart[product_id]["qty"] += 1
        else:
            self.cart[product_id] = {
                "name": name,
                "price": price,
                "qty": 1
            }

        self.status_label.text = f"Added: {name}"
        self.refresh_cart()

    def refresh_cart(self):
        self.cart_layout.clear_widgets()

        if not self.cart:
            self.cart_layout.add_widget(Label(
                text="Cart is empty",
                font_size="16sp",
                size_hint_y=None,
                height=dp(40)
            ))
        else:
            for product_id, item in self.cart.items():
                subtotal = item["price"] * item["qty"]

                card = BoxLayout(
                    orientation="vertical",
                    spacing=dp(4),
                    size_hint_y=None,
                    height=dp(90),
                    padding=dp(4)
                )

                item_label = Label(
                    text=f'{item["name"]} x{item["qty"]} = RM {subtotal:.2f}',
                    font_size="16sp",
                    size_hint=(1, None),
                    height=dp(28)
                )
                card.add_widget(item_label)

                btn_row = BoxLayout(orientation="horizontal", spacing=dp(4), size_hint=(1, None), height=dp(42))

                minus_btn = Button(text="-", font_size="18sp")
                minus_btn.bind(on_press=lambda instance, pid=product_id: self.decrease_qty(pid))

                plus_btn = Button(text="+", font_size="18sp")
                plus_btn.bind(on_press=lambda instance, pid=product_id: self.increase_qty(pid))

                remove_btn = Button(text="Remove", font_size="15sp")
                remove_btn.bind(on_press=lambda instance, pid=product_id: self.remove_item(pid))

                btn_row.add_widget(minus_btn)
                btn_row.add_widget(plus_btn)
                btn_row.add_widget(remove_btn)

                card.add_widget(btn_row)
                self.cart_layout.add_widget(card)

        self.update_summary_labels()

    def update_summary_labels(self):
        subtotal = self.get_cart_subtotal()
        discount = self.get_discount_value()
        total = subtotal - discount
        if total < 0:
            total = 0.0

        cash = self.get_cash_value()
        balance = cash - total

        self.subtotal_label.text = f"Subtotal: RM {subtotal:.2f}"
        self.discount_label.text = f"Discount: RM {discount:.2f}"
        self.total_label.text = f"Total: RM {total:.2f}"
        self.balance_label.text = f"Balance: RM {balance:.2f}"

    def get_cart_subtotal(self):
        subtotal = 0.0
        for item in self.cart.values():
            subtotal += item["price"] * item["qty"]
        return subtotal

    def get_discount_value(self):
        text = self.discount_input.text.strip()
        if text == "":
            return 0.0
        try:
            return float(text)
        except ValueError:
            return 0.0

    def get_cash_value(self):
        text = self.cash_input.text.strip()
        if text == "":
            return 0.0
        try:
            return float(text)
        except ValueError:
            return 0.0

    def increase_qty(self, product_id):
        if product_id in self.cart:
            self.cart[product_id]["qty"] += 1
            self.refresh_cart()

    def decrease_qty(self, product_id):
        if product_id in self.cart:
            self.cart[product_id]["qty"] -= 1
            if self.cart[product_id]["qty"] <= 0:
                del self.cart[product_id]
            self.refresh_cart()

    def remove_item(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.refresh_cart()

    def remove_last_item(self, instance):
        if not self.cart:
            self.status_label.text = "Cart is empty"
            return

        last_key = list(self.cart.keys())[-1]
        del self.cart[last_key]
        self.refresh_cart()
        self.status_label.text = "Last item removed"

    def clear_cart(self, instance):
        self.cart = {}
        self.customer_input.text = ""
        self.payment_input.text = ""
        self.discount_input.text = ""
        self.cash_input.text = ""
        self.status_label.text = "Cart cleared"
        self.refresh_cart()

    def calculate_payment(self, instance):
        self.update_summary_labels()
        self.status_label.text = "Payment calculated"

    def checkout(self, instance):
        if not self.cart:
            self.show_message("Checkout", "Cart is empty.")
            return

        customer_name = self.customer_input.text.strip() or "Walk-in Customer"
        payment_method = self.payment_input.text.strip() or "Cash"

        discount = self.get_discount_value()
        subtotal = self.get_cart_subtotal()
        total = subtotal - discount
        if total < 0:
            total = 0.0

        cash_received = self.get_cash_value()

        if payment_method.lower() == "cash" and cash_received < total:
            self.show_message("Error", "Cash received is not enough.")
            return

        if payment_method.lower() != "cash" and cash_received == 0:
            cash_received = total

        sale_id, sale_time, subtotal, total, balance = save_sale_db(
            self.cart,
            customer_name,
            payment_method,
            discount,
            cash_received
        )

        lines = []
        lines.append("DURIAN POS RECEIPT")
        lines.append("--------------------")
        lines.append(f"Receipt No: {sale_id}")
        lines.append(f"Time: {sale_time}")
        lines.append(f"Customer: {customer_name}")
        lines.append(f"Payment: {payment_method}")
        lines.append("")
        for item in self.cart.values():
            item_subtotal = item["price"] * item["qty"]
            lines.append(f'{item["name"]} x{item["qty"]} = RM {item_subtotal:.2f}')
        lines.append("")
        lines.append(f"Subtotal: RM {subtotal:.2f}")
        lines.append(f"Discount: RM {discount:.2f}")
        lines.append(f"Total: RM {total:.2f}")
        lines.append(f"Cash: RM {cash_received:.2f}")
        lines.append(f"Balance: RM {balance:.2f}")
        lines.append("--------------------")
        lines.append("Thank you")

        self.show_message("Payment Success", "\n".join(lines))

        self.cart = {}
        self.customer_input.text = ""
        self.payment_input.text = ""
        self.discount_input.text = ""
        self.cash_input.text = ""
        self.refresh_cart()
        self.today_total_label.text = f"Today Sales: RM {get_today_total_db():.2f}"
        self.status_label.text = f"Checkout completed. Receipt No: {sale_id}"

    def show_message(self, title, message):
        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        scroll = ScrollView()
        msg = Label(
            text=message,
            font_size="16sp",
            size_hint_y=None,
            text_size=(dp(260), None),
            halign="left",
            valign="top"
        )
        msg.bind(texture_size=lambda instance, value: setattr(instance, "height", value[1] + dp(20)))
        scroll.add_widget(msg)
        layout.add_widget(scroll)

        close_btn = Button(text="Close", size_hint=(1, None), height=dp(50))
        layout.add_widget(close_btn)

        popup = Popup(title=title, content=layout, size_hint=(0.9, 0.8))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def open_manage_products(self, instance):
        products = get_products_db()

        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))

        self.manage_name_input = TextInput(multiline=False, hint_text="New Product Name", size_hint=(1, None), height=dp(45))
        self.manage_price_input = TextInput(multiline=False, hint_text="New Price", input_filter="float", size_hint=(1, None), height=dp(45))

        layout.add_widget(self.manage_name_input)
        layout.add_widget(self.manage_price_input)

        add_btn = Button(text="Add New Product", size_hint=(1, None), height=dp(48))
        layout.add_widget(add_btn)

        scroll = ScrollView()
        product_list = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        product_list.bind(minimum_height=product_list.setter("height"))

        for product_id, name, price in products:
            card = BoxLayout(orientation="vertical", spacing=dp(4), size_hint_y=None, height=dp(100))

            info = Label(
                text=f"ID {product_id} | {name} | RM {price:.2f}",
                font_size="15sp",
                size_hint=(1, None),
                height=dp(30)
            )
            card.add_widget(info)

            row = BoxLayout(orientation="horizontal", spacing=dp(6), size_hint=(1, None), height=dp(45))
            edit_btn = Button(text="Edit")
            edit_btn.bind(on_press=lambda btn, pid=product_id, n=name, p=price: self.open_edit_product(pid, n, p))

            delete_btn = Button(text="Delete")
            delete_btn.bind(on_press=lambda btn, pid=product_id: self.confirm_delete_product(pid))

            row.add_widget(edit_btn)
            row.add_widget(delete_btn)
            card.add_widget(row)

            product_list.add_widget(card)

        scroll.add_widget(product_list)
        layout.add_widget(scroll)

        close_btn = Button(text="Close", size_hint=(1, None), height=dp(50))
        layout.add_widget(close_btn)

        popup = Popup(title="Manage Products", content=layout, size_hint=(0.95, 0.92))

        def do_add(instance):
            name = self.manage_name_input.text.strip()
            price_text = self.manage_price_input.text.strip()

            if not name or not price_text:
                self.show_message("Error", "Please enter product name and price.")
                return

            try:
                price = float(price_text)
            except ValueError:
                self.show_message("Error", "Invalid price.")
                return

            add_product_db(name, price)
            self.status_label.text = f"Added new product: {name}"
            self.manage_name_input.text = ""
            self.manage_price_input.text = ""
            self.load_products()
            popup.dismiss()
            self.open_manage_products(None)

        add_btn.bind(on_press=do_add)
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def open_edit_product(self, product_id, old_name, old_price):
        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        name_input = TextInput(text=old_name, multiline=False, size_hint=(1, None), height=dp(45))
        price_input = TextInput(text=str(old_price), multiline=False, input_filter="float", size_hint=(1, None), height=dp(45))

        layout.add_widget(Label(text=f"Edit Product ID {product_id}", font_size="18sp", size_hint=(1, None), height=dp(30)))
        layout.add_widget(name_input)
        layout.add_widget(price_input)

        row = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint=(1, None), height=dp(50))
        save_btn = Button(text="Save")
        cancel_btn = Button(text="Cancel")
        row.add_widget(save_btn)
        row.add_widget(cancel_btn)
        layout.add_widget(row)

        popup = Popup(title="Edit Product", content=layout, size_hint=(0.85, 0.45))

        def do_save(instance):
            new_name = name_input.text.strip()
            new_price_text = price_input.text.strip()

            if not new_name or not new_price_text:
                self.show_message("Error", "Please enter product name and price.")
                return

            try:
                new_price = float(new_price_text)
            except ValueError:
                self.show_message("Error", "Invalid price.")
                return

            update_product_db(product_id, new_name, new_price)
            self.status_label.text = f"Updated product ID {product_id}"
            self.load_products()
            popup.dismiss()

        save_btn.bind(on_press=do_save)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    def confirm_delete_product(self, product_id):
        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        layout.add_widget(Label(text=f"Delete product ID {product_id}?", font_size="18sp"))

        row = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint=(1, None), height=dp(50))
        yes_btn = Button(text="Yes")
        no_btn = Button(text="No")
        row.add_widget(yes_btn)
        row.add_widget(no_btn)
        layout.add_widget(row)

        popup = Popup(title="Confirm Delete", content=layout, size_hint=(0.75, 0.32))

        def do_delete(instance):
            delete_product_db(product_id)
            self.status_label.text = f"Deleted product ID {product_id}"
            self.load_products()
            popup.dismiss()

        yes_btn.bind(on_press=do_delete)
        no_btn.bind(on_press=popup.dismiss)
        popup.open()

    def open_sales_history(self, instance):
        sales = get_sales_db()

        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))

        if not sales:
            layout.add_widget(Label(text="No sales record found.", font_size="18sp"))
        else:
            scroll = ScrollView()
            sales_layout = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
            sales_layout.bind(minimum_height=sales_layout.setter("height"))

            for sale_id, sale_time, customer_name, payment_method, total in sales:
                card = BoxLayout(orientation="vertical", spacing=dp(5), size_hint_y=None, height=dp(95))

                name_text = customer_name if customer_name else "Walk-in Customer"
                pay_text = payment_method if payment_method else "Cash"

                sale_label = Label(
                    text=f"Receipt {sale_id}\n{sale_time}\n{name_text} | {pay_text} | RM {total:.2f}",
                    font_size="14sp",
                    size_hint=(1, None),
                    height=dp(50)
                )
                card.add_widget(sale_label)

                view_btn = Button(text="View", size_hint=(1, None), height=dp(40))
                view_btn.bind(on_press=lambda btn, sid=sale_id: self.open_sale_detail(sid))
                card.add_widget(view_btn)

                sales_layout.add_widget(card)

            scroll.add_widget(sales_layout)
            layout.add_widget(scroll)

        close_btn = Button(text="Close", size_hint=(1, None), height=dp(50))
        layout.add_widget(close_btn)

        popup = Popup(title="Sales History", content=layout, size_hint=(0.95, 0.9))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def open_sale_detail(self, sale_id):
        sale = get_sale_main_db(sale_id)
        items = get_sale_items_db(sale_id)

        if not sale:
            self.show_message("Error", "Sale not found.")
            return

        sale_time, customer_name, payment_method, subtotal, discount, total, cash_received, balance = sale

        customer_name = customer_name or "Walk-in Customer"
        payment_method = payment_method or "Cash"

        lines = []
        lines.append("DURIAN POS RECEIPT")
        lines.append("--------------------")
        lines.append(f"Receipt No: {sale_id}")
        lines.append(f"Time: {sale_time}")
        lines.append(f"Customer: {customer_name}")
        lines.append(f"Payment: {payment_method}")
        lines.append("")
        for product_name, price, qty, item_subtotal in items:
            lines.append(f"{product_name} x{qty} = RM {item_subtotal:.2f}")
        lines.append("")
        lines.append(f"Subtotal: RM {subtotal:.2f}")
        lines.append(f"Discount: RM {discount:.2f}")
        lines.append(f"Total: RM {total:.2f}")
        lines.append(f"Cash: RM {cash_received:.2f}")
        lines.append(f"Balance: RM {balance:.2f}")
        lines.append("--------------------")
        lines.append("Thank you")

        self.show_message("Sale Detail", "\n".join(lines))


class DurianPOSApp(App):
    def build(self):
        return DurianPOSLayout()


if __name__ == "__main__":
    DurianPOSApp().run()
