Development log


Milestone 1(08/11/2026): Initial Commit
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

        I initially wasn't sure what should have been indented to so I used copilot to debug it which pointed out what was wrong with my code. I was then able to test as follows:

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

Milestone 2(16/11/2026): Database models and schemas 
    Work completed
    Created Post, Topic, Reaction, and Comment models
    Added Foreign keys to link the models
    Added a many-to-many assosciation between posts and topics
    Added a unique constraint to post reactions so users can only have one reaction per post
    Added validation where required
    Created a seed.py with the four topics: Politics, Health, Sport, and Tech

Testing at this stage:
    The previous tests should still work as per the last milestone.
    
    After the virtual environment has been created, run the following line to populate the topics:
        python seed.py
    
    Then run the following to inspect the database:
        sqlite3 piazza.db
    
    This should move the terminal to sql, then enter:
        .tables
    
    This returned:
        comments     posts     posts_topics     reactions     topics     users

    The next test is to run:
        select * from topics;
    
    This shoud display the four topics, but initial runs of this would only display id and name headers with no topics despite multiple runs of seeds.py. As I was unsure, I used copilot which suggested using:
        from seed import seed_topics
        seed_topics()
    I wasn't entirely sure of how to implement it and was sure that the code was correct and did not require it to be added. I exited the application and ran seed.py again in the terminal.
    Having done that, the select * from topics; query worked and displayed:
        ╭────┬──────────╮
        │ id │   name   │
        ╞════╪══════════╡
        │  1 │ Politics │
        │  2 │ Health   │
        │  3 │ Sport    │
        │  4 │ Tech     │
        ╰────┴──────────╯
    Additionally, I tested running seed.py twice and then testing the topics to ensure it did not create duplicates which it did not.
    
Milestone 3(19/11/2026): Authentication, Core Post API, and automated tests
    Work completed
    Added password hashing using pwdlib
    Added user registration and login endpointS
    Added JWT access tokes with a 30 minute expiry time
    Added bearer-token authentication and a method to identify the current user
    Added protected post creation so the post author is taken from the user who has been authenticated rather than allow the author to be provided in the request
    Added validation for:
        Expiry dates cannot be in the past
        A minimum of one topic being selected
        Valid topic IDs
        Duplicate topics IDs
    Added post-topic records to the posts_topics assosciation table
    Added GET/ posts and GET/ posts/{post-id} to retrieve all or a single post
    Added automated tests using pytest

Testing at this stage:
    Registration was tested for
        Successful registration
        Duplicate email
        Invalide data
    Login was tested for:
        Succesful login
        Incorrect password
        Unknown email
    JWT Authentication was tested for:
        No token
        Valid Token
        Invalid Token
    Post functionalities tested:
        Unauthenticated post creation
        Successful post creation
        Missing topics
        Invalid topic IDs
        Duplicate topic IDs
        Retrieving all posts
        Retrieving a specific post

    Automated tests ran using:
        python -m pytest -q
        This returned 16 passed

Issues encountered:
    Once again I faced an issue with indentation, and I had to rely on copliot to assist with debugging the code. But it turned out I had already fixed the issue but not saved my file. I resaved it and it worked ok.

    Another error that came up was: NameError: name 'models' is not defined
    This was because I had failed to add import models to the conftest.py file - Copilot was used here for debugging as well

    The third issue after that had been corrected was a mislabellign issue where I named the assosciation posts_topics in models.py but was referencing post_topics. This returned an error that module 'models' has no attribute in 'post_topics'. I used copilot to help with debugging it which identified the issue and corrected it.

    Additionally, during testing mid-development some test posts had saved to the database before the topic-assosciation error arose because they had already been committed, thios showed when I looked at the database using: 
        SELECT * FROM posts;
        This returned four posts
        Testing: 
        SELECT * FROM posts_topics;
        This return two rows.
    I then deleted the additional posts which had no assosciation. At this stage, I have not yet learnt how to prevent this from happening, it is something that I will need to consider in future.

