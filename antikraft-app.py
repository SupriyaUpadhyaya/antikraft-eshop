from datetime import datetime
import json, subprocess
from statistics import mean
from flask import Flask, redirect, render_template, request, session, url_for, jsonify, request, abort
from backend.controller import getAllCategoriesList, getSearch, getSpecificCategoryList, getSpecificCategoryImages, getSubCategoryProductList, getProductData, getProductRatings
from backend.controllers.account import validateCredentails, validateRegistration, validateSellerRegistration, validateSellerCredentails, getOrderHistory, updatePersonalDetails, verifyUserAccount, updateUserPassword, verifySellerAccount, updateSellerPassword
from backend.controllers.cart import getOrder, addItemToCart, deleteItemFromCart, getCurrentQuantityForAProduct, updateOrder, getPlacedOrder
from backend.controllers.product import addNewProductFromSeller, uploadImageToDrive, getSellerProducts, updateProductOffers, getSellerProductsHistory
from backend.model import insertNewRatings, getSellerAwardData, create_chat_table, get_db_connection, getAllSellers
import time

import nltk
# nltk.download('punkt')
from backend.chat import get_response


subprocess.run(f"python backend/train.py")

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# @app.route("/")
@app.route('/',  methods=['GET'])
def home():
    if 'login_status' not in session:
        session["login_status"] = 'False'
    categories = getAllCategories()
    return render_template('homepage/home.html', categories=categories.json, user="None")

@app.route('/predict',  methods=['POST'])
def predict():
    text = request.get_json().get('message')
    response = get_response(text)
    message = {"answer": response}
    print(message)
    return json.dumps(message)

# To render category HTML page when user clicks on category in top nav 
@app.route("/category")
def getSpecificCategory():
    if 'login_status' not in session:
        session["login_status"] = 'False'
    qTerm = request.args.get('categoryid')
    row_val = getSpecificCategoryRow(qTerm)
    row_json = row_val.json
    category_id = row_json['category_id']
    db_images = getSpecificCategoryImages(category_id)
    categories = getAllCategories()
    return render_template('category/category_landing_page.html', categories=categories.json, \
                           row_val=row_val.json, image_list=db_images['sub_category_image_id'], \
                            sub_cat_list=db_images['sub_category_name'], sub_cat_id_list=db_images['sub_category_id'])

def getSpecificCategoryRow(qTerm):
    spec_cat = getSpecificCategoryList(qTerm)
    
    response = app.response_class(
        response=json.dumps(spec_cat),
        status=200,
        mimetype='application/json'
    )

    return response


# To render sub category HTML page when user clicks on category page tiles
@app.route("/subcategory")
def getSpecificSubCategory():
    if 'login_status' not in session:
        session["login_status"] = 'False'
    sub_category_id = request.args.get('subcategoryid')
    category_id = request.args.get('categoryid')
    
    sub_cat_product_json = getSubCategoryProductList(category_id, sub_category_id)
    category_table_row = getSpecificCategoryRow(category_id)
    sub_cat_name = getSpecificCategoryImages(category_id)
    sub_cat_name = sub_cat_name['sub_category_name'][int(sub_category_id)-1]
    categories = getAllCategories()
    return render_template('subcategory/subcategory_landing_page.html', categories = categories.json, \
                           category_name = category_table_row.json['category_name'], \
                           sub_category_name = sub_cat_name, \
                           sub_category_id = sub_category_id, \
                           category_id = category_id, \
                           range=range, \
                           len=len, sub_cat_product_json=sub_cat_product_json)

def getSubCategoryJson(category_id, sub_category_id):
    spec_cat = getSubCategoryProductList(category_id, sub_category_id)
    
    response = app.response_class(
        response=json.dumps(spec_cat),
        status=200,
        mimetype='application/json'
    )

    return response

