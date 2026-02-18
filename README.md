# Billing System - Django Project

A comprehensive Django-based billing system for managing products, purchases, and generating invoices.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Database Setup](#database-setup)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before running the project, ensure you have the following installed:

1. **Python** (3.8 or higher)
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **PostgreSQL** (12 or higher)
   - Download from [postgresql.org](https://www.postgresql.org/download/)
   - Install and ensure the PostgreSQL server is running
   - Verify installation: `psql --version`

3. **Git** (optional, for cloning)
   - Download from [git-scm.com](https://git-scm.com/download/win)

## Installation

### 1. Extract the Project
Extract the billing_system project folder to your desired location.

### 2. Create and Activate Virtual Environment

**On Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Configuration

### 1. Create Environment File
Create a `.env` file in the project root directory with your Gmail credentials:

```
USER=username
PASSWORD=password
HOST=host/address
PORT=port

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

**Note:** For Gmail:
- Use your Gmail address for `EMAIL_HOST_USER`
- Generate an App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- If you don't have 2-factor authentication enabled, you may need to enable it first

### 2. Database Configuration
The project is configured to use PostgreSQL with the following default credentials:
- **Database Name:** `billing_system_db`
- **Username:** `postgres`
- **Password:** ``
- **Host:** `localhost`
- **Port:** `5432`

If you need to use different credentials, update them in `billing_system/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```

## Running the Project

### 1. Start PostgreSQL Server
Ensure PostgreSQL is running on your machine. 

**On Windows:** PostgreSQL typically runs as a service. Check Services (services.msc) to ensure it's running.

**On macOS:** 
```bash
brew services start postgresql
```

**On Linux:**
```bash
sudo systemctl start postgresql
```

### 2. Apply Migrations
```bash
python manage.py migrate
```

### 3. Create a Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account (username, email, password).

### 4. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

#### Access Points:
- **Main Application:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

### 5. Stop the Server
Press `Ctrl+C` in the terminal where the server is running.

## Database Setup

### First-Time Setup
1. Ensure PostgreSQL is installed and running
2. Create the database (the project will handle this during migration):
   ```bash
   python manage.py migrate
   ```

### Load Sample Data
The project includes migrations that seed initial data:
   ```bash
   python manage.py migrate
   ```
   This will automatically run the seed migrations (`0002_seed_products.py`, `0004_seed_shopdenomination.py`)

### Reset Database (Caution!)
To delete and recreate the entire database:
```bash
# Delete all migration files except __init__.py in products/migrations/
# Then run:
python manage.py migrate
```

### Backup Database
```bash
pg_dump -U postgres billing_system_db > backup.sql
```

### Restore Database
```bash
psql -U postgres billing_system_db < backup.sql
```

## Troubleshooting

### 1. "ModuleNotFoundError: No module named 'django'"
**Solution:** Ensure your virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### 2. "psycopg2: connection refused"
**Problem:** PostgreSQL is not running or credentials are incorrect.

**Solutions:**
- Verify PostgreSQL is running
- Check database credentials in `billing_system/settings.py`
- Verify PostgreSQL user 'postgres' exists with password ''

### 3. "database 'billing_system_db' does not exist"
**Solution:** Create the database first:
```bash
psql -U postgres -c "CREATE DATABASE billing_system_db;"
```

### 4. "connection refused" on port 5432
**Problem:** PostgreSQL service is not running.

**Solutions:**
- **Windows:** Start PostgreSQL service from Services
- **macOS:** `brew services start postgresql`
- **Linux:** `sudo systemctl start postgresql`

### 5. "SyntaxError: invalid syntax"
**Problem:** Python version incompatibility.

**Solution:** Ensure you're using Python 3.8 or higher:
```bash
python --version
```

### 6. Static files not loading
**Solution:** Collect static files:
```bash
python manage.py collectstatic
```

### 7. Email sending not working
**Problem:** Gmail credentials not set or incorrect.

**Solutions:**
- Verify `.env` file exists in project root with correct credentials
- Use Gmail App Password (not regular password)
- Enable 2-factor authentication on Gmail account
- Check firewall/antivirus blocking SMTP

### 8. Port 8000 already in use
**Solution:** Run on a different port:
```bash
python manage.py runserver 8001
```

### 9. "no pg_hba.conf entry for host" error
**Problem:** PostgreSQL authentication issue.

**Solution:** Verify PostgreSQL connection settings and try:
```bash
psql -U postgres -h localhost -d postgres
```

## Project Structure

```
django-billing-system-task/
├── README.md                 # This file
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3               # SQLite database (if using SQLite)
├── billing_system/          # Project configuration
│   ├── settings.py          # Project settings
│   ├── urls.py              # Project URL routing
│   ├── asgi.py              # ASGI configuration
│   └── wsgi.py              # WSGI configuration
└── products/                # Products app
    ├── models.py            # Database models
    ├── views.py             # View logic
    ├── urls.py              # App URL routing
    ├── admin.py             # Admin interface
    ├── tests.py             # Tests
    ├── utils.py             # Utility functions
    ├── migrations/          # Database migrations
    └── templates/           # HTML templates
```

## Additional Commands

### Create a New Migration
```bash
python manage.py makemigrations
```

### Check Database Queries
```bash
python manage.py sqlmigrate products 0001
```

### Interactive Python Shell
```bash
python manage.py shell
```

### Check Project Setup
```bash
python manage.py check
```

## Support

For issues or questions, check the [Django documentation](https://docs.djangoproject.com/) or refer to the official [Django troubleshooting guide](https://docs.djangoproject.com/en/6.0/faq/).
