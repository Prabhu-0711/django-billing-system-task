# Django Billing System

A simple billing system built using Django.

## Features

- Product Management
- Billing Calculation
- Tax Computation
- Denomination Based Change Calculation
- Purchase History
- Email Invoice (SMTP)

## Tech Stack

- Python
- Django
- TailwindCSS
- PostgreSQL

## Setup

```bash
git clone <repo-url>
cd billing-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
