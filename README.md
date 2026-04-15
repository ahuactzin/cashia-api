# Cashia API

**cashia-api** is the web service layer of the Cashia ecosystem.\
It exposes the core functionality of the system through a REST API built
with **FastAPI**.

The API integrates several internal Cashia packages:

-   **cashia-core** -- Shared utilities and configuration
-   **cashia-model** -- Machine learning models used for prediction
-   **cce** -- Cashia Credit Engine

The API is intended for local development first, and can later be
deployed in environments such as AWS.

------------------------------------------------------------------------

# 1. Requirements

Before installing the API, ensure the following are available:

-   Python **3.11**
-   `pip`
-   Access to the Cashia repositories:
    -   `cashia-core`
    -   `cashia-model`
    -   `cce`
    -   `cashia-api`

Recommended development tools:

-   **Anaconda / Miniconda**
-   **Visual Studio Code**

------------------------------------------------------------------------

# 2. Environment Setup

## Option A --- Using Conda (recommended)

Create the environment:

``` bash
conda create -n cashia_env python=3.11
```

Activate it:

``` bash
conda activate cashia_env
```

------------------------------------------------------------------------

## Option B --- Using venv

Create a virtual environment:

``` bash
python -m venv cashia_env
```

Activate it:

### Windows

``` bash
cashia_env\Scripts\activate
```

### Linux / macOS

``` bash
source cashia_env/bin/activate
```

------------------------------------------------------------------------

# 3. Install Dependencies

Navigate to the root directory that contains all Cashia repositories.

Example structure:

``` text
cashia
│
├── cashia-core
├── cashia-model
├── cashia-api
├── cce
└── mlp
```

Install each package in **editable mode**:

``` bash
pip install -e cashia-core
pip install -e cashia-model
pip install -e cce
pip install -e mlp
pip install -e cashia-api
```

Editable mode allows development changes without reinstalling the
package.

------------------------------------------------------------------------

# 4. Project Structure

A typical `cashia-api` structure is:

``` text
cashia-api
│   pyproject.toml
│   README.md
│
└───src
    └───cashia_api
        │   __init__.py
        │   main.py
        │   dependencies.py
        │   schemas.py
        │
        ├───routers
        │       ...
        │
        ├───services
        │       ...
        │
        └───utils
                ...
```

## Suggested role of each module

-   **main.py**\
    Entry point of the FastAPI application. Usually defines the `app`,
    CORS configuration, startup/shutdown logic, and router registration.

-   **routers/**\
    Defines the API endpoints grouped by domain or functionality.

-   **services/**\
    Contains business logic that should remain separate from the HTTP
    layer.

-   **schemas.py**\
    Defines request and response models using **Pydantic**.

-   **dependencies.py**\
    Centralizes FastAPI dependencies such as shared services,
    configuration managers, or state accessors.

-   **utils/**\
    Utility functions used across the API package.

------------------------------------------------------------------------

# 5. Running the API

The API is built with **FastAPI** and can be launched using **Uvicorn**.

From any directory, with the environment activated:

``` bash
uvicorn cashia_api.main:app --reload
```

The API will start at:

``` text
http://127.0.0.1:8000
```

------------------------------------------------------------------------

# 6. Interactive API Documentation

FastAPI automatically generates documentation.

After starting the server, you can access:

## Swagger UI

``` text
http://127.0.0.1:8000/docs
```

## ReDoc

``` text
http://127.0.0.1:8000/redoc
```

These interfaces allow testing endpoints directly from the browser.

------------------------------------------------------------------------

# 7. Example Development Workflow

Typical development cycle:

1.  Modify API code
2.  Run the API with reload enabled
3.  Test endpoints using:
    -   Swagger UI
    -   curl
    -   Postman
    -   frontend applications

Example:

``` bash
uvicorn cashia_api.main:app --reload
```

If package metadata or dependencies change:

``` bash
pip install -e cashia-api --upgrade
```

------------------------------------------------------------------------

# 8. Environment Variables

Depending on your current architecture, the API may use environment
variables such as:

``` text
STORAGE_BACKEND
LOCAL_STORAGE_ROOT
S3_BUCKET
S3_PREFIX
```

## Example: local storage

### Windows PowerShell

``` powershell
$env:STORAGE_BACKEND="local"
$env:LOCAL_STORAGE_ROOT="G:\My Drive\19_Projects\cashia\cashia-core"
```

### Linux / macOS

``` bash
export STORAGE_BACKEND=local
export LOCAL_STORAGE_ROOT=/path/to/cashia-core
```

## Example: S3 storage

### Windows PowerShell

``` powershell
$env:STORAGE_BACKEND="s3"
$env:S3_BUCKET="my-cashia-bucket"
$env:S3_PREFIX="cashia-dev"
```

### Linux / macOS

``` bash
export STORAGE_BACKEND=s3
export S3_BUCKET=my-cashia-bucket
export S3_PREFIX=cashia-dev
```

------------------------------------------------------------------------

# 9. CORS Configuration

If the API is accessed from a frontend application running in a browser,
**CORS** may need to be configured.

A typical FastAPI configuration looks like:

``` python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Adjust allowed origins according to your frontend environment.

------------------------------------------------------------------------

# 10. Example Request and Response

The exact endpoints depend on your router definitions, but a typical
prediction endpoint might look like this.

## Example request

``` http
POST /predict
Content-Type: application/json
```

``` json
{

}
```

## Example response

``` json
{

}
```

ToDo: Replace this example with the real request/response schemas used by your
API.

------------------------------------------------------------------------

# 11. Running in Development

Recommended command:

``` bash
uvicorn cashia_api.main:app --reload
```

Optional custom port:

``` bash
uvicorn cashia_api.main:app --reload --port 8001
```

Optional host binding:

``` bash
uvicorn cashia_api.main:app --reload --host 0.0.0.0
```

------------------------------------------------------------------------

# 12. Troubleshooting

## Port already in use

If port 8000 is busy, run:

``` bash
uvicorn cashia_api.main:app --reload --port 8001
```

## Environment issues

Verify the Python version:

``` bash
python --version
```

Expected:

``` text
Python 3.11.x
```

## Import errors

If imports fail after code changes, reinstall editable packages:

``` bash
pip install -e cashia-core --upgrade
pip install -e cashia-model --upgrade
pip install -e cce --upgrade
pip install -e mlp --upgrade
pip install -e cashia-api --upgrade
```

## Wrong interpreter in VS Code

Ensure that VS Code is using the correct Python interpreter, usually the
one from:

``` text
cashia_env
```

------------------------------------------------------------------------

# 13. Future Documentation

Additional documentation can later include:

-   AWS deployment
-   Docker containers
-   CI/CD pipelines
-   API authentication and security
-   Production configuration
-   Logging and monitoring

------------------------------------------------------------------------

# Author

Juan Manuel Ahuactzin\
Cashia Project
