# Tuinue Wasichana Backend

A Flask-based REST API backend for managing charitable donations and menstrual health support programs.

## Overview

Tuinue Wasichana is a platform that connects donors with charities focused on menstrual health initiatives. The system allows charities to manage inventories, share success stories, and receive donations while donors can contribute to various causes.

## Features

- **User Authentication**

  - Multi-user type support (Admin, Donor, Charity)
  - Email verification for registration
  - JWT-based authentication
  - Secure password handling
- **Charity Management**

  - Charity profile creation and management
  - Story sharing functionality
  - Inventory tracking
  - Donation history
- **Donation System**

  - One-time and recurring donations
  - Anonymous donation option
  - Donation tracking per charity
- **Admin Features**

  - User management
  - Charity application approval
  - System-wide monitoring

## Tech Stack

- **Backend Framework**: Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Cache**: Redis
- **Migration Tool**: Alembic
- **Security**: Flask-Bcrypt

## Prerequisites

- Python 3.12
- Redis Server
- Pipenv

## Installation

1. Clone the repository:

```sh
git clone <repository-url>
cd Tuinue-Wasichana-Back
```

2. Install dependencies:

```sh
pipenv install
```

3. Set up environment variables:

```sh
cp .env.example .env
```

Configure the following variables in `.env`:

```
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

4. Initialize the database:

```sh
flask db upgrade
python seed.py
```

## Running the Application

1. Start the Redis server:

```sh
redis-server
```

2. Run the Flask application:

```sh
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/verify-token` - Verify email token
- `POST /auth/login` - User login

### Charities

- `GET /charities` - List all charities
- `GET /charities/<id>` - Get charity details
- `POST /charities` - Create charity profile

### Donations

- `POST /donations` - Make a donation
- `GET /donations/charity/<id>` - Get charity donations

### Stories

- `GET /stories/charity/<id>` - Get charity stories
- `POST /stories` - Create new story

### Inventory

- `GET /inventory/charity/<id>` - Get charity inventory
- `POST /inventory` - Add inventory item

## Database Schema

The application uses the following main models:

- User (Base class for authentication)
- Donor (Extends User)
- Charity (Extends User)
- Donation
- Story
- Inventory
- CharityApplication

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
