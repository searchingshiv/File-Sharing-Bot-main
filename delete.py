from pyrogram import Client
from pyrogram.raw import functions
import schedule
import time
from pymongo import MongoClient
from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT,DB_URI,DB_NAME

# Replace with your own values
api_id = APP_ID
api_hash = API_HASH
bot_token = TG_BOT_TOKEN
mongo_uri = DB_URI
database_name = DB_NAME
collection_name = "user_ids_to_be_deleted"

app = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

mongo_client = MongoClient(mongo_uri)
db = mongo_client[database_name]
user_ids_collection = db[collection_name]

async def delete_private_chat(user_id):
    try:
        await app.send(
            functions.messages.DeleteChat(peer=user_id)
        )
        print(f"Private chat with user {user_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting private chat with user {user_id}: {e}")

def add_user_id_to_db(user_id):
    # Check if the user ID is already present in the database
    existing_user = user_ids_collection.find_one({"user_id": user_id})
    if existing_user:
        print(f"User ID {user_id} is already in the database.")
    else:
        # Add the user ID to the database
        user_ids_collection.insert_one({"user_id": user_id})
        print(f"User ID {user_id} added to the database.")

def get_user_ids_from_db():
    return [user_id['user_id'] for user_id in user_ids_collection.find()]

def delete_chats():
    user_ids_to_delete = get_user_ids_from_db()
    for user_id in user_ids_to_delete:
        delete_private_chat(user_id)

if __name__ == "__main__":
    with app:
        # Add user IDs to MongoDB when the bot starts
        for user_id in ["USER_ID_1", "USER_ID_2"]:
            add_user_id_to_db(user_id)

        # Schedule deletion at 12:00 AM every day
        schedule.every().day.at("21:30").do(delete_chats)

        while True:
            schedule.run_pending()
            time.sleep(1)
