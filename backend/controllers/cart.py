from backend.model import getPrice, addItemToNewOrder, getProductsFromOrder, addNewItemToOrder, updateExistingItem, getOrderID, deleteItemFromOrder, readOrder, validateOrderId, getImageUrl, readOrderForHeaderCart, getQuantity, readOrderByOrderId, getStock, updateOrderStatus, readPlacedOrder, getUserRating, getSellerById
from flask import session
import random
from datetime import datetime


def addItemToCart(productid, quantity):
    userid = session["user_id"][0]
    if session["order_id"] == 'None':
        orderid = 'None'
    else:
        orderid = int(session["order_id"])
    sp = getPrice(productid)
    for i in sp:
        product_price = i['product_price']
        offer_flag = i['offer_flag']
        offer_percent = i['offer_percent']
    if offer_flag == 1:
        selling_price = round((product_price - (product_price * offer_percent) / 100),2)
    else:
        selling_price = round(product_price, 2)
    

    if orderid == "None":
        orderid = 0
        orderExists = "True"
        while orderExists == "True":
            orderid = random.randint(1111,9999)
            val = validateOrderId(orderid)
            for i in val:
                count = i[0]
            if count == 0:
                orderExists = "False" 
        addItemToNewOrder(orderid, userid, productid, selling_price, quantity)
        session["order_id"] = orderid
        session["total_items"] = 1
        refreshCart()
    else:
        count = getProductsFromOrder(orderid, productid)
        for i in count:
            count = i[0]
        if int(count) == 1:
            updateExistingItem(orderid, productid, selling_price, quantity)
        else:
            addNewItemToOrder(orderid, userid, productid, selling_price, quantity)

        session["order_id"] = orderid
        session["total_items"] = count
        refreshCart()
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
        item_total = round(float(row["quantity"]) * float(row["selling_price"]), 2)
        item['item_total'].append(item_total)
        image_id = getImageUrl(row["product_serial_number"])
        for url in image_id:
            item['image_id'].append(url["image_id"])
            item['product_name'].append(url["product_name"])
            p_url = "http://127.0.0.1:5000/product?categoryid=" + str(url["category_id"]) + "&subcategoryid=" +  str(url["sub_category_id"]) + "&product_serial_number=" + str(url["product_serial_number"])
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
    refreshCart()
    return "True"

def refreshCart():
    # cart = readOrderItemsForProductPage(orderid)
    # order = []
    # for item in cart:
    #     items = {}
    #     items["product_serial_number"] = item['product_serial_number']
    #     items["quantity"] = item['quantity']
    #     order.append(items)
    order = readOrderForHeaderCart(session["user_email"][0])
    order_id = 'None'
    item_count = '0'
    if order.rowcount != 0:
        for i in order:
            order_id = i['order_id']
            item_count = i['item_count']
            print("order id is")
            print(order_id)
            session["order_id"] = i['order_id']
    session["total_items"] = item_count


def getCurrentQuantityForAProduct(productid):
    quantity = getQuantity(productid, session['order_id'])
    return quantity


def updateOrder():
    orderid = session["order_id"]
    order = readOrderByOrderId(orderid)
    new_stock = {}
    for item in order:
        print("order id :", item["order_id"])
        print("product_serial_number :", item["product_serial_number"])
        print("quantity :", item["quantity"])
        stock = getStockValue(item["product_serial_number"])
        new_stock[item["product_serial_number"]] = int(stock) - int(item["quantity"])
        if int(stock) < int(item["quantity"]):
            return "incomplete"
    date = datetime.now().strftime("%d-%m-%Y")
    status = updateOrderStatus(orderid, new_stock, date, session['user_address'][0])
    if status is True:
        session.pop("order_id")
        session["order_id"] = 'None'
        refreshCart()
        order = readOrderByOrderId(orderid)
        return order, status
    order = readOrderByOrderId(orderid)
    return order, status


def getStockValue(product_serial_number):
    stock = getStock(product_serial_number)
    for item in stock:
        value = int(item["stock"])
        return value
    return False

def getPlacedOrder(orderid):
    order = readPlacedOrder(orderid)
    keyList = ["order_id", "user_id", "ship_address", "order_date", "quantity", "selling_price", "order_status", "product_serial_number", "image_id", "item_total", "order_total", "product_name", "product_url", "rating", "seller_name", "seller_email", "seller_address", "seller_id"]
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
        item_total = round(float(row["quantity"]) * float(row["selling_price"]), 2)
        item['item_total'].append(item_total)
        image_id = getImageUrl(row["product_serial_number"])
        for url in image_id:
            item['seller_id'].append(url["seller_id"])
            item['image_id'].append(url["image_id"])
            item['product_name'].append(url["product_name"])
            p_url = "http://127.0.0.1:5000/product?categoryid=" + str(url["category_id"]) + "&subcategoryid=" +  str(url["sub_category_id"]) + "&product_serial_number=" + str(url["product_serial_number"])
            item['product_url'].append(p_url)
        seller = getSellerById(item["seller_id"][0])
        for ss in seller:
            print("ss['seller_name']", ss["seller_name"])
            item["seller_name"].append(ss["seller_name"])
            item["seller_email"].append(ss["seller_email"])
            item["seller_address"].append(ss["seller_address"])
        rating = getUserRating(row["product_serial_number"], row["user_id"])
        for rr in rating:
            item['rating'].append(rr["rating_score"])
        cart.append(item)
        i += 1
        order_total += item_total
        item
    if cart is not None:
        return cart, order_total
    else:
        return "ERROR"


