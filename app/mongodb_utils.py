# mongodb_utils.py - Utility functions for MongoDB database operations.

from typing import List, Tuple
from pymongo import MongoClient
import os
import certifi

# Global MongoDB client (initialized once)
MONGO_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "academicworld"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]


def get_mongo_connection():
    """Create and return a new MongoDB client and database connection."""
    try:
        # Use TLS/SSL configuration with certifi
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=30000,  # 30-second timeout
            tls=True,
            tlsCAFile=certifi.where()
        )
        print("MongoDB Connection Successful")
        return client, client[DATABASE_NAME]
    except Exception as e:
        print(f"MongoDB Connection Failed: {e}")
        raise


def close_mongo_connection(client):
    """Safely close MongoDB client connection."""
    if client:
        client.close()


def get_all_collections() -> list:
    """Fetch all collection names from the MongoDB database."""
    client = None
    try:
        client, db = get_mongo_connection()
        return db.list_collection_names()
    except Exception as e:
        print("MongoDB connection error:", e)
        return []
    finally:
        close_mongo_connection(client)


def get_collection_count(collection_name: str) -> int:
    """Fetch document count for the selected collection."""
    client = None
    try:
        client, db = get_mongo_connection()
        count = db[collection_name].count_documents({})
        return count if count is not None else 0  # Ensure valid int count
    except Exception as e:
        print(f"Error fetching count for collection '{collection_name}':", e)
        return 0
    finally:
        close_mongo_connection(client)


def get_all_affiliations() -> List[str]:
    """Fetch all affiliations from the MongoDB database."""
    client = None
    try:
        client, db = get_mongo_connection()
        result = db.faculty.distinct("affiliation.name")
        return result
    except Exception as e:
        print("Error fetching affiliations:", e)
        return []
    finally:
        close_mongo_connection(client)


def get_all_keywords_mongo() -> List[str]:
    """Fetch all keywords from the MongoDB database."""
    client = None
    try:
        client, db = get_mongo_connection()
        result = db.publications.distinct("keywords.name")
        return result
    except Exception as e:
        print("Error fetching keywords:", e)
        return []
    finally:
        close_mongo_connection(client)


# For 1. Widget One: MongoDB Bar Chart
def find_most_popular_keywords_mongo(year: int) -> List[Tuple[str, int]]:
    """Find the top-10 most popular keywords in publications since the given year."""
    client = None
    try:
        client, db = get_mongo_connection()
        
        # Create indexes for optimized query performance
        db.publications.create_index([("keywords.name", 1)])  # Optimizes keyword search
        db.publications.create_index([("year", 1)])  # Optimizes year-based search

        # Define the aggregation pipeline
        pipeline = [
            { "$unwind": "$keywords" },
            { "$match": { "year": { "$gte": year } } },
            { "$group": { "_id": "$keywords.name", "pubcnt": { "$sum": 1 } } },
            { "$sort": { "pubcnt": -1 } },
            { "$limit": 10 },
            { "$project": { "_id": 1, "pubcnt": 1 } }
        ]

        # Execute the aggregation query
        query_result = list(db.publications.aggregate(pipeline))
        return [(keyword["_id"], keyword["pubcnt"]) for keyword in query_result]  # [(keyword, count), ...]
    except Exception as e:
        print(f"Error fetching keywords since {year}:", e)
        return []
    finally:
        close_mongo_connection(client)


# For 4. Widget Four: MongoDB Bar Chart
def find_top_faculties_with_highest_KRC_keyword(keyword: str, affiliation: str) -> List[Tuple[str, int]]:
    """Find top faculties with the highest number of researchers working on the given keyword."""
    client = None
    try:
        client, db = get_mongo_connection()
        
        # Create indexes for optimized query performance
        db.faculty.create_index([("affiliation.name", 1)])  # Optimizes filtering
        db.faculty.create_index([("publications", 1)])  # Optimizes lookup
        db.publications.create_index([("id", 1)])  # Optimizes join
        db.publications.create_index([("keywords.name", 1)])  # Optimizes keyword search
        db.publications.create_index([("keywords.score", 1), ("numCitations", 1)])  # Optimizes calculations

        # Define the aggregation pipeline
        pipeline = [
            { "$match": { "affiliation.name": affiliation } },
            { "$lookup": {
                "from": "publications",
                "localField": "publications",
                "foreignField": "id",
                "as": "pubs"
            }},
            { "$unwind": "$pubs" },
            { "$unwind": "$pubs.keywords" },
            { "$match": { "pubs.keywords.name": keyword } },  # Match the exact keyword
            { "$group": {
                "_id": "$name",
                "KRC": { "$sum": { "$multiply": ["$pubs.keywords.score", "$pubs.numCitations"] } }
            }},
            { "$sort": { "KRC": -1 } },
            { "$limit": 10 },
            { "$project": { "_id": 1, "KRC": { "$round": ["$KRC", 2] } } }
        ]

        # Execute the aggregation query
        query_result = list(db.faculty.aggregate(pipeline))
        return [(faculty["_id"], faculty["KRC"]) for faculty in query_result]  # [(faculty, KRC), ...]

    except Exception as e:
        print(f"Error fetching faculties for keyword '{keyword}' and affiliation '{affiliation}':", e)
        return []
    finally:
        close_mongo_connection(client)
