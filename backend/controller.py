from flask import Flask
from backend.model import readOperation

app = Flask(__name__)


def getAllCategoriesList():
    data = {}
    data = readOperation("CATEGORY", "category_name")
    return data



