from flask import Flask
from backend.model import readOperation, readOperationProductList

app = Flask(__name__)


def getAllCategoriesList():
    data = {}
    data = readOperation("CATEGORY", "category_name")
    return data


def getCategoryProductsList(catId):
    data = {}
    data = readOperationProductList("PRODUCT", "*", catId, 0)
    return data


def getSubCategoryProductsList(catId, subCatId):
    data = {}
    data = readOperationProductList("PRODUCT", "*", catId, subCatId)
    return data


