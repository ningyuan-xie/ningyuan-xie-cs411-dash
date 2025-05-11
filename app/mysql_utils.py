# mysql_utils.py - Utility functions for MySQL database operations.

from typing import List, Tuple
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Create and return a new connection to AWS RDS MySQL."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306)),
            connect_timeout=30  # 30-second timeout
        )
        print("MySQL Connection Successful")
        return connection
    except Error as e:
        print(f"MySQL Connection Failed: {e}")
        raise


def close_db_connection(cursor, cnx):
    """Safely close MySQL cursor and connection."""
    if cursor:
        cursor.close()
    if cnx:
        cnx.close()


def get_all_tables() -> list:
    """Fetch all table names from the MySQL database."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SHOW TABLES")
        return [table[0] for table in cursor.fetchall()]  # (table_name,) -> table_name
    except Exception as e:
        print("Database connection error:", e)
        return []
    finally:
        close_db_connection(cursor, cnx)


def get_table_count(table_name: str) -> int:
    """Fetch row count for the selected table."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        query = f"SELECT COUNT(*) FROM {table_name}"
        cursor.execute(query)
        return cursor.fetchone()[0]  # (count,) -> count
    except Exception as e:
        print(f"Error fetching count for table '{table_name}':", e)
        return 0
    finally:
        close_db_connection(cursor, cnx)


def find_universities_with_faculties_working_keywords(keyword: str) -> List[Tuple[str, int]]:
    """Find top 5 universities with number of faculties working on the given keyword."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Create a View to store the top universities with faculty count
        query_view = """CREATE OR REPLACE VIEW TOP_UNIVERSITIES AS
                        SELECT university.name, COUNT(distinct(faculty.id)) AS faculty_count
                        FROM university, faculty, faculty_keyword, keyword
                        WHERE university.id = faculty.university_id
                        AND faculty.id = faculty_keyword.faculty_id
                        AND faculty_keyword.keyword_id = keyword.id
                        AND keyword.name LIKE %s
                        GROUP BY university.name;"""
        cursor.execute(query_view, (f"%{keyword}%",))  # Secure way to pass parameters
        cnx.commit()

        # Query the view to fetch top universities with faculty count
        query = "SELECT * FROM TOP_UNIVERSITIES ORDER BY faculty_count DESC LIMIT 5"
        cursor.execute(query)
        
        return cursor.fetchall()  # [(university, faculty_count), ...]
    except Exception as e:
        print("Error fetching universities:", e)
        return []
    finally:
        close_db_connection(cursor, cnx)


# For 1. Widget One: MongoDB Bar Chart (with MySQL option)
def find_most_popular_keywords_sql(year: int) -> List[Tuple[str, int]]:
    """Find top-10 most popular keywords among publications since 2015."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Create indexes for optimized query performance
        index_definitions = {
            "idx_publication_year": "CREATE INDEX idx_publication_year ON publication(year);",
            "idx_pubkw_pubid_kwid": "CREATE INDEX idx_pubkw_pubid_kwid ON publication_keyword(publication_id, keyword_id);",
            "idx_pubkw_kwid": "CREATE INDEX idx_pubkw_kwid ON publication_keyword(keyword_id);",
            "idx_keyword_id": "CREATE INDEX idx_keyword_id ON keyword(id);"
        }

        for index_name, index_sql in index_definitions.items():
            cursor.execute("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
                WHERE table_schema = DATABASE()
                AND index_name = %s
            """, (index_name,))
            exists = cursor.fetchone()[0]
            if not exists:
                try:
                    cursor.execute(index_sql)
                except Exception as index_error:
                    print(f"Index creation failed for {index_name}:", index_error)
        
        query = """SELECT keyword.name, COUNT(publication.id)
                   FROM keyword, publication_keyword, publication
                   WHERE keyword.id = publication_keyword.keyword_id
                   AND publication_keyword.publication_id = publication.id
                   AND publication.year >= %s
                   GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC LIMIT 10;"""
        cursor.execute(query, (year,))
        return cursor.fetchall()  # [(keyword, count), ...]
    except Exception as e:
        print("Error fetching popular keywords:", e)
        return []
    finally:
        close_db_connection(cursor, cnx)
    

# For 2. Widget Two: MySQL Controller
def get_all_keywords() -> List[str]:
    """Fetch all keywords from the MySQL database."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT DISTINCT(name) FROM keyword")
        return [keyword[0] for keyword in cursor.fetchall()]  # (keyword,) -> keyword
    except Exception as e:
        print("Error fetching keywords:", e)
        return []
    finally:
        close_db_connection(cursor, cnx)


