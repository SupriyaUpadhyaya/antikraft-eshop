from datetime import datetime
import json
from statistics import mean
from flask import Flask, redirect, render_template, request, session
from backend.controller import getAllCategoriesList, getSearch, getSpecificCategoryList, getSpecificCategoryImages, getSubCategoryProductList, getProductData, getProductRatings
from backend.controllers.account import validateCredentails, validateRegistration, validateSellerRegistration, validateSellerCredentails, getOrderHistory
from backend.controllers.cart import getOrder, addItemToCart, deleteItemFromCart, getCurrentQuantityForAProduct, updateOrder, getPlacedOrder
from backend.controllers.product import addNewProductFromSeller, uploadImageToDrive
from backend.model import insertNewRatings
import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def home():
    if len(session) == 0:
        session["login_status"] = 'False'
    categories = getAllCategories()
    return render_template('homepage/home.html', categories=categories.json, user="None")


# To render category HTML page when user clicks on category in top nav 
@app.route("/category")
def getSpecificCategory():
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
    sub_category_id = request.args.get('subcategoryid')
    category_id = request.args.get('categoryid')
    
    sub_cat_product_json = getSubCategoryJson(category_id, sub_category_id)
    category_table_row = getSpecificCategoryRow(category_id)
    sub_cat_json = sub_cat_product_json.json
    sub_cat_name = getSpecificCategoryImages(category_id)
    sub_cat_name = sub_cat_name['sub_category_name'][int(sub_category_id)-1]
    categories = getAllCategories()
    return render_template('subcategory/subcategory_landing_page.html', categories = categories.json, \
                           category_name = category_table_row.json['category_name'], \
                           sub_category_name = sub_cat_name, \
                           product_count = len(sub_cat_json['category_id']), \
                           product_name_list = sub_cat_json['product_name'], \
                           product_image_list = sub_cat_json['image_id'], \
                           product_price_list = sub_cat_json['product_price'], \
                           product_id_list = sub_cat_json['product_id'], \
                           sub_category_id = sub_category_id, \
                           category_id = category_id, \
                           range=range)

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
    if len(session) == 0:
        session["login_status"] = 'False'
    sub_category_id = request.args.get('subcategoryid')
    category_id = request.args.get('categoryid')
    product_id = request.args.get('productid')
    categories = getAllCategories()
    category_table_row = getSpecificCategoryRow(category_id)
    cat_name = category_table_row.json['category_name']

    sub_cat_name = getSpecificCategoryImages(category_id)
    sub_cat_name = sub_cat_name['sub_category_name'][int(sub_category_id)-1]    

    product_json = getProductJson(category_id, sub_category_id, product_id)
    product_json = product_json.json

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
        offer_price = (product_json['product_price'][0] - (product_json['product_price'][0] * product_json['offer_percent'][0]) / 100)
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
    return render_template('login/login.html', error="False")


@app.route('/userAccountLogin', methods=['POST'])
def userAccountLogin():
    username = request.form['username']
    password = request.form['password']
    user = validateCredentails(username, password)
    for item in user:
        session[item]=user[item]
    loginStatus = session["login_status"]
    print(loginStatus)
    categories = getAllCategories()
    if loginStatus == "True":
        return render_template('homepage/home.html', categories=categories.json)
    else:
        return render_template('login/login.html', categories=categories.json, error="True")


@app.route("/signup")
def signup():
    return render_template('signup/signup.html')

@app.route("/sellersignup")
def sellersignup():
    return render_template('seller-signup/sellersignup.html')

@app.route("/useraccount")
def useraccount():
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

    return render_template('user-account/useraccount.html', categories=categories.json, user="None", orders=orders, orderWithItems=orderWithItems, total=total)

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
    user = validateRegistration(salutation, firstname, lastname, email, password, phonenumber)
    for item in user:
        session[item] = user[item]
    login_status = session["login_status"]
    categories = getAllCategories()
    print("Login status")
    print(login_status)
    if login_status == "True":
        return render_template('homepage/home.html', categories=categories.json)
    else:
        return render_template('signup/signup.html', categories=categories.json, error ="True")

@app.route('/sellerregister', methods=['POST'])
def sellerAccountRegistration():
    sellername = request.form['sellername']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    seller = validateSellerRegistration(sellername, email, password, address)
    for item in seller:
        session[item] = seller[item]
    seller_login_status = session["seller_login_status"]
    categories = getAllCategories()
    print("seller Login status")
    print(seller_login_status)
    if seller_login_status == "True":
        return render_template('seller-account/selleraccount.html', categories=categories.json, loginStatus=seller_login_status)
    else:
        return render_template('seller-signup/sellersignup.html', categories=categories.json, loginStatus=seller_login_status)


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
    for item in user:
        session[item]=user[item]
    loginStatus = session["seller_login_status"]
    print(loginStatus)
    categories = getAllCategories()
    if loginStatus == "True":
        return render_template('seller-account/selleraccount.html', categories=categories.json)
    else:
        return render_template('seller-login/seller-login.html', categories=categories.json, error="True")

@app.route('/sellerAccount')
def sellerAccount():
    if "seller_login_status" not in session:
        loginStatus = "False"
    else:
        loginStatus = session["seller_login_status"]
    if loginStatus == "True":
        return render_template('seller-account/selleraccount.html')
    else:
        return render_template('seller-login/seller-login.html')


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
    # print(rating_score)
    # print(product_serial_number)
    user_id = session["user_id"][0]
    # print(user_id)
    
    insertNewRatings(rating_score, product_serial_number, user_id, comments="")
        
    time.sleep(1)
    return redirect('useraccount') #render_template_string('<script>alert("{{ message }}");</script>', message=message)


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
    image_id, secondary_images = uploadImageToDrive(inputFile)
    if offerpercent == "0":
        offerflag = False
    else: 
        offerflag = True
    seller_id = session["seller_id"][0]
    date = datetime.now().strftime("%d-%m-%Y")  
    product_id = 6 
    print("Form values", productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory, stock, image_id, category, product_id, secondary_images)
    status = addNewProductFromSeller(productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory, stock, image_id, category, product_id, secondary_images)
    status = "True"
    if status == "True":
        return render_template('seller-account/selleraccount.html', addProdError="False")
    else:
        return render_template('seller-account/selleraccount.html', addProdError="True")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
