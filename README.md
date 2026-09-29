# TaskFlow

An Intelligent Task Management System built for modern software engineering workflows.

## Features

- **User Authentication**: Secure session-based login and registration using password hashing.
- **Task Management**: Create, view, update, and delete tasks with priority, status, and due dates.
- **Dashboard**: Quick overview of task statistics (pending, completed, overdue, etc.).
- **Search & Filtering**: Easily find tasks by text search or filter by status, priority, and category.
- **Responsive UI**: Clean, responsive frontend powered by modern HTML5, CSS3, and JavaScript.

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Fetch API
- **Backend**: Python 3, Flask, REST API Architecture
- **Database**: SQLite, SQLAlchemy (ORM)
- **Security**: Flask-Login, Werkzeug Security

## Architecture

TaskFlow uses a hybrid approach:
- The Flask backend serves server-rendered HTML templates for the main views (`/login`, `/dashboard`).
- Interactions on the pages (creating a task, loading tasks) use asynchronous JavaScript (`fetch`) to communicate with the RESTful JSON API (`/api/...`).
- Data is stored in a SQLite database and queried using SQLAlchemy ORM.

## Database

1. **Users Table**: Stores user credentials securely (`id`, `name`, `email`, `password_hash`).
2. **Tasks Table**: Stores task details (`id`, `user_id` as foreign key, `title`, `priority`, `status`, `due_date`, etc.).

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register` | Register a new user |
| POST | `/api/login` | Authenticate a user |
| POST | `/api/logout` | End user session |
| GET | `/api/tasks` | Get user's tasks (supports search & filters) |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/<id>` | Get a specific task |
| PUT | `/api/tasks/<id>` | Update a task completely |
| PATCH| `/api/tasks/<id>/status` | Update task status |
| GET | `/api/dashboard` | Get dashboard statistics |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TaskFlow.git
cd TaskFlow
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env to set your SECRET_KEY
```

## Running the Application

```bash
python run.py
```
The application will be available at `http://localhost:5000`.

## Testing

Run the automated test suite using pytest:
```bash
pytest
```

## Screenshots

*(Add screenshots of your application here)*

## Future Improvements

- Email notifications for overdue tasks
- Migration to PostgreSQL for production readiness
- Role-based access control (Admin vs Regular users)
- Dedicated mobile application using React Native or Flutter
- Cloud deployment on AWS/GCP or Heroku
