import json
from flask import Flask, jsonify, render_template
from backend.controller import getAllCategoriesList

app = Flask(__name__)


@app.route("/")
def antiqkraft():
    categories = getAllCategories()
    print(categories.json)
    return render_template('base.html', categories=categories.json)

@app.route('/getAllCategories',  methods=['GET'])
def getAllCategories():
    categories = getAllCategoriesList()
    response = app.response_class(
        response=json.dumps(categories),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)