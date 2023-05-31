from backend.model import getPrice, addItemToNewOrder, getProductsFromOrder, addNewItemToOrder, updateExistingItem, getOrderID, readOrder, validateOrderId
from flask import session
import uuid


def addItemToCart(productid, quantity):
    userid = session["user_id"]
    orderid = getOrderID(userid)
    if orderid == "NULL":
        orderid = 0
        orderExists = "True"
        while orderExists == "True":
            orderid = uuid.uuid4()
            count = validateOrderId(orderid)
            if count == 0:
                orderExists = "False"
        selling_price = getPrice(productid) 
        addItemToNewOrder(orderid, userid, productid, selling_price, quantity)
        session["order-id"] = orderid
        session["total-items"] = 1
    else:
        count = getProductsFromOrder(orderid, productid)
        if count == 1:
            updateExistingItem(orderid, productid, selling_price, quantity)
        else:
            addNewItemToOrder(orderid, userid, productid, selling_price, quantity)

        session["order-id"] = orderid
        session["total-items"] = count
    return "True"
    

def getOrder(userid):
    order = readOrder(userid[0])
    keyList = ["order_id", "user_id", "ship_address", "order_date", "user_city", "quantity", "selling_price", "order_status", "product_id"]
    cart = {}
    i = 1
    for row in order:
        item = {key: [] for key in keyList}
        item['order_id'].append(row["order_id"])
        item['user_id'].append(row["user_id"])
        item['ship_address'].append(row["ship_address"])
        item['order_date'].append(row["order_date"])
        item['user_city'].append(row["user_city"])
        item['quantity'].append(row["quantity"])
        item['selling_price'].append(row["selling_price"])
        item['order_status'].append(row["order_status"])
        item['product_id'].append(row["product_id"])
        cart[i] = item

    if cart is not None:
        return cart
    else:
        return "ERROR"
