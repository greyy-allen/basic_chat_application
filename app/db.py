from pymongo import MongoClient
from werkzeug.security import generate_password_hash

from .models import User

client = MongoClient("mongodb+srv://GreyTech:Kronos12@chatapp.2ebkk3a.mongodb.net/")
chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")