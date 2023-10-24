from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from util.text_formatter import format_model_name

client = MongoClient()
database = client['scraper']


def execute_insert(col, doc):
    collection = database[col]
    result = None
    result_doc = doc.copy()
    result_doc.pop('_id', None)
    try:
        result = collection.insert_one(doc)
        print(f"Added successfully to Collection:{col} for document: {result_doc}")
    except DuplicateKeyError:
        if result:
            query = {"_id": result.inserted_id}
            update_doc = {"$set": doc}
            collection.update_one(query, update_doc, upsert=True)
            print(f"Updated successfully in Collection: {col} for document: {result_doc}")
        else:
            print(f"No changes for document: {result_doc}")


def pre_action(col_name, doc, opt=None):
    col = database[col_name]
    brand = doc.get('brand').lower()
    model = doc.get('model')

    doc['brand'] = brand
    doc.update({'model': format_model_name(brand, model)} if model is not None else {})
    return col.find(doc, opt)


def add_brand(brand):
    brand_doc = {"brand": brand.lower()}
    execute_insert("brands", brand_doc)


def add_model(brand, model):
    brand_exist = pre_action("brands", {"brand": brand})
    if not brand_exist:
        add_brand(brand)

    model_doc = {"brand": brand.lower(), "model": model.lower()}
    execute_insert("models", model_doc)


def add_product(brand, url, col, model=None, storage=None, ram=None):
    product_doc = {"brand": brand}
    product_doc.update({"model": model} if model is not None else {})
    model_exist = pre_action("brands", product_doc)

    if not model_exist:
        add_model(brand, model)

    product_doc.update({'storage': storage} if storage is not None else {})
    product_doc.update({'ram': ram} if ram is not None else {})

    product_doc['url'] = url
    execute_insert(col, product_doc)


def fetch_data(col, brand, model=None):
    query = {"brand": brand, "model": model} if model else {"brand": brand}
    fields = {"_id": 0, "brand": 1, "storage": 1, "ram": 1, "url": 1}
    return list(pre_action(col, query, fields))
