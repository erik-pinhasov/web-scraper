import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["scraper"]

brands_col = db["brands"]
brands_col.create_index(["brand"], unique=True)

models_col = db["models"]
models_col.create_index(
    [("brand", pymongo.ASCENDING),
     ("model", pymongo.ASCENDING)],
    unique=True
)

ksp_col = db["ksp"]
ksp_col.create_index(
    [("brand", pymongo.ASCENDING),
     ("model", pymongo.ASCENDING)],
    unique=True
)

ivory_col = db["ivory"]
ivory_col.create_index(
    [("brand", pymongo.ASCENDING),
     ("model", pymongo.ASCENDING),
     ("storage", pymongo.ASCENDING),
     ("ram", pymongo.ASCENDING)],
    unique=True
)

