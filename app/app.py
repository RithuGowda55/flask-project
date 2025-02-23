from flask import Flask, jsonify, request, g
import psycopg2
import psycopg2.pool
from flask_cors import CORS

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


# PostgreSQL connection management
def get_db_connection():
    if "db" not in g:
        g.db = db_pool.getconn()
    return g.db


@app.teardown_appcontext
def close_db_connection(exception=None):
    db = g.pop("db", None)
    if db:
        db_pool.putconn(db)


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

        return jsonify(users_data), 200

    except Exception as e:
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

        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
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

        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/users/<int:id>", methods=["PUT"])
def update_user(id):

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

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET first_name = %s, last_name = %s, company_name = %s, email = %s,
                city = %s, state = %s, zip = %s, web = %s, age = %s
            WHERE id = %s;
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
                id,
            ),
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/users/<int:id>", methods=["DELETE"])
def delete_user(id):

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Attempt to delete the user
        cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (id,))
        deleted_user = cur.fetchone()

        if deleted_user:
            conn.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route("/api/users/<int:id>", methods=["PATCH"])
def partially_update_user(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT city, COUNT(*) AS count, AVG(age) AS avg_age FROM users GROUP BY city;
        """
        )
        summary = cursor.fetchall()
        conn.close()

        summary_data = [
            {"city": row[0], "count": row[1], "avg_age": row[2]} for row in summary
        ]

        return jsonify(summary_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/users/count", methods=["GET"])
def get_user_count():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]

        return jsonify({"total_users": user_count}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
