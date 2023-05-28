import sqlite3


def get_db_connection():
    conn = sqlite3.connect('antiqkraft-database.db')
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
        category_row['category_description'] = row["category_description"]
    if category_row is not None:
        return category_row

def readOperationCategoryImages(TABLE_NAME: str, CAT_ID: int):
    conn = get_db_connection()
    query = "SELECT * from " + TABLE_NAME + " where category_id=" + str(CAT_ID)
    
    data = conn.execute(query)

    keyList = ["category_id", "sub_category_id", "sub_category_name", "sub_category_image_id"]
    sub_category_row = {key: [] for key in keyList}

    for row in data:
        # print('row', row)
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

def readOperationProductList(TABLE_NAME: str, COLS: str, CAT_ID: int, SUB_CAT_ID: int):
    conn = get_db_connection()
    if SUB_CAT_ID == 0:
        query = "SELECT * from " + TABLE_NAME + " where category_id=" + str(CAT_ID)
    else:
        query = "SELECT * from " + TABLE_NAME + " where category_id=" + str(CAT_ID) + " AND subcategory_id=" + str(SUB_CAT_ID)
    data = conn.execute(query)
    products = {}
    for row in data:
        products[row["product_id"]] = row["description"]
    if products is not None:
        return products


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
