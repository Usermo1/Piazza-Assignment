Blog API

A simple blog API, it currently uses FastAPI, SQLAlchemy, and SQLite. Future development will add new features to meet the assignment requirements.

Milestone 1: Initial Commit
    Includes basic project structure
    Dependencies: fastapi==0.141.1, uvicorn==0.52.4, sqlalchemy==2.0.55, email-validator==2.3.0
    This first commit creates the initial structure based on waht we have learnt in the Advanced computing course. The application at this stage connects FastAPI to an SQLite database and defines the User model with an ID, username, email address, and hashed password.

    Testing at this stage:
        Create a virtual environment: 
            python -m venv .venv
            .venv\Scripts\Activate.ps1

        Install requirements:
            python -m pip install -r requirements.txt

        Run the app:
            uvicorn main:app --reload
        
        Open the endpoint browser:
            http://127.0.0.1:8000/docs

            Try the GET/health endpoint, this returns 200 OK

            Additionaly, opening:
            http://127.0.0.1:8000/health
            This will display 200 OK

