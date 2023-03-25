import tkinter as tk
import tkinter.messagebox
import mysql.connector

# Establish database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cp363"
)

# Create a cursor to interact with the database
cursor = db.cursor()

# Create the GUI
class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Ecommerce Database Manager") 
        # Create button to drop tables from database
        self.drop_button = tk.Button(master, text="Drop Tables", command=self.drop_tables)
        self.drop_button.pack()
        
        #create button to add tables to database
        self.insert_button = tk.Button(master, text="Add Tables", command=self.add_tables)
        self.insert_button.pack()
       
        #create button to populate tables to database
        self.populate_button = tk.Button(master, text="Populate Tables", command=self.add_tables)
        self.populate_button.pack()
        
        # Create label to display tables
        self.tables_label = tk.Label(master, text="Tables:")
        self.tables_label.pack()
        # Display tables
        self.display_tables()
        
        # Create textbox for SQL query
        self.query_label = tk.Label(root, text="Enter Query Here:")
        self.query_label.pack()
        self.query_textbox = tk.Text(self.master)
        self.query_textbox.pack()
        # Create button to execute query
        self.execute_button = tk.Button(self.master, text="Execute", command=self.execute_query)
        self.execute_button.pack()
        
     
        
        # Create the result_textbox
        self.result_label = tk.Label(root, text="Result:")
        self.result_label.pack()
        self.result_textbox = tk.Text(root, height=10, width=50)
        self.result_textbox.pack()
        
        #exit button
        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.pack()
        
    
    
    def drop_tables(self):
        # Execute SQL query to drop tables
        for command in drop_table_commands:
            cursor.execute(command)
        # Commit changes to database
        db.commit()
        
        # Display confirmation message
        tk.messagebox.showinfo("Tables dropped", "The tables have been dropped successfully.")
        
        #update tables list
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        # Delete all items in the current Listbox
        self.tables_list.delete(0, tk.END)

        # Insert the new tables into the Listbox
        for table in tables:
            self.tables_list.insert(tk.END, table[0])
        

        
    def display_tables(self):
        # Execute SQL query to get tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        # Create label to display tables
        tables_string = "\n".join([table[0] for table in tables])
        self.tables_value = tk.StringVar(value=tables_string)
        self.tables_list = tk.Listbox(self.master, listvariable=self.tables_value)
        self.tables_list.pack()
    
    def exit_app(self):
        root.destroy() # Close the main window

 
    def add_tables(self):
        for command in add_table_commands:
            cursor.execute(command)
        db.commit()
        # Display confirmation message
        tk.messagebox.showinfo("Tables added", "The tables have been added successfully.")

        #update tables list
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        # Delete all items in the current Listbox
        self.tables_list.delete(0, tk.END)
        # Insert the new tables into the Listbox
        for table in tables:
            self.tables_list.insert(tk.END, table[0])
        
    def execute_query(self):
        # Get SQL query from textbox
        query = self.query_textbox.get("1.0", "end-1c")
        
        try:
            # Execute SQL query
            cursor.execute(query)
            results = cursor.fetchall()
            
            
            # Display the result in the result_textbox
            self.result_textbox.delete("1.0", tk.END)
            for row in results:
                self.result_textbox.insert(tk.END, str(row) + "\n")
                # Commit changes
                db.commit()
            
        except Exception as e:
            print("Error executing query:", e)

        



