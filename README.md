# ECSE3038 Lab 4 - FastAPI MongoDB RESTful API

## Project Overview

This project demonstrates a RESTful API server built with **FastAPI** in Python, connected to a **MongoDB** database using the `motor` asynchronous driver. It manages a **single profile** and multiple **water tank entries**.

The API supports full CRUD operations and can be tested via tools like **Postman** or **Swagger UI** (`/docs`).

## Features

* **MongoDB Integration**: Asynchronous communication using `motor`.
* **Single Profile Limitation**: Only one profile document allowed.
* **Tank Management**: Create, read, update, and delete tank entries.
* **CORS Middleware**: Allows requests from the official lab tester site.
* **Data Validation**: Enforced via `pydantic` models.
* **Automatic Timestamping**: Profile's `last_updated` field updates when tank data changes.

---

## API Routes and Examples

### POST `/profile`

**Create the single profile object. Only one profile allowed.**

#### Request Body Example:

```json
{
  "username": "coolname",
  "role": "Engineer",
  "color": "#3478ff"
}
```

#### Expected Response:

```json
{
  "id": "60b8a9e9e4a3f4a67ccac3e2",
  "last_updated": "06/27/2025, 06:32:09 PM",
  "username": "coolname",
  "role": "Engineer",
  "color": "#3478ff"
}
```

<img width="453" alt="image" src="https://github.com/user-attachments/assets/100ccabf-d4e9-46af-8ba4-70fcf59c81d5" />

---

### GET `/profile`

**Retrieve the profile object. Returns an empty object if none exists.**

#### Expected Response:

```json
{
  "id": "60b8a9e9e4a3f4a67ccac3e2",
  "last_updated": "06/27/2025, 06:32:09 PM",
  "username": "coolname",
  "role": "Engineer",
  "color": "#3478ff"
}
```

---

### POST `/tank`

**Create a new tank entry with a unique ID.**

#### Request Body Example:

```json
{
  "location": "Indira's Farm",
  "lat": 83.8484,
  "long": 35.39383
}
```
<img width="452" alt="image" src="https://github.com/user-attachments/assets/67c7477d-5323-4e78-96b2-af4113596267" />

#### Expected Response:

```json
{
  "id": "6c344168-4756-43ac-927b-d29b790ba506",
  "location": "Indira's Farm",
  "lat": 83.8484,
  "long": 35.39383
}
```

---

### GET `/tank`

**Retrieve a list of all stored tanks.**

#### Expected Response:

```json
[
  {
    "id": "601394d4-25c4-4e73-9fae-b380e0e4466a",
    "location": "Engineering Departmentt",
    "lat": 189.41,
    "long": -67.743
  },
 {
  "id": "6c344168-4756-43ac-927b-d29b790ba506",
  "location": "Indira's Farm",
  "lat": 83.8484,
  "long": 35.39383
}
]
```
<img width="491" alt="image" src="https://github.com/user-attachments/assets/e2b0f63e-3edd-4468-97ae-cb46bca54c28" />

---

### PATCH `/tank/{id}`

**Update a specific tank entry**

#### Request Body Example:

```json
{
  "location": "Updated location"
}
```

#### Expected Response:

```json
{
  "id": "a8bfb9e1-268f-41e1-b85f-77c9760547f3",
  "location": "Updated location",
  "lat": 18.004741,
  "long": -76.748753
}
```

---

### DELETE `/tank/{id}`

**Deletes a tank with the specified ID.**

#### Expected Response:

* No content (HTTP 204 No Content)

---

## How to Run the App

1. Create a `.env` file and set the following:

```
MONGODB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/ECSE3038?retryWrites=true&w=majority
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi motor uvicorn python-dotenv
```

3. Run the app:

```bash
uvicorn app:app --reload
```

4. Use Postman, https://ecse3038-lab3-tester.netlify.app/ website UI and MongoDb to test.

---

## Notes

* If you try to POST a second profile, it will return a 400 error.
* MongoDB Object IDs are automatically generated for tanks.
* All tank changes automatically update the profile's `last_updated` timestamp.

* example terminal outputs:
* <img width="613" alt="image" src="https://github.com/user-attachments/assets/5c746a96-01e4-49b5-bc8d-22af8098375c" />

