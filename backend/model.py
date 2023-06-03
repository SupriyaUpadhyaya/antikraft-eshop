import sqlite3


def get_db_connection():
    conn = sqlite3.connect('antiqkraft-database.db', isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn.cursor()


def readOperationCategory(TABLE_NAME: str, CAT_ID: int):
    conn = get_db_connection()
    query = "SELECT * from " + TABLE_NAME + " where category_id=" + str(CAT_ID)
    
    data = conn.execute(query)

    category_row = {}
    for row in data:
        category_row['category_id'] = row["category_id"]
        category_row['category_name'] = row["category_name"]
    if category_row is not None:
        return category_row


def readOperationCategoryImages(TABLE_NAME: str, CAT_ID: int):
    conn = get_db_connection()
    query = "SELECT * from " + TABLE_NAME + " where category_id=" + str(CAT_ID)
    
    data = conn.execute(query)

    keyList = ["category_id", "sub_category_id", "sub_category_name", "sub_category_image_id"]
    sub_category_row = {key: [] for key in keyList}

    for row in data:
        sub_category_row['category_id'].append(row["category_id"])
        sub_category_row['sub_category_id'].append(row["sub_category_id"])
        sub_category_row['sub_category_name'].append(row["sub_category_name"])
        sub_category_row['sub_category_image_id'].append(row["sub_category_image_id"])

    if sub_category_row is not None:
        return sub_category_row


def readOperation(TABLE_NAME: str, COLS: str):
    conn = get_db_connection()
    query = "SELECT * from " + TABLE_NAME
    data = conn.execute(query)
    categories = {}
    for row in data:
        url = "http://127.0.0.1:5000/category?categoryid=" + str(row["category_id"])
        categories[url] = row["category_name"]
    if categories is not None:
        return categories

def readOperationSubCategory(TABLE_NAME: str, CAT_ID: int, SUB_CAT_ID: int):
    conn = get_db_connection()
    query = "SELECT * from " + TABLE_NAME + " where category_id=" + str(CAT_ID) + " and sub_category_id=" + str(SUB_CAT_ID)
    
    data = conn.execute(query)
  
    keyList = ["category_id", "sub_category_id", "product_id", "product_name", "product_price", "product_description", "image_id", "url"]
    sub_category_row = {key: [] for key in keyList}

    for row in data:
        url = "http://127.0.0.1:5000/subcategory?categoryid=" + str(row["category_id"]) + "&subcategoryid=" + str(row["sub_category_id"])
        sub_category_row['category_id'].append(row["category_id"])
        sub_category_row['sub_category_id'].append(row["sub_category_id"])
        sub_category_row['product_id'].append(row["product_id"])
        sub_category_row['product_name'].append(row["product_name"])
        sub_category_row['product_description'].append(row["product_description"])
        sub_category_row['product_price'].append(row["product_price"])
        sub_category_row['image_id'].append(row["image_id"])
        sub_category_row['url'].append(url)
    
    if sub_category_row is not None:
        return sub_category_row

def readOperationProduct(TABLE_NAME: str, CAT_ID: int, SUB_CAT_ID: int, PRODUCT_ID:int):
    conn = get_db_connection()
    query = "SELECT * from " + TABLE_NAME + " where category_id=" + str(CAT_ID) + " and sub_category_id=" + str(SUB_CAT_ID) + " and product_id=" + str(PRODUCT_ID)
    
    data = conn.execute(query)
  
    keyList = ["category_id", "sub_category_id", "product_id", "product_name", "product_description", "product_price", "seller_id", "stock", 
               "posted_date", "offer_flag", "offer_percent", "product_serial_number", "image_id", "secondary_images", "url"]
    product_row = {key: [] for key in keyList}

    for row in data:
        url = "http://127.0.0.1:5000/product?categoryid=" + str(row["category_id"]) + "&subcategoryid=" + str(row["sub_category_id"]) + "&productid=" + str(row["product_id"])
        product_row['category_id'].append(row["category_id"])
        product_row['sub_category_id'].append(row["sub_category_id"])
        product_row['product_id'].append(row["product_id"])
        product_row['product_name'].append(row["product_name"])
        product_row['product_description'].append(row["product_description"])
        product_row['product_price'].append(row["product_price"])
        product_row['seller_id'].append(row["seller_id"])
        product_row['stock'].append(row["stock"])
        product_row['posted_date'].append(row["posted_date"])
        product_row['offer_flag'].append(row["offer_flag"])
        product_row['offer_percent'].append(row["offer_percent"])
        product_row['product_serial_number'].append(row["product_serial_number"])
        product_row['image_id'].append(row["image_id"])
        product_row['secondary_images'].append(row["secondary_images"])
        product_row['url'].append(url)

    if product_row is not None:
        return product_row

def searchProductList(query):
    conn = get_db_connection()
    sqlquery = "SELECT * from PRODUCT where product_description LIKE '%" + str(query) + "%' OR product_name LIKE '%" + str(query) + "%'"
    data = conn.execute(sqlquery)
    return data


def readUserAccount(username):
    conn = get_db_connection()
    print(username)
    sqlquery = "SELECT * from USER where user_email='" + username + "'"
    data = conn.execute(sqlquery)
    return data


def readSellerAccount(username):
    conn = get_db_connection()
    print(username)
    sqlquery = "SELECT * from SELLER where seller_email='" + username + "'"
    data = conn.execute(sqlquery)
    return data


def insertUserAccount(salutation, firstname, lastname, email, password, phonenumber):
    conn = get_db_connection()
    sqlquery = "INSERT INTO USER (user_firstname, user_lastname, user_salutation, user_email, user_password, user_phone ) VALUES (?, ?, ?, ?, ?, ?)"
    print(sqlquery)
    try:
        conn.execute(sqlquery, (firstname, lastname, salutation, email, password, phonenumber ))
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
        print(error)
        status = "False"
    return status


def insertSellerAccount(sellername, email, password, address):
    conn = get_db_connection()
    sqlquery = "INSERT INTO SELLER (seller_name, seller_email, seller_password, seller_address ) VALUES (?, ?, ?, ?)"
    print(sqlquery)
    try:
        conn.execute(sqlquery, (sellername, email, password, address ))
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
        print(error)
        status = "False"
    return status


def addItemToNewOrder(userid, productid, selling_price, quantity):
    conn = get_db_connection()
    sqlquery = "INSERT INTO ORDER (order_id, user_id, quantity, selling_price, order_status, product_serial_number) VALUES (?, ?, ?, ?, ?)"
    try:
        order_id = 1
        conn.execute(sqlquery, (order_id, userid, quantity, selling_price, "incomplete", productid))
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
        print(error)
        status = "False"
    return status


def getOrderID(userid):
    conn = get_db_connection()
    sqlquery = "SELECT order_id from ORDER where user_id=" + int(userid)
    orderid = conn.execute(sqlquery)
    return orderid


def getPrice(productid):
    conn = get_db_connection()
    sqlquery = "SELECT product_price from PRODUCT where product_serial_number=" + str(productid)
    price = conn.execute(sqlquery)
    return price


def getProductsFromOrder(orderid, productid):
    conn = get_db_connection()
    sqlquery = "SELECT count(*) from ORDERS where product_serial_number=" + str(productid) + " AND order_id=" + str(orderid)
    count = conn.execute(sqlquery)
    return count


def updateExistingItem(orderid, productid, selling_price, quantity):
    conn = get_db_connection()
    sqlquery = "UPDATE ORDERS SET quantity =" + str(quantity) + " AND " + str(selling_price)  + " = " + str(selling_price)  + " where order_id=" + str(orderid) + " AND product_serial_number=" + productid
    print("Quanity from update:")
    print(quantity)
    print("product number")
    print(productid)
    try:
        conn.execute(sqlquery)
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
        print(error)
        status = "False"
    return status


def addNewItemToOrder(orderid, userid, productid, selling_price, quantity):
    conn = get_db_connection()
    sqlquery = "INSERT INTO ORDERS (order_id, user_id, quantity, selling_price, order_status, product_serial_number) VALUES (?, ?, ?, ?, ?, ?)"
    try:
        conn.execute(sqlquery, (int(orderid), int(userid), int(quantity), float(selling_price), "incomplete", int(productid)))
        conn.close()
        status = "True" 
    except sqlite3.IntegrityError as error:
        print(error)
        status = "False"
    return status


def readOrder(userid):
    conn = get_db_connection()
    sqlquery = "SELECT * from ORDERS where user_id='" + str(userid) + "' AND order_status='incomplete'"
    data = conn.execute(sqlquery)
    return data


def readOrderForHeaderCart(user_email):
    conn = get_db_connection()
    sqlquery =  "SELECT order_id, count(*) AS item_count from orders LEFT OUTER JOIN user ON orders.user_id = user.user_id where user.user_email='" + str(user_email) + "' and order_status='incomplete' GROUP BY order_id LIMIT 1"
    data = conn.execute(sqlquery)
    return data


def validateOrderId(orderid):
    conn = get_db_connection()
    sqlquery = "SELECT count(*) from ORDERS where order_id='" + str(orderid) + "'"
    count = conn.execute(sqlquery)
    return count


def getImageUrl(productid):
    conn = get_db_connection()
    sqlquery = "SELECT * from PRODUCT where product_serial_number='" + str(productid) + "'"
    url = conn.execute(sqlquery)
    print(url)
    return url