# To render sub category HTML page when user clicks on category page tiles
@app.route("/product")
def getSpecificProduct():
    if 'login_status' not in session:
        session["login_status"] = 'False'
    sub_category_id = request.args.get('subcategoryid')
    category_id = request.args.get('categoryid')
    product_serial_number = request.args.get('product_serial_number')
    categories = getAllCategories()
    category_table_row = getSpecificCategoryRow(category_id)
    cat_name = category_table_row.json['category_name']
    print(sub_category_id)
    sub_cat_name = getSpecificCategoryImages(category_id)
    print(sub_cat_name)
    sub_cat_name = sub_cat_name['sub_category_name'][int(sub_category_id)-1]    

    product_json = getProductData(category_id, sub_category_id, product_serial_number)

    sec_images = product_json['secondary_images'][0]
    li_sec_images = sec_images.split(';')

    quantity = request.args.get('quantity')
    print("quantity", quantity)

    quant = 1
    if session["login_status"] == 'True':
        if session["order_id"] != 'None':
            orderquantity = getCurrentQuantityForAProduct(product_json['product_serial_number'][0])
            for i in orderquantity:
                quant = i[0]
            print(quant)

    product_sn = product_json['product_serial_number']
    product_sn = product_sn[0]

    product_rating_json = getProductRatingsJson(product_sn)
    product_rating_json = product_rating_json.json
    rating_score_li = product_rating_json['rating_score']
    print(product_rating_json)
    print(product_rating_json['rating_score'])
    no_of_ratings = len(rating_score_li)

    if rating_score_li == []:
        avg_rating_score = 0
    else:
        avg_rating_score = mean(rating_score_li)
        avg_rating_score = round(avg_rating_score)
        print("avg_rating_score", avg_rating_score)
    
    print("Offer flag: ", product_json['offer_flag'][0])
    print("Offer flag: ", product_json['offer_percent'][0])

    offer_price = 'None'
    if product_json['offer_flag'][0] == 1:
        offer_price = round((product_json['product_price'][0] - (product_json['product_price'][0] * product_json['offer_percent'][0]) / 100), 2)
        print(offer_price)
        
    return render_template('product/product_page.html', categories = categories.json, orderquantity=quant, \
                           category_name = cat_name, \
                           sub_category_name = sub_cat_name, \
                           sub_category_id = sub_category_id, \
                           category_id = category_id, \
                           product_id = product_json['product_id'], \
                           product_sn = product_sn, \
                           product_name = product_json['product_name'], \
                           product_price = product_json['product_price'], \
                           product_stock = product_json['stock'], \
                           product_main_image = product_json['image_id'], \
                           product_sec_image1 = li_sec_images[0], \
                           product_sec_image2 = li_sec_images[1], \
                           product_sec_image3 = li_sec_images[2], \
                           product_sec_image4 = li_sec_images[3], \
                           product_description = product_json['product_description'],\
                           avg_rating_score = avg_rating_score,\
                           no_of_ratings = no_of_ratings, \
                           range=range,\
                           seller = product_json['seller'],\
                           badge = product_json['badge'],\
                           offer_flag = product_json['offer_flag'][0], \
                           offer_price = offer_price, \
                           offer_percent = int(product_json['offer_percent'][0]))


def getProductJson(category_id, sub_category_id, product_id):
    spec_cat = getProductData(category_id, sub_category_id, product_id)
    
    response = app.response_class(
        response=json.dumps(spec_cat),
        status=200,
        mimetype='application/json'
    )

    return response

def getProductRatingsJson(product_sn):
    spec_cat = getProductRatings(product_sn)
    
    response = app.response_class(
        response=json.dumps(spec_cat),
        status=200,
        mimetype='application/json'
    )

    return response

