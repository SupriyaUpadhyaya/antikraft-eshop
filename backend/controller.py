from flask import Flask
from backend.model import readOperation, searchProductList, readOperationCategory, readOperationCategoryImages, \
                          readOperationSubCategory, readOperationProduct, readOperationProductRatings

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

def getSubCategoryProductList(category_id, sub_category_id):
    data = {}
    data = readOperationSubCategory("PRODUCT", category_id, sub_category_id)
        
    return data

def getProductData(category_id, sub_category_id, product_serial_number):
    data = {}
    data = readOperationProduct("PRODUCT", category_id, sub_category_id, product_serial_number)
        
    return data

def getProductRatings(product_serial_number):
    data = {}
    data = readOperationProductRatings("RATINGS", product_serial_number)
        
    return data

def getSearch(query):
    if not query:
        print("You did not search for anything")
        return "Error"
    elif query:
        data = searchProductList(query)
        
        products = {}
        i = 1
        for row in data:
            block = {}
            url = "http://127.0.0.1:5000/product?categoryid=" + str(row["category_id"]) + "&subcategoryid=" +  str(row["sub_category_id"]) + "&product_serial_number=" + str(row["product_serial_number"])
            block["product_serial_number"] = row["product_serial_number"]
            block["product_name"] = row["product_name"]
            block["product_description"] = row["product_description"]
            block["image_id"] = row["image_id"]
            block["product_price"] = row["product_price"]
            block["url"] = url
            products[i] = block
            i += 1
        return products


