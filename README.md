# Marrow Assignment: Movie Content Upload & Review System

This project is a backend service that allows users to upload CSV files containing movie-related data and then review the uploaded content. The system is built with Flask (wrapped as an ASGI app via Uvicorn) for the web API and uses Celery to offload heavy CSV processing tasks to background workers. MongoDB is used to store movie, task, and user data. Authentication is handled with JWT, and sensitive configuration is managed via environment variables.

## Postman Collection
Link to the Postman collection: [Marrow Assignment API](https://documenter.getpostman.com/view/33491654/2sAYX3rip3)

## Overview

1. **User Registration & Login:**
    - Before uploading any content, a user must register or log in.
    - Upon successful registration or login, the API returns an access token (JWT) that is valid for 15 minutes (or a duration set in the `.env` file).

2. **Uploading CSV Files:**
    - Authenticated users (by providing the access token in the Bearer header) can upload CSV files.
    - Each file upload creates a new "task" (recorded in the MongoDB tasks collection) with a unique task ID.
    - Once the file is uploaded, the CSV processing task is offloaded to a Celery worker. The worker reads the CSV file, processes its contents, inserts movie records into MongoDB, and updates the task status to "done" (or "failed" on errors).

3. **Reviewing Uploaded Data:**
    - Users can query tasks to check the status of their uploads.
    - There is also a dedicated API to list movies, supporting pagination, filtering, and sorting options.

---

## API Routes

### Authentication Routes

#### **Register**
- **URL:** `/auth/register`
- **Method:** `POST`
- **Request Body:** (JSON)
  ```json
  {
     "username": "johndoe",
     "password": "securepassword",
     "email": "johndoe@example.com",
     "name": "John Doe"
  }
  ```
- **Expected Output:**
  - **Success (HTTP 201):**
     ```json
     {
        "message": "User registered successfully",
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJI..."
     }
     ```
  - **Error (HTTP 400/404):** Appropriate error message if required fields are missing or if the user already exists.

#### **Login**
- **URL:** `/auth/login`
- **Method:** `POST`
- **Request Body:** (JSON)
  ```json
  {
     "username": "johndoe",
     "password": "securepassword"
  }
  ```
- **Expected Output:**
  - **Success (HTTP 201):**
     ```json
     {
        "message": "User logged in successfully",
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJI..."
     }
     ```
  - **Error (HTTP 400/404):** Error message if the user is not found or credentials are invalid.

---

### **File Upload Route**

#### **Upload CSV File**
- **URL:** `/files/upload`
- **Method:** `POST`
- **Headers:** 
  - `Authorization: Bearer <access_token>`
- **Form Data:**
  - File field: `file` (the CSV file to be uploaded)
- **Expected Output:**
  - **Success (HTTP 202):**
     ```json
     {
        "task_id": "unique-task-id",
        "message": "File uploaded successfully. Please wait while it processes."
     }
     ```

**Process Flow:**
- The file is saved to a designated uploads directory.
- A task record is created in MongoDB with the status "pending".
- The task is offloaded to a Celery worker. The worker updates the task status to "processing", processes the CSV file, and finally sets it to "done" or "failed" if errors occur.

---

### Task Routes

#### **Get Single Task Status**
- **URL:** `/task/<task_id>`
- **Method:** `GET`
- **Headers:**
  - `Authorization: Bearer <access_token>`
- **Expected Output:**
  - **Success (HTTP 200):**
     ```json
     {
        "task_id": "unique-task-id",
        "status": "processing"  // or "done", or "failed"
     }
     ```
  - **Error (HTTP 404/403):** Appropriate error message if the task is not found or the user is not authorized.

#### **Get All Tasks for a User**
- **URL:** `/tasks`
- **Method:** `GET`
- **Headers:**
  - `Authorization: Bearer <access_token>`
- **Expected Output:**
  - **Success (HTTP 200):**
     ```json
     [
        {
          "task_id": "unique-task-id-1",
          "status": "done",
          "file_path": "uploads/test1.csv",
          "user": "johndoe"
        },
        {
          "task_id": "unique-task-id-2",
          "status": "processing",
          "file_path": "uploads/test2.csv",
          "user": "johndoe"
        }
     ]
     ```
  - **Error:** Appropriate error message if no tasks are found or if unauthorized.

---

### Movie Routes

#### **List Movies with Pagination, Filtering, and Sorting**
- **URL:** `/movies`
- **Method:** `GET`
- **Query Parameters:**
  - `page` (optional, default: 1) – The page number.
  - `limit` (optional, default: 50) – Number of movies per page.
  - `year` (optional) – Filter movies by the year of the release_date.
  - `language` (optional) – Filter movies by original_language.
  - `sort_field` (optional) – Field to sort by (release_date or rating). Default is release_date.
  - `sort_order` (optional) – "asc" or "desc". Default is "asc".
- **Expected Output:**
  - **Success (HTTP 200):** A JSON array of movie documents.
     ```json
     [
        {
          "_id": "609c0f1e3d9b3b0a1a2b3c4d",
          "title": "Example Movie",
          "release_date": "2020-05-15T00:00:00",
          "original_language": "en",
          "vote_average": 7.5
          // ...other fields
        },
        {
          "_id": "609c0f1e3d9b3b0a1a2b3c4e",
          "title": "Another Movie",
          "release_date": "2020-07-22T00:00:00",
          "original_language": "en",
          "vote_average": 8.2
          // ...other fields
        }
     ]
     ```
  - **Error:** Appropriate error messages if parameters are invalid or other issues arise.

---

## Background Task Processing with Celery

**How It Works:**
- When a CSV file is uploaded, a task record is created in MongoDB and offloaded to a Celery worker (`process_csv_task`).
- The worker reads the CSV (in chunks if necessary), creates movie records in MongoDB, and updates the task status to "done" or "failed" if any error occurs.

**Why Celery?**
- CSV processing can be time-consuming. By offloading it to Celery, the user’s request finishes quickly (202 Accepted), and the heavy lifting is done asynchronously.

---

## Deployment with Docker & Docker Compose

**Dockerfile**
- Builds a single image for both the web service (using Uvicorn) and the Celery worker (by overriding the container’s command).

**docker-compose.yml**
- `web`: Runs your Uvicorn server on port 8000.
- `worker`: Runs Celery to process tasks.
- `mongo`: A MongoDB container if you need a local database (otherwise, connect to an external one).

**Environment Variables**
- Managed via a `.env` file (excluded in `.gitignore`).
- Provide secrets like `JWT_SECRET_KEY`, `MONGO_URI`, and your Redis `CELERY_BROKER_URL`.

**Run with:**
```sh
docker-compose up --build
```
- This starts the web server, the Celery worker, and MongoDB. Access the web API at `http://localhost:8000`.

---

## Summary of Workflow

1. **Register/Login**
    - Obtain JWT access token.
2. **Upload CSV**
    - Endpoint: `/files/upload` (Bearer token required).
    - Returns task ID. The file is processed in the background.
3. **Check Task**
    - Endpoint: `/task/<task_id>` to see the status of the upload.
4. **List All Tasks**
    - Endpoint: `/tasks` for the user’s tasks.
5. **List Movies**
    - Endpoint: `/movies` with optional pagination, filtering, and sorting.

The system ensures that CSV processing doesn’t block user requests and organizes movie data in MongoDB.
