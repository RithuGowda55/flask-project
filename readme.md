#!/bin/bash

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
curl -X PATCH "$BASE_URL/1" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "Janet"
    }'

# 6. ❌ Delete User by ID
curl -X DELETE "$BASE_URL/2"

# 7. 📊 Get User Summary (Statistics)
curl -X GET "$BASE_URL/summary"

# 8. tO COUNT THE RECORDS
curl -X GET "$BASE_URL/count"