add_table_commands = [
"CREATE TABLE Merchandise (Merchandise_ID int PRIMARY KEY NOT NULL, ProductName varchar(255) NOT NULL, Category varchar(255) NOT NULL, Pet varchar(255) NULL, Gender ENUM ('Male', 'Female', 'Other') NOT NULL, Size ENUM ('XS', 'S', 'M', 'L', 'XL') NOT NULL, Discount_Price double, Retail_Price double NOT NULL)",
"CREATE TABLE Staff (Staff_ID int PRIMARY KEY NOT NULL, Staff_First_Name varchar(255) NOT NULL, Staff_Last_Name varchar(255) NOT NULL, Staff_Phone_Number char(10) NOT NULL, Staff_Email varchar(255) NOT NULL)",
"CREATE TABLE Store (Store_ID int PRIMARY KEY NOT NULL, Store_Address varchar(255) NOT NULL, Store_Phone_Number char(10) NOT NULL, Manager_ID int NOT NULL, FOREIGN KEY (Manager_ID) REFERENCES Staff(Staff_ID))",
"CREATE TABLE WarehouseCart(WarehouseCart_ID int PRIMARY KEY NOT NULL, Store_ID int NOT NULL, FOREIGN KEY (Store_ID) REFERENCES Store(Store_ID))",
"ALTER TABLE Store ADD (WarehouseCart_ID int NULL, FOREIGN KEY (WarehouseCart_ID) REFERENCES WarehouseCart(WarehouseCart_ID))",
"CREATE TABLE WarehouseItem(WarehouseItem_ID int PRIMARY KEY NOT NULL, WarehouseCart_ID int NOT NULL, Merchandise_ID int NOT NULL, Quantity int NOT NULL, FOREIGN KEY (WarehouseCart_ID) REFERENCES WarehouseCart(WarehouseCart_ID), FOREIGN KEY (Merchandise_ID) REFERENCES Merchandise(Merchandise_ID))",
"ALTER TABLE Staff ADD (Store_ID int DEFAULT NULL, FOREIGN KEY (Store_ID) REFERENCES Store(Store_ID))",
"CREATE TABLE Customer(Customer_ID int PRIMARY KEY NOT NULL, First_Name varchar(255) NOT NULL, Last_Name varchar(255) NOT NULL, Email varchar(255) NULL, Mailing_Status BIT NOT NULL DEFAULT 0, Customer_Address varchar(255) NULL, Reward_Points int NOT NULL DEFAULT 0, Password_Hash char(128) NOT NULL, Customer_Cart int NULL)",
"CREATE TABLE Cart (Cart_ID int PRIMARY KEY NOT NULL, Customer_ID int NOT NULL, FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID))",
"CREATE TABLE CartItem (CartItem_ID int PRIMARY KEY NOT NULL, Cart_ID int NOT NULL, Merchandise_ID int NOT NULL, Quantity int NOT NULL DEFAULT 1, FOREIGN KEY (Cart_ID) REFERENCES Cart(Cart_ID), FOREIGN KEY (Merchandise_ID) REFERENCES Merchandise(Merchandise_ID))",
"ALTER TABLE Customer ADD (FOREIGN KEY (Customer_Cart) REFERENCES Cart(Cart_ID))",
"CREATE TABLE Inventory(Inventory_ID int PRIMARY KEY NOT NULL, Merchandise_ID int NOT NULL, Store_ID int NOT NULL, Quantity int NOT NULL DEFAULT 0, FOREIGN KEY (Store_ID) REFERENCES Store(Store_ID), FOREIGN KEY (Merchandise_ID) REFERENCES Merchandise(Merchandise_ID))",
"CREATE TABLE Transactions(Transaction_ID int PRIMARY KEY NOT NULL, TransactionDate datetime NOT NULL, Category ENUM ('Customer', 'Warehouse', 'Other'), Notes varchar(255) NULL, Store_ID int NOT NULL, FOREIGN KEY (Store_ID) REFERENCES Store(Store_ID))",
"CREATE TABLE TransactionItem(TransactionItem_ID int PRIMARY KEY NOT NULL, Transaction_ID int NOT NULL, Merchandise_ID int NOT NULL, Quantity int NOT NULL, FOREIGN KEY (Transaction_ID) REFERENCES Transactions(Transaction_ID), FOREIGN KEY (Merchandise_ID) REFERENCES Merchandise(Merchandise_ID))",
"CREATE TABLE CustomerShipment(CustomerShipment_ID int PRIMARY KEY NOT NULL, Customer_ID int NOT NULL, Transaction_ID int NOT NULL, FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID), FOREIGN KEY (Transaction_ID) REFERENCES Transactions(Transaction_ID))",
"CREATE TABLE WarehouseOrder(WarehouseOrder_ID int PRIMARY KEY NOT NULL, WarehouseCart_ID int NOT NULL, Transaction_ID int NOT NULL, FOREIGN KEY (WarehouseCart_ID) REFERENCES WarehouseCart(WarehouseCart_ID), FOREIGN KEY (Transaction_ID) REFERENCES Transactions(Transaction_ID))",
]

drop_table_commands = [
    "ALTER TABLE cp363.cart DROP FOREIGN KEY cart_ibfk_1;",
    "ALTER TABLE cp363.cartitem DROP FOREIGN KEY cartitem_ibfk_1;",
    "ALTER TABLE cp363.cartitem DROP FOREIGN KEY cartitem_ibfk_2;",
    "ALTER TABLE cp363.customer DROP FOREIGN KEY customer_ibfk_1;",
    "ALTER TABLE cp363.customershipment DROP FOREIGN KEY customershipment_ibfk_1;",
    "ALTER TABLE cp363.customershipment DROP FOREIGN KEY customershipment_ibfk_2;",
    "ALTER TABLE cp363.inventory DROP FOREIGN KEY inventory_ibfk_1;",
    "ALTER TABLE cp363.inventory DROP FOREIGN KEY inventory_ibfk_2;",
    "ALTER TABLE cp363.staff DROP FOREIGN KEY staff_ibfk_1;",
    "ALTER TABLE cp363.store DROP FOREIGN KEY store_ibfk_1;",
    "ALTER TABLE cp363.store DROP FOREIGN KEY store_ibfk_2;",
    "ALTER TABLE cp363.transactionitem DROP FOREIGN KEY transactionitem_ibfk_1;",
    "ALTER TABLE cp363.transactionitem DROP FOREIGN KEY transactionitem_ibfk_2;",
    "ALTER TABLE cp363.transactions DROP FOREIGN KEY transactions_ibfk_1;",
    "ALTER TABLE cp363.warehousecart DROP FOREIGN KEY warehousecart_ibfk_1;",
    "ALTER TABLE cp363.warehouseitem DROP FOREIGN KEY warehouseitem_ibfk_1;",
    "ALTER TABLE cp363.warehouseitem DROP FOREIGN KEY warehouseitem_ibfk_2;",
    "ALTER TABLE cp363.warehouseorder DROP FOREIGN KEY warehouseorder_ibfk_1;",
    "ALTER TABLE cp363.warehouseorder DROP FOREIGN KEY warehouseorder_ibfk_2;",
    "DROP TABLE Cart;",
    "DROP TABLE CartItem;",
    "DROP TABLE Customer;",
    "DROP TABLE CustomerShipment;",
    "DROP TABLE Inventory;",
    "DROP TABLE Merchandise;",
    "DROP TABLE Staff;",
    "DROP TABLE Store;",
    "DROP TABLE TransactionItem;",
    "DROP TABLE Transactions;",
    "DROP TABLE WarehouseCart;",
    "DROP TABLE WarehouseItem;",
    "DROP TABLE WarehouseOrder;",
    ]


# Run the GUI
root = tk.Tk()
my_gui = MyGUI(root)
root.mainloop()

