# neo4j_utils.py - Utility functions for Neo4j database operations.

from typing import List, Tuple
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Aura connection details
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
database = os.getenv("NEO4J_DATABASE", "neo4j")

# Initialize the driver
driver = GraphDatabase.driver(uri, auth=(username, password))


def get_neo4j_connection():
    """Create and return a new Neo4j driver session."""
    try:
        session = driver.session(database=database)
        print("Neo4j Connection Successful")
        return session
    except Exception as e:
        print(f"Neo4j Connection Failed: {e}")
        raise


def close_neo4j_connection(session):
    """Safely close Neo4j session."""
    if session:
        session.close()


def get_all_labels() -> List[str]:
    """Fetch all labels from the Neo4j database."""
    session = None
    try:
        session = get_neo4j_connection()
        result = session.run("CALL db.labels()")
        return [record[0] for record in result]
    except Exception as e:
        print("Neo4j connection error:", e)
        return []
    finally:
        close_neo4j_connection(session)


def get_label_count(label_name: str) -> int:
    """Get count of nodes with a specific label."""
    session = None
    try:
        session = get_neo4j_connection()
        query = f"MATCH (n:{label_name}) RETURN COUNT(n) AS count"
        result = session.run(query)
        count = result.single()["count"]
        return count if count is not None else 0  # Ensure valid int count
    except Exception as e:
        print(f"Error fetching count for label '{label_name}':", e)
        return 0
    finally:
        close_neo4j_connection(session)


def get_all_institutes() -> List[str]:
    """Get all institutes from the Neo4j database."""
    session = None
    try:
        session = get_neo4j_connection()
        result = session.run("MATCH (i:INSTITUTE) RETURN i.name AS name")
        return [record["name"] for record in result]
    except Exception as e:
        print("Error fetching institutes:", e)
        return []
    finally:
        close_neo4j_connection(session)


# For 5.1 Widget Five: Neo4j Table
def faculty_interested_in_keywords(university_name: str) -> List[Tuple[int, str, int]]:
    """Fetch faculty members interested in keywords from the Neo4j database."""
    session = None
    try:
        session = get_neo4j_connection()
        query = (
            "MATCH (u:INSTITUTE {name: $university_name})<-[:AFFILIATION_WITH]-(f:FACULTY)-[:INTERESTED_IN]->(k:KEYWORD) "
            "WHERE k.is_deleted = false "
            "RETURN k.id AS id, k.name AS keyword, COUNT(f) AS faculty_count "
            "ORDER BY faculty_count DESC LIMIT 10"
        )
        result = session.run(query, university_name=university_name)
        return [(record["id"], record["keyword"], record["faculty_count"]) for record in result]  # [(id, keyword, count), ...]
    except Exception as e:
        print(f"Error fetching faculty data for '{university_name}':", e)
        return []
    finally:
        close_neo4j_connection(session)


# For 5.2 Widget Five: Neo4j Table - Count Keywords
def get_keyword_count() -> int:
    """Get the total number of keywords in the Neo4j database."""
    session = None
    try:
        session = get_neo4j_connection()
        
        # Ensure all Keyword nodes have the is_deleted property
        session.run("""
            MATCH (k:KEYWORD)
            WHERE k.is_deleted IS NULL
            SET k.is_deleted = false
        """)

        # Count active (non-deleted) Keyword nodes
        result = session.run("""
            MATCH (k:KEYWORD)
            WHERE k.is_deleted = false
            RETURN COUNT(k) AS count
        """)
        count = result.single()["count"]

        return count if count is not None else 0  # Ensure valid int count
    except Exception as e:
        print("Error fetching keyword count:", e)
        return 0
    finally:
        close_neo4j_connection(session)


# For 5.3 Widget Five: Neo4j Table - Delete Keywords
def delete_keyword(keyword_id: str) -> bool:
    """Soft delete a keyword from the Neo4j database using a Transaction."""
    session = None
    tx = None
    try:
        session = get_neo4j_connection()
        tx = session.begin_transaction()  # Start transaction

        result = tx.run("""
            MATCH (k:KEYWORD {id: $id})
            SET k.is_deleted = true
            RETURN k
        """, id=keyword_id)

        if result.single():  # Check if the update was successful
            tx.commit()  # Commit the transaction
            return True
        else:
            tx.rollback()  # Rollback if no keyword was found
            return False

    except Exception as e:
        print(f"Error deleting keyword '{keyword_id}':", e)
        if tx:
            tx.rollback()  # Rollback in case of an error
        return False

    finally:
        close_neo4j_connection(session)


# For 5.4 Widget Five: Neo4j Table - Restore Keywords
def restore_keyword() -> bool:
    """Restore all deleted keywords in the Neo4j database using a Transaction."""
    session = None
    tx = None
    try:
        session = get_neo4j_connection()
        tx = session.begin_transaction()  # Start transaction

        result = tx.run("""
            MATCH (k:KEYWORD)
            WHERE k.is_deleted = true
            SET k.is_deleted = false
        """)

        tx.commit()  # Commit the transaction
        return True

    except Exception as e:
        print(f"Error restoring keywords:", e)
        if tx:
            tx.rollback()  # Rollback if an error occurs
        return False

    finally:
        close_neo4j_connection(session)


# For 6. Widget Six: Neo4j Sunburst Chart
def university_collaborate_with(university_name: str) -> List[Tuple[str, int]]:
    """Fetch institutes collaborating with a specific university from the Neo4j database."""
    session = None
    try:
        session = get_neo4j_connection()
        query = (
            "MATCH (:INSTITUTE {name: $university_name})<-[:AFFILIATION_WITH]-(f1:FACULTY)-[:PUBLISH]->"
            "(p:PUBLICATION)<-[:PUBLISH]-(f2:FACULTY)-[:AFFILIATION_WITH]->(university:INSTITUTE) "
            "WHERE university.name <> $university_name "
            "RETURN university.name AS university, count(DISTINCT f1) AS faculty_count "
            "ORDER BY faculty_count DESC LIMIT 10"
        )
        result = session.run(query, university_name=university_name)
        return [(record["university"], record["faculty_count"]) for record in result]  # [(university, count), ...]
    except Exception as e:
        print(f"Error fetching collaboration data for '{university_name}':", e)
        return []
    finally:
        close_neo4j_connection(session)
