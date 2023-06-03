import json
from flask import Flask, jsonify, redirect, render_template, request, session
from backend.controller import getAllCategoriesList, getSearch, getSpecificCategoryList, getSpecificCategoryImages, getSubCategoryProductList, getProductData
from backend.controllers.account import validateCredentails, validateRegistration, validateSellerRegistration, validateSellerCredentails
from backend.controllers.cart import getOrder, addItemToCart, deleteItemFromCart, getCurrentQuantityForAProduct

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def home():
    categories = getAllCategories()
    session["start"] = True
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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# To render sub category HTML page when user clicks on category page tiles
@app.route("/product")
def getSpecificProduct():
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
    if session["start"] == True:
        quant = 1
    elif session["order_id"] != 'None':
        orderquantity = getCurrentQuantityForAProduct(product_json['product_serial_number'][0])
        for i in orderquantity:
            quant = i[0]
        print(quant)
    
    return render_template('product/product_page.html', categories = categories.json, orderquantity=quant, \
                           category_name = cat_name, \
                           sub_category_name = sub_cat_name, \
                           sub_category_id = sub_category_id, \
                           category_id = category_id, \
                           product_id = product_json['product_id'], \
                           product_sn = product_json['product_serial_number'], \
                           product_name = product_json['product_name'], \
                           product_price = product_json['product_price'], \
                           product_stock = product_json['stock'], \
                           product_main_image = product_json['image_id'], \
                           product_sec_image1 = li_sec_images[0], \
                           product_sec_image2 = li_sec_images[1], \
                           product_sec_image3 = li_sec_images[2], \
                           product_sec_image4 = li_sec_images[3], \
                           product_description = product_json['product_description'], \
                           range=range)


def getProductJson(category_id, sub_category_id, product_id):
    spec_cat = getProductData(category_id, sub_category_id, product_id)
    
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
        session["start"] = False
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
    return render_template('user-account/useraccount.html', categories=categories.json, user="None")

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
        return render_template('homepage/home.html', categories=categories.json, loginStatus=seller_login_status)
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
    loginStatus = session["login_status"]
    print(loginStatus)
    categories = getAllCategories()
    if loginStatus == "True":
        return render_template('homepage/home.html', categories=categories.json)
    else:
        return render_template('login/login.html', categories=categories.json, error="True")


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
    return render_template('checkout/checkout.html', categories=categories.json, order=order, order_total=order_total)


@app.route('/updateQuantity',  methods=['POST'])
def updateQuantity():
    if session["start"] == False:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
