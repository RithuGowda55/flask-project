# Flask Project

## Setup Instructions

# 1. Clone the repository:
git clone <repository_url>
cd FLASK-PROJ

# 2. Install dependencies:
Using Poetry:
poetry add $(cat requirements.txt)

# 3. Activate the Poetry virtual environment:
poetry shell

# 4. Run the Flask application:
Move to the app directory and run the app on port 5000:
cd app
flask --app app run --port 5000

# 5. Run Unit Tests:
Move to the test directory and run the tests on port 5001:
cd test
flask --app log_data run --port 5001

# 6. Run Pre-commit Hooks:
To ensure code quality and style consistency, run pre-commit hooks:
pre-commit run --all-files



#  API Usage Examples

BASE_URL="http://127.0.0.1:5000/api/users"

# 1. 📝 List Users with Pagination, Search, and Sorting
curl -X GET "$BASE_URL?page=1&limit=10&search=James&sort=-age"

# 2. 👤 Get User by ID
curl -X GET "$BASE_URL/1"

# 3. ➕ Create a New User
curl -X POST "$BASE_URL" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "John",
        "last_name": "Doe",
        "company_name": "Tech Solutions",
        "city": "San Francisco",
        "state": "CA",
        "zip": 94105,
        "email": "john.doe@example.com",
        "web": "http://www.techsolutions.com",
        "age": 30
    }'

# 4. ✏️ Update User by ID (Full Update)
curl -X PUT "$BASE_URL/1" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "John",
        "last_name": "Doe",
        "company_name": "Tech Solutions",
        "city": "San Francisco",
        "state": "CA",
        "zip": 94105,
        "email": "john.doe@example.com",
        "web": "http://www.techsolutions.com",
        "age": 30
    }'

# 5. 🔄 Partially Update User by ID (PATCH)
curl -X PATCH "$BASE_URL/11" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "Janet-updated"
    }'

# 6. ❌ Delete User by ID
curl -X DELETE "$BASE_URL/2"

# 7. 📊 Get User Summary (Statistics)
curl -X GET "$BASE_URL/summary"


# 8. tO COUNT THE RECORDS
curl -X GET "$BASE_URL/count"
