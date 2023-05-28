
from flask import Flask
from backend.model import readUserAccount, insertUserAccount
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
    user = {}
    print("user len")
    data.moveToFirst()
    print(len(data.fetchall()))
    if len(data.fetchall()):
        user = {}
        user["user_id"] = data.fetchall()[0]
        user["user_firstname"] = data.fetchall()[1]
        user["user_lastname"] = data.fetchall()[2]
        user["user_email"] = data.fetchall()[3]
        user["user_password"] = data.fetchall()[4]
        user["user_city"] = data.fetchall()[5]
        user["user_state"] = data.fetchall()[6]
        user["user_zip"] = data.fetchall()[7]
        user["user_phone"] = data.fetchall()[8]
        user["user_address"] = data.fetchall()[9]
        return user
    else:
        return "ERROR"


def validateCredentails(username, password):
    user = getUserAccount(username)
    for item in user:
        print(item)
    if user == "ERROR":
        return "ERROR: Username does not exist"
    else:
        passwordEntered = cipher.encrypt(password)
        print(user)
        if passwordEntered == user["user_password"].decode('ascii'):
            return "True"
    return "False"

def validateRegistration(salutation, firstname, lastname, email, password, phonenumber):
    status = addUserAccount(salutation, firstname, lastname, email, password, phonenumber)
    if status == "False":
        return "ERROR: Registration not successful"
    else:
        return "True"

def addUserAccount(salutation, firstname, lastname, email, password, phonenumber):
    status = insertUserAccount(salutation, firstname, lastname, email, password, phonenumber)
    if status == "True":
        #user = getUserAccount(email)
        #user["login_status"]="True"
        return "True"
    else:
        return "False"

