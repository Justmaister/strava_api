# Strava API Project

This project provides a Python-based interface to interact with the Strava API, allowing you to fetch and analyze your Strava activity data.

## Features

- Authentication with Strava API
- Token management (access and refresh tokens)
- Activity data retrieval
- Asynchronous API requests
- Interactive progress tracking
- Configurable endpoints
- Package management with pyproject.toml

## Project Structure

strava_api/
├── api_app/
│   ├── data/
│   ├── utils/
│   └── strava_api.ipynb
├── resources/
└── token_cache.json

## Getting Started

1. Clone this repository
2. Create a virtual environment:
   ```bash
   uv venv
   source .venv/Scripts/activate # In Windows
   ```
3. Install dependencies:
   ```bash
   uv pip install -e .
   ```
4. To deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Usage

1. Follow the API setup instructions in [api_setup.md](api_setup.md)
2. Run the Jupyter notebook:
   ```bash
   python -m api_app
   ```

## Project Features

### Package Management
The project uses `pyproject.toml` for modern Python packaging:
```toml
[project]
name = "strava_api"
version = "0.1.0"
description = "Strava API Integration"
dependencies = [
    "requests",
    "aiohttp",
    "pandas",
    "jupyter"
]
```

### API Configuration
The `EndpointConfig` class manages API endpoints and authentication:
```python
from api_app.utils.endpoint_config import EndpointConfig

config = EndpointConfig(
    base_url="https://www.strava.com/api/v3",
    endpoints={
        "activities": "/athlete/activities",
        "athlete": "/athlete"
    }
)
```

### Asynchronous Requests
The project supports async API calls for better performance:
```python
from api_app.utils.async_client import AsyncStravaClient

async with AsyncStravaClient() as client:
    activities = await client.get_activities()
```

### Custom API Call Selection
Interactive API call selection using `thinker` for a better user experience:
```python
from api_app.utils.thinker import ThinkerAPI
from api_app.utils.endpoint_config import EndpointConfig

