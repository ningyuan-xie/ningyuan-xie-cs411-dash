from pymongo.mongo_client import MongoClient
import os

uri = os.getenv("MONGODB_CLUSTER_URI")

# Create a new client and connect to the server
client = MongoClient(uri)
print(client)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
