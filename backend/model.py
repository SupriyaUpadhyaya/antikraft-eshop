import sqlite3
import pandas as pd

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
  
    keyList = ["category_id", "sub_category_id", "product_id", "product_name", "product_price", "product_description", "image_id", "url", "product_serial_number"]
    products = []
    for row in data:
        sub_category_row = {key: [] for key in keyList}
        url = "http://127.0.0.1:5000/subcategory?categoryid=" + str(row["category_id"]) + "&subcategoryid=" + str(row["sub_category_id"])
        sub_category_row['category_id'].append(row["category_id"])
        sub_category_row['sub_category_id'].append(row["sub_category_id"])
        sub_category_row['product_id'].append(row["product_id"])
        sub_category_row['product_name'].append(row["product_name"])
        sub_category_row['product_description'].append(row["product_description"])
        sub_category_row['product_price'].append(row["product_price"])
        sub_category_row['image_id'].append(row["image_id"])
        sub_category_row['product_serial_number'].append(row["product_serial_number"])
        sub_category_row['url'].append(url)
        products.append(sub_category_row)
    
    return products

def readOperationProduct(TABLE_NAME: str, CAT_ID: int, SUB_CAT_ID: int, product_serial_number:int):
    conn = get_db_connection()
    query = "SELECT * from " + TABLE_NAME + " where category_id=" + str(CAT_ID) + " and sub_category_id=" + str(SUB_CAT_ID) + " and product_serial_number=" + str(product_serial_number)
    data = conn.execute(query)
  
    keyList = ["category_id", "sub_category_id", "product_id", "product_name", "product_description", "product_price", "seller_id", "stock", 
               "posted_date", "offer_flag", "offer_percent", "product_serial_number", "image_id", "secondary_images", "url", "seller", "badge", "offer_image_id", "offer_id"]
    product_row = {key: [] for key in keyList}

    for row in data:
        url = "http://127.0.0.1:5000/product?categoryid=" + str(row["category_id"]) + "&subcategoryid=" + str(row["sub_category_id"]) + "&product_serial_number=" + str(row["product_serial_number"])
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
        product_row['offer_id'].append(row["offer_id"])
        product_row['product_serial_number'].append(row["product_serial_number"])
        product_row['image_id'].append(row["image_id"])
        product_row['secondary_images'].append(row["secondary_images"])
        product_row['url'].append(url)
    
    sellerquery = "select * from seller where seller_id = " +  str(product_row['seller_id'][0])
    seller = conn.execute(sellerquery)
    for item in seller:
        product_row['seller'].append(item['seller_name'])
        product_row['badge'].append("static/badge/b" + str(item['badge']) + ".png")

    if product_row['offer_flag'][0] != 0:
        offerquery = "select * from offers where product_serial_number = " + str(product_row['product_serial_number'][0]) + " and offer_id=" + str(product_row['offer_id'][0])
        offers = conn.execute(offerquery)
        for item in offers:
            product_row['offer_percent'].append(item['offer_percent'])
            product_row['offer_image_id'].append(str(item['offer_image_id']))
    else:
        product_row['offer_percent'].append(0)
        product_row['offer_image_id'].append(0)

    if product_row is not None:
        return product_row

def readOperationProductRatings(TABLE_NAME: str, PRODUCT_S_N:int):
    conn = get_db_connection()
    query = "SELECT * from " + TABLE_NAME + " where product_serial_number=" + str(PRODUCT_S_N)

    data = conn.execute(query)

    keyList = ["rating_id", "rating_score", "product_serial_number", "comments", "user_id"]
    ratings_row = {key: [] for key in keyList}

    for row in data:
        ratings_row['rating_id'].append(row["rating_id"])
        ratings_row['rating_score'].append(row["rating_score"])
        ratings_row['product_serial_number'].append(row["product_serial_number"])
        ratings_row['comments'].append(row["comments"])
        ratings_row['user_id'].append(row["user_id"])

    if ratings_row is not None:
        return ratings_row
    
def searchProductList(query):
    conn = get_db_connection()
    sqlquery = "SELECT * from PRODUCT where product_description LIKE '%" + str(query) + "%' OR product_name LIKE '%" + str(query) + "%' ORDER BY sponsored DESC"
    data = conn.execute(sqlquery)
    return data


def readUserAccount(username):
    conn = get_db_connection()
    sqlquery = "SELECT * from USER where user_email='" + username + "'"
    data = conn.execute(sqlquery)
    return data


