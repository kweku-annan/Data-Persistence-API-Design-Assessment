# Data Persistence & API Design Assessment

A FastAPI-based backend system that integrates with three external APIs (Genderize, Agify, and Nationalize) to collect user demographic data, apply classification logic, persist data to a database, and expose RESTful endpoints for managing user profiles.

## 🎯 Project Overview

This project is part of the **HNG Backend Stage 1** challenge. It demonstrates core backend engineering principles including:
- Multi-API integration with concurrent requests
- Data persistence and idempotency handling
- Proper HTTP semantics and error handling
- Clean architecture with separation of concerns
- Database query filtering and optimization

### Key Features

- **Create Profiles**: Accept a name, fetch data from three external APIs, classify data, and store in database
- **Idempotency**: Prevent duplicate profiles by checking the database before making external API calls
- **Data Classification**: Apply business logic to classify age groups and select the most probable nationality
- **Profile Management**: Retrieve single or multiple profiles with optional filtering by gender, country, or age group
- **Robust Error Handling**: Proper HTTP status codes and error responses for various failure scenarios

## 🔧 Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **HTTP Client**: httpx (async-compatible)
- **Validation**: Pydantic
- **Configuration**: pydantic-settings with .env support
- **Python Version**: ≥3.12

## 📋 External APIs Used

1. **Genderize API** - https://api.genderize.io?name={name}
2. **Agify API** - https://api.agify.io?name={name}
3. **Nationalize API** - https://api.nationalize.io?name={name}

