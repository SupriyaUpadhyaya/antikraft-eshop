import linecache
from backend.model import insertNewProduct, getCategoryId, getSubCategoryId, readSellerProducts, getProductRating, writeProductOffers, readSellerProductsHistory, readOffers, readAllOffers, specialCategoryProductList
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build
from io import BytesIO
from cryptography.fernet import Fernet


def encrypt(filename):
    key = Fernet.generate_key()
    with open("config/key.key", "wb") as key_file:
        key_file.write(key)
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    return True


def decrypt():
    key = open("config/key.key", "rb").read()
    f = Fernet(key)
    filename = "config/isee-390607-511411524749.json"
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open("config/drive.json", "wb") as file:
        file.write(decrypted_data)
    return True


def addNewProductFromSeller(productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory, stock, image_id, category, product_id, secondary_images, sponsored, offer_iamge_id):
    category_ids = getCategoryId(category)
    for i in category_ids:
        category_id = i["category_id"]
    subcategory_ids = getSubCategoryId(subcategory)
    for i in subcategory_ids:
        subcategory_id = i["sub_category_id"]
    status = insertNewProduct(productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory_id, stock, image_id, category_id, product_id, secondary_images, sponsored, offer_iamge_id)
    return status


def uploadImageToDrive(inputFile) :
    scope = ["https://www.googleapis.com/auth/drive"]
    decrypt()
    credentials = ServiceAccountCredentials.from_json_keyfile_name("config/drive.json", scope)
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


def uploadOffersImageToDrive(inputFile) :
    scope = ["https://www.googleapis.com/auth/drive"]
    decrypt()
    credentials = ServiceAccountCredentials.from_json_keyfile_name("config/drive.json", scope)
    drive_service = build("drive", "v3", credentials=credentials, cache_discovery=False)
    image_link = []
    for uploaded_file in inputFile:
        print("uploaded_file.filename ", uploaded_file.filename)
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
    return image_id


def getSellerProducts(sellerid):
    data = readSellerProducts(sellerid)
    keyList = ["product_serial_number", "product_name", "product_description", "seller_id", "posted_date", "offer_flag", "offer_id", "product_price", "sub_category_id", "stock", "image_id", "category_id", "product_id", "product_url", "rating", "sponsored", "offer_image_id", "offer_percent", "old_offers"]
    products_list = []
    for row in data:
        products = {key: [] for key in keyList}
        products['product_serial_number'].append(row["product_serial_number"])
        products['product_name'].append(row["product_name"])
        products['product_description'].append(row["product_description"])
        products['posted_date'].append(row["posted_date"])
        products['offer_flag'].append(row["offer_flag"])
        products['offer_id'].append(row["offer_id"])
        products['product_price'].append(row["product_price"])
        products['sub_category_id'].append(row["sub_category_id"])
        products['stock'].append(row["stock"])
        products['image_id'].append(row["image_id"])
        products['category_id'].append(row["category_id"])
        products['product_id'].append(row["product_id"])
        products['sponsored'].append(row['sponsored'])
        url = "/product?categoryid=" + str(products['category_id'][0]) + "&subcategoryid=" + str(products['sub_category_id'][0]) + "&product_serial_number=" + str(products['product_serial_number'][0])
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
        if products['offer_flag'][0] != 0:
            offers = readOffers(str(products['product_serial_number'][0]), str(products['offer_id'][0]))
            for item in offers:
                products['offer_percent'].append(item['offer_percent'])
                products['offer_image_id'].append(str(item['offer_image_id']))
        else:
            products['offer_percent'].append(0)
            products['offer_image_id'].append(0)
        allOffers = readAllOffers(str(products['product_serial_number'][0]))
        allOldOffers = []
        keys = ["offer_id", "offer_percent", "offer_image_id"]
        for items in allOffers:
            offers = {k: [] for k in keys}
            offers['offer_id'].append(items['offer_id'])
            offers['offer_percent'].append(items['offer_percent'])
            offers['offer_image_id'].append(items['offer_image_id'])
            allOldOffers.append(offers)
        products['old_offers'].append(allOldOffers)
        products_list.append(products)
    if products_list is not None:
        return products_list
    else:
        return "ERROR"
    
