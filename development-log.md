Development log


Milestone 1: Initial Commit
    Work completed
    Created the FastAPI application
    Setup the SQLite database connections using SQLAlchemy
    Created the User model with ID, username, email address, and hashed password
    Created pydantic schemas with emailStr and field length validation
    Created the requirements.txt file and documented requirement versions used
    Created a .gitignore files witht the files to be excluded from the commit
    Created a Readme file to describe how to run the application at this stage

    Testing at this stage:
        Trying to start the application with Uvicorn gave the following error: "C:\Users\Mohammud\Documents\Birkbeck\Term 1\Advanced Computing\Piazza Assignment\models.py", line 8
        id = Column(Integer, primary_key=True, index=True)
        ^
        IndentationError: unindent does not match any outer indentation level

        I initially wasn't sure what it should have been indented to so I used copilto to debug it which pointed out what was wrong with my code. I was then able to test as follows:

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

