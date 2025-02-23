import logging
from flask import Flask, jsonify, request, g
import psycopg2
import psycopg2.pool
from flask_cors import CORS

# Flask App Setup
app = Flask(__name__)
CORS(app)

# Database Configuration for PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "dbname": "postgres1",
    "user": "postgres",
    "password": "Oscar@123",
}

# Initialize PostgreSQL Connection Pool
db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **DB_CONFIG)

# Logger Setup
logger = logging.getLogger("flask_logger")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# PostgreSQL connection management
def get_db_connection():
    if "db" not in g:
        g.db = db_pool.getconn()
        logger.debug("New database connection established.")
    return g.db


@app.teardown_appcontext
def close_db_connection(exception=None):
    db = g.pop("db", None)
    if db:
        db_pool.putconn(db)
        logger.debug("Database connection released.")


@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 5, type=int)
        search = request.args.get("search", "", type=str)
        sort = request.args.get("sort", "", type=str)
        city = request.args.get("city", "", type=str)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Initialize the base query
        query = "SELECT * FROM users"
        params = []

        # Apply search filter if provided
        if search:
            query += " WHERE first_name LIKE %s OR last_name LIKE %s"
            params.extend(["%" + search + "%", "%" + search + "%"])

        # Apply partial city filter if provided
        if city:
            if "WHERE" in query:
                query += " AND city LIKE %s"
            else:
                query += " WHERE city LIKE %s"
            params.append("%" + city + "%")

        # Define valid sort fields
        valid_sort_fields = [
            "id",
            "first_name",
            "last_name",
            "company_name",
            "email",
            "city",
            "state",
            "zip",
            "web",
            "age",
        ]
        sort_field = sort[1:] if sort.startswith("-") else sort
        sort_order = "DESC" if sort.startswith("-") else "ASC"

        # Apply sorting if valid
        if sort_field in valid_sort_fields:
            query += f" ORDER BY {sort_field} {sort_order}"

        # Apply pagination
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, (page - 1) * limit])

        # Execute query
        cursor.execute(query, params)
        users = cursor.fetchall()
        conn.close()

        # Process and return user data
        users_data = [
            {
                "id": user[0],
                "first_name": user[1],
                "last_name": user[2],
                "company_name": user[3],
                "email": user[4],
                "city": user[5],
                "state": user[6],
                "zip": user[7],
                "web": user[8],
                "age": user[9],
            }
            for user in users
        ]

        logger.info(f"Fetched {len(users_data)} users.")
        return jsonify(users_data), 200

    except Exception as e:
        logger.error(f"Error occurred while fetching users: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/users", methods=["POST"])
def create_user():
    try:
        user_data = request.get_json()
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        company_name = user_data.get("company_name")
        email = user_data.get("email")
        city = user_data.get("city")
        state = user_data.get("state")
        zip_code = user_data.get("zip")
        web = user_data.get("web")
        age = user_data.get("age")

        if not first_name or not last_name or not email:
            logger.warning("Missing required fields: First Name, Last Name, or Email.")
            return (
                jsonify({"error": "First Name, Last Name, and Email are required"}),
                400,
            )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (first_name, last_name, company_name, email, city, state,
            zip, web, age)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                first_name,
                last_name,
                company_name,
                email,
                city,
                state,
                zip_code,
                web,
                age,
            ),
        )
        conn.commit()
        conn.close()

        logger.info("User created successfully.")
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        logger.error(f"Error occurred while creating user: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/users/<int:id>", methods=["GET"])
def get_user_by_id(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM users WHERE id = %s;
        """,
            (id,),
        )
        user = cursor.fetchone()
        conn.close()

        if not user:
            logger.warning(f"User with ID {id} not found.")
            return jsonify({"error": "User not found"}), 404

        user_data = {
            "id": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "company_name": user[3],
            "email": user[4],
            "city": user[5],
            "state": user[6],
            "zip": user[7],
            "web": user[8],
            "age": user[9],
        }

        logger.info(f"Fetched user with ID {id}.")
        return jsonify(user_data), 200
    except Exception as e:
        logger.error(f"Error occurred while fetching user by ID: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Add similar logging for other routes (PUT, DELETE, PATCH)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
