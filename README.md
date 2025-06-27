ECSE3038 Lab 4 - RESTful API with FastAPI and MongoDB
Overview
This project implements a RESTful API server using FastAPI in Python, integrated with MongoDB via Motor (an async MongoDB driver). The API manages two main resources:

Profile: A singular user profile containing username, role, and color attributes.

Tank: Multiple water tank objects with location and GPS coordinates.

The API demonstrates the use of standard HTTP request handlers: POST, GET, PATCH, and DELETE for CRUD operations on these resources. The server supports cross-origin requests from the ECSE3038 lab tester site.

Installation and Setup
Python 3.9+

MongoDB Atlas cluster or local MongoDB

Dependencies installed via requirements.txt:

fastapi

uvicorn

motor

python-dotenv

pydantic

Create a .env file with your MongoDB connection string:

bash
Copy
Edit
MONGODB_URL="your_mongodb_connection_string_here"
Run the app using:

bash
Copy
Edit
uvicorn app:app --reload
API Endpoints and Usage
Profile Endpoints
GET /profile
Description:
Retrieve the single stored user profile.

Expected Response (Before profile creation):

json
Copy
Edit
{}
Expected Response (After profile creation):

json
Copy
Edit
{
  "id": "507f1f77bcf86cd799439011",
  "last_updated": "06/27/2025, 06:06:41 PM",
  "username": "coolname",
  "role": "Engineer",
  "color": "#3478ff"
}
POST /profile
Description:
Create the user profile. Only one profile is allowed; duplicate attempts result in an error.

Example Request:

json
Copy
Edit
{
  "username": "coolname",
  "role": "Engineer",
  "color": "#3478ff"
}
Expected Response:

json
Copy
Edit
{
  "id": "507f1f77bcf86cd799439011",
  "last_updated": "06/27/2025, 06:06:41 PM",
  "username": "coolname",
  "role": "Engineer",
  "color": "#3478ff"
}
Error Response (If profile exists):

json
Copy
Edit
{
  "detail": "Profile already exists"
}
Tank Endpoints
POST /tank
Description:
Create a new tank entry with a unique ID, location, latitude, and longitude.

Example Request:

json
Copy
Edit
{
  "location": "Chemistry Department",
  "lat": 26.262525,
  "long": 262.3833333
}
Expected Response:

json
Copy
Edit
{
  "id": "0f34995e-4ee8-4cce-9636-52110ea4bacd",
  "location": "Chemistry Department",
  "lat": 26.262525,
  "long": 262.3833333
}
GET /tank
Description:
Retrieve a list of all stored tanks.

Expected Response:

json
Copy
Edit
[
  {
    "id": "0f34995e-4ee8-4cce-9636-52110ea4bacd",
    "location": "Chemistry Department",
    "lat": 26.262525,
    "long": 262.3833333
  },
  {
    "id": "c8944b35-825c-4eae-b6a7-52c947829edf",
    "location": "Engineering Department",
    "lat": 26.2525,
    "long": 19.3833333
  }
]
PATCH /tank/{id}
Description:
Update an existing tank's attributes (location, lat, long). Partial updates are allowed.

Example Request:

json
Copy
Edit
{
  "location": "Old Chemistry Department"
}
Expected Response:

json
Copy
Edit
{
  "id": "0f34995e-4ee8-4cce-9636-52110ea4bacd",
  "location": "Old Chemistry Department",
  "lat": 26.262525,
  "long": 262.3833333
}
Error Response (If tank not found):

json
Copy
Edit
{
  "detail": "Tank not found"
}
DELETE /tank/{id}
Description:
Delete a specific tank entry by ID.

Expected Response:

No content, status code 204.

Error Response (If tank not found):

json
Copy
Edit
{
  "detail": "Tank not found"
}
