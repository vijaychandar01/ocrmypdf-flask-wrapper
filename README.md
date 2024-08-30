# ocrmypdf-flask-wrapper

## Project Structure

ocrmypdf-flask-wrappert/
│
├── app/
│   ├── __init__.py            # Initialize the Flask app and configurations
│   ├── routes.py              # Define the routes and views
│   ├── processing.py          # Contains the PDF processing logic
│   ├── utils.py               # Utility functions (e.g., for file handling, progress tracking)
│   └── templates/
│       ├── index.html         # Index page template
│       ├── progress.html      # Progress tracking page template
│       └── partial_download.html  # Partial download template
│
├── uploads/                   # Folder for uploaded files
├── processed/                 # Folder for processed files
├── requirements.txt           # List of dependencies
├── config.py                  # Configuration settings
├── run.py                     # Run the Flask app
└── .env                       # Environment variables
