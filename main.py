import datetime
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from products import create_product_table, add_product, get_products, create_sales_table, save_sale, delete_product, get_sales

class POSLayout(BoxLayout):

    def update_daily_sales(self):

        sales = get_sales()

        today = str(datetime.date.today())

        total = 0
        count = 0

        for sale in sales:

            if today in sale[1]:
                total += sale[2]
                count += 1

        self.today_sales_label.text = "Today's Sales: RM" + str(total)
        self.transaction_label.text = "Transactions: " + str(count)

    def clear_cart(self, instance):

        self.cart = {}

        self.update_cart()

    def delete_product_confirm(self, name):

        print("Deleting product:", name)

        delete_product(name)

        self.load_products()

    def view_sales(self, instance):

        sales = get_sales()

        layout = BoxLayout(orientation="vertical")

        text = ""

        for sale in sales:
            text += "Date: " + str(sale[1]) + "   Total: RM" + str(sale[2]) + "\n"

        if text == "":
            text = "No sales yet."

        sales_label = Label(text=text)

        close_btn = Button(text="Close", size_hint_y=None, height=50)

        layout.add_widget(sales_label)
        layout.add_widget(close_btn)

        popup = Popup(
            title="Sales History",
            content=layout,
            size_hint=(0.7, 0.7)
        )

        close_btn.bind(on_press=popup.dismiss)

        popup.open()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.cart = {}

        # LEFT PANEL
        self.left_panel = GridLayout(cols=3, spacing=20, padding=20)
        self.add_widget(self.left_panel)

        # RIGHT PANEL
        self.right_panel = BoxLayout(orientation="vertical")
        self.add_widget(self.right_panel)

        # CART LABEL
        self.cart_label = Label(text="Cart Empty", font_size=20)
        self.total_label = Label(text="Total: RM0", font_size=26)
        self.today_sales_label = Label(text="Today's Sales: RM0", font_size=22)
        self.transaction_label = Label(text="Transactions: 0", font_size=20)

        self.right_panel.add_widget(self.today_sales_label)
        self.right_panel.add_widget(self.transaction_label)
        self.right_panel.add_widget(self.cart_label)
        self.right_panel.add_widget(self.total_label)
        clear_btn = Button(text="Clear Cart", size_hint_y=None, height=50)
        clear_btn.bind(on_press=self.clear_cart)
        self.right_panel.add_widget(clear_btn)

        # REMOVE BUTTON
        remove_btn = Button(text="Remove Last Item", size_hint_y=None, height=50)
        remove_btn.bind(on_press=self.remove_last_item)
        self.right_panel.add_widget(remove_btn)

        # CHECKOUT BUTTON
        checkout_btn = Button(text="Checkout", size_hint_y=None, height=80, font_size=24)
        checkout_btn.bind(on_press=self.checkout)
        self.right_panel.add_widget(checkout_btn)

        # PRODUCT INPUT
        self.name_input = TextInput(hint_text="Durian Name")
        self.price_input = TextInput(hint_text="Price")

        self.right_panel.add_widget(self.name_input)
        self.right_panel.add_widget(self.price_input)

        # ADD PRODUCT BUTTON
        add_btn = Button(text="Add Product", size_hint_y=None, height=50)
        add_btn.bind(on_press=self.add_product_clicked)

        self.right_panel.add_widget(add_btn)

        self.load_products()
        
        sales_btn = Button(text="View Sales", size_hint_y=None, height=50)
        sales_btn.bind(on_press=self.view_sales)
        self.right_panel.add_widget(sales_btn)
        self.update_daily_sales()

    def load_products(self):

        self.left_panel.clear_widgets()

        products = get_products()

        for product in products:

            name = product[1]
            price = product[2]

            btn = Button(
                text=name + "\nRM" + str(price),
                font_size=28,
                size_hint_y=None,
                height=180
            )

            btn.bind(on_press=lambda instance, n=name, p=price: self.add_to_cart(n, p))

            self.left_panel.add_widget(btn)

    def add_to_cart(self, name, price):

        if name in self.cart:
            self.cart[name]["qty"] += 1
        else:
            self.cart[name] = {"price": price, "qty": 1}

        self.update_cart()


    def update_cart(self):

        text = ""
        total = 0

        for item in self.cart:

            qty = self.cart[item]["qty"]
            price = self.cart[item]["price"]

            subtotal = qty * price
            total += subtotal

            text += item + " x" + str(qty) + " = RM" + str(subtotal) + "\n"

        if text == "":
            text = "Cart Empty"

        self.cart_label.text = text
        self.total_label.text = "Total: RM" + str(total)


    def remove_last_item(self, instance):

        if len(self.cart) == 0:
            return

        last_item = list(self.cart.keys())[-1]

        if self.cart[last_item]["qty"] > 1:
            self.cart[last_item]["qty"] -= 1
        else:
            del self.cart[last_item]

        self.update_cart()


    def checkout(self, instance):

        if len(self.cart) == 0:
            return

        total = 0

        for item in self.cart:
            qty = self.cart[item]["qty"]
            price = self.cart[item]["price"]
            total += qty * price

        date = str(datetime.datetime.now())

        save_sale(date, total)

        print("SALE SAVED:", total)

        self.cart = {}
        self.update_cart()
        self.update_daily_sales()

    def add_product_clicked(self, instance):

        name = self.name_input.text
        price = self.price_input.text

        if name == "" or price == "":
            return

        try:
            price = float(price)
        except:
            return

        add_product(name, price)

        self.name_input.text = ""
        self.price_input.text = ""

        self.load_products()


class DurianPOSApp(App):

    def build(self):

        create_product_table()
        create_sales_table()   

        return POSLayout()


DurianPOSApp().run()