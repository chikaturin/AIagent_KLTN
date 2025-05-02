from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_DB_URI")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    client.server_info()
    print("✅ Kết nối MongoDB thành công.")
except Exception as e:
    print("❌ Kết nối MongoDB thất bại:", e)
    exit()

db = client["Scheduler"]


def get_db():
    return db
