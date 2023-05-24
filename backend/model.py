import json
import sqlite3

from flask import jsonify


def get_db_connection():
    conn = sqlite3.connect('antiqkraft-database.db')
    conn.row_factory = sqlite3.Row
    return conn.cursor()


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


def searchProductList(qterm):
    conn = get_db_connection()
    query = "SELECT * from PRODUCT where product_description LIKE " + str(qterm)
    data = conn.execute(query)
    products = {}
    for row in data:
        products[row["product_id"]] = row["product_description"]
    if products is not None:
        return products

