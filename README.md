# HeidiTool

An end-to-end Flask application for exploring high-dimensional datasets with Heidi matrices. Users can upload tabular data, clean and normalize it on the fly, and generate interactive visualizations for subspace analysis directly from the browser.

## Features
- Upload CSV/TSV/JSON datasets and persist them to SQLite for reuse.
- Automated data-cleaning pipeline with multiple strategies for resolving missing values and categorical encoding.
- Heidi matrix generation, legend creation, and point lookup APIs exposed via the `/heidi` blueprint.
- User authentication (registration, login, account updates) backed by `Flask-Login` and `Flask-SQLAlchemy`.
- Frontend assets and static exports for viewing generated Heidi images.

## Project Layout
```
TOOL/
├─ app/                        # Flask application package
│  ├─ controllers.py           # Auth views and upload workflow
│  ├─ heidi/                   # Heidi API, dataset IO, visualization logic
│  ├─ mod_datacleaning/        # Cleaning utilities used during uploads
│  ├─ static/ & templates/     # App-specific static assets and Jinja templates
│  └─ run.py                   # Entry point for local development
├─ frontend/                   # UI assets (React/JS) if you extend the SPA
├─ static/                     # Served assets and generated uploads (`static/uploads`)
└─ tests/                      # Pytest suites for Heidi dataset and dimension modules
```

## Getting Started

### Prerequisites
- Python 3.9+ (virtual environment recommended)
- SQLite (bundled with Python, used via SQLAlchemy)
- Node.js (optional, only if you plan to work on the `frontend/` assets)

### Setup
```bash
git clone <repo-url>
cd TOOL
python3 -m venv .venv
source .venv/bin/activate
pip install Flask Flask-Login Flask-SQLAlchemy Flask-Cors pandas numpy pillow
```

If you prefer a requirements file, pin the versions you use and replace the last command with `pip install -r requirements.txt`.

## Running the Application
```bash
source .venv/bin/activate
python app/run.py
```

The development server binds to `http://0.0.0.0:8080` by default (see `app/config.py`). The first launch creates the SQLite database (`app/app.db`) and any required upload directories under `app/static/uploads/`.

### Upload Workflow
1. Sign up or log in from the web UI.
2. Upload a CSV, TSV, or JSON file.  
   - CSV uploads must contain `id` and `classLabel` columns.  
   - Choose a missing-value strategy (`skip`, `mean`, `median`, `max frequent`, `max`, `min`).
3. The cleaned dataset is stored in `app/static/uploads/` and registered in the database.
4. Heidi matrices and legends are generated and can be visualized or requested via API.

## Heidi API Overview

| Endpoint | Method | Description |
| --- | --- | --- |
| `/heidi/read-dataset?dataset_path=…` | GET | Return the uploaded dataset as JSON records. |
| `/heidi/create-heidi-matrix?dataset_path=…` | POST | Persist matrices for all subspaces to the database. |
| `/heidi/columns?datasetPath=…` | GET | List all available dimensions for a dataset. |
| `/heidi/image` | POST | Generate a Heidi image and corresponding matrix map for selected subspaces. |
| `/heidi/consolidated-image` | POST | Produce a consolidated image across subspaces. |
| `/heidi/legend?datasetPath=…` | GET | Fetch the legend describing colors per subspace. |
| `/heidi/points` | POST | Retrieve point details for a selected row/column cell. |
| `/heidi/subspace-comparison-matrix` | GET | Download a subspace overlap matrix CSV. |
| `/heidi/subspace-summary` | GET | Return summary stats for a subspace. |

All POST endpoints expect JSON payloads; check `app/heidi/routes.py` for the required fields.

## Development Notes
- Logging is configured through Python’s standard library. Adjust the level or handlers in your Flask entry point if you need structured output.
- Uploaded files, intermediate matrices, and exported CSVs live in `static/uploads/`. Clean up this folder periodically during development.
- Database models (`app/models.py`) store users, Heidi matrices, legends, and dataset metadata. Drop `app/app.db` if you need a clean slate.

## Testing
```bash
source .venv/bin/activate
pytest
```

The suites under `tests/` cover dataset ingestion, Heidi matrix generation, and dimension utilities. Add new tests alongside the relevant module directories.

## Troubleshooting
- **Missing dependencies**: double-check your virtual environment and reinstall the packages listed above.
- **Upload errors**: inspect the Flask logs—data-cleaning failures and validation issues are logged with context.
- **Static directory errors**: ensure `app/static/uploads/` exists and is writable (the app creates it on startup, but permissions matter on shared systems).

Happy exploring!