def readSellerAccount(username):
    conn = get_db_connection()
    sqlquery = "SELECT * from SELLER where seller_email='" + username + "'"
    print(sqlquery)
    data = conn.execute(sqlquery)
    return data


def insertUserAccount(salutation, firstname, lastname, email, password, phonenumber,  address, securityquestion):
    conn = get_db_connection()
    sqlquery = "INSERT INTO USER (user_firstname, user_lastname, user_salutation, user_email, user_password, user_phone,  user_address, security_question ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    print(sqlquery)
    try:
        conn.execute(sqlquery, (firstname, lastname, salutation, email, password, phonenumber, address, securityquestion ))
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
        print(error)
        status = "False"
    return status

def updateUserAccount(salutation, firstname, lastname, email, phonenumber,  address, securityquestion):
    conn = get_db_connection()
    sqlquery = "UPDATE USER SET user_firstname='" + str(firstname) + "', user_lastname='" + str(lastname) + "', user_salutation='" + str(salutation) + "', user_phone=" + str(phonenumber) + ", user_address='" + str(address) + "', security_question='" + str(securityquestion) + "' where user_email='" + str(email) +"'"
    try:
        conn.execute(sqlquery)
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
        status = "False"
    return status


def insertSellerAccount(sellername, email, password, address, securityquestion):
    conn = get_db_connection()
    sqlquery = "INSERT INTO SELLER (seller_name, seller_email, seller_password, seller_address, security_question ) VALUES (?, ?, ?, ?, ?)"
    try:
        conn.execute(sqlquery, (sellername, email, password, address, securityquestion ))
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
        status = "False"
    return status


def addItemToNewOrder(orderid, userid, productid, selling_price, quantity):
    conn = get_db_connection()
    status_s = "incomplete"
    sqlquery = "INSERT INTO ORDERS (order_id, user_id, quantity, selling_price, order_status, product_serial_number) VALUES (" + str(orderid) + ", " + str(userid) + ", " + str(quantity) + ", " + str(selling_price) + ", " + "'" + status_s + "'" + ", " + str(productid)+ ")"
    try:
        conn.execute(sqlquery)
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
        status = "False"
    return status


def getOrderID(userid):
    conn = get_db_connection()
    sqlquery = "SELECT order_id from ORDER where user_id=" + int(userid) + " ORDER BY order_id"
    orderid = conn.execute(sqlquery)
    return orderid


def getPrice(productid):
    conn = get_db_connection()
    sqlquery = "SELECT * from PRODUCT where product_serial_number=" + str(productid)
    price = conn.execute(sqlquery)
    return price


def getProductsFromOrder(orderid, productid):
    conn = get_db_connection()
    sqlquery = "SELECT count(*) from ORDERS where product_serial_number=" + str(productid) + " AND order_id=" + str(orderid)
    count = conn.execute(sqlquery)
    return count


def updateExistingItem(orderid, productid, selling_price, quantity):
    conn = get_db_connection()
    sqlquery = "UPDATE ORDERS SET quantity=" + str(quantity) + ", selling_price=" + str(selling_price)  + " where order_id=" + str(orderid) + " AND product_serial_number=" + productid
    try:
        conn.execute(sqlquery)
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
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
        status = "False"
    return status


def deleteItemFromOrder(orderid, userid, productid):
    conn = get_db_connection()
    sqlquery = "DELETE FROM ORDERS where order_id=" + str(orderid) + " AND user_id=" + str(userid) + " AND product_serial_number=" + str(productid)
    try:
        conn.execute(sqlquery)
        conn.close()
        status = "True" 
    except sqlite3.IntegrityError as error:
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

def readOrderByOrderId(orderid):
    conn = get_db_connection()
    sqlquery =  "SELECT * from orders where order_id='" + str(orderid) + "' and order_status='incomplete'"
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
    return url


def getQuantity(productid, orderid):
    conn = get_db_connection()
    sqlquery = "SELECT quantity from ORDERS where product_serial_number='" + str(productid) + "' and order_id=" + str(orderid)
    url = conn.execute(sqlquery)
    return url


def getStock(product_serial_number):
    conn = get_db_connection()
    sqlquery = "SELECT stock from PRODUCT where product_serial_number='" + str(product_serial_number) + "'"
    stock = conn.execute(sqlquery)
    return stock


