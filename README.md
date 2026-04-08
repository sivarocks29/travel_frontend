# Pyolliv - Fleet Management System Backend

This repository contains the backend for the Pyolliv fleet booking system built with Django REST Framework and PostgreSQL.

## Architecture
The system supports three user roles:
1. `admin` - Manage users, vehicles, create bookings, and assign trips.
2. `car` - Vehicle owner panel to track earnings and individual trips.
3. `driver` - Dashboard to start/end trips, submit KM readings, and upload photos.

## Local Development Setup

1. **Prerequisites**
   - Python 3.10+
   - PostgreSQL (Running locally)

2. **Database Setup**
   Ensure PostgreSQL is running. Create a new database named `pyolliv_dev` (or match your `.env`):
   ```sql
   CREATE DATABASE pyolliv_dev;
   ```

3. **Environment Setup**
   Copy `.env.example` to `.env` and fill in DB credentials and secret variables.
   ```bash
   cp .env.example .env
   ```

4. **Install Dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Migrations & Seeding**
   Apply migrations, run seed data, and start server:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python seed.py # Optional: Seeds initial roles, users, and generic bookings
   python manage.py runserver
   ```

## API Documentation
Base URL: `http://localhost:8000/api`

- **Auth endpoints:** `POST /api/auth/login/` -> Bearer token.
- **Admin routes:** Protected under `/api/admin/...` for analytical processing.
- **Driver routes:** Protected under `/api/driver/...`
- **Car routes:** Protected under `/api/car/...`

## Production Deployment
The backend includes a `render.yaml` specifically tailored for deployment on **Render.com**. Connect the repository and it will auto-provision PostgreSQL, the Python Web Service, and map environment overrides securely.
