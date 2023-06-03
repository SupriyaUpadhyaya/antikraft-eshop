from backend.model import getPrice, addItemToNewOrder, getProductsFromOrder, addNewItemToOrder, updateExistingItem, getOrderID, deleteItemFromOrder, readOrder, validateOrderId, getImageUrl
from flask import session
import uuid


def addItemToCart(productid, quantity):
    userid = session["user_id"][0]
    orderid = int(session["order_id"])
    sp = getPrice(productid)
    for i in sp:
        selling_price = i[0]
    print(orderid)
    if orderid == "None":
        orderid = 0
        orderExists = "True"
        while orderExists == "True":
            orderid = uuid.uuid4()
            count = validateOrderId(orderid)
            if count == 0:
                orderExists = "False" 
        addItemToNewOrder(orderid, userid, productid, selling_price, quantity)
        session["order-id"] = orderid
        session["total-items"] = 1
    else:
        count = getProductsFromOrder(orderid, productid)
        for i in count:
            count = i[0]
        if int(count) == 1:
            updateExistingItem(orderid, productid, selling_price, quantity)
        else:
            addNewItemToOrder(orderid, userid, productid, selling_price, quantity)

        session["order-id"] = orderid
        session["total-items"] = count
    return "True"
    

def getOrder(userid):
    order = readOrder(userid[0])
    keyList = ["order_id", "user_id", "ship_address", "order_date", "quantity", "selling_price", "order_status", "product_serial_number", "image_id", "item_total", "order_total", "product_name", "product_url"]
    cart = []
    i = 1
    order_total = 0
    for row in order:
        item = {key: [] for key in keyList}
        item['order_id'].append(row["order_id"])
        item['user_id'].append(row["user_id"])
        item['ship_address'].append(row["ship_address"])
        item['order_date'].append(row["order_date"])
        item['quantity'].append(row["quantity"])
        item['selling_price'].append(row["selling_price"])
        item['order_status'].append(row["order_status"])
        item['product_serial_number'].append(row["product_serial_number"])
        item_total = float(int(row["quantity"]) * int(row["selling_price"]))
        item['item_total'].append(item_total)
        image_id = getImageUrl(row["product_serial_number"])
        for url in image_id:
            item['image_id'].append(url["image_id"])
            item['product_name'].append(url["product_name"])
            p_url = "http://127.0.0.1:5000/product?categoryid=" + str(url["category_id"]) + "&subcategoryid=" +  str(url["sub_category_id"]) + "&productid=" + str(url["product_id"])
            item['product_url'].append(p_url)
        cart.append(item)
        i += 1
        order_total += item_total
        item
    if cart is not None:
        return cart, order_total
    else:
        return "ERROR"
    
def deleteItemFromCart(productid):
    userid = session["user_id"][0]
    print("User :")
    print(userid)
    orderid = int(session["order_id"])
    deleteItemFromOrder(orderid, userid, productid)
    return "True"