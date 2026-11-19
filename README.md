# Job Application Tracker

A Django REST Framework backend application for managing job applications, companies, and interview rounds.

The system helps users organize their job search by tracking applications, monitoring application statuses, scheduling interviews, and viewing application pipeline statistics.

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- drf-spectacular (Swagger / OpenAPI documentation)
- Git and GitHub

## Features

### Company Management
- Create, view, update, and delete companies.
- Store company details such as name, website, location, and industry.

### Application Management
- Create and manage job applications.
- Track application statuses: Wishlist, Applied, Interview, Offer, and Rejected.
- Filter applications by status and application date.
- View applications with their associated company names.

### Interview Management
- Create and manage interview rounds.
- Track interview outcomes: Pending, Passed, and Failed.
- Filter interviews by outcome and date.
- View upcoming pending interviews.

### Application Pipeline
- View the total number of applications.
- See application counts grouped by status.

### API Documentation
- Interactive API documentation using Swagger UI.
- OpenAPI schema generation.


## Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/rain-baba/job_application_tracker.git
cd job_application_tracker
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

The application will be available at:

http://127.0.0.1:8000/


## Database Models

The application uses three main models:

- **Company:** Stores company information such as name, website, location, and industry.
- **Application:** Stores job application details and links each application to a company.
- **InterviewRound:** Stores interview details and links each interview to an application.

### Model Relationships

- One company can have multiple job applications.
- One job application can have multiple interview rounds.

## Project Status

Phase 1 backend development is complete.

The project currently includes company management, job application tracking, interview management, filtering, pipeline statistics, and interactive API documentation.

Future improvements may include user authentication, frontend integration, and additional features.
