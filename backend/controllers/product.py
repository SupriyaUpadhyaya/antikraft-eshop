from backend.model import insertNewProduct, getCategoryId, getSubCategoryId, readSellerProducts, getProductRating, writeProductOffers, readSellerProductsHistory
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build
from io import BytesIO


def addNewProductFromSeller(productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory, stock, image_id, category, product_id, secondary_images, sponsored):
    category_ids = getCategoryId(category)
    for i in category_ids:
        category_id = i["category_id"]
    subcategory_ids = getSubCategoryId(subcategory)
    for i in subcategory_ids:
        subcategory_id = i["sub_serial_number"]
    status = insertNewProduct(productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory_id, stock, image_id, category_id, product_id, secondary_images, sponsored)
    return status


def uploadImageToDrive(inputFile) :
    scope = ["https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("isee-390607-511411524749.json", scope)
    drive_service = build("drive", "v3", credentials=credentials, cache_discovery=False)
    image_link = []
    for uploaded_file in inputFile:
        if uploaded_file.filename != '':
            buffer_memory = BytesIO()
            uploaded_file.save(buffer_memory)
            media_body = MediaIoBaseUpload(uploaded_file, uploaded_file.mimetype, resumable=True)
            folderid = '14CMpny02eYL2o-dzBuDDrBk2bxGMCw3I'
            file_metadata = {
                "name": uploaded_file.filename,
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader',
                'parents': [folderid]
            }
            returned_fields = "id, name, mimeType, webViewLink, exportLinks, webContentLink, parents"
            upload_response = drive_service.files().create(
                body=file_metadata, 
                media_body=media_body,  
                fields=returned_fields
            ).execute()
            url = "https://drive.google.com/uc?export=view&id=" + upload_response['id']
            image_link.append(url)
            permission = {
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'}
            drive_service.permissions().create(fileId=upload_response['id'],body=permission).execute()
    image_id = image_link[0]
    secondary_images = image_link[1] + ";" + image_link[2] + ";" + image_link[3] + ";" + image_link[4]
    return image_id, secondary_images


def getSellerProducts(sellerid):
    data = readSellerProducts(sellerid)
    keyList = ["product_serial_number", "product_name", "product_description", "seller_id", "posted_date", "offer_flag", "offer_percent", "product_price", "sub_category_id", "stock", "image_id", "category_id", "product_id", "product_url", "rating", "sponsored"]
    products_list = []
    for row in data:
        products = {key: [] for key in keyList}
        products['product_serial_number'].append(row["product_serial_number"])
        products['product_name'].append(row["product_name"])
        products['product_description'].append(row["product_description"])
        products['posted_date'].append(row["posted_date"])
        products['offer_flag'].append(row["offer_flag"])
        products['offer_percent'].append(row["offer_percent"])
        products['product_price'].append(row["product_price"])
        products['sub_category_id'].append(row["sub_category_id"])
        products['stock'].append(row["stock"])
        products['image_id'].append(row["image_id"])
        products['category_id'].append(row["category_id"])
        products['product_id'].append(row["product_id"])
        products['sponsored'].append(row['sponsored'])
        url = "http://127.0.0.1:5000/product?categoryid=" + str(products['category_id'][0]) + "&subcategoryid=" + str(products['sub_category_id'][0]) + "&product_serial_number=" + str(products['product_serial_number'][0])
        products['product_url'].append(url)
        rating = getProductRating(row["product_serial_number"])
        avg = 0
        total = 0
        i = 0
        for rr in rating:
            total += rr['rating_score']
            i += 1
        if total != 0:
            avg = total / i
        products['rating'].append(avg)
        products_list.append(products)
    if products_list is not None:
        return products_list
    else:
        return "ERROR"
    
def getSellerProductsHistory(sellerid):
    data = readSellerProductsHistory(sellerid)
    keyList = ["product_serial_number", "product_name", "product_description", "seller_id", "posted_date", "offer_flag", "offer_percent", "product_price", "sub_category_id", "stock", "image_id", "category_id", "product_id", "product_url", "rating", "sponsored"]
    products_list = []
    for row in data:
        products = {key: [] for key in keyList}
        products['product_serial_number'].append(row["product_serial_number"])
        products['product_name'].append(row["product_name"])
        products['product_description'].append(row["product_description"])
        products['posted_date'].append(row["posted_date"])
        products['offer_flag'].append(row["offer_flag"])
        products['offer_percent'].append(row["offer_percent"])
        products['product_price'].append(row["product_price"])
        products['sub_category_id'].append(row["sub_category_id"])
        products['stock'].append(row["stock"])
        products['image_id'].append(row["image_id"])
        products['category_id'].append(row["category_id"])
        products['product_id'].append(row["product_id"])
        products['sponsored'].append(row['sponsored'])
        url = "http://127.0.0.1:5000/product?categoryid=" + str(products['category_id'][0]) + "&subcategoryid=" + str(products['sub_category_id'][0]) + "&product_serial_number=" + str(products['product_serial_number'][0])
        products['product_url'].append(url)
        rating = getProductRating(row["product_serial_number"])
        avg = 0
        total = 0
        i = 0
        for rr in rating:
            total += rr['rating_score']
            i += 1
        if total != 0:
            avg = total / i
        products['rating'].append(avg)
        products_list.append(products)
    if products_list is not None:
        return products_list
    else:
        return "ERROR"
    
def updateProductOffers(product_serial_number, offer_flag, offer_percent):
    status = writeProductOffers(product_serial_number, offer_flag, offer_percent)
    return status