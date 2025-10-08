# Spy Cat Agency Management System

A comprehensive CRUD application built with FastAPI for managing spy cats, missions, and targets. This system allows the Spy Cat Agency to efficiently manage their feline operatives and their espionage activities.

## Features

- **Spy Cat Management**: Create, read, update, and delete spy cats with breed validation
- **Mission Management**: Create missions with 1-3 targets and assign them to available cats
- **Target Tracking**: Update target notes and mark completion status
- **Business Logic**: Automatic mission completion when all targets are done, notes freezing for completed targets
- **Breed Validation**: Integration with TheCatAPI for authenticating cat breeds

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Validation**: Pydantic models with custom validators
- **External API**: TheCatAPI for breed validation
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Architecture**: Modular structure with separate routers, models, and services

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd spy_cat_agency
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

4. **Access API Documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Spy Cats

| Method | Endpoint             | Description            |
| ------ | -------------------- | ---------------------- |
| POST   | `/spy-cats/`         | Create a new spy cat   |
| GET    | `/spy-cats/`         | List all spy cats      |
| GET    | `/spy-cats/{cat_id}` | Get a specific spy cat |
| PUT    | `/spy-cats/{cat_id}` | Update spy cat salary  |
| DELETE | `/spy-cats/{cat_id}` | Delete a spy cat       |

### Missions

| Method | Endpoint                        | Description                       |
| ------ | ------------------------------- | --------------------------------- |
| POST   | `/missions/`                    | Create a new mission with targets |
| GET    | `/missions/`                    | List all missions                 |
| GET    | `/missions/{mission_id}`        | Get a specific mission            |
| PUT    | `/missions/{mission_id}/assign` | Assign a cat to a mission         |
| DELETE | `/missions/{mission_id}`        | Delete a mission                  |

### Targets

| Method | Endpoint               | Description                              |
| ------ | ---------------------- | ---------------------------------------- |
| PUT    | `/targets/{target_id}` | Update target notes or completion status |

## Data Models

### Spy Cat

```json
{
  "id": 1,
  "name": "Whiskers",
  "years_of_experience": 5,
  "breed": "Persian",
  "salary": 50000
}
```

### Mission

```json
{
  "id": 1,
  "cat_id": 1,
  "is_completed": false,
  "targets": [
    {
      "id": 1,
      "name": "John Doe",
      "country": "USA",
      "notes": "Target spotted at downtown cafe",
      "is_completed": false
    }
  ]
}
```

## Business Rules

1. **Cat Assignment**: One cat can only have one mission at a time
2. **Target Limits**: Missions must have between 1-3 targets
3. **Notes Protection**: Notes cannot be updated if target or mission is completed
4. **Mission Completion**: Mission is automatically marked complete when all targets are done
5. **Deletion Constraints**:
   - Cannot delete cats with active missions
   - Cannot delete missions assigned to cats
6. **Breed Validation**: All cat breeds are validated against TheCatAPI

## Postman Collection

A complete Postman collection is available: [Spy_Cat_Agency_API.postman_collection.json](./Spy_Cat_Agency_API.postman_collection.json)

**Import Instructions:**

1. Open Postman
2. Click "Import" button
3. Select the `Spy_Cat_Agency_API.postman_collection.json` file
4. Set the `base_url` variable to `http://localhost:8000`

## Example Usage

### 1. Create a Spy Cat

```bash
curl -X POST "http://localhost:8000/spy-cats/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Shadow",
    "years_of_experience": 3,
    "breed": "Siamese",
    "salary": 45000
  }'
```

### 2. Create a Mission

```bash
curl -X POST "http://localhost:8000/missions/" \
  -H "Content-Type: application/json" \
  -d '{
    "targets": [
      {
        "name": "John Doe",
        "country": "USA"
      },
      {
        "name": "Jane Smith",
        "country": "Canada"
      }
    ]
  }'
```

### 3. Assign Cat to Mission

```bash
curl -X PUT "http://localhost:8000/missions/1/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "cat_id": 1
  }'
```

### 4. Update Target Notes

```bash
curl -X PUT "http://localhost:8000/targets/1" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Target spotted at downtown cafe. Meeting with unknown contact.",
    "is_completed": false
  }'
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid data or business rule violations
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors

Example error response:

```json
{
  "detail": "Invalid cat breed"
}
```

## Project Structure

```text
spy_cat_agency/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── database.py          # Database configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py            # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── spy_cats.py          # Spy cats endpoints
│   │   ├── missions.py          # Missions endpoints
│   │   └── targets.py           # Targets endpoints
│   └── services/
│       ├── __init__.py
│       └── breed_validator.py   # External API integration
├── main.py                      # Application entry point
├── requirements.txt             # Dependencies
├── test_api.py                  # Test script
├── Spy_Cat_Agency_API.postman_collection.json
└── README.md
```

## Database

The application uses SQLite with the following tables:

- `spy_cats`: Stores spy cat information
- `missions`: Stores mission data and completion status
- `targets`: Stores target information and notes

The database file (`spy_cat_agency.db`) is created automatically on first run.

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload
```

### Testing

You can test the API using the provided Postman collection or by accessing the interactive documentation at `http://localhost:8000/docs`.
