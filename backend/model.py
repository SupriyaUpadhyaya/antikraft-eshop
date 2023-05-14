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
        categories[row["category_id"]] = row["category_name"]
    if categories is not None:
        return categories