def updateOrderStatus(orderid, new_stock, date, address):
    conn = get_db_connection()
    sqlquery = "UPDATE ORDERS SET order_status='completed'" + ", ship_address='" + str(address) + "', order_date='" + str(date) + "' where order_id=" + str(orderid)
    query = []
    k = new_stock.keys()
    for item in k:
        item_query = "UPDATE PRODUCT SET stock=" + str(new_stock[item]) + " where product_serial_number=" + str(item)
        query.append(item_query)
    try:
        conn.execute(sqlquery)
        for q in query:
            conn.execute(q)
        conn.close()
        status = True  
    except sqlite3.IntegrityError as error:
        status = False
    return status

def readPlacedOrder(orderid):
    conn = get_db_connection()
    sqlquery = "SELECT * from ORDERS where order_id=" + str(orderid)
    data = conn.execute(sqlquery)
    return data

def readOrderHistory(userid):
    conn = get_db_connection()
    sqlquery = "SELECT * from ORDERS where user_id=" + str(userid) + " GROUP BY order_id"
    data = conn.execute(sqlquery)
    return data

def insertNewRatings(rating_score, product_serial_number, user_id, comments=""):
    conn = get_db_connection()

    checkquery = "SELECT COUNT(*) FROM RATINGS WHERE user_id = " + str(user_id) + " AND product_serial_number = " + str(product_serial_number)
    # print(checkquery)
    conn.execute(checkquery)
    counts = conn.fetchall()
    content_list = []
    for row in counts:
        content_list.append(list(row))

    count_value = content_list[0]

    if count_value[0] != 0:
        del_query = "DELETE FROM RATINGS WHERE user_id = " + str(user_id) + " AND product_serial_number = " + str(product_serial_number)
        # print(del_query)
        conn.execute(del_query)

    sqlquery = "INSERT INTO RATINGS (rating_score, product_serial_number, comments, user_id) VALUES (?, ?, ?, ?)"
    # print(sqlquery)
    try:
        conn.execute(sqlquery, (int(rating_score), int(product_serial_number), str(comments), int(user_id)))
        conn.close()
        status = True
    except sqlite3.IntegrityError as error:
        status = False
    return status


def insertNewProduct(productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory, stock, image_id, category, product_id, secondary_images, sponsored, offer_image_id):
    conn = get_db_connection()
    offer_id = 0
    sqlquery = "INSERT INTO PRODUCT (product_name, product_description, seller_id, posted_date, offer_flag, offer_id, product_price, sub_category_id, stock, image_id, category_id, product_id, secondary_images, sponsored) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    print(sqlquery)
    try:
        data = conn.execute(sqlquery, (productName, productDescription, int(seller_id), date, offerflag, int(offer_id), float(productPrice), subcategory, int(stock), image_id, int(category), int(product_id), secondary_images, sponsored))
        newProdID = int(data.lastrowid)
        print("New prod id ", newProdID)
        offerQuery = "INSERT INTO OFFERS (product_serial_number, offer_percent, offer_image_id) VALUES (?, ?, ?)"
        newOfferID = conn.execute(offerQuery, (newProdID, offerpercent, offer_image_id ))
        print("new offer if ", int(newOfferID.lastrowid))
        productUpdateQuery = "UPDATE PRODUCT SET offer_id=" + int(newOfferID.lastrowid) + " where product_serial_number=" + newProdID
        conn.execute(productUpdateQuery)
        conn.close()
        status = True
    except sqlite3.IntegrityError as error:
        print(error)
        status = False
    return status


def getCategoryId(category):
    conn = get_db_connection()
    sqlquery = "SELECT category_id from category where category_name='" + category + "'"
    data = conn.execute(sqlquery)
    return data


def getSubCategoryId(subcategory):
    conn = get_db_connection()
    sqlquery = "SELECT sub_category_id from sub_category where sub_category_name='" + subcategory + "'"
    data = conn.execute(sqlquery)
    return data


def readSellerProducts(sellerid):
    conn = get_db_connection()
    sqlquery = "SELECT * from product where seller_id=" + str(sellerid[0]) + " and stock != 0 ORDER BY product_serial_number"
    data = conn.execute(sqlquery)
    return data

def readSellerProductsHistory(sellerid):
    conn = get_db_connection()
    sqlquery = "SELECT * from product where seller_id=" + str(sellerid[0]) + " and stock == 0 ORDER BY product_serial_number"
    data = conn.execute(sqlquery)
    return data


def getUserRating(sn, userid):
    conn = get_db_connection()
    sqlquery = "SELECT * from ratings where product_serial_number=" + str(sn) + " and user_id=" + str(userid)
    data = conn.execute(sqlquery)
    return data


