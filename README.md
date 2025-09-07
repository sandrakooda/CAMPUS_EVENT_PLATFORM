# Campus_Event_Platform
Project documentation for My Campus Event Platform Project:

1.Technology used in the implementation:

a) Frontend : [CLIENT SIDE]

	HTML -> For Web Page
	CSS3 & Bootstrap-> For good user interface.
	
	JavaScript-> For Handling Client Side logic like
		* To Fetch data from the backend API
		* To Handle user interactions like searching, filtering, and opening different modals
		* To making API calls to register for events.
	Bootstrap Icons-> For clean and modern iconography in the application.

b) Backend: [SERVER SIDE]

	Python 3 -> For building the server logic.
	Flask -> This is a framework used for Python used to build the web server and REST API.
	SQLite-> This is a serverless, self-contained SQL database engine. The database is stored in a single file .

c) API & Data Format:

	RESTful API-> The backend will exposes a RESTful API for the frontend to be consume. This will decouples the client from the server, allowing them to be developed and scaled independently.
	JSON (JavaScript Object Notation)-> This one of the frequently used standard data format which is used for exchanging information between the frontend and the backend API.
 
 STRUCTURE OF CODE IN VS CODE:
 
campus-event-platform/  <-- This is your main folder
├── frontend/
│   └── index.html
├── venv/
├── app.py              <-- The Python BACKEND. It must be here.
├── campus_events.db
├── requirements.txt
└── test_api.py
	
2.Setup and Execution Commands
Commands that was use to set up environment and run this application.

    Step 1: To setup a Virtual Environment
    This will help to isolate your project dependencies.
		# We would create a virtual environment with name 'venv'
		python -m venv venv

		# To activate the virtual environment on windows
		venv\Scripts\activate

    Step 2: To install Dependencies
    We would need to install all the required Python packages file.

		#cmd
		pip install -r requirements.txt


    Step 3: We would need to initialize the Database
    We would need to create the database and schema and ingest data that is required for application. The app.py script will start and run the application. The init_db() is called automatically when we run the app.py directly.
    

    Step 4: Run the Flask Backend Server
    This command starts the development server, which will serve both the API and the index.html file.

		#cmd
		flask run --host=0.0.0.0 --port=5000


        * --host=0.0.0.0 makes the server accessible from other devices on your network.
        * --port=5000 runs it on the standard Flask port.
        * We will see output indicating the server is running, likely with debug=True.

    Step 5: Access the Website
    Open your web browser and navigate to:
		http://127.0.0.1:5000 or http://localhost:5000
        The Flask server will serve the index.html file, which will then use JavaScript to fetch data from the API endpoints running on the same server.


3.Project Documentation

Campus Event Platform: This is a full-stack web application designed to help university students explore/discover and register for campus events. This platform has responsive frontend and  robust RESTful API backend.

Key Features
Multi-Campus Support: Easily switch between different universities (MIT, CMU, Stanford) find events.
Event Discovery: We can Search/Browse all upcoming events on theinterface.
Search & Filter: We can quickly find events by title or filter by type (Workshop, Tech Talk, Hackathon, etc.).
Detailed Event View: Click on any event to see details about the date, time, location, and capacity and rating for the event
Real-time Registration: Register for an event by inputting the USN of the student

TO RUN THIS PROJECT:
Open this folder in VS Code (File -> Open Folder...).
Open the terminal in VS Code (View -> Terminal).

Create a virtual environment (this isolates your project's libraries):
First command------>python -m venv venv

Second command to activate the environment----> .\venv\Scripts\activate

THRID COMMAND,Ensure test_api.py is successfull 
Like this:<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7bfc2c13-ea6e-4b36-a967-4ef80324f34e" />

IN ANOTHER TERMINAL RUN python app.py:
FOUTH command----->python app.py
When we run python app.py we will get a url above like this:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0bc23c30-1190-45c4-9fcf-cbb204319490" />

whem you click on Webpage of campus event:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/eaf25e74-e86b-49d2-8c24-598fc0e4ce10" />

Registration of event by USN:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d2ae396b-0320-4c8f-ad52-c36f0f2f1555" />

Dropdown of all UNIVERSITIES:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1e50f61c-fe89-4ec6-bb3b-6522211b4372" />


Dropdown of all events happening in Event Platform:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2794dad8-4606-4123-a370-376cf8f9c418" />


Hackthon Event in CMU UNIVERSITY:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/165f90a4-8ae3-4de6-9459-ba9cd0343840" />

Techtalk in Massachusetts Institute of Technology:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d399b840-e816-4a36-842d-a6bd7cf89a26" />






