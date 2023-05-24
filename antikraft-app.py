import json
from flask import Flask, jsonify, render_template, request
from backend.controller import getAllCategoriesList, getSubCategoryProductsList, getCategoryProductsList, getCategoryProductsList

app = Flask(__name__)


@app.route("/")
def home():
    categories = getAllCategories()
    return render_template('homepage/home.html', categories=categories.json)

# To render category HTML page when user clicks on category in top nav 
@app.route("/category")
def getCategory():
    categories = getAllCategories()
    print(categories.json)
    return render_template('category/category.html', categories=categories.json)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)