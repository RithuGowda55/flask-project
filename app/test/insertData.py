import logging
import psycopg2
import psycopg2.pool
import json

# Set up logging to log queries and results
logging.basicConfig(
    filename="insertData.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Database Configuration for PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "dbname": "postgres2",
    "user": "postgres",
    "password": "Oscar@123",
}

# Initialize PostgreSQL Connection Pool
db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **DB_CONFIG)


# PostgreSQL connection management
def get_db_connection():
    conn = db_pool.getconn()
    return conn


# Insert data into the database and log queries and results
def init_db_from_json():
    try:
        json_file_path = "/Users/druthigs/Desktop/Flask-proj/users.json"

        with open(json_file_path, "r") as f:
            users_data = json.load(f)

        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO users (first_name, last_name, company_name, email, city, state, zip, web, age)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
        """

        # Log the query before executing
        logging.info(f"Executing query: {insert_query}")

        for user in users_data:
            # Log the individual user data
            logging.info(f"User data: {user}")

            cursor.execute(
                insert_query,
                (
                    user["first_name"],
                    user["last_name"],
                    user.get("company_name", None),
                    user["email"],
                    user.get("city", None),
                    user.get("state", None),
                    user.get("zip", None),
                    user.get("web", None),
                    user.get("age", None),
                ),
            )

            # Log the result (e.g., the number of affected rows)
            logging.info(f"Inserted row for user: {user['email']}")

        conn.commit()
        logging.info("Database initialized and users inserted successfully.")

    except Exception as e:
        logging.error(f"Error during database initialization: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Call the function
init_db_from_json()