# API to get names of all categories
@app.route('/getAllCategories',  methods=['GET'])
def getAllCategories():
    categories = getAllCategoriesList()
    response = app.response_class(
        response=json.dumps(categories),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/login')
def login():
    if request.args.get('error') is None:
        error = "False"
    else:
        error = request.args['error']
    return render_template('login/login.html', error=error)


@app.route('/userAccountLogin', methods=['POST'])
def userAccountLogin():
    username = request.form['username']
    password = request.form['password']
    user = validateCredentails(username, password)
    if user == "False":
        return redirect(url_for('login', error="True")) 
    else: 
        for item in user:
            session[item]=user[item]
        loginStatus = session["login_status"]
        print(loginStatus)
        return redirect('/')
    
@app.route("/signup")
def signup():
    return render_template('signup/signup.html')

@app.route("/sellersignup")
def sellersignup():
    return render_template('seller-signup/sellersignup.html')

@app.route("/useraccount")
def useraccount():
    if request.args.get('messages') is None:
        messages = ""
    else:
        messages = request.args['messages']
    if "login_status" not in session:
        return redirect("/login")
    elif session["login_status"] == "False":
        return redirect("/login")
    else:
        categories = getAllCategories()
        orders = getOrderHistory(session['user_id'][0])
        neworders = getOrderHistory(session['user_id'][0])
        orderWithItems = {}
        total = {}
        for i in neworders:
            print(i['order_id'])
            owi, order_total = getPlacedOrder(i['order_id'])
            orderWithItems[i['order_id']] = owi
            total[i['order_id']] = order_total

        return render_template('user-account/useraccount.html', categories=categories.json, user="None", orders=orders, orderWithItems=orderWithItems, total=total, messages=messages)

@app.route("/sellerpasswordreset")
def sellerpasswordreset():
    return render_template('password-reset/seller-password-reset.html')

@app.route("/userpasswordreset")
def userpasswordreset():
    return render_template('password-reset/user-password-reset.html')
    
@app.route('/search', methods=['POST'])
def search():
    query = request.form['search']
    result = getSearch(query)
    productList = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    categories = getAllCategories()
    return render_template('search/search.html', productList=productList.json, categories=categories.json)

@app.route('/register', methods=['POST'])
def userAccountRegistration():
    salutation = request.form['salutation']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    phonenumber = request.form['phonenumber']
    address = request.form['address']
    securityquestion = request.form['security-question']
    user = validateRegistration(salutation, firstname, lastname, email, password, phonenumber, address, securityquestion)
    print("user value", user)
    if user == "exists":
        return render_template('signup/signup.html', userexists="True")
    elif user["login_status"] == "True":
        for item in user:
            session[item] = user[item]
        return redirect('/')
    else:
        return render_template('signup/signup.html', error="True")

@app.route('/sellerregister', methods=['POST'])
def sellerAccountRegistration():
    sellername = request.form['sellername']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    securityquestion = request.form['security-question']
    seller = validateSellerRegistration(sellername, email, password, address, securityquestion)
    if seller == "exists" or seller == "False":
        return render_template('seller-signup/sellersignup.html', sellerexists="True")
    else:
        for item in seller:
            session[item] = seller[item]
        return redirect('/sellerAccount')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    key = []
    for item in session:
        print(item)
        key.append(item)
    for item in key:
        session.pop(item, None)
    session["login_status"] = 'False'
    return redirect('http://127.0.0.1:5000/')

@app.route('/seller-login')
def sellerLogin():
    return render_template('seller-login/seller-login.html', error="False")


@app.route('/sellerAccountLogin', methods=['POST'])
def sellerAccountLogin():
    username = request.form['username']
    password = request.form['password']
    user = validateSellerCredentails(username, password)
    if user != "False":
        for item in user:
            session[item] = user[item]
        return redirect('/sellerAccount')
    else:
        return render_template('seller-login/seller-login.html', error="True")

@app.route('/sellerAccount')
def sellerAccount():
    if "seller_login_status" not in session:
        loginStatus = "False"
    else:
        loginStatus = session["seller_login_status"]
    if loginStatus == "True":
        if request.args.get('messages') is None:
            messages = ""
        else:
            messages = request.args['messages']
        products = getSellerProducts(session["seller_id"])
        history = getSellerProductsHistory(session["seller_id"])
        award_data, total_sold = getSellerAwardData(session["seller_id"][0])
                
        return render_template('seller-account/selleraccount.html', products=products, history=history, award_data=award_data, total_sold=total_sold, messages=messages)
    else:
        return redirect('/seller-login')


@app.route('/sellerPasswordReset')
def sellerPasswordReset():
    return render_template('password-rest/seller-password-reset.html', error="False")


@app.route('/userPasswordReset')
def userPasswordReset():
    return render_template('password-rest/user-password-reset.html', error="False")

@app.route('/checkout')
def checkout():
    categories = getAllCategories()
    order, order_total = getOrder(session["user_id"])
    return render_template('checkout/checkout.html', categories=categories.json, order=order, order_total=order_total, error=False)


@app.route('/updateQuantity',  methods=['POST'])
def updateQuantity():
    if session["login_status"] == "True":
        quantity = request.form['quantity']
        product_serial_number = request.form['product_serial_number']
        print("quantity")
        print(quantity)
        print("p_s_n")
        print(product_serial_number)
        addItemToCart(product_serial_number, quantity)
        return redirect(redirect_url())
    else:
        return render_template('login/login.html', error="False")


@app.route('/deleteItem',  methods=['POST'])
def deleteItem():
    product_serial_number = request.form['product_serial_number']
    deleteItemFromCart(product_serial_number)
    return redirect('checkout')


def redirect_url(default='/'):
    return request.args.get('next') or \
           request.referrer 


@app.route('/placeOrder',  methods=['POST'])
def placeOrder():
    orderid = session["order_id"]
    orders, status = updateOrder()
    if status is False:
        categories = getAllCategories()
        order, order_total = getOrder(session["user_id"])
        return render_template('checkout/checkout.html', categories=categories.json, order=order, order_total=order_total, error=True)
    else:
        categories = getAllCategories()
        order, order_total = getPlacedOrder(orderid)
        return render_template('checkout/order-confirmation.html', order=order, order_total=order_total, categories=categories.json, orderid=orderid)

@app.route('/submitRatings', methods=['POST'])
def submit_ratings():
    rating_score = int(request.form['quantity'])
    product_serial_number = request.form['product_serial_number']
    user_id = session["user_id"][0]
       
    insertNewRatings(rating_score, product_serial_number, user_id, comments="")
    time.sleep(1)
    return redirect(url_for('useraccount', messages="Successfully updated ratings!")) 


@app.route('/addNewProduct', methods=['POST'])
def addNewProduct():
    productName = request.form['productName']
    productDescription = request.form['productDescription']
    category = request.form['topic']
    subcategory = request.form['chapter']
    productPrice = request.form['productPrice']
    stock = request.form['stock']
    offerpercent = request.form['offerpercent']
    inputFile = request.files.getlist('image')
    if request.form.get("sponsor"):
        sponsored = 1
    else:
        sponsored = 0
    image_id, secondary_images = uploadImageToDrive(inputFile)
    if offerpercent == "0":
        offerflag = False
    else: 
        offerflag = True
    seller_id = session["seller_id"][0]
    date = datetime.now().strftime("%d-%m-%Y")  
    product_id = 6 
    print("Form values", productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory, stock, image_id, category, product_id, secondary_images, sponsored)
    status = addNewProductFromSeller(productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory, stock, image_id, category, product_id, secondary_images, sponsored)
    status = "True"
    if status == "True":
        return redirect(url_for('sellerAccount', messages="Product added successfully!"))
    else:
        return redirect(url_for('sellerAccount', messages="Failed to add product, please try again!"))

@app.route('/updateOffer', methods=['POST'])   
def updateOffer():
    product_serial_number = request.form['product_serial_number']
    offer_percent = request.form['offerpercent']
    if float(offer_percent) > 0:
        offer_flag = True
    else:
        offer_flag = False
    status = updateProductOffers(product_serial_number, offer_flag, offer_percent)
    if status == True:
        return redirect(url_for('sellerAccount', messages="Offer updated successfully!"))
    else:
        return redirect(url_for('sellerAccount', messages="Failed to update offer, please try again!"))
    
@app.route('/editUserProfile')
def editUserProfile():
    categories = getAllCategories()
    return render_template('user-account/editPersonalInfo.html', error="False", categories=categories)

@app.route('/updatePersonalInfo', methods=['POST'])
def updatePersonalInfo():
    salutation = request.form['salutation']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    phonenumber = request.form['phonenumber']
    address = request.form['address']
    securityquestion = request.form['security-question']
    user = updatePersonalDetails(salutation, firstname, lastname, email, phonenumber, address, securityquestion)
    if user == "False":
        return redirect(url_for('editUserProfile', error="True"))
    else:
        print("user ", user["user_address"])
        session["user_address"] = user["user_address"]
        session["user_firstname"] = user["user_firstname"]
        session["user_lastname"] = user["user_lastname"]
        session["user_phone"] = user["user_phone"]
        session["user_salutation"] = user["user_salutation"]
        return redirect(url_for('useraccount', messages="Successfully updated personal infoamtion"))
    
@app.route('/reset-password', methods=['POST'])
def reset_password():
    username = request.form['email']
    security_answer = request.form['security_question']
    new_password = request.form['newPassword']

    # Check if the user exists and retrieve their account information
    user = verifyUserAccount(username, security_answer)
    print(user)
    if user is False:
        error_message = 'User not found or security answer is wrong, please try again.'
        return render_template('password-reset/user-password-reset.html', error_message=error_message)


    # Update the user's password in the database
    success = updateUserPassword(username, new_password)
    
    if success == "True":
        return redirect('/login')
    else:
        return redirect(redirect_url)
    
@app.route('/seller-reset-password', methods=['POST'])
def reset_seller_password():
    username = request.form['email']
    security_answer = request.form['security_question']
    new_password = request.form['newPassword']

    # Check if the user exists and retrieve their account information
    user = verifySellerAccount(username, security_answer)
    if user is False:
        error_message = 'Seller not found or security answer is wrong, please try again.'
        return render_template('password-reset/seller-password-reset.html', error_message=error_message)

    success = updateSellerPassword(username, new_password)
    
    if success == "True":
        return redirect('/login')
    else:
        return redirect(redirect_url())

@app.route('/messages')
def messages():
    if request.args.get('idx') is None:
        idx = 0
    else:
        idx = int(request.args['idx'])
    messages = ['Page Not Found!', 'Something went wrong, please try again later!', 'BadRequestKeyError: 400 Bad Request. Please provide all the details in the form!']
    try:
        return render_template('error-pages/messages.html', message=messages[idx])
    except IndexError:
        abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('messages', idx=0))

