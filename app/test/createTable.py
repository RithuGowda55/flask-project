from flask import Flask, g
import psycopg2
import psycopg2.pool
import logging

app = Flask(__name__)

# Database Configuration for PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "dbname": "postgres2",
    "user": "postgres",
    "password": "Oscar@123"
}

# Initialize PostgreSQL Connection Pool
db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **DB_CONFIG)

# Configure logging to log to createTable.log file
logging.basicConfig(
    filename='createTable.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# PostgreSQL connection management
def get_db_connection():
    if 'db' not in g:
        g.db = db_pool.getconn()
    return g.db

# Initialize database (Create tables)
def init_db():
    with app.app_context():  # Create app context
        conn = get_db_connection()
        cursor = conn.cursor()
        
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                company_name TEXT,
                email TEXT NOT NULL UNIQUE,
                city TEXT,
                state TEXT,
                zip INTEGER,
                web TEXT,
                age INTEGER
            )
        """
        
        try:
            cursor.execute(create_table_query)
            conn.commit()
            logging.info("Query executed successfully: %s", create_table_query)
        except Exception as e:
            logging.error("Error executing query: %s", e)
        finally:
            conn.close()

if __name__ == '__main__':
    init_db()
