# SellControl Application

## Overview
SellControl is a comprehensive sales management and inventory control application designed to streamline business operations. This application helps businesses manage their sales pipeline, track inventory, and generate reports.

## Prerequisites
- Docker Engine
- Docker Compose
- Git (for cloning the repository)

## Deployment with Docker Compose

### Quick Start
1. Clone the repository:
```bash
git clone https://github.com/sgonzr12/sellControl.git
cd sellControl
```

2. Deploy the application:
```bash
docker compose up -d
```

3. Access the application at `http://localhost:8080`

### Docker Compose Configuration
The application is deployed using Docker Compose with the following services:

- **Web Frontend**: User interface for the SellControl application
- **API Backend**: RESTful services for business logic
- **Database**: Persistent storage for application data
- **Cache**: In-memory caching for performance optimization

## Environment Variables
Configure the application by setting environment variables in a `.env` file:

### Database Configuration
The application uses a `database.ini` file for database connection details. Create this file in the root directory with the following format:

```ini
[postgresql]
host=your_database_host
database=your_database_name
user=your_database_username
password=your_database_password
```

### Authentication Variables

```
# ps.env file
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secretç

# Frontend Environment
Create a `.env` file in the frontend directory with:

```
# frontend/.env file
VITE_GOOGLE_ID=your_google_client_id
```

This is required for Google authentication integration with the frontend application.
```

## Features
- Inventory management
- Sales tracking
- Customer relationship management
- Reporting and analytics
- User access control

## License
[MIT License](LICENSE)