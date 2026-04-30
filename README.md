HCP Interaction Management Backend

A backend system for managing Healthcare Professional (HCP) interactions with AI-powered insights like summarization and follow-up suggestions.

Features

*   Log interactions with HCPs
    
*   Edit or update interaction records
    
*   Retrieve HCP interaction history
    
*   AI-based follow-up suggestions
    
*   AI-powered interaction summarization
    

Tech Stack

*   Python
    
*   MySQL
    
*   Groq API (LLM)
    
*   Virtualenv
    

Environment Setup

Create a .env file inside the backend folder and add the following variables:

GROQ\_API\_KEY=MY\_SQL\_HOST=MY\_SQL\_USER=MY\_SQL\_PASSWORD=MY\_SQL\_DB=

Description of variables:

GROQ\_API\_KEY → API key for GroqMY\_SQL\_HOST → MySQL host (example: localhost)MY\_SQL\_USER → MySQL usernameMY\_SQL\_PASSWORD → MySQL passwordMY\_SQL\_DB → Database name

Virtual Environment Setup

Step 1: Install virtualenvRun: pip install virtualenv

Step 2: Create virtual environmentRun: virtualenv venv

Step 3: Activate virtual environment

For Windows:Run: venv\\Scripts\\activate

For Mac/Linux:Run: source venv/bin/activate

Install Dependencies

After activating the virtual environment, run:pip install -r requirements.txt

Database Setup

Step 1: Create databaseRun: CREATE DATABASE your\_database\_name;

Step 2: Create table

CREATE TABLE interactions (id INT AUTO\_INCREMENT PRIMARY KEY,hcp\_name VARCHAR(255),interaction\_type VARCHAR(100),date DATE,time TIME,attendees TEXT,topics TEXT,materials TEXT,samples TEXT,sentiment VARCHAR(50),outcomes TEXT,follow\_up TEXT,created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP);

Running the Application

Backend:

Go to backend folder and run:uvicorn app.main:app --reload

Frontend:

Go to frontend folder and run:npm run dev

Core Functionalities (Modes)

log\_interactionsStores a new interaction in the database.

Example input:{"hcp\_name": "Dr. John","interaction\_type": "Meeting","date": "2026-06-03","time": "10:30","attendees": "Sajith, Sudharshan","topics": "LLM emotional understanding","sentiment": "Neutral","outcomes": "Model failed to detect emotions","follow\_up": "Retrain model"}

edit\_interactionsUpdates an existing interaction record.

get\_hcp\_historyFetches all interactions of a given HCP.

Example:{"hcp\_name": "Dr. John"}

suggest\_followupUses AI to recommend next steps.

Example:{"suggestion": "Schedule retraining with improved dataset"}

summarize\_interactionGenerates a short summary.

Example:{"summary": "Discussion focused on improving emotion detection in LLM models"}

Project Structure

backend/app/main.pytools.pydb.py.envrequirements.txtREADME.md

Notes

*   Do not commit the .env file
    
*   Add .env to .gitignore
    
*   Ensure MySQL is running before starting
    

Author

Venna Chandra Sekhar Reddy

License

This project is for educational and development purposes.