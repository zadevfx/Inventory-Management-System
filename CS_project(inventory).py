import mysql.connector
#password and database spaces are blank as you need to put in your own password and database name
def connect():
    con = mysql.connector.connect(host = "localhost",user = "root",password = "",database = "")
    return con

def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    con = connect()
    cur = con.cursor()
    q1 = "INSERT INTO products(product_name, price) VALUES ('{}', {})".format(name, price)
    cur.execute(q1)
    pid = cur.lastrowid
    q2 = "INSERT INTO stock(product_id, quantity) VALUES ({}, {})".format(pid, 0)
    cur.execute(q2)
    con.commit()
    con.close()
    print("Product added successfully.\n")

def purchase():
    product_id = int(input("Enter product ID: "))
    qty = int(input("Enter quantity purchased: "))
    cost = float(input("Enter cost per item: "))
    total = qty * cost
    con = connect()
    cur = con.cursor()
    q1 = "INSERT INTO purchases(product_id, quantity, total_cost) VALUES ({}, {}, {})".format(product_id,
                                                                                              qty, total)
    cur.execute(q1)
    q2 = "UPDATE stock SET quantity = quantity + {} WHERE product_id = {}".format(qty, product_id)
    cur.execute(q2)
    con.commit()
    con.close()
    print("Purchase recorded and stock updated.\n")

def sale():
    product_id = int(input("Enter product ID: "))
    qty = int(input("Enter quantity sold: "))
    con = connect()
    cur = con.cursor()
    q1 = "SELECT price FROM products WHERE product_id = {}".format(product_id)
    cur.execute(q1)
    price_row = cur.fetchone()
    if not price_row:
        print("Invalid Product ID!\n")
        return
    price = price_row[0]
    q2 = "SELECT quantity FROM stock WHERE product_id = {}".format(product_id)
    cur.execute(q2)
    stock_row = cur.fetchone()
    if stock_row is None:
        print("No stock entry found!\n")
        return
    stock_qty = stock_row[0]
    if qty > stock_qty:
        print("Not enough stock!\n")
        return
    total_amount = qty * price
    q3 = "INSERT INTO sales(product_id, quantity, total_amount) VALUES ({}, {}, {})".format(
        product_id, qty, total_amount)
    cur.execute(q3)
    q4 = "UPDATE stock SET quantity = quantity - {} WHERE product_id = {}".format(qty, product_id)
    cur.execute(q4)
    con.commit()
    con.close()
    print("Sale recorded.\n")
    
def view_inventory():
    con = connect()
    cur = con.cursor()
    query = """
    SELECT p.product_id, p.product_name, p.price, s.quantity 
    FROM products p, stock s 
    WHERE p.product_id = s.product_id
    """
    cur.execute(query)
    rows = cur.fetchall()
    print("----- INVENTORY LIST -----")
    for r in rows:
        print("ID:", r[0], "| Name:", r[1], "| Price:", r[2], "| Stock:", r[3])
    print("---------------------------")
    con.close()

while True:
    print("===== INVENTORY MENU =====")
    print("1. Add Product")
    print("2. Purchase (Add Stock)")
    print("3. Sale (Reduce Stock)")
    print("4. View Inventory")
    print("5. Exit")
    print("==========================")
    choice = input("Enter choice: ")
    if choice == '1':
        add_product()
    elif choice == '2':
        purchase()
    elif choice == '3':
        sale()
    elif choice == '4':
        view_inventory()
    elif choice == '5':
        print("Exiting Program...")
        break
    else:
        print("Invalid choice!")


