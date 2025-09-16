from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_client = MongoClient(os.getenv("MONGO_URI"))

pets_db = mongo_client["pet_gallery"]

pets_collection = pets_db["FavouritePets"]