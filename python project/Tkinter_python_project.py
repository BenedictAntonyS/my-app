import tkinter as tk
from tkinter import ttk
import sqlite3
import re
from tkinter import messagebox

class CustomerTracker(tk.Tk):
    def __init__(self):
        super().__init__()  
        self.title("Customer Tracker")
        self.geometry("800x600")

        # Create style for tabs
        self.style = ttk.Style(self)
        self.style.theme_create("ModernTabs", parent="alt", settings={
                "TNotebook": {
                    "configure": {"tabmargins": [2, 5, 2, 0], "background": "green", "borderwidth": 0}
                },
                "TNotebook.Tab": {
                    "configure": {
                        "padding": [10, 5], 
                        "font": ('Helvetica', 10, 'bold'),
                        "background": "#ffffff",
                        "foreground": "#555555",
                        "borderwidth": 1,
                        "bordercolor": "#dddddd"
                    },
                    "map": {
                        "background": [("selected", "#007acc")],
                        "foreground": [("selected", "#ffffff")],
                        "expand": [("selected", [1, 1, 1, 0])]
                    }
                }
            })

        self.style.theme_use("ModernTabs")


        # Create SQLite database connection
        self.conn = sqlite3.connect("customer_tracker.db")
        self.cur = self.conn.cursor()

        # Create customer and order tables
        self.create_tables()

        # Create tabs
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=1)

        # Create frames for each tab
        self.customer_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.customer_frame, text="Customers")

        self.order_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.order_frame, text="Orders")

        # Create customer frame widgets
        self.create_customer_widgets()

        # Create order frame widgets
        self.create_order_widgets()

        # Populate customer combo box
        self.populate_customer_combo()

    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                phone TEXT
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product TEXT,
                date TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
        self.conn.commit()

    def create_customer_widgets(self):
        self.customer_label = ttk.Label(self.customer_frame, text="Customer Information")
        self.customer_label.pack(pady=10)

        self.customer_name_label = ttk.Label(self.customer_frame, text="Name:")
        self.customer_name_label.pack()
        self.customer_name_entry = ttk.Entry(self.customer_frame, width=30)
        self.customer_name_entry.pack()

        self.customer_email_label = ttk.Label(self.customer_frame, text="Email:")
        self.customer_email_label.pack()
        self.customer_email_entry = ttk.Entry(self.customer_frame, width=30)
        self.customer_email_entry.pack()

        self.customer_phone_label = ttk.Label(self.customer_frame, text="Phone:")
        self.customer_phone_label.pack()
        self.customer_phone_entry = ttk.Entry(self.customer_frame, width=30)
        self.customer_phone_entry.pack()

        self.add_customer_button = ttk.Button(self.customer_frame, text="Add Customer", command=self.add_customer)
        self.add_customer_button.pack(pady=10)

        self.delete_customer_button = ttk.Button(self.customer_frame, text="Delete Customer", command=self.delete_customer)
        self.delete_customer_button.pack(pady=10)

        # Create treeview for displaying customers
        self.customer_treeview = ttk.Treeview(self.customer_frame, columns=("Name", "Email", "Phone"))
        self.customer_treeview.pack(fill="both", expand=True)
        self.customer_treeview.heading("#0", text="ID")
        self.customer_treeview.heading("Name", text="Name")
        self.customer_treeview.heading("Email", text="Email")
        self.customer_treeview.heading("Phone", text="Phone")

        # Bind events for hovering effect
        self.customer_treeview.bind("<Enter>", lambda event: self.on_enter(event.widget.focus()))
        self.customer_treeview.bind("<Leave>", lambda event: self.on_leave(event.widget.focus()))

    def create_order_widgets(self):
        self.order_label = ttk.Label(self.order_frame, text="Order Information")
        self.order_label.pack(pady=10)

        self.order_customer_label = ttk.Label(self.order_frame, text="Customer:")
        self.order_customer_label.pack()
        self.order_customer_combo = ttk.Combobox(self.order_frame, values=["Select Customer"])
        self.order_customer_combo.pack()

        self.order_product_label = ttk.Label(self.order_frame, text="Product:")
        self.order_product_label.pack()
        self.order_product_entry = ttk.Entry(self.order_frame, width=30)
        self.order_product_entry.pack()

        self.order_date_label = ttk.Label(self.order_frame, text="Date (YYYY-MM-DD):")
        self.order_date_label.pack()
        self.order_date_entry = ttk.Entry(self.order_frame, width=30)
        self.order_date_entry.pack()

        self.add_order_button = ttk.Button(self.order_frame, text="Add Order", command=self.add_order)
        self.add_order_button.pack(pady=10)

        # Create treeview for displaying orders
        self.order_treeview = ttk.Treeview(self.order_frame, columns=("Customer", "Product", "Date"))
        self.order_treeview.pack(fill="both", expand=True)
        self.order_treeview.heading("#0", text="ID")
        self.order_treeview.heading("Customer", text="Customer")
        self.order_treeview.heading("Product", text="Product")
        self.order_treeview.heading("Date", text="Date")

    def populate_customer_combo(self):
        self.cur.execute("SELECT id, name FROM customers")
        customers = self.cur.fetchall()
        customer_list = ["Select Customer"]
        for customer in customers:
            customer_list.append(f"{customer[0]}: {customer[1]}")
        self.order_customer_combo["values"] = customer_list

    def add_customer(self):
        customer_name = self.customer_name_entry.get()
        customer_email = self.customer_email_entry.get()
        customer_phone = self.customer_phone_entry.get()

        if not re.match(r'^\d{10}$', customer_phone):
            tk.messagebox.showerror("Error", "Please enter a valid 10-digit phone number.")
            return

        if not re.match(r'^[a-zA-Z0-9._%+-]+@+gmail+.com', customer_email):
            tk.messagebox.showerror("Error", "Please enter a valid email address.")
            return

        self.cur.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", (customer_name, customer_email, customer_phone))
        self.conn.commit()

        self.populate_customer_combo()

        self.customer_name_entry.delete(0, "end")
        self.customer_email_entry.delete(0, "end")
        self.customer_phone_entry.delete(0, "end")

        self.refresh_customer_treeview()

    def delete_customer(self):
        selected_item = self.customer_treeview.selection()
        if not selected_item:
            tk.messagebox.showwarning("Warning", "Please select a customer to delete.")
            return

        customer_id = self.customer_treeview.item(selected_item)['values'][0]

        if tk.messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this customer?"):
            self.cur.execute("DELETE FROM customers WHERE id=?", (customer_id,))
            self.conn.commit()

            self.populate_customer_combo()
            self.refresh_customer_treeview()

    def on_enter(self, event):
        self.customer_treeview.item(event, tags=("hover",{'background': '#c2dfff'}))


    def on_leave(self, event):
        self.customer_treeview.item(event, tags=())

    def refresh_customer_treeview(self):
        for item in self.customer_treeview.get_children():
            self.customer_treeview.delete(item)

        self.cur.execute("SELECT * FROM customers")
        customers = self.cur.fetchall()
        for customer in customers:
            self.customer_treeview.insert("", "end", values=customer)

    def add_order(self):
        order_customer_index = self.order_customer_combo.current()
        if order_customer_index == 0:
            tk.messagebox.showwarning("Warning", "Please select a customer for the order.")
            return
        order_customer_id = order_customer_index

        order_product = self.order_product_entry.get()
        order_date = self.order_date_entry.get()

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', order_date):
            tk.messagebox.showerror("Error", "Please enter the date in YYYY-MM-DD format.")
            return

        self.cur.execute("INSERT INTO orders (customer_id, product, date) VALUES (?, ?, ?)", (order_customer_id, order_product, order_date))
        self.conn.commit()

        self.order_customer_combo.set("Select Customer")
        self.order_product_entry.delete(0, "end")
        self.order_date_entry.delete(0, "end")

        self.refresh_order_treeview()

    def refresh_order_treeview(self):
        for item in self.order_treeview.get_children():
            self.order_treeview.delete(item)

        self.cur.execute("SELECT * FROM orders")
        orders = self.cur.fetchall()
        for order in orders:
            self.order_treeview.insert("", "end", values=order)

if __name__ == "__main__":
    app = CustomerTracker()
    app.mainloop()
