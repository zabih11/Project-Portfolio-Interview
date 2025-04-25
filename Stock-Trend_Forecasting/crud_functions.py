import pymongo
import pandas as pd
import json
from bson.objectid import ObjectId
from typing import Any, Dict


def mongo_connect():
    uri = "mongodb+srv://zabihm11:c51P8iuUJMz3KvRS@cluster0.xe8a23d.mongodb.net/?retryWrites=true&w=majority" 
    # Create a new client and connect to the server
    client = pymongo.MongoClient(uri)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    return client

def create(client, item: Any) -> bool:
    db = client["Stock_Data"]
    collections = db["Microsoft (MSFT)"]
    inserted = collections.insert_one(item)
    if inserted.inserted_id:
        print("Item was successfully inserted!")
        idee = str(inserted.inserted_id)
        print(idee)
        return True, idee
    else:
        print("Insertion has failed!")
        return False
    
def read(client, query: str) -> Any:
    db = client["Stock_Data"]
    collections = db["Microsoft (MSFT)"]
    retrieved = list(collections.find(query))
    if not retrieved:
        print("No items matched your query!")
    else:
        print("Matching data to query was retrieved.")
        print(retrieved)
    return retrieved


def update(client, item_id: Any, properties: Dict) -> bool:
    db = client["Stock_Data"]
    collections = db["Microsoft (MSFT)"]
    existing_db = collections.find({"_id": item_id})
    if len(list(existing_db)) > 0:
        update_parts = {"$set": properties}
        updating = collections.update_one({"_id": item_id}, update_parts)
        if updating.modified_count:
            print("Item was updated in database!")
            return True
        else:
            print("Update was unsuccessful!")
            return False
    else:
        print("Item with that id was not found!")
        return False


def delete(client, item_id: str) -> bool:
    db = client["Stock_Data"]
    collections = db["Microsoft (MSFT)"]
    existing_db = collections.find({"_id":  item_id})
    if len(list(existing_db)) > 0:
        collections.delete_one({"_id":  item_id})
        if len(list(existing_db)) == 0:
            print("Item was deleted from database!")
            return True
        else:
            print("Deletion was unsuccessful!")
            return False
    else:
        print("Item with that id was not found!")
        return False


if __name__ == "__main__":
    client = mongo_connect()
    item = {"date": "2023-04-01", "open": "284.04", "high": "285.01", "low": "275.03", "close": "283.01", "volume": "20065433"}
    idee = create(client, item)
    query = {"volume" : "20065433"}
    read(client, query)
    #item_id = ObjectId('65a6928ec97968d603431f1d')
    item_id = ObjectId(idee[1])
    properties = {"open": "284.05", "low": "285.02", "volume": "20065434"}
    update(client, item_id, properties)
    delete(client, item_id)
    client.close()
