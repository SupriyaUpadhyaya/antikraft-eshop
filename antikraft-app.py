import json
from flask import Flask, jsonify, render_template, request

from backend.controller import getAllCategoriesList, getSearch, getSpecificCategoryList, getSpecificCategoryImages, getSubCategoryProductList
from backend.controllers.account import validateCredentails, validateRegistration

app = Flask(__name__)

@app.route("/")
def home():
    categories = getAllCategories()
    return render_template('homepage/home.html', categories=categories.json)


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
    return render_template('subcategory/subcategory_landing_page.html', categories=categories.json, \
                           category_name=category_table_row.json['category_name'], \
                           sub_category_name=sub_cat_name, \
                           sub_cat_product_list=sub_cat_json['product_name'], \
                           product_image_list=sub_cat_json['image_id'])

def getSubCategoryJson(category_id, sub_category_id):
    spec_cat = getSubCategoryProductList(category_id, sub_category_id)
    
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
    return render_template('login/login.html')


@app.route('/userAccountLogin', methods=['POST'])
def userAccountLogin():
    username = request.form['username']
    password = request.form['password']
    loginStatus = validateCredentails(username, password)
    categories = getAllCategories()
    print("Login status")
    print(loginStatus)
    if loginStatus == "True":
        return render_template('homepage/home.html', categories=categories.json, loginStatus=loginStatus)
    else:
        return render_template('login/login.html', categories=categories.json, loginStatus=loginStatus)


@app.route("/signup")
def signup():
    return render_template('signup/signup.html')

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
    registration_status = validateRegistration(salutation, firstname, lastname, email, password, phonenumber)
    categories = getAllCategories()
    print("Login status")
    print(registration_status)
    if registration_status == "True":
        return render_template('homepage/home.html', categories=categories.json, loginStatus=registration_status)
    else:
        return render_template('login/login.html', categories=categories.json, loginStatus=registration_status)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
