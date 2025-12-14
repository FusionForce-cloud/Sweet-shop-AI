# Sweet Shop Management System

A full-stack web application for managing a sweet shop inventory, built with TDD approach.

## Features

- User authentication (register/login)
- View available sweets
- Search sweets by name, category, price
- Purchase sweets (decreases quantity)
- Admin features: add, update, delete sweets, restock inventory

## Tech Stack

- Backend: Python FastAPI, SQLAlchemy, SQLite
- Frontend: React
- Testing: pytest

## Setup

### Backend

1. Navigate to backend directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run server: `uvicorn app.main:app --reload`

### Frontend

1. Navigate to frontend directory
2. Install dependencies: `npm install`
3. Run app: `npm start`

## API Endpoints

- POST /api/auth/register
- POST /api/auth/login
- GET /api/sweets
- GET /api/sweets/search
- POST /api/sweets (admin)
- PUT /api/sweets/:id (admin)
- DELETE /api/sweets/:id (admin)
- POST /api/sweets/:id/purchase (user)
- POST /api/sweets/:id/restock (admin)

## Testing

Run tests: `pytest`
