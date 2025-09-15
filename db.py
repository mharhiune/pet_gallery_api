from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# connect to Mongo Atlas Cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))

# Acess database
event_manager_db = mongo_client["event_manager_db"]

# Pick a collection to operate on
events_collection = event_manager_db["events"]