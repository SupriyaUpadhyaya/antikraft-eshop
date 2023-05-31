
from flask import Flask
from backend.model import readUserAccount, insertUserAccount, insertSellerAccount, readSellerAccount
from flask_simple_crypt import SimpleCrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "antiqkraft"

cipher = SimpleCrypt()
cipher.init_app(app)
pw = "password124"
# encryptedP = cipher.encrypt("password124")
# print(encryptedP)
# deencryptedP = cipher.decrypt(encryptedP)
# print(deencryptedP)
# if pw == deencryptedP.decode('ascii'):
#     print("TRUE")
# else:
#     print("FALSE")


def getUserAccount(username):
    data = readUserAccount(username)

    keyList = ["user_id", "user_firstname", "user_lastname", "user_email", "user_password", "user_city", "user_state", "user_zip", "user_phone", "user_address", "login_status", "user_salutation"]
    user = {key: [] for key in keyList}

    for row in data:
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

    if user is not None:
        return user
    else:
        return "ERROR"


def validateCredentails(username, password):
    user = getUserAccount(username)
    if user == "ERROR":
        return "ERROR: Username does not exist"
    else:
        if password == cipher.decrypt(user["user_password"][0]).decode("ascii"):
            status = "True"
        else:
            status = "False"
    user["login_status"] = status
    return user


def validateRegistration(salutation, firstname, lastname, email, password, phonenumber):
    encrypted_password = cipher.encrypt(password).decode("ascii")
    status = addUserAccount(salutation, firstname, lastname, email, encrypted_password, phonenumber)
    if status == "True":
        user = getUserAccount(email)
    user["login_status"] = status
    return user
    

def addUserAccount(salutation, firstname, lastname, email, password, phonenumber):
    status = insertUserAccount(salutation, firstname, lastname, email, password, phonenumber)
    if status == "True":
        return "True"
    else:
        return "False"
  
   
def validateSellerRegistration(sellername, email, password, address):
    encrypted_spassword = cipher.encrypt(password).decode("ascii")
    status = addSellerAccount(sellername, email, encrypted_spassword, address)
    if status == "False":
        return "ERROR: Seller Registration not successful"
    else:
        return "True"


def addSellerAccount(sellername, email, password, address):
    status = insertSellerAccount(sellername, email, password, address)
    if status == "True":
        return "True"
    else:
        return "False"


def getSellerAccount(username):
    data = readSellerAccount(username)

    keyList = ["seller_id", "seller_name", "seller_emai", "seller_password", "seller_address", "seller_address"]
    seller = {key: [] for key in keyList}
    for row in data:
        seller['seller_id'].append(row["seller_id"])
        seller['seller_name'].append(row["seller_name"])
        seller['seller_emai'].append(row["seller_emai"])
        seller['seller_password'].append(row["seller_password"])
        seller['seller_address'].append(row["seller_address"])
    if seller is not None:
        return seller
    else:
        return "ERROR"


def validateSellerCredentails(username, password):
    seller = getSellerAccount(username)
    if seller == "ERROR":
        return "ERROR: Username does not exist"
    else:
        if password == cipher.decrypt(seller["user_password"][0]).decode("ascii"):
            status = "True"
        else:
            status = "False"
    seller["seller_login_status"] = status
    return seller
    