@app.errorhandler(500)
def page_not_found(error):
    return redirect(url_for('messages', idx=1))

@app.errorhandler(400)
def page_not_found(error):
    return redirect(url_for('messages', idx=2))

@app.route('/chat_session', methods=['GET', 'POST'])
def index():
    conn, cursor = create_chat_table()
    cursor = get_db_connection()
    
    cursor.execute("SELECT * FROM CHAT ORDER BY timestamp DESC")
    chat_messages = cursor.fetchall()
    chat_list = [list(message) for message in chat_messages]

    categories = getAllCategories()
    sellers = getAllSellers()
    
    try:
        if len(chat_list) == 0:
            message = ''
            seller_id = ''
            seller_name = ''
        else:
            if 'message' not in request.form:
                seller_id = int(request.form.get('selected_seller_id'))
                seller_name = str(request.form.get('selected_seller_name'))
                print("seller_id here2", seller_id)
                print("seller_name here2", seller_name)
                print(type(seller_id))
                print(type(seller_name))
                message = ''
            else:
                seller_id = int(request.form.get('selected_seller_id'))
                seller_name = str(request.form.get('selected_seller_name'))
                message = request.form['message']            
    except:
        message = ''
        seller_id = 0
        seller_name = ''

    # Insert the message into the database
    user_id = int(session['user_id'][0])
    user_name = str(session['user_firstname'][0]) + ' ' + str(session['user_lastname'][0])
    sender = user_name

    cursor.execute("INSERT INTO CHAT (user_id, user_name, seller_id, seller_name, sender, message) VALUES (?, ?, ?, ?, ?, ?)", (user_id, user_name, seller_id, seller_name, sender, message))
    conn.commit()
    
    chat_list = []
    try:
        select_query = "SELECT user_id, user_name, seller_id, seller_name, sender, message, timestamp FROM CHAT WHERE seller_id=" + str(seller_id) + " ORDER BY timestamp DESC"
        cursor.execute(select_query)
        chat_messages = cursor.fetchall()
        chat_messages = chat_messages[:-1]
    except:
        select_query = "SELECT user_id, user_name, seller_id, seller_name, sender, message, timestamp FROM CHAT ORDER BY timestamp DESC"
        print(select_query)
        cursor.execute(select_query)
        chat_messages = cursor.fetchall()
        chat_messages = chat_messages[:-1]

    chat_list = [list(message) for message in chat_messages]
    seen = set()
    unique_chat_list = [message for message in chat_list if tuple(message[:6]) not in seen and not seen.add(tuple(message[:6]))]
    chat_list = [message for message in unique_chat_list if message[5] != '']
    # print('chat_messages:', chat_list)   
    
    return render_template('chat_session/chat_session.html', categories=categories.json, \
                            chat_messages=chat_list, \
                            sellers=sellers, \
                            len=len, \
                            user_name=user_name, \
                            datetime=datetime, \
                            current_seller_id=seller_id)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