All APIs are free and require no authentication.

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- pip or uv package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Data-Persistence-API-Design-Assessment
   ```

2. **Install dependencies** (using uv)
   ```bash
   uv sync
   ```
   
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** (optional - uses defaults if not provided)
   ```bash
   DATABASE_URL=sqlite:///./app.db
   ```

### Running the Application

1. **Start the development server**
   ```bash
   uv run uvicorn app.main:app --reload
   ```
   
   Or with Python:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

2. **Access the API**
   - Base URL: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## 📡 API Endpoints

### 1. Create Profile
**POST** `/api/profiles`

Request:
```json
{
  "name": "ella"
}
```

Success Response (201 Created):
```json
{
  "status": "success",
  "data": {
    "id": "b3f9c1e2-7d4a-4c91-9c2a-1f0a8e5b6d12",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "DRC",
    "country_probability": 0.85,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
```

**Idempotency**: If the same name already exists, the existing profile is returned with a 200 status and a message indicating the profile already exists.

### 2. Get Single Profile
**GET** `/api/profiles/{id}`

Success Response (200):
```json
{
  "status": "success",
  "data": {
    "id": "b3f9c1e2-7d4a-4c91-9c2a-1f0a8e5b6d12",
    "name": "emmanuel",
    "gender": "male",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 25,
    "age_group": "adult",
    "country_id": "NG",
    "country_probability": 0.85,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
```

### 3. Get All Profiles
**GET** `/api/profiles`

Query Parameters (all optional):
- `gender`: Filter by gender (case-insensitive)
- `country_id`: Filter by country ID (case-insensitive)
- `age_group`: Filter by age group (case-insensitive)

Example: `/api/profiles?gender=male&country_id=NG`

Success Response (200):
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "id-1",
      "name": "emmanuel",
      "gender": "male",
      "age": 25,
      "age_group": "adult",
      "country_id": "NG"
    },
    {
      "id": "id-2",
      "name": "sarah",
      "gender": "female",
      "age": 28,
      "age_group": "adult",
      "country_id": "US"
    }
  ]
}
```

### 4. Delete Profile
**DELETE** `/api/profiles/{id}`

Success Response: 204 No Content

## ⚠️ Error Handling

All errors follow this structure:
```json
{
  "status": "error",
  "message": "<error message>"
}
```

### Error Codes

| Status | Scenario |
|--------|----------|
| 400 | Missing or empty name |
| 422 | Invalid data type |
| 404 | Profile not found |
| 502 | External API returned invalid response |
| 500 | Internal server error |

### Edge Cases Handled

- **Genderize API fails**: Returns null gender or count of 0 → 502 error
- **Agify API fails**: Returns null age → 502 error
- **Nationalize API fails**: Returns no country data → 502 error

## 📊 Data Classification

### Age Groups (based on Agify age)
- **0–12** → "child"
- **13–19** → "teenager"
- **20–59** → "adult"
- **60+** → "senior"

### Nationality
The country with the highest probability from Nationalize API is selected.

## 🏗️ Project Architecture

```
app/
├── main.py              # FastAPI app initialization & CORS setup
├── config.py            # Environment configuration
├── database.py          # SQLAlchemy setup & Base model
├── integrations/
│   └── external_apis.py # Integration with external APIs
├── models/
│   └── profile.py       # SQLAlchemy ORM model
├── routers/
│   └── profiles.py      # API endpoints
├── schemas/
│   └── profile.py       # Pydantic request/response schemas
└── services/
    └── profile_service.py # Business logic layer
```

## 🧠 Engineering Principles Applied

### 1. **Separation of Concerns**
Each module has a single responsibility:
- **Routers**: Handle HTTP requests/responses
- **Services**: Contain business logic
- **Integrations**: Manage external API calls
- **Models**: Define database structure
- **Schemas**: Define data validation and serialization

### 2. **Layer Independence**
- Database dependencies are passed as parameters, not imported directly
- External API integration layer is independent of HTTP layer
- Services contain only business logic
- Each layer can be tested independently

### 3. **Async Best Practices**
- Uses `httpx` for async HTTP requests (not blocking `requests`)
- Uses `asyncio.gather` to make concurrent API calls
- Proper async/await usage throughout

### 4. **Data Validation at Boundaries**
- Pydantic schemas validate all incoming data
- Empty or invalid names are rejected at the request boundary
- Type validation happens before reaching business logic

### 5. **Idempotency Before External Calls**
- Database is checked BEFORE making expensive external API calls
- Prevents duplicate data and unnecessary API consumption
- Improves performance by avoiding redundant operations

### 6. **Consistency Across Layers**
- Names are lowercased consistently: on input validation, database storage, and idempotency checks
- Ensures reliable duplicate detection

### 7. **HTTP Semantics**
- `201` for resource creation
- `200` for successful retrieval
- `204` for successful deletion with no content
- `400` for client errors
- `422` for validation errors
- `404` for not found
- `502` for upstream failures

### 8. **Configuration Management**
- Uses `pydantic-settings` with `.env` file support
- Database URL and other secrets are environment variables
- Code remains unchanged across different deployment environments

## 🧪 Testing the API

Use the interactive API docs at `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` (ReDoc).

### Example requests:

**Create a profile:**
```bash
curl -X POST "http://localhost:8000/api/profiles" \
  -H "Content-Type: application/json" \
  -d '{"name": "Emmanuel"}'
```

**Get all profiles:**
```bash
curl "http://localhost:8000/api/profiles"
```

**Get profiles by filter:**
```bash
curl "http://localhost:8000/api/profiles?gender=male&country_id=NG"
```

**Get a single profile:**
```bash
curl "http://localhost:8000/api/profiles/{profile_id}"
```

**Delete a profile:**
```bash
curl -X DELETE "http://localhost:8000/api/profiles/{profile_id}"
```

## 📚 Key Learnings From Building This Project

### 1. **Think Before You Code**
Before writing a single line, mapping out the flow, identifying failure points, and designing the data model separates engineers from coders. **Code is the last step, not the first.**

### 2. **Separation of Concerns**
Every folder in the project has one job:
- Routers handle HTTP
- Services handle business logic
- Integrations handle external APIs
- Models define database structure
- Schemas define input/output shapes

When something breaks, you know exactly where to look. When something needs to change, you know exactly what to touch.

### 3. **Layer Independence**
- `Depends(get_db)` belongs in the router, not the service
- `HTTPException` belongs in the router or service, not the integration layer
- `Base` belongs in database.py, not in individual model files

Each layer should be usable and testable **without knowing about the layers above it.**

### 4. **Environment-Driven Configuration**
Hardcoding database URLs or secrets is a bad habit. Using `pydantic-settings` with a `.env` file means:
- Your code never changes between environments
- Secrets never end up in your GitHub repository
- Railway, Heroku, or any platform just sets environment variables and your app works

### 5. **Async Awareness**
FastAPI is async. Using `requests` instead of `httpx` inside an async route **blocks the event loop** and kills your server's ability to handle concurrent requests. Always match your tools to your framework's execution model.

### 6. **Concurrency With `asyncio.gather`**
Calling three external APIs sequentially means waiting for each one to finish before starting the next. With `asyncio.gather`, all three run **at the same time**. This is not just a performance optimization — it's correct async thinking.

### 7. **Data Validation At The Boundary**
Pydantic schemas are the **gate** between the outside world and your system. Validate everything at entry:
- Empty names
- Names with numbers or symbols
- Wrong types

Never let bad data reach your service or database layer.

### 8. **Idempotency Is A Design Decision**
The idempotency check must happen **before** external API calls — not after. This is both a correctness and a performance decision. Don't do expensive work you don't need to do.

### 9. **Consistency Across Layers**
Lowercasing the name in the schema alone is not enough. You must be consistent:
- Lowercase on input validation
- Lowercase when storing in the database
- Lowercase when querying for idempotency

One layer being inconsistent breaks the entire guarantee.

### 10. **HTTP Semantics Matter**
- `201` means something was **created**
- `200` means something was **found**
- `204` means success with **no content to return**
- `400` means the **client sent bad input**
- `422` means the **client sent the wrong type**
- `404` means something **wasn't found in your system**
- `502` means an **upstream service failed**

Using the wrong status code is not just incorrect — it misleads every client and developer who consumes your API.

### 11. **Spec Compliance Is Exact**
`"2026-04-01T12:00:00+00:00"` and `"2026-04-01T12:00:00Z"` mean the same thing to a human. To an automated grader, they are different. **Read specs carefully. Match them exactly.**

### 12. **Clean Imports Signal Clean Architecture**
Every unused import is a question — *why is this here?* Imports tell the story of your dependencies. If your service imports `Depends` from FastAPI, something is wrong architecturally. Clean imports are a byproduct of clean thinking.

### 13. **Testing Starts With Thinking**
Before writing a single test, listing every valid and invalid input for every endpoint **is** the testing work. The code just confirms what you already reasoned through.

## 📖 The Bigger Picture

You didn't just build an API. You built a **system** — with layers, boundaries, contracts between those layers, and intentional decisions at every step. That's what software engineering is. Not syntax. Not frameworks. **Thinking in systems.**

## 📝 License

This project is part of the HNG Backend Internship Stage 1 challenge.

## 🚀 Next Steps

These lessons are foundational and carry into every future project. Keep these principles in mind as you advance to Stage 2 and beyond!
