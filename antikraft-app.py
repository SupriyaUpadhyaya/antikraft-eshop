import json
from flask import Flask, jsonify, render_template, request
from backend.controller import getAllCategoriesList, getSubCategoryProductsList, getCategoryProductsList, getCategoryProductsList

app = Flask(__name__)


@app.route("/")
def home():
    categories = getAllCategories()
    return render_template('base.html', categories=categories.json)

# To render category HTML page when user clicks on category in top nav 
@app.route("/category")
def getCategory():
    catId = int(request.args.get('categoryid'))
    products = getCategoryProductsList(catId)
    response = app.response_class(
        response=json.dumps(products),
        status=200,
        mimetype='application/json'
    )
    return render_template('category/category.html', categories=response.json)

# To render category HTML page when user clicks on sub-category in top nav 
@app.route("/subcategory")
def getSubCategory():
    catId = int(request.args.get('categoryid'))
    subCatId = int(request.args.get('subCategoryid'))
    categories = getSubCategoryProductsList(catId, subCatId)
    response = app.response_class(
        response=json.dumps(categories),
        status=200,
        mimetype='application/json'
    )
    return render_template('category/category.html', categories=response.json)

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

# API to get product list for a specific category
@app.route('/getCatProducts',  methods=['GET'])
def getCatProducts():
    catId = int(request.args.get('categoryid'))
    products = getCategoryProductsList(catId)
    response = app.response_class(
        response=json.dumps(products),
        status=200,
        mimetype='application/json'
    )
    return response

# API to get product list for a specific sub category of a category
@app.route('/getSubCategoryProducts',  methods=['GET'])
def getSubCategoryProducts():
    catId = int(request.args.get('categoryid'))
    subCatId = int(request.args.get('subCategoryid'))
    categories = getSubCategoryProductsList(catId, subCatId)
    response = app.response_class(
        response=json.dumps(categories),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/login")
def login():
    return render_template('login/login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)