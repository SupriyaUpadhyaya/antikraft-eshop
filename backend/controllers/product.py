from backend.model import insertNewProduct, getCategoryId, getSubCategoryId
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build
from io import BytesIO


def addNewProductFromSeller(productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory, stock, image_id, category, product_id, secondary_images):
    category_ids = getCategoryId(category)
    for i in category_ids:
        category_id = i["category_id"]
    subcategory_ids = getSubCategoryId(subcategory)
    for i in subcategory_ids:
        subcategory_id = i["sub_serial_number"]
    status = insertNewProduct(productName, productDescription, seller_id, date, offerflag, offerpercent, productPrice, subcategory_id, stock, image_id, category_id, product_id, secondary_images)
    return status


def uploadImageToDrive(inputFile) :
    scope = ["https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("isee-390607-511411524749.json", scope)
    drive_service = build("drive", "v3", credentials=credentials, cache_discovery=False)
    image_link = []
    for uploaded_file in inputFile:
        if uploaded_file.filename != '':
            print(uploaded_file.filename)
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
            print(upload_response)
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
