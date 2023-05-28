from flask import Flask
from backend.model import readOperation, readOperationProductList, searchProductList, readOperationCategory, readOperationCategoryImages

app = Flask(__name__)


def getAllCategoriesList():
    data = {}
    data = readOperation("CATEGORY", "category_name")
    return data

def getSpecificCategoryList(category_id):
    data = {}
    data = readOperationCategory("CATEGORY", category_id)
        
    return data

def getSpecificCategoryImages(category_id):
    data = {}
    data = readOperationCategoryImages("SUB_CATEGORY", category_id)
        
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