def getProductRating(sn):
    conn = get_db_connection()
    sqlquery = "SELECT * from ratings where product_serial_number=" + str(sn) 
    data = conn.execute(sqlquery)
    return data


def writeProductOffers(product_serial_number, offer_flag, offer_percent):
    conn = get_db_connection()
    sqlquery = "UPDATE PRODUCT SET offer_flag=" + str(offer_flag) + ", offer_percent= " + str(offer_percent) + " where product_serial_number=" + str(product_serial_number)
    try:
        conn.execute(sqlquery)
        conn.close()
        status = True
    except sqlite3.IntegrityError as error:
        status = False
    return status

def getSellerById(id):
    conn = get_db_connection()
    sqlquery = "SELECT * from SELLER where seller_id='" + str(id) + "'"
    data = conn.execute(sqlquery)
    return data

def updatepassword(username, encrypted_password):
    conn = get_db_connection()
    sqlquery = "UPDATE USER SET user_password='" + str(encrypted_password) + "' where user_email='" + str(username) + "'"
    try:
        conn.execute(sqlquery)
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
        status = "False"
    return status

def getSellerAwardData(sellerid):
    conn = get_db_connection()
    
    sqlquery1 = "SELECT * FROM ORDERS"
    result1 = conn.execute(sqlquery1)
    columns1 = [column[0] for column in conn.description]
    df_order = pd.DataFrame(result1.fetchall(), columns=columns1)

    sqlquery2 = "SELECT PRODUCT.product_serial_number, PRODUCT.product_name, PRODUCT.seller_id  FROM PRODUCT"
    result2 = conn.execute(sqlquery2)
    columns2 = [column[0] for column in conn.description]
    df_product = pd.DataFrame(result2.fetchall(), columns=columns2)

    df_award_data = df_order.merge(df_product, how='left', on='product_serial_number')
    df_award_data = df_award_data[df_award_data.seller_id == sellerid]
    df_award_data = df_award_data[(df_award_data.order_status == 'complete') | (df_award_data.order_status == 'completed')]

    df_award_data = df_award_data[['product_serial_number', 'product_name', 'quantity', 'seller_id']]
    df_award_data2 = df_award_data.groupby(['product_name'])['quantity'].sum().reset_index()
    df_award_data2.rename(columns={'quantity': 'total_quantity'}, inplace=True)

    df_award_data = df_award_data.merge(df_award_data2, how='left', on='product_name')
    df_award_data = df_award_data[['product_serial_number','product_name','seller_id','total_quantity']]
    df_award_data.drop_duplicates(subset=['product_serial_number', 'product_name'], inplace=True)
    
    total_sold = df_award_data['total_quantity'].sum()

    badge = ""
    if (total_sold < 10):
        badge = "5"
    elif (total_sold >= 10) and (total_sold < 20):
        badge = "4"
    elif (total_sold >= 20) and (total_sold < 30):
        badge = "3"
    elif (total_sold >= 30) and (total_sold < 40):
        badge = "2"
    elif (total_sold >= 40):
        badge = "1"

    update_sqlquery = "UPDATE SELLER set badge='" + badge + "' WHERE seller_id=" + str(sellerid)
    # print(update_sqlquery)

    conn.execute(update_sqlquery)
    conn.close()
        
    keyList = ["product_serial_number", "product_name", "seller_id", "total_quantity"]
    products_list = []
    for index,row in df_award_data.iterrows():
        products = {key: [] for key in keyList}
        products['product_serial_number'].append(row["product_serial_number"])
        products['product_name'].append(row["product_name"])
        products['seller_id'].append(row["seller_id"])
        products['total_quantity'].append(row["total_quantity"])
        products_list.append(products)
     
    if products_list is not None:
        return products_list, total_sold
    else:
        return "ERROR"


def updatepasswordseller(username, encrypted_password):
    conn = get_db_connection()
    sqlquery = "UPDATE SELLER SET seller_password='" + str(encrypted_password) + "' where seller_email='" + str(username) + "'"
    try:
        conn.execute(sqlquery)
        conn.close()
        status = "True"    
    except sqlite3.IntegrityError as error:
        status = "False"
    return status


def readOffers(product_serial_number, offer_id):
    conn = get_db_connection()
    offerquery = "select * from offers where product_serial_number = " + product_serial_number + " and offer_id=" + offer_id
    data = conn.execute(offerquery)
    return data