def getSellerProductsHistory(sellerid):
    data = readSellerProductsHistory(sellerid)
    keyList = ["product_serial_number", "product_name", "product_description", "seller_id", "posted_date", "offer_flag", "offer_percent", "product_price", "sub_category_id", "stock", "image_id", "category_id", "product_id", "product_url", "rating", "sponsored", "offer_id", "offer_image_id", "old_offers"]
    products_list = []
    for row in data:
        products = {key: [] for key in keyList}
        products['product_serial_number'].append(row["product_serial_number"])
        products['product_name'].append(row["product_name"])
        products['product_description'].append(row["product_description"])
        products['posted_date'].append(row["posted_date"])
        products['offer_flag'].append(row["offer_flag"])
        products['offer_id'].append(row["offer_id"])
        products['product_price'].append(row["product_price"])
        products['sub_category_id'].append(row["sub_category_id"])
        products['stock'].append(row["stock"])
        products['image_id'].append(row["image_id"])
        products['category_id'].append(row["category_id"])
        products['product_id'].append(row["product_id"])
        products['sponsored'].append(row['sponsored'])
        url = "/product?categoryid=" + str(products['category_id'][0]) + "&subcategoryid=" + str(products['sub_category_id'][0]) + "&product_serial_number=" + str(products['product_serial_number'][0])
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
        if products['offer_flag'][0] != 0:
            offers = readOffers(str(products['product_serial_number'][0]), str(products['offer_id'][0]))
            for item in offers:
                products['offer_percent'].append(item['offer_percent'])
                products['offer_image_id'].append(str(item['offer_image_id']))
        else:
            products['offer_percent'].append(0)
            products['offer_image_id'].append(0)
        allOffers = readAllOffers(str(products['product_serial_number'][0]))
        allOldOffers = []
        keys = ["offer_id", "offer_percent", "offer_image_id"]
        for items in allOffers:
            offers = {k: [] for k in keys}
            offers['offer_id'].append(items['offer_id'])
            offers['offer_percent'].append(items['offer_percent'])
            offers['offer_image_id'].append(items['offer_image_id'])
            allOldOffers.append(offers)
        products['old_offers'].append(allOldOffers)
        products_list.append(products)
    if products_list is not None:
        return products_list
    else:
        return "ERROR"


def getspecialcategory(id):
    query = linecache.getline(r"backend/controllers/queries.txt", int(id))
    data = specialCategoryProductList(query)
    products = {}
    i = 1
    for row in data:
        block = {}
        url = "/product?categoryid=" + str(row["category_id"]) + "&subcategoryid=" +  str(row["sub_category_id"]) + "&product_serial_number=" + str(row["product_serial_number"])
        block["product_serial_number"] = row["product_serial_number"]
        block["product_name"] = row["product_name"]
        block["product_description"] = row["product_description"]
        block["image_id"] = row["image_id"]
        block["product_price"] = row["product_price"]
        block["sponsored"] = row["sponsored"]
        block["url"] = url
        block['offer_flag'] = row["offer_flag"]
        if block['offer_flag'] != 0:
            offers = readOffers(block['product_serial_number'], row['offer_id'])
            for item in offers:
                block['offer_percent'] = item['offer_percent']
                block['offer_image_id'] = item['offer_image_id']
                offer_price = round((block['product_price'] - (block['product_price'] * block['offer_percent']) / 100), 2)
                block['offer_price'] = offer_price
        else:
            block['offer_percent'] = 0
            block['offer_image_id'] = 0
            block['offer_price'] = 'None'
        products[i] = block
        i += 1
    return products
    
def updateProductOffers(product_serial_number, offer_flag, offer_percent, offer_image_id):
    status = writeProductOffers(product_serial_number, offer_flag, offer_percent, offer_image_id)
    return status
