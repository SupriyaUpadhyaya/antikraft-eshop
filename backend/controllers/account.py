
from flask import Flask
from backend.model import readUserAccount, insertUserAccount, insertSellerAccount, readSellerAccount, readOrderForHeaderCart, readOrderHistory, updateUserAccount, updatepassword, updatepasswordseller
from flask_simple_crypt import SimpleCrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "antiqkraft"

cipher = SimpleCrypt()
cipher.init_app(app)

def getUserAccount(username):
    data = readUserAccount(username)
    order = readOrderForHeaderCart(username)
    order_id = 'None'
    item_count = '0'
    if order.rowcount != 0:
        for i in order:
            order_id = i['order_id']
            item_count = i['item_count']
            print("order id is")
            print(order_id)
    keyList = ["user_id", "user_firstname", "user_lastname", "user_email", "user_password", "user_city", "user_state", "user_zip", "user_phone", "user_address", "login_status", "user_salutation", "order_id", "total_items", "security_question"]
    user = {key: [] for key in keyList}
    user["order_id"] = order_id
    user["total_items"] = item_count
    count = 0
    for row in data:
        count += 1
        user['user_id'].append(row["user_id"])
        user['user_firstname'].append(row["user_firstname"])
        user['user_lastname'].append(row["user_lastname"])
        user['user_email'].append(row["user_email"])
        user['user_password'].append(row["user_password"])
        user['user_city'].append(row["user_city"])
        user['user_state'].append(row["user_state"])
        user['user_zip'].append(row["user_zip"])
        user['user_phone'].append(row["user_phone"])
        user['user_address'].append(row["user_address"])
        user['user_salutation'].append(row["user_salutation"])
        user['security_question'].append(row["security_question"])
    if count != 0:
        return user
    else:
        return "ERROR"


def validateCredentails(username, password):
    user = getUserAccount(username)
    if user == "ERROR":
        return "False"
    else:
        if password == cipher.decrypt(user["user_password"][0]).decode("ascii"):
            status = "True"
        else:
            status = "False"
            return "False"
    user["login_status"] = status
    return user


def validateRegistration(salutation, firstname, lastname, email, password, phonenumber, address, securityquestion):
    userexists = getUserAccount(email)
    if userexists == "ERROR":
        encrypted_password = cipher.encrypt(password).decode("ascii")
        status = addUserAccount(salutation, firstname, lastname, email, encrypted_password, phonenumber, address, securityquestion)
        if status == "True":
            user = getUserAccount(email)
            user["login_status"] = status
            return user
        else:
            return "False"
    else:
        return "exists"
    

def addUserAccount(salutation, firstname, lastname, email, password, phonenumber, address, securityquestion):
    status = insertUserAccount(salutation, firstname, lastname, email, password, phonenumber, address, securityquestion)
    if status == "True":
        return "True"
    else:
        return "False"


def getSellerAccount(username):
    data = readSellerAccount(username)
    count = 0
    keyList = ["seller_id", "seller_name", "seller_email", "seller_password", "seller_address", "seller_address", "seller_login_status", "security_question"]
    seller = {key: [] for key in keyList}
    for row in data:
        count += 1
        seller['seller_id'].append(row["seller_id"])
        seller['seller_name'].append(row["seller_name"])
        seller['seller_email'].append(row["seller_email"])
        seller['seller_password'].append(row["seller_password"])
        seller['seller_address'].append(row["seller_address"])
        seller['security_question'].append(row["security_question"])
    if count != 0:
        return seller
    else:
        return "ERROR"


def validateSellerCredentails(username, password):
    seller = getSellerAccount(username)
    if seller == "ERROR":
        return "False"
    else:
        if password == cipher.decrypt(seller["seller_password"][0]).decode("ascii"):
            status = "True"
        else:
            status = "False"
    seller["seller_login_status"] = status
    return seller


def validateSellerRegistration(sellername, email, password, address, securityquestion):
    sellerexists = getSellerAccount(email)
    if sellerexists == "ERROR":
        encrypted_password = cipher.encrypt(password).decode("ascii")
        status = addSellerAccount(sellername, email, encrypted_password, address, securityquestion)
        if status == "True":
            seller = getSellerAccount(email)
            seller["seller_login_status"] = status
            return seller
        else:
            return "False"
    else:
        return "exists"


def addSellerAccount(sellername, email, password, address, securityquestion):
    status = insertSellerAccount(sellername, email, password, address, securityquestion)
    if status == "True":
        return "True"
    else:
        return "False"

def verifyUserAccount(email, security_answer):
    status = getUserAccount(email)
    if status == "ERROR":
        return False
    else:
        if status['security_question'][0] == security_answer:
            return True
        else:
            return False
     
def updateUserPassword(username, new_password):
    encrypted_password = cipher.encrypt(new_password).decode("ascii")
    status = updatepassword(username, encrypted_password)
    return status

def verifySellerAccount(username, security_answer):
    status = getSellerAccount(username)
    if status == "ERROR":
        return False
    else:
        if status['security_question'][0] == security_answer:
        
            return True
        else:
            return False
     
def updateSellerPassword(username, new_password):
    encrypted_password = cipher.encrypt(new_password).decode("ascii")
    status = updatepasswordseller(username, encrypted_password)
    return status

def getOrderHistory(userid):
    order = readOrderHistory(userid)
    return order


def updatePersonalDetails(salutation, firstname, lastname, email, phonenumber, address, securityquestion):
    userexists = getUserAccount(email)
    if userexists != "ERROR":
        status = updateUserAccount(salutation, firstname, lastname, email, phonenumber, address, securityquestion)
        print(status)
        if status == "True":
            user = getUserAccount(email)
            return user
        else:
            return "False"
    else:
        return "False"