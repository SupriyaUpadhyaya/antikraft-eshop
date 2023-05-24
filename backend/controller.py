from flask import Flask
from backend.model import readOperation, readOperationProductList, searchProductList

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


def getSearch(qTerm):
    if not qTerm:
        print("You did not search for anything")
        return "Error"
    elif qTerm:
        searchResult = searchProductList(qTerm)
        return searchResult


