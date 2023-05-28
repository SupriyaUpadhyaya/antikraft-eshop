from backend.model import readOperation, readOperationProductList, searchProductList


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
            url = "http://127.0.0.1:5000/category?productid=" + str(row["product_id"])
            block["product_id"] = row["product_id"]
            block["product_name"] = row["product_name"]
            block["product_description"] = row["product_description"]
            block["image_id"] = row["image_id"]
            block["url"] = url
            products[i] = block
            i += 1
        return products