# For 3.1 Widget Three: MySQL Table
def find_faculty_relevant_to_keyword(keyword: str) -> List[Tuple[str, int]]:
    """Find faculty members relevant to the selected keyword."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Prepared Statement: define the SQL statement with a placeholder
        # Benefit: avoid SQL injection and improve performance
        prepare_query = """PREPARE stmt FROM 
                           'SELECT faculty.id, faculty.name, university.name
                            FROM university, faculty, faculty_keyword, keyword
                            WHERE university.id = faculty.university_id
                            AND faculty.id = faculty_keyword.faculty_id
                            AND faculty_keyword.keyword_id = keyword.id
                            AND keyword.name = ? 
                            AND faculty_keyword.score >= 50
                            AND faculty.is_deleted = FALSE';"""
        # Prepare the statement
        cursor.execute(prepare_query)

        # Assign value to the parameter
        cursor.execute("SET @keyword = %s", (keyword,))

        # Execute the prepared statement using the variable
        cursor.execute("EXECUTE stmt USING @keyword;")

        # Fetch results
        result = cursor.fetchall()

        # Deallocate the prepared statement
        cursor.execute("DEALLOCATE PREPARE stmt;")

        return result  # [(faculty_id, faculty_name, university_name), ...]
    except Exception as e:
        print("Error fetching faculty members:", e)
        return []
    finally:
        close_db_connection(cursor, cnx)


# For 3.1 Widget Three: MySQL Table - Count Faculty
def get_faculty_count() -> int:
    """Fetch the total number of faculty members from the MySQL database."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Check if 'is_deleted' column exists (case-insensitive check)
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'faculty' 
            AND COLUMN_NAME = 'is_deleted'
        """)
        column_exists = cursor.fetchone()[0] > 0

        if not column_exists:
            try:
                cursor.execute("ALTER TABLE faculty ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE")
                cnx.commit()
            except Exception as alter_error:
                print(f"Error adding column: {alter_error}")
                # Continue even if column creation fails

        cursor.execute("SELECT COUNT(*) FROM faculty WHERE is_deleted = FALSE")
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error fetching faculty count: {e}")
        return 0
    finally:
        close_db_connection(cursor, cnx)
    

# For 3.2 Widget Three: MySQL Table - Delete Faculty
def delete_faculty(faculty_id: int) -> bool:
    """Soft delete a faculty member by marking it as deleted using a Transaction."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Start transaction
        cnx.start_transaction()

        # Mark the faculty record as deleted
        cursor.execute("UPDATE faculty SET is_deleted = TRUE WHERE id = %s", (faculty_id,))
        
        # Commit transaction to finalize changes
        cnx.commit()
        return True

    except Exception as e:
        print("Error deleting faculty member:", e)

        # Rollback transaction in case of failure
        if cnx:
            cnx.rollback()
        return False

    finally:
        close_db_connection(cursor, cnx)


# For 3.3 Widget Three: MySQL Table - Restore Faculty
def restore_faculty() -> bool:
    """Restore all faculty members by setting is_deleted back to FALSE using a Transaction."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Start transaction
        cnx.start_transaction()

        # Restore all soft-deleted faculty members
        cursor.execute("UPDATE faculty SET is_deleted = FALSE WHERE is_deleted = TRUE")

        # Commit transaction to finalize changes
        cnx.commit()
        return True

    except Exception as e:
        print("Error restoring faculty members:", e)

        # Rollback transaction in case of failure
        if cnx:
            cnx.rollback()
        return False

    finally:
        close_db_connection(cursor, cnx)


# For 4.1 Widget Four: MongoDB Bar Chart (with MySQL option) - Database Dropdown
def get_all_universities() -> List[str]:
    """Fetch all universities from the MySQL database."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT DISTINCT(name) FROM university")
        return [university[0] for university in cursor.fetchall()]  # (university,) -> university
    except Exception as e:
        print("Error fetching universities:", e)
        return []
    finally:
        close_db_connection(cursor, cnx)


# For 4.2 Widget Four: MongoDB Bar Chart (with MySQL option)
def find_top_faculties_with_highest_KRC_keyword_sql(keyword, university) -> List[Tuple[str, int]]:
    """Find top faculties with highest KRC for the selected keyword and affiliation."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Query the view to fetch top faculties with highest KRC
        query = """SELECT faculty.name, 
                   ROUND(SUM(publication_keyword.score * publication.num_citations), 2) AS KRC
                   FROM faculty, faculty_publication, publication, publication_keyword, keyword, university
                   WHERE faculty.id = faculty_publication.faculty_Id
                   AND faculty_publication.publication_Id = publication.ID
                   AND publication.ID = publication_keyword.publication_id
                   AND publication_keyword.keyword_id = keyword.id
                   AND keyword.name = %s
                   AND faculty.university_id = university.id
                   AND university.name = %s
                   GROUP BY faculty.id ORDER BY KRC DESC LIMIT 10;
                   """
        cursor.execute(query, (keyword, university))
        return cursor.fetchall()  # [(faculty, KRC), ...]
    except Exception as e:
        print(f"Error fetching faculties for keyword '{keyword}' and affiliation '{university}':", e)
        return []
    finally:
        close_db_connection(cursor, cnx)


# For 6.2 Widget Six: Neo4j Sunburst Chart - University Information
def get_university_information(university_name: str) -> List[Tuple[str, str]]:
    """Fetch university information based on the university name."""
    cnx, cursor = None, None
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        query = """SELECT university.name, COUNT(faculty.id) AS faculty_count, university.photo_url
                   FROM university, faculty
                   WHERE university.name = %s
                   AND university.id = faculty.university_id
                   GROUP BY university.name, university.photo_url;"""
        cursor.execute(query, (university_name,))
        return cursor.fetchall()  # [(id, name), ...]
    except Exception as e:
        print("Error fetching university information:", e)
        return []
    finally:
        close_db_connection(cursor, cnx)
