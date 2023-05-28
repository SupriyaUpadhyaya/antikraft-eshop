import json
from flask import Flask, jsonify, render_template, request
from backend.controller import getAllCategoriesList, getSearch, getSpecificCategoryList, getSpecificCategoryImages

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
    return render_template('category/category_landing_page.html', categories=categories.json, row_val=row_val.json, image_list=db_images['sub_category_image_id'], sub_cat_list=db_images['sub_category_name'])

def getSpecificCategoryRow(qTerm):
    spec_cat = getSpecificCategoryList(qTerm)
    
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

@app.route("/login")
def login():
    return render_template('login/login.html')


@app.route("/signup")
def signup():
    return render_template('signup/signup.html')

@app.route('/search/', methods=['GET'])
def search():
    qTerm = request.args.get('s')
    productList = getSearch(qTerm)
    return render_template('search.html', productList=productList.json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)