Blog API

A simple blog API, it currently uses FastAPI, SQLAlchemy, and SQLite. Future development will add new features to meet the assignment requirements.
    Dependencies: fastapi==0.141.1, uvicorn==0.52.4, sqlalchemy==2.0.55, email-validator==2.3.0
    
    Setup:
        Create a virtual environment: 
            python -m venv .venv
            .venv\Scripts\Activate.ps1

        Install requirements:
            python -m pip install -r requirements.txt

        Before starting the app, generate a secret:
            python -c "import secrets; print(secrets.token_hex(32))"

        Copy the result into an environment variable in the terminal.
            $env:JWT_SECRET = "paste-the-generated-value-here"

        Run the app:
            uvicorn main:app --reload
        
    Testing:
        Open the endpoint browser:
            http://127.0.0.1:8000/docs

            Try the GET/health endpoint, this returns 200 OK

        Additionaly, opening:
            http://127.0.0.1:8000/health
            This will display 200 OK

        Automated tests can now be ran using:
            python -m pytest -q
            This should result in 16 passed

        