import sys
# DISBALE '__pycache__' GENERATION
sys.dont_write_bytecode = True

import os
# NAVIGATE TO THE BASE DIRECTORY "../ecommerce-order-manager/app/"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# AUTO CREATE FOLDER 'csv' IF NOT EXISTED
CSV_DIR = BASE_DIR + "/csv"
os.makedirs(CSV_DIR, exist_ok=True)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db.connection import Connection
import csv
from services import customer_orders, order_details, orders_by_status, products_revenue_summary, revenue_by_date
customer_orders, order_details, orders_by_status, products_revenue_summary, revenue_by_date
from models import create, delete, read, update
create, delete, read, update


class _Ecommerce:
    """ ROOT METHODS """
    def dbConnect(self):
        self.con = Connection()
        self.cur = self.con.cur
        self.connect_db = self.con.connect_db


    def __init__(self, root):
        # INITIALIZE WINDOW
        self.root = root
        self.root.title("E-commerce Order Manager v1.0")
       
        # WINDOW CONFIGURATION
        self.width = 1600
        self.height = 900
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.configure(bg="#4A93FF")
        
        # GLOBAL VARIABLES FOR FUNCTIONS
        self.active_table = []
        self.curr_data = None
        self.file_name = None

        # MAIN TITLE
        main_title = tk.Label(self.root, text="E-commerce Order Manager", bd=5, relief="raised", bg="#0066ff", fg="white", font=("Courier",40,"bold"))
        main_title.pack(side="top", fill="x")

        # OPTIONS FRAME
        self.main_menu_frame = tk.Frame(self.root, bg="#4dc3ff", bd=5, relief="ridge")
        self.main_menu_frame.place(width=self.width/4.5, height=self.height/1.3, x=30, y=100)

        # MAIN BUTTONS (MAIN MENU OPTIONS)
        addBtn = tk.Button(self.main_menu_frame, text="Add", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                   command=self.addOptions)
        addBtn.grid(row=0, column=0, padx=40, pady=20)

        updateBtn = tk.Button(self.main_menu_frame, text="Update", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                   command=self.updateOptions)
        updateBtn.grid(row=1, column=0, padx=40, pady=20)

        removeCustomerBtn = tk.Button(self.main_menu_frame, text="Remove", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"), 
                                      command=self.removeOptions)
        removeCustomerBtn.grid(row=2, column=0, padx=40, pady=20)

        searchCustomerBtn = tk.Button(self.main_menu_frame, text="Search", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                      command=self.searchOptions)
        searchCustomerBtn.grid(row=3, column=0, padx=40, pady=20)

        showAllBtn = tk.Button(self.main_menu_frame, text="Show All", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                               command=self.showAllOptions)
        showAllBtn.grid(row=4, column=0, padx=40, pady=20)
        
        viewsBtn = tk.Button(self.main_menu_frame, text="Views", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                             command=self.viewOptions)
        viewsBtn.grid(row=5, column=0, padx=40, pady=20)

        csvBtn = tk.Button(self.main_menu_frame, text="Export CSV", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                             command=self.export_csv)
        csvBtn.grid(row=6, column=0, padx=40, pady=20)

        exitBtn = tk.Button(self.main_menu_frame, text="Exit", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                             command=self.exitWindow)
        exitBtn.grid(row=7, column=0, padx=40, pady=25)


        # DETAIL FRAME
        self.det_frame = tk.Frame(self.root, bg="#0066ff", bd=5, relief="ridge")
        self.det_frame.place(width=self.width/1.525, height=self.height/1.3, x=500, y=100)

        det_label = tk.Label(self.det_frame, text="Details", fg="white", bg="#0066ff", font=("Courier",30,"bold"))
        det_label.pack(side="top")


    def __closeTable(self):
        while self.active_table:
            (self.active_table.pop(0)).destroy()


    def export_csv(self):
        # IF NO TABLE IS SHOWN, RETURN ERROR
        if self.curr_data == None:
            messagebox.showerror("Unavailable table !", "You must open a table from 'Show all' or 'views' !")
            return

        # RECREATE THE 'csv' FOLDER IF IT IS DELETED IN EXECUTION.
        os.makedirs(CSV_DIR, exist_ok=True)

        try:
        # CREATE AND WRITE CSV FILE TO THE STORE FOLDER
            output_csv = os.path.join(CSV_DIR, self.file_name)

            with open(output_csv, 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(self.curr_data)
            file.close()
            messagebox.showinfo("Success !", f"{self.file_name} is Exported Successfully !")
            return
        
        except:
            messagebox.showerror("Missing folder !", "Output Directory '.../ecommerce-order-manager/app/csv' Not Found !")
            return


    """ MAIN MENU """
    def addOptions(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.add_frame = tk.Frame(self.root, bg="#629FFA", bd=3, relief="ridge")
        self.add_frame.place(width=self.width/5, height=self.height/2, x=600, y=200)

        # CREATE BUTTONS
        addCustomerBtn = tk.Button(self.add_frame, text="Add Customer", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                    command=self.addCustomerTab)
        addCustomerBtn.grid(row=0, column=0, padx=30, pady=30)

        addProductBtn = tk.Button(self.add_frame, text="Add Product", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                   command=self.addProductTab)
        addProductBtn.grid(row=1, column=0, padx=30, pady=0)

        addOrderBtn = tk.Button(self.add_frame, text="Add Order", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                 command=self.addOrderTab)
        addOrderBtn.grid(row=2, column=0, padx=30, pady=30)

        addOrderitemsBtn = tk.Button(self.add_frame, text="Add Ordered Products", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                 command=self.addOrderitemsTab)
        addOrderitemsBtn.grid(row=3, column=0, padx=30, pady=0)

        cancelBtn = tk.Button(self.add_frame, text="Cancel", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                              command=self.add_frame.destroy)
        cancelBtn.grid(row=4, column=0, padx=30, pady=60)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.add_frame)


    def updateOptions(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.update_frame = tk.Frame(self.root, bg="#629FFA", bd=3, relief="ridge")
        self.update_frame.place(width=self.width/5, height=self.height/3, x=600, y=200)

        # CREATE BUTTONS
        updatePriceBtn = tk.Button(self.update_frame, text="Product's Price", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                    command=self.updateProductTab)
        updatePriceBtn.grid(row=0, column=0, padx=30, pady=30)

        updateStatusBtn = tk.Button(self.update_frame, text="Order's Status", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                   command=self.updateStatusTab)
        updateStatusBtn.grid(row=1, column=0, padx=30, pady=0)

        cancelBtn = tk.Button(self.update_frame, text="Cancel", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                              command=self.update_frame.destroy)
        cancelBtn.grid(row=2, column=0, padx=30, pady=75)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.update_frame)


    def removeOptions(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.remove_frame = tk.Frame(self.root, bg="#629FFA", bd=3, relief="ridge")
        self.remove_frame.place(width=self.width/5, height=self.height/2.5, x=600, y=200)

        # ADD BUTTONS
        removeCustomerBtn = tk.Button(self.remove_frame, text="Remove Customer", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                    command=self.deleteCustomerTab)
        removeCustomerBtn.grid(row=0, column=0, padx=30, pady=30)

        removeProductBtn = tk.Button(self.remove_frame, text="Remove Product", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                   command=self.deleteProductTab)
        removeProductBtn.grid(row=1, column=0, padx=30, pady=0)

        removeOrderBtn = tk.Button(self.remove_frame, text="Remove Order", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                 command=self.deleteOrderTab)
        removeOrderBtn.grid(row=2, column=0, padx=30, pady=30)

        cancelBtn = tk.Button(self.remove_frame, text="Cancel", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                              command=self.remove_frame.destroy)
        cancelBtn.grid(row=3, column=0, padx=30, pady=30)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.remove_frame)


    def searchOptions(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.search_frame = tk.Frame(self.root, bg="#629FFA", bd=3, relief="ridge")
        self.search_frame.place(width=self.width/4.5, height=self.height/2, x=600, y=200)

        # CREATE BUTTONS
        searchCustomerBtn = tk.Button(self.search_frame, text="Search Customer", bd=3, relief="raised", bg="light gray", width=23, font=("Courier",15,"bold"),
                                    command=self.searchCustomerTab)
        searchCustomerBtn.grid(row=0, column=0, padx=30, pady=30)

        searchProductBtn = tk.Button(self.search_frame, text="Search Product", bd=3, relief="raised", bg="light gray", width=23, font=("Courier",15,"bold"),
                                   command=self.searchProductTab)
        searchProductBtn.grid(row=1, column=0, padx=30, pady=0)

        searchOrderBtn = tk.Button(self.search_frame, text="Search Order", bd=3, relief="raised", bg="light gray", width=23, font=("Courier",15,"bold"),
                                 command=self.searchOrderTab)
        searchOrderBtn.grid(row=2, column=0, padx=30, pady=30)

        searchCustomerOrdersBtn = tk.Button(self.search_frame, text="Search Customer Orders", bd=3, relief="raised", bg="light gray", width=23, font=("Courier",15,"bold"),
                              command=self.searchCusOrdersTab)
        searchCustomerOrdersBtn.grid(row=3, column=0, padx=30, pady=0)

        cancelBtn = tk.Button(self.search_frame, text="Cancel", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                              command=self.search_frame.destroy)
        cancelBtn.grid(row=4, column=0, padx=30, pady=60)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.search_frame)


    def showAllOptions(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.showall_frame = tk.Frame(self.root, bg="#629FFA", bd=3, relief="ridge")
        self.showall_frame.place(width=self.width/5, height=self.height/2.5, x=600, y=200)

        allCustomersBtn = tk.Button(self.showall_frame, text="All Customers", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                    command=self.tabAllCustomerFunc)
        allCustomersBtn.grid(row=0, column=0, padx=30, pady=30)

        allProductsBtn = tk.Button(self.showall_frame, text="All Products", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                   command=self.tabAllProductFunc)
        allProductsBtn.grid(row=1, column=0, padx=30, pady=0)

        allOrdersBtn = tk.Button(self.showall_frame, text="All Orders", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                 command=self.tabAllOrderFunc)
        allOrdersBtn.grid(row=2, column=0, padx=30, pady=30)

        cancelBtn = tk.Button(self.showall_frame, text="Cancel", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                              command=self.showall_frame.destroy)
        cancelBtn.grid(row=3, column=0, padx=30, pady=30)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.showall_frame)


    def viewOptions(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.view_frame = tk.Frame(self.root, bg="#629FFA", bd=3, relief="ridge")
        self.view_frame.place(width=self.width/5, height=self.height/2, x=600, y=200)

        # CREATE BUTTONS
        orderDetailsBtn = tk.Button(self.view_frame, text="Order Details", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                    command=self.tabOrderDetailsFunc)
        orderDetailsBtn.grid(row=0, column=0, padx=30, pady=20)

        customerOrdersBtn = tk.Button(self.view_frame, text="Customer Orders", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                      command=self.tabCustomerOrdersFunc)
        customerOrdersBtn.grid(row=1, column=0, padx=30, pady=0)

        datesRevenueBtn = tk.Button(self.view_frame, text="Revenue by Dates", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                    command=self.tabDateRevenueFunc)
        datesRevenueBtn.grid(row=2, column=0, padx=30, pady=20)

        productsRevenueBtn = tk.Button(self.view_frame, text="Revenue by Products", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                       command=self.tabProductRevenueFunc)
        productsRevenueBtn.grid(row=3, column=0, padx=30, pady=0)

        statusCountBtn = tk.Button(self.view_frame, text="Order Status Count", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                                   command=self.tabStatusCountFunc)
        statusCountBtn.grid(row=4, column=0, padx=30, pady=20)

        cancelBtn = tk.Button(self.view_frame, text="Cancel", bd=3, relief="raised", bg="light gray", width=20, font=("Courier",15,"bold"),
                              command=self.view_frame.destroy)
        cancelBtn.grid(row=5, column=0, padx=30, pady=30)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.view_frame)


    def exitWindow(self):
        # CLOSE THE MAIN WINDOW
        self.root.destroy()


    """ OPTIONS OF (MAIN MENU) 'UPDATE'"""
    def updateProductTab(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.update_product = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.update_product.place(width=self.width/3, height=self.height/3.5, x=600, y=200)

        # INPUT BAR FOR 'ProductID'
        pid_label = tk.Label(self.update_product, text="Product ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        pid_label.grid(row=0, column=0, padx=20, pady=20)
        self.pid_input = tk.Entry(self.update_product, font=("Courier",15,"bold"), width=25)
        self.pid_input.grid(row=0, column=1, padx=5, pady=0)

        # INPUT BAR FOR 'New Price'
        price_label = tk.Label(self.update_product, text="New Price ($)", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        price_label.grid(row=1, column=0, padx=20, pady=0)
        self.price_input = tk.Entry(self.update_product, font=("Courier",15,"bold"), width=25)
        self.price_input.grid(row=1, column=1, padx=5, pady=30)

        # ENTER BUTTON
        enterBtn = tk.Button(self.update_product, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.updateProductFunc)
        enterBtn.grid(row=2, column=0, padx=30, pady=25)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.update_product, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.update_product.destroy)
        cancelBtn.grid(row=2, column=1, padx=30, pady=25)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.update_product)


    def updateStatusTab(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.update_status = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.update_status.place(width=self.width/3, height=self.height/3.5, x=600, y=200)

        # INPUT BAR FOR 'OrderID'
        ordid_label = tk.Label(self.update_status, text="Order ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        ordid_label.grid(row=0, column=0, padx=20, pady=20)
        self.ordid_input = tk.Entry(self.update_status, font=("Courier",15,"bold"), width=25)
        self.ordid_input.grid(row=0, column=1, padx=5, pady=0)

        # INPUT BAR FOR 'New Status'
        sts_label = tk.Label(self.update_status, text="New Status", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        sts_label.grid(row=1, column=0, padx=20, pady=0)
        self.sts_input = tk.Entry(self.update_status, font=("Courier",15,"bold"), width=25)
        self.sts_input.grid(row=1, column=1, padx=5, pady=30)

        # ENTER BUTTON
        enterBtn = tk.Button(self.update_status, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.updateStatusFunc)
        enterBtn.grid(row=2, column=0, padx=30, pady=25)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.update_status, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.update_status.destroy)
        cancelBtn.grid(row=2, column=1, padx=30, pady=25)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.update_status)


    """ OPTIONS AND FUNCTIONS OF (MAIN MENU) 'SHOW ALL' """
    def tabAllCustomerFunc(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.customer_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
        self.customer_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

        # SLIDE BARS
        x_scroll = tk.Scrollbar(self.customer_frame, orient="horizontal", width=15)
        x_scroll.pack(side="bottom", fill="x")
        y_scroll = tk.Scrollbar(self.customer_frame, orient="vertical", width=15)
        y_scroll.pack(side="right", fill="y")

        # INITIALIZE TABLE
        all_customer_table = ttk.Treeview(self.customer_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                          columns=("CustomerID", "CustomerName"))
        x_scroll.config(command=all_customer_table.xview)
        y_scroll.config(command=all_customer_table.yview)
        all_customer_table.pack(fill="both", expand=1)
        all_customer_table.heading("CustomerID", text="Customer ID")
        all_customer_table.heading("CustomerName", text="Customer Name")
        all_customer_table["show"] = "headings"
        
        # ADD TO ACTIVE TABLE
        self.active_table.append(self.customer_frame)

        # CONNECTING TO DATABASE AND FETCHING ROWS
        self.dbConnect()
        self.cur.execute("SELECT * FROM customers;")
        rows = self.cur.fetchall()
        self.connect_db.close()

        # ASSIGN FETCHED DATA TO GLOBAL VARIABLES FOR EXPORTING TO CSV FILES
        self.file_name = 'all_customers.csv'
        self.curr_data = rows

        # PRINT DATA TO THE TREE VIEW (DETAILS)
        for row in rows:
            all_customer_table.insert("", "end", values=row)

        # CLOSE THE PREVIOUS TAB
        self.showall_frame.destroy()


    def tabAllProductFunc(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.product_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
        self.product_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

        # SLIDE BARS
        x_scroll = tk.Scrollbar(self.product_frame, orient="horizontal", width=15)
        x_scroll.pack(side="bottom", fill="x")
        y_scroll = tk.Scrollbar(self.product_frame, orient="vertical", width=15)
        y_scroll.pack(side="right", fill="y")

        # INITIALIZE TABLE
        all_product_table = ttk.Treeview(self.product_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                          columns=("ProductID", "ProductName", "Price"))
        x_scroll.config(command=all_product_table.xview)
        y_scroll.config(command=all_product_table.yview)
        all_product_table.pack(fill="both", expand=1)
        all_product_table.heading("ProductID", text="Product ID")
        all_product_table.heading("ProductName", text="Product Name")
        all_product_table.heading("Price", text="Price")
        all_product_table["show"] = "headings"

        # ADD TO ACTIVE TABLE
        self.active_table.append(self.product_frame)

        # CONNECTING TO DATABASE AND FETCHING ROWS
        self.dbConnect()
        self.cur.execute("SELECT * FROM products;")
        rows = self.cur.fetchall()
        self.connect_db.close()

        # ASSIGN FETCHED DATA TO GLOBAL VARIABLES FOR EXPORTING TO CSV FILES
        self.file_name = 'all_products.csv'
        self.curr_data = rows

        # PRINT DATA TO THE TREE VIEW (DETAILS)
        for row in rows:
            all_product_table.insert("", "end", values=row)

        # CLOSE THE PREVIOUS TAB
        self.showall_frame.destroy()


    def tabAllOrderFunc(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.order_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
        self.order_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

        # SLIDE BARS
        x_scroll = tk.Scrollbar(self.order_frame, orient="horizontal", width=15)
        x_scroll.pack(side="bottom", fill="x")
        y_scroll = tk.Scrollbar(self.order_frame, orient="vertical", width=15)
        y_scroll.pack(side="right", fill="y")

        # INITIALIZE TABLE
        all_order_table = ttk.Treeview(self.order_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                          columns=("OrderID", "OrderDate", "Status", "CustomerID"))
        x_scroll.config(command=all_order_table.xview)
        y_scroll.config(command=all_order_table.yview)
        all_order_table.pack(fill="both", expand=1)
        all_order_table.heading("OrderID", text="Order ID")
        all_order_table.heading("OrderDate", text="Order Date")
        all_order_table.heading("Status", text="Status")
        all_order_table.heading("CustomerID", text="Ordered by")
        all_order_table["show"] = "headings"

        # ADD TO ACTIVE TABLE
        self.active_table.append(self.order_frame)

        # CONNECTING TO DATABASE AND FETCHING ROWS
        self.dbConnect()
        self.cur.execute("SELECT * FROM orders;")
        rows = self.cur.fetchall()
        self.connect_db.close()

        # ASSIGN FETCHED DATA TO GLOBAL VARIABLES FOR EXPORTING TO CSV FILES
        self.file_name = 'all_orders.csv'
        self.curr_data = rows

        # PRINT DATA TO THE TREE VIEW (DETAILS)
        for row in rows:
            all_order_table.insert("", "end", values=row)
        
        # CLOSE THE PREVIOUS TAB
        self.showall_frame.destroy()


    """ OPTIONS AND FUNCTIONS OF (MAIN MENU) 'VIEW' """
    def tabOrderDetailsFunc(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.orderdet_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
        self.orderdet_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

        # SLIDE BARS
        x_scroll = tk.Scrollbar(self.orderdet_frame, orient="horizontal", width=15)
        x_scroll.pack(side="bottom", fill="x")
        y_scroll = tk.Scrollbar(self.orderdet_frame, orient="vertical", width=15)
        y_scroll.pack(side="right", fill="y")

        # INITIALIZE TABLE
        orderdet_table = ttk.Treeview(self.orderdet_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                          columns=("OrderID", "CustomerID", "CustomerName", "ProductName", "OrderDate", "Quantity", "total_price", "Status"))
        x_scroll.config(command=orderdet_table.xview)
        y_scroll.config(command=orderdet_table.yview)
        orderdet_table.pack(fill="both", expand=1)
        orderdet_table.heading("OrderID", text="Order ID")
        orderdet_table.heading("CustomerID", text="Customer ID")
        orderdet_table.heading("CustomerName", text="Customer Name")
        orderdet_table.heading("ProductName", text="Product Name")
        orderdet_table.heading("OrderDate", text="Order Date")
        orderdet_table.heading("Quantity", text="Quantity")
        orderdet_table.heading("total_price", text="Total Price")
        orderdet_table.heading("Status", text="Status")
        orderdet_table["show"] = "headings"

        # ADD TO ACTIVE TABLE
        self.active_table.append(self.orderdet_frame)

        # CONNECTING TO DATABASE AND FETCHING ROWS
        self.dbConnect()
        self.cur.execute("SELECT * FROM order_details;")
        rows = self.cur.fetchall()
        self.connect_db.close()

        # ASSIGN FETCHED DATA TO GLOBAL VARIABLES FOR EXPORTING TO CSV FILES
        self.file_name = 'view_order_details.csv'
        self.curr_data = rows

        # PRINT DATA TO THE TREE VIEW (DETAILS)
        for row in rows:
            orderdet_table.insert("", "end", values=row)

        # CLOSE THE PREVIOUS TAB
        self.view_frame.destroy()


    def tabCustomerOrdersFunc(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.cusorder_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
        self.cusorder_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

        # SLIDE BARS
        x_scroll = tk.Scrollbar(self.cusorder_frame, orient="horizontal", width=15)
        x_scroll.pack(side="bottom", fill="x")
        y_scroll = tk.Scrollbar(self.cusorder_frame, orient="vertical", width=15)
        y_scroll.pack(side="right", fill="y")

        # INITIALIZE TABLE
        cusorder_table = ttk.Treeview(self.cusorder_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                          columns=("CustomerID", "CustomerName", "OrderID", "OrderDate", "Status"))
        x_scroll.config(command=cusorder_table.xview)
        y_scroll.config(command=cusorder_table.yview)
        cusorder_table.pack(fill="both", expand=1)
        cusorder_table.heading("CustomerID", text="Customer ID")
        cusorder_table.heading("CustomerName", text="Customer Name")
        cusorder_table.heading("OrderID", text="Order ID")
        cusorder_table.heading("OrderDate", text="Order Date")
        cusorder_table.heading("Status", text="Status")
        cusorder_table["show"] = "headings"

        # ADD TO ACTIVE TABLE
        self.active_table.append(self.cusorder_frame)

        # CONNECTING TO DATABASE AND FETCHING ROWS
        self.dbConnect()
        self.cur.execute("SELECT * FROM customer_orders;")
        rows = self.cur.fetchall()
        self.connect_db.close()

        # ASSIGN FETCHED DATA TO GLOBAL VARIABLES FOR EXPORTING TO CSV FILES
        self.file_name = 'view_customer_orders.csv'
        self.curr_data = rows

        # PRINT DATA TO THE TREE VIEW (DETAILS)
        for row in rows:
            cusorder_table.insert("", "end", values=row)

        # CLOSE THE PREVIOUS TAB
        self.view_frame.destroy()


    def tabDateRevenueFunc(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.dt_rev_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
        self.dt_rev_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

        # SLIDE BARS
        x_scroll = tk.Scrollbar(self.dt_rev_frame, orient="horizontal", width=15)
        x_scroll.pack(side="bottom", fill="x")
        y_scroll = tk.Scrollbar(self.dt_rev_frame, orient="vertical", width=15)
        y_scroll.pack(side="right", fill="y")

        # INITIALIZE TABLE
        dt_rev_table = ttk.Treeview(self.dt_rev_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                          columns=("OrderDate", "orders_count", "revenue"))
        x_scroll.config(command=dt_rev_table.xview)
        y_scroll.config(command=dt_rev_table.yview)
        dt_rev_table.pack(fill="both", expand=1)
        dt_rev_table.heading("OrderDate", text="Order Date")
        dt_rev_table.heading("orders_count", text="Orders Count")
        dt_rev_table.heading("revenue", text="Revenue")
        dt_rev_table["show"] = "headings"

        # ADD TO ACTIVE TABLE
        self.active_table.append(self.dt_rev_frame)

        # CONNECTING TO DATABASE AND FETCHING ROWS
        self.dbConnect()
        self.cur.execute("SELECT * FROM revenue_by_date;")
        rows = self.cur.fetchall()
        self.connect_db.close()

        # ASSIGN FETCHED DATA TO GLOBAL VARIABLES FOR EXPORTING TO CSV FILES
        self.file_name = 'view_revenue_by_date.csv'
        self.curr_data = rows

        # PRINT DATA TO THE TREE VIEW (DETAILS)
        for row in rows:
            dt_rev_table.insert("", "end", values=row)

        # CLOSE THE PREVIOUS TAB
        self.view_frame.destroy()


    def tabProductRevenueFunc(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.p_rev_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
        self.p_rev_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

        # SLIDE BARS
        x_scroll = tk.Scrollbar(self.p_rev_frame, orient="horizontal", width=15)
        x_scroll.pack(side="bottom", fill="x")
        y_scroll = tk.Scrollbar(self.p_rev_frame, orient="vertical", width=15)
        y_scroll.pack(side="right", fill="y")

        # INITIALIZE TABLE
        p_rev_table = ttk.Treeview(self.p_rev_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                          columns=("ProductID", "ProductName", "sold_quantity", "revenue"))
        x_scroll.config(command=p_rev_table.xview)
        y_scroll.config(command=p_rev_table.yview)
        p_rev_table.pack(fill="both", expand=1)
        p_rev_table.heading("ProductID", text="Product ID")
        p_rev_table.heading("ProductName", text="Product Name")
        p_rev_table.heading("sold_quantity", text="Sold Quantity")
        p_rev_table.heading("revenue", text="Revenue")
        p_rev_table["show"] = "headings"

        # ADD TO ACTIVE TABLE
        self.active_table.append(self.p_rev_frame)

        # CONNECTING TO DATABASE AND FETCHING ROWS
        self.dbConnect()
        self.cur.execute("SELECT * FROM products_revenue_summary;")
        rows = self.cur.fetchall()
        self.connect_db.close()

        # ASSIGN FETCHED DATA TO GLOBAL VARIABLES FOR EXPORTING TO CSV FILES
        self.file_name = 'view_revenue_by_products.csv'
        self.curr_data = rows

        # PRINT DATA TO THE TREE VIEW (DETAILS)
        for row in rows:
            p_rev_table.insert("", "end", values=row)

        # CLOSE THE PREVIOUS TAB
        self.view_frame.destroy()


    def tabStatusCountFunc(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE FRAME
        self.sts_cnt_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
        self.sts_cnt_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

        # SLIDE BARS
        x_scroll = tk.Scrollbar(self.sts_cnt_frame, orient="horizontal", width=15)
        x_scroll.pack(side="bottom", fill="x")
        y_scroll = tk.Scrollbar(self.sts_cnt_frame, orient="vertical", width=15)
        y_scroll.pack(side="right", fill="y")

        # INITIALIZE TABLE
        sts_cnt_table = ttk.Treeview(self.sts_cnt_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                          columns=("Status", "total_count"))
        x_scroll.config(command=sts_cnt_table.xview)
        y_scroll.config(command=sts_cnt_table.yview)
        sts_cnt_table.pack(fill="both", expand=1)
        sts_cnt_table.heading("Status", text="Status")
        sts_cnt_table.heading("total_count", text="Count")
        sts_cnt_table["show"] = "headings"

        # ADD TO ACTIVE TABLE
        self.active_table.append(self.sts_cnt_frame)

        # CONNECTING TO DATABASE AND FETCHING ROWS
        self.dbConnect()
        self.cur.execute("SELECT * FROM orders_by_status;")
        rows = self.cur.fetchall()
        self.connect_db.close()

        # ASSIGN FETCHED DATA TO GLOBAL VARIABLES FOR EXPORTING TO CSV FILES
        self.file_name = 'view_status_count.csv'
        self.curr_data = rows

        # PRINT DATA TO THE TREE VIEW (DETAILS)
        for row in rows:
            sts_cnt_table.insert("", "end", values=row)

        # CLOSE THE PREVIOUS TAB
        self.view_frame.destroy()


    """ OPTIONS OF (MAIN MENU) 'ADD' """
    def addCustomerTab(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.add_customer = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.add_customer.place(width=self.width/3, height=self.height/4, x=600, y=200)

        # INPUT BAR FOR 'CustomerID'
        cid_label = tk.Label(self.add_customer, text="Customer ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        cid_label.grid(row=0, column=0, padx=20, pady=30)
        self.cid_input = tk.Entry(self.add_customer, font=("Courier",15,"bold"), width=25)
        self.cid_input.grid(row=0, column=1, padx=5, pady=30)
        
        # INPUT BAR FOR 'CustomerName'
        cname_label = tk.Label(self.add_customer, text="Full Name", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        cname_label.grid(row=1, column=0, padx=20, pady=0)
        self.cname_input = tk.Entry(self.add_customer, font=("Courier",15,"bold"), width=25)
        self.cname_input.grid(row=1, column=1, padx=5, pady=0)

        # ENTER BUTTON
        enterBtn = tk.Button(self.add_customer, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.addCustomerFunc)
        enterBtn.grid(row=2, column=0, padx=30, pady=30)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.add_customer, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.add_customer.destroy)
        cancelBtn.grid(row=2, column=1, padx=30, pady=30)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.add_customer)


    def addProductTab(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.add_product = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.add_product.place(width=self.width/3, height=self.height/3, x=600, y=200)

        # INPUT BAR FOR 'ProductID'
        pid_label = tk.Label(self.add_product, text="Product ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        pid_label.grid(row=0, column=0, padx=20, pady=30)
        self.pid_input = tk.Entry(self.add_product, font=("Courier",15,"bold"), width=25)
        self.pid_input.grid(row=0, column=1, padx=5, pady=30)
        
        # INPUT BAR FOR 'ProductName'
        pname_label = tk.Label(self.add_product, text="Product Name", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        pname_label.grid(row=1, column=0, padx=20, pady=0)
        self.pname_input = tk.Entry(self.add_product, font=("Courier",15,"bold"), width=25)
        self.pname_input.grid(row=1, column=1, padx=5, pady=0)

        # INPUT BAR FOR 'Price'
        price_label = tk.Label(self.add_product, text="Price ($)", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        price_label.grid(row=2, column=0, padx=20, pady=0)
        self.price_input = tk.Entry(self.add_product, font=("Courier",15,"bold"), width=25)
        self.price_input.grid(row=2, column=1, padx=5, pady=30)

        # ENTER BUTTON
        enterBtn = tk.Button(self.add_product, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.addProductFunc)
        enterBtn.grid(row=3, column=0, padx=30, pady=0)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.add_product, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.add_product.destroy)
        cancelBtn.grid(row=3, column=1, padx=30, pady=0)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.add_product)


    def addOrderTab(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.add_order = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.add_order.place(width=self.width/3, height=self.height/4, x=600, y=200)

        # INPUT BAR FOR 'OrderID'
        ordid_label = tk.Label(self.add_order, text="Order ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        ordid_label.grid(row=0, column=0, padx=20, pady=30)
        self.ordid_input = tk.Entry(self.add_order, font=("Courier",15,"bold"), width=25)
        self.ordid_input.grid(row=0, column=1, padx=5, pady=30)
        
        # INPUT BAR FOR 'CustomerID'
        cid_label = tk.Label(self.add_order, text="Ordered by", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        cid_label.grid(row=1, column=0, padx=20, pady=0)
        self.cid_input = tk.Entry(self.add_order, font=("Courier",15,"bold"), width=25)
        self.cid_input.grid(row=1, column=1, padx=5, pady=0)

        # ENTER BUTTON
        enterBtn = tk.Button(self.add_order, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.addOrderFunc)
        enterBtn.grid(row=2, column=0, padx=30, pady=30)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.add_order, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.add_order.destroy)
        cancelBtn.grid(row=2, column=1, padx=30, pady=30)

        # ADD TO ACTIVE TABS
        self.active_table.append(self.add_order)


    def addOrderitemsTab(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.add_orderitems = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.add_orderitems.place(width=self.width/3, height=self.height/3.5, x=600, y=200)

        # INPUT BAR FOR 'OrderID'
        ordid_label = tk.Label(self.add_orderitems, text="Order ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        ordid_label.grid(row=0, column=0, padx=20, pady=25)
        self.ordid_input = tk.Entry(self.add_orderitems, font=("Courier",15,"bold"), width=25)
        self.ordid_input.grid(row=0, column=1, padx=5, pady=25)

        # INPUT BAR FOR 'ProductID'
        pid_label = tk.Label(self.add_orderitems, text="Product ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        pid_label.grid(row=1, column=0, padx=20, pady=0)
        self.pid_input = tk.Entry(self.add_orderitems, font=("Courier",15,"bold"), width=25)
        self.pid_input.grid(row=1, column=1, padx=5, pady=0)
        
        # INPUT BAR FOR 'Quantity'
        qty_label = tk.Label(self.add_orderitems, text="Quantity", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        qty_label.grid(row=2, column=0, padx=20, pady=25)
        self.qty_input = tk.Entry(self.add_orderitems, font=("Courier",15,"bold"), width=25)
        self.qty_input.grid(row=2, column=1, padx=5, pady=25)

        # ENTER BUTTON
        enterBtn = tk.Button(self.add_orderitems, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.addOrderitemsFunc)
        enterBtn.grid(row=3, column=0, padx=30, pady=0)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.add_orderitems, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.add_orderitems.destroy)
        cancelBtn.grid(row=3, column=1, padx=30, pady=0)


    """ OPTIONS OF (MAIN MENU) 'REMOVE' """    
    def deleteCustomerTab(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.delete_customer = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.delete_customer.place(width=self.width/3, height=self.height/4, x=600, y=200)

        # INPUT BAR FOR 'CustomerID'
        cid_label = tk.Label(self.delete_customer, text="Customer ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        cid_label.grid(row=0, column=0, padx=20, pady=30)
        self.cid_input = tk.Entry(self.delete_customer, font=("Courier",15,"bold"), width=25)
        self.cid_input.grid(row=0, column=1, padx=5, pady=30)
        
        # ENTER BUTTON
        enterBtn = tk.Button(self.delete_customer, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.deleteCustomerFunc)
        enterBtn.grid(row=1, column=0, padx=30, pady=30)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.delete_customer, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.delete_customer.destroy)
        cancelBtn.grid(row=1, column=1, padx=30, pady=30)

        self.active_table.append(self.delete_customer)


    def deleteProductTab(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.delete_product = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.delete_product.place(width=self.width/3, height=self.height/4, x=600, y=200)

        # INPUT BAR FOR 'ProductID'
        pid_label = tk.Label(self.delete_product, text="Product ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        pid_label.grid(row=0, column=0, padx=20, pady=30)
        self.pid_input = tk.Entry(self.delete_product, font=("Courier",15,"bold"), width=25)
        self.pid_input.grid(row=0, column=1, padx=5, pady=30)
        
        # ENTER BUTTON
        enterBtn = tk.Button(self.delete_product, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.deleteProductFunc)
        enterBtn.grid(row=1, column=0, padx=30, pady=30)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.delete_product, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.delete_product.destroy)
        cancelBtn.grid(row=1, column=1, padx=30, pady=30)

        self.active_table.append(self.delete_product)


    def deleteOrderTab(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.delete_order = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.delete_order.place(width=self.width/3, height=self.height/4, x=600, y=200)

        # INPUT BAR FOR 'OrderID'
        ordid_label = tk.Label(self.delete_order, text="Order ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        ordid_label.grid(row=0, column=0, padx=20, pady=30)
        self.ordid_input = tk.Entry(self.delete_order, font=("Courier",15,"bold"), width=25)
        self.ordid_input.grid(row=0, column=1, padx=5, pady=30)
        
        # ENTER BUTTON
        enterBtn = tk.Button(self.delete_order, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.deleteOrderFunc)
        enterBtn.grid(row=1, column=0, padx=30, pady=30)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.delete_order, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.delete_order.destroy)
        cancelBtn.grid(row=1, column=1, padx=30, pady=30)

        self.active_table.append(self.delete_order)


    """ OPTIONS OF (MAIN MENU) 'SEARCH' """
    def searchCustomerTab(self):
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.search_customer = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.search_customer.place(width=self.width/3, height=self.height/4, x=600, y=200)

        # INPUT BAR TO SEARCH CUSTOMERS BY NAME
        cname_label = tk.Label(self.search_customer, text="Customer Name", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        cname_label.grid(row=0, column=0, padx=20, pady=30)
        self.cname_input = tk.Entry(self.search_customer, font=("Courier",15,"bold"), width=25)
        self.cname_input.grid(row=0, column=1, padx=5, pady=30)
        
        # ENTER BUTTON
        enterBtn = tk.Button(self.search_customer, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.searchCustomerFunc)
        enterBtn.grid(row=1, column=0, padx=30, pady=30)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.search_customer, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.search_customer.destroy)
        cancelBtn.grid(row=1, column=1, padx=30, pady=30)

        self.active_table.append(self.search_customer)


    def searchProductTab(self):
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.search_product = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.search_product.place(width=self.width/3, height=self.height/4, x=600, y=200)

        # INPUT BAR TO SEARCH PRODUCTS BY NAME
        pname_label = tk.Label(self.search_product, text="Product Name", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        pname_label.grid(row=0, column=0, padx=20, pady=30)
        self.pname_input = tk.Entry(self.search_product, font=("Courier",15,"bold"), width=25)
        self.pname_input.grid(row=0, column=1, padx=5, pady=30)
        
        # ENTER BUTTON
        enterBtn = tk.Button(self.search_product, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.searchProductFunc)
        enterBtn.grid(row=1, column=0, padx=30, pady=30)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.search_product, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.search_product.destroy)
        cancelBtn.grid(row=1, column=1, padx=30, pady=30)

        self.active_table.append(self.search_product)


    def searchOrderTab(self):
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.search_order = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.search_order.place(width=self.width/3, height=self.height/4, x=600, y=200)

        # INPUT BAR TO SEARCH ORDERS BY ID
        ordid_label = tk.Label(self.search_order, text="Order ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        ordid_label.grid(row=0, column=0, padx=20, pady=30)
        self.ordid_input = tk.Entry(self.search_order, font=("Courier",15,"bold"), width=25)
        self.ordid_input.grid(row=0, column=1, padx=5, pady=30)
        
        # ENTER BUTTON
        enterBtn = tk.Button(self.search_order, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.searchOrderFunc)
        enterBtn.grid(row=1, column=0, padx=30, pady=30)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.search_order, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.search_order.destroy)
        cancelBtn.grid(row=1, column=1, padx=30, pady=30)

        self.active_table.append(self.search_order)


    def searchCusOrdersTab(self):
        # CLOSE THE PREVIOUS TAB
        self.curr_data = None
        self.__closeTable()

        # INITIALIZE QUERY FRAME
        self.search_cus_ords = tk.Frame(self.root, bd=3, relief="ridge", bg="#629FFA")
        self.search_cus_ords.place(width=self.width/3, height=self.height/4, x=600, y=200)

        # INPUT BAR TO SEARCH ORDERS BY CUSTOMER ID
        cid_label = tk.Label(self.search_cus_ords, text="Customer ID", fg="black", bg="#629FFA", font=("Courier",15,"bold"))
        cid_label.grid(row=0, column=0, padx=20, pady=30)
        self.cid_input = tk.Entry(self.search_cus_ords, font=("Courier",15,"bold"), width=25)
        self.cid_input.grid(row=0, column=1, padx=5, pady=30)
        
        # ENTER BUTTON
        enterBtn = tk.Button(self.search_cus_ords, text="Enter", bd=3, relief="raised", width=10, font=("Courier",15,"bold"), 
                             command=self.searchCusOrdersFunc)
        enterBtn.grid(row=1, column=0, padx=30, pady=30)

        # CANCEL BUTTON
        cancelBtn = tk.Button(self.search_cus_ords, text="Cancel", bd=3, relief="raised", width=10, font=("Courier",15,"bold"),
                              command=self.search_cus_ords.destroy)
        cancelBtn.grid(row=1, column=1, padx=30, pady=30)

        self.active_table.append(self.search_cus_ords)


    """ FUNCTIONS OF (MAIN MENU) 'ADD' """
    def addCustomerFunc(self):
        # GET INPUTS FROM INPUT BARS
        cid = self.cid_input.get()
        cname = self.cname_input.get()

        if cid and cname: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(cid) != 8: raise TypeError
                if cid[0] != "C": raise KeyError
                
                try: int(cid[1:])
                except: raise KeyError

                # Add new customer if valid
                self.dbConnect()
                self.cur.execute("CALL add_customer(%s, %s);", (cid, cname))
                self.connect_db.commit()
                messagebox.showinfo("Success!", f"Customer {cname} with ID {cid} is Added")
                self.connect_db.close()

            except TypeError:
                messagebox.showerror("Error", "Customer ID Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First Character Is Always 'C' & The Remainings Are Numbers !")
            except:
                messagebox.showerror("Error", "This Customer Is Already Existed !")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    def addProductFunc(self):
        # GET INPUTS FROM INPUT BARS
        pid = self.pid_input.get()
        pname = self.pname_input.get()
        price = self.price_input.get()

        if pid and pname and price: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(pid) != 8: raise IndexError
                if pid[0] != "P": raise KeyError
                
                try: int(pid[1:])
                except: raise KeyError
                try: float(price)
                except: raise TabError

                if float(price) <= 0: raise TabError

                # Add new product if valid
                self.dbConnect()
                self.cur.execute("CALL add_product(%s, %s, %s);", (pid, pname, price))
                self.connect_db.commit()
                messagebox.showinfo("Success!", f"Product '{pname}' with ID {pid} is Added")
                self.connect_db.close()

            except IndexError:
                messagebox.showerror("Error", "Product ID Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First Character Is Always 'P' & The Remainings Are Numbers !")
            except TabError:
                messagebox.showerror("Wrong Format", "Price Must Be DECIMAL(10,2) and Positive !")
            except:
                messagebox.showerror("Error", "This Product Is Already Existed !")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    def addOrderFunc(self):
        # GET INPUTS FROM INPUT BARS
        ordid = self.ordid_input.get()
        cid = self.cid_input.get()

        if ordid and cid: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(ordid) != 8 or len(cid) != 8: raise IndexError
                if ordid[0] != "O" or cid[0] != "C": raise KeyError
                
                try: int(ordid[1:]); int(cid[1:])
                except: raise KeyError

                # Add new order if valid
                self.dbConnect()
                self.cur.execute("CALL add_order(%s, %s);", (ordid, cid))
                self.connect_db.commit()
                messagebox.showinfo("Success!", f"New Order {ordid} of Customer ID {cid} is Added")
                self.add_order.destroy()

            except IndexError:
                messagebox.showerror("Error", "IDs Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First Character Is Always 'O' or 'C' & The Remainings Are Numbers !")
            except:
                messagebox.showerror("Error", "This Order Is Already Existed !")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    def addOrderitemsFunc(self):
        # GET INPUTS FROM INPUT BARS
        ordid = self.ordid_input.get()
        pid = self.pid_input.get()
        qty = self.qty_input.get()

        if ordid and pid and qty: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(pid) != 8 or len(ordid) != 8: raise IndexError
                if pid[0] != "P" or ordid[0] != "O": raise KeyError
                
                try: int(pid[1:]); int(ordid[1:])
                except: raise KeyError
                try: int(qty)
                except: raise TabError

                if int(qty) <= 0: raise TabError

                # Add a product to the order if valid
                self.dbConnect()
                self.cur.execute("CALL add_orderitem(%s, %s, %s);", (ordid, pid, qty))
                self.connect_db.commit()
                messagebox.showinfo("Success!", f"Order {ordid} is Added x{qty} Product {pid} !")
                self.connect_db.close()

            except IndexError:
                messagebox.showerror("Error", "IDs Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First Character Is Always 'O' and 'P' & The Remainings Are Numbers !")
            except TabError:
                messagebox.showerror("Wrong Format", "Quantity Is An Positive Integer !")
            except:
                messagebox.showerror("Error", "Unavailable IDs or The Product Is Included")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    """ FUNCTION OF (MAIN MENU) 'REMOVE' """
    def deleteCustomerFunc(self):
        # GET INPUTS FROM INPUT BARS
        cid = self.cid_input.get()

        if cid: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(cid) != 8: raise TypeError
                if cid[0] != "C": raise KeyError
                
                try: int(cid[1:])
                except: raise KeyError

                # Remove a customer if valid
                self.dbConnect()
                self.cur.execute("CALL delete_customer(%s);", (cid))
                self.connect_db.commit()
                messagebox.showinfo("Success!", f"Customer with ID {cid} is Removed !")
                self.connect_db.close()
                self.delete_customer.destroy()

            except TypeError:
                messagebox.showerror("Error", "Customer ID Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First Character Is Always 'C' & The Remainings Are Numbers !")
            except:
                messagebox.showerror("Error", "Unavailable Customer !")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    def deleteProductFunc(self):
        # GET INPUTS FROM INPUT BARS
        pid = self.pid_input.get()

        if pid: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(pid) != 8: raise TypeError
                if pid[0] != "P": raise KeyError
                
                try: int(pid[1:])
                except: raise KeyError

                # Remove a product if valid
                self.dbConnect()
                self.cur.execute("CALL delete_product(%s);", (pid))
                self.connect_db.commit()
                messagebox.showinfo("Success!", f"Product with ID {pid} is Removed !")
                self.connect_db.close()
                self.delete_product.destroy()

            except TypeError:
                messagebox.showerror("Error", "Product ID Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First Character Is Always 'P' & The Remainings Are Numbers !")
            except:
                messagebox.showerror("Error", "Unavailable Product !")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    def deleteOrderFunc(self):
        # GET INPUTS FROM INPUT BARS
        ordid = self.ordid_input.get()

        if ordid: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(ordid) != 8: raise TypeError
                if ordid[0] != "O": raise KeyError
                
                try: int(ordid[1:])
                except: raise KeyError

                # Remove a product if valid
                self.dbConnect()
                self.cur.execute("CALL delete_order(%s);", (ordid))
                self.connect_db.commit()
                messagebox.showinfo("Success!", f"Order with ID {ordid} is Removed !")
                self.connect_db.close()
                self.delete_product.destroy()

            except TypeError:
                messagebox.showerror("Error", "Order ID Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First Character Is Always 'O' & The Remainings Are Numbers !")
            except:
                messagebox.showerror("Error", "Unavailable Order !")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    """ FUNCIONS OF (MAIN MENU) 'SEARCH' """
    def searchCustomerFunc(self):
        # GET INPUTS FROM INPUT BARS
        cname = self.cname_input.get()

        if cname: # Inputs are non-empty
            # CLOSE THE PREVIOUS TAB
            self.__closeTable()

            # INITIALIZE FRAME
            self.sch_customer_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
            self.sch_customer_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

            # SLIDE BARS
            x_scroll = tk.Scrollbar(self.sch_customer_frame, orient="horizontal", width=15)
            x_scroll.pack(side="bottom", fill="x")
            y_scroll = tk.Scrollbar(self.sch_customer_frame, orient="vertical", width=15)
            y_scroll.pack(side="right", fill="y")

            # INITIALIZE TABLE
            sch_customer_table = ttk.Treeview(self.sch_customer_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                            columns=("CustomerID", "CustomerName"))
            x_scroll.config(command=sch_customer_table.xview)
            y_scroll.config(command=sch_customer_table.yview)
            sch_customer_table.pack(fill="both", expand=1)
            sch_customer_table.heading("CustomerID", text="Customer ID")
            sch_customer_table.heading("CustomerName", text="Customer Name")
            sch_customer_table["show"] = "headings"

            # ADD TO ACTIVE TABLE
            self.active_table.append(self.sch_customer_frame)

            # CONNECTING TO DATABASE AND FETCHING ROWS
            self.dbConnect()
            self.cur.execute("CALL search_customer(%s);", (cname))
            rows = self.cur.fetchall()
            self.connect_db.close()

            for row in rows:
                sch_customer_table.insert("", "end", values=row)

            self.search_customer.destroy()


        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    def searchProductFunc(self):
        # GET INPUTS FROM INPUT BARS
        pname = self.pname_input.get()

        if pname: # Inputs are non-empty
            # CLOSE THE PREVIOUS TAB
            self.__closeTable()

            # INITIALIZE FRAME
            self.sch_product_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
            self.sch_product_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

            # SLIDE BARS
            x_scroll = tk.Scrollbar(self.sch_product_frame, orient="horizontal", width=15)
            x_scroll.pack(side="bottom", fill="x")
            y_scroll = tk.Scrollbar(self.sch_product_frame, orient="vertical", width=15)
            y_scroll.pack(side="right", fill="y")

            # INITIALIZE TABLE
            sch_product_table = ttk.Treeview(self.sch_product_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                            columns=("ProductID", "ProductName", "Price"))
            x_scroll.config(command=sch_product_table.xview)
            y_scroll.config(command=sch_product_table.yview)
            sch_product_table.pack(fill="both", expand=1)
            sch_product_table.heading("ProductID", text="Product ID")
            sch_product_table.heading("ProductName", text="Product Name")
            sch_product_table.heading("Price", text="Price")
            sch_product_table["show"] = "headings"

            # ADD TO ACTIVE TABLE
            self.active_table.append(self.sch_product_frame)

            # CONNECTING TO DATABASE AND FETCHING ROWS
            self.dbConnect()
            self.cur.execute("CALL search_product(%s);", (pname))
            rows = self.cur.fetchall()
            self.connect_db.close()

            for row in rows:
                sch_product_table.insert("", "end", values=row)

            self.search_product.destroy()


        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    def searchOrderFunc(self):
        # GET INPUTS FROM INPUT BARS
        ordid = self.ordid_input.get()

        if ordid: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(ordid) != 8: raise IndexError
                if ordid[0] != "O": raise KeyError
                
                try: int(ordid[1:])
                except: raise KeyError

                # CLOSE THE PREVIOUS TAB
                self.__closeTable()

                # INITIALIZE FRAME
                self.sch_order_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
                self.sch_order_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

                # SLIDE BARS
                x_scroll = tk.Scrollbar(self.sch_order_frame, orient="horizontal", width=15)
                x_scroll.pack(side="bottom", fill="x")
                y_scroll = tk.Scrollbar(self.sch_order_frame, orient="vertical", width=15)
                y_scroll.pack(side="right", fill="y")

                # INITIALIZE TABLE
                sch_order_table = ttk.Treeview(self.sch_order_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                                columns=("OrderID", "CustomerID", "ProductID", "ProductName", "unit_price", "Quantity", "Status"))
                x_scroll.config(command=sch_order_table.xview)
                y_scroll.config(command=sch_order_table.yview)
                sch_order_table.pack(fill="both", expand=1)
                sch_order_table.heading("OrderID", text="Order ID")
                sch_order_table.heading("CustomerID", text="Ordered by")
                sch_order_table.heading("ProductName", text="Product Name")
                sch_order_table.heading("unit_price", text="Unit Price")
                sch_order_table.heading("Quantity", text="Quantity")
                sch_order_table.heading("Status", text="Status")
                sch_order_table["show"] = "headings"

                # ADD TO ACTIVE TABLE
                self.active_table.append(self.sch_order_frame)

                # CONNECTING TO DATABASE AND FETCHING ROWS
                self.dbConnect()
                self.cur.execute("CALL search_orderdetail(%s);", (ordid))
                rows = self.cur.fetchall()
                self.connect_db.close()

                for row in rows:
                    sch_order_table.insert("", "end", values=row)

                self.search_order.destroy()

            except IndexError:
                messagebox.showerror("Error", "IDs Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First Character Is Always 'O' & The Remainings Are Numbers !")
            except:
                messagebox.showerror("Error", "This Order Does not Exist !")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    def searchCusOrdersFunc(self):
        # GET INPUTS FROM INPUT BARS
        cid = self.cid_input.get()

        if cid: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(cid) != 8: raise IndexError
                if cid[0] != "C": raise KeyError
                
                try: int(cid[1:])
                except: raise KeyError
                # CLOSE THE PREVIOUS TAB
                self.__closeTable()

                # INITIALIZE FRAME
                self.sch_cus_ords_frame = tk.Frame(self.det_frame, bd=4, relief="sunken", bg="#4dc3ff")
                self.sch_cus_ords_frame.place(width=self.width/1.6, height=self.height/1.45, x=20, y=45)

                # SLIDE BARS
                x_scroll = tk.Scrollbar(self.sch_cus_ords_frame, orient="horizontal", width=15)
                x_scroll.pack(side="bottom", fill="x")
                y_scroll = tk.Scrollbar(self.sch_cus_ords_frame, orient="vertical", width=15)
                y_scroll.pack(side="right", fill="y")

                # INITIALIZE TABLE
                sch_cus_ords_table = ttk.Treeview(self.sch_cus_ords_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                                                columns=("CustomerID", "CustomerName", "OrderID", "OrderDate", "Status"))
                x_scroll.config(command=sch_cus_ords_table.xview)
                y_scroll.config(command=sch_cus_ords_table.yview)
                sch_cus_ords_table.pack(fill="both", expand=1)
                sch_cus_ords_table.heading("OrderID", text="Order ID")
                sch_cus_ords_table.heading("CustomerID", text="Customer ID")
                sch_cus_ords_table.heading("CustomerName", text="Customer Name")
                sch_cus_ords_table.heading("OrderDate", text="Order Date")
                sch_cus_ords_table.heading("Status", text="Status")
                sch_cus_ords_table["show"] = "headings"

                # ADD TO ACTIVE TABLE
                self.active_table.append(self.sch_cus_ords_frame)

                # CONNECTING TO DATABASE AND FETCHING ROWS
                self.dbConnect()
                self.cur.execute("CALL search_customer_orders(%s);", (cid))
                rows = self.cur.fetchall()
                self.connect_db.close()

                for row in rows:
                    sch_cus_ords_table.insert("", "end", values=row)

                self.search_cus_ords.destroy()

            except IndexError:
                messagebox.showerror("Error", "IDs Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First Character Is Always 'C' & The Remainings Are Numbers !")
            except:
                messagebox.showerror("Error", "This Customer Does not Exist !")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    """ FUNCTION OF (MAIN MENU) 'REMOVE' """
    def updateProductFunc(self):
        # GET INPUTS FROM INPUT BARS
        pid = self.pid_input.get()
        price = self.price_input.get()

        if pid and price: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(pid) != 8: raise IndexError
                if pid[0] != "P": raise KeyError
                
                try: int(pid[1:])
                except: raise KeyError
                try: float(price)
                except: raise TabError

                # Update new product's price if valid
                self.dbConnect()
                self.cur.execute("CALL update_price(%s, %s);", (pid, price))
                self.connect_db.commit()
                messagebox.showinfo("Success!", f"The New price of Product with ID {pid} is Updated !")
                self.connect_db.close()

            except IndexError:
                messagebox.showerror("Error", "Product ID Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First Character Is Always 'P' & The Remainings Are Numbers !")
            except TabError:
                messagebox.showerror("Wrong Format", "Price Must Be DECIMAL(10,2) Data Type !")
            except:
                messagebox.showerror("Error", "This Product Is Already Existed !")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


    def updateStatusFunc(self):
        # GET INPUTS FROM INPUT BARS
        ordid = self.ordid_input.get()
        sts = (self.sts_input.get()).lower()

        if ordid and sts: # Inputs are non-empty
            try:
                # Validate inputs format
                if len(ordid) != 8: raise IndexError
                if ordid[0] != "O": raise KeyError

                try: int(ordid[1:])
                except: raise KeyError

                if sts not in ["pending", "processing", "shipped", "delivered"]:
                    raise BufferError

                # Update new status query if valid
                self.dbConnect()
                self.cur.execute("CALL update_status(%s, %s);", (ordid, sts))
                self.connect_db.commit()
                messagebox.showinfo("Success!", f"New Status of Order with ID {ordid} is Updated to '{sts}'")
                self.connect_db.close()

            except IndexError:
                messagebox.showerror("Error", "IDs Length Must Be 8 Characters !")
            except KeyError:
                messagebox.showerror("Wrong Format", "The First ID Character Is Always 'O' & The Remainings Are Numbers !")
            except BufferError:
                messagebox.showerror("Wrong Format", "The Status Must Be 'pending', 'processing', 'shipped' or 'delivered' !")
            except:
                messagebox.showerror("Error", "This Order Does Not Exist !")
        else:
            messagebox.showerror("Error", "Information Must Not Be Empty !")


class ExecuteEcommerce:
    def __init__(self):
        self.root = tk.Tk()
        self.obj = _Ecommerce(self.root)
        self.root.mainloop()