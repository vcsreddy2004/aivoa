# HCP Interaction Management Backend

A backend system for managing Healthcare Professional (HCP) interactions with AI-powered insights like summarization and follow-up suggestions.

## Features

*   Log interactions with HCPs
    
*   Edit or update interaction records
    
*   Retrieve HCP interaction history
    
*   AI-based follow-up suggestions
    
*   AI-powered interaction summarization
    

## Tech Stack

*   Python
    
*   MySQL
    
*   Groq API (LLM)
    
*   Virtualenv
    

# Environment Setup

Create a .env file inside the backend folder and add the following variables:

GROQ_API_KEY=

MY_SQL_HOST=

MY_SQL_USER=

MY_SQL_PASSWORD=

MY_SQL_DB=

## Description of variables:

GROQ_API_KEY → API key for Groq

MY_SQL_HOST → MySQL host (example: localhost)

MY_SQL_USER → MySQL username

MY_SQL_PASSWORD → MySQL password

MY_SQL_DB → Database name

# Virtual Environment Setup

Step 1: Install virtualenvRun: pip install virtualenv

Step 2: Activate virtual environment

For Windows: Run: venv\\Scripts\\activate

For Mac/Linux: Run: source venv/bin/activate

# Database Setup

Step 1: Create databaseRun: CREATE DATABASE your\_database\_name;

Step 2: Create table

```
CREATE TABLE interactions (id INT AUTO\_INCREMENT PRIMARY KEY,hcp\_name VARCHAR(255),interaction\_type VARCHAR(100),date DATE,time TIME,attendees TEXT,topics TEXT,materials TEXT,samples TEXT,sentiment VARCHAR(50),outcomes TEXT,follow\_up TEXT,created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP);
```

Running the Application

# Backend:

Go to backend folder and run: uvicorn app.main:app --reload

# Frontend:

Go to frontend folder and run: npm run dev

Core Functionalities (Modes)

log_interactions Stores a new interaction in the database.

Example input:{"hcp\_name": "Dr. John","interaction\_type": "Meeting","date": "2026-06-03","time": "10:30","attendees": "Sajith, Sudharshan","topics": "LLM emotional understanding","sentiment": "Neutral","outcomes": "Model failed to detect emotions","follow\_up": "Retrain model"}

* edit_interactions Updates an existing interaction record.

* get_hcp_history Fetches all interactions of a given HCP.

Example:{"hcp\_name": "Dr. John"}

* suggest_followup Uses AI to recommend next steps.

Example:{"suggestion": "Schedule retraining with improved dataset"}

* summarize_interaction Generates a short summary.

Example:{"summary": "Discussion focused on improving emotion detection in LLM models"}

Author

Venna Chandra Sekhar Reddy

License

This project is for educational and development purposes.
