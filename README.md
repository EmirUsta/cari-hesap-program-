# Current Account and POS Management System

## Project Overview
This project is a comprehensive accounting, current account (customer balance), and Point of Sale (POS) system built from scratch. The system is designed to handle inventory management, customer debt/credit tracking, and fast checkout processes.

## System Architecture & Modules
1. **Core Database & API:** The central backbone storing customers, products, inventory levels, and financial transactions (debt/credit).
2. **Back-Office Management Panel:** An administrative interface for creating new customer accounts, tracking balances, managing inventory, and viewing reports.
3. **POS (Point of Sale) Panel:** A fast-paced screen for sales staff to search for products, add them to a cart, and complete transactions that instantly update customer balances and inventory.

## Tech Stack
- **Backend:** Python (Targeting a modern framework like FastAPI or Django)
- **Frontend:** React.js
- **Database:** PostgreSQL

## Deployment
The application will be containerized using Docker to ensure seamless deployment and testing across different environments.

### Local Development via Docker

To start the entire stack (FastAPI Backend + PostgreSQL Database) locally without managing Python versions or a local database installation:

1. Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine is installed and running.
2. From the root directory of this repository, run:

```bash
docker compose up --build
```

3. **Admin Panel:** Available at `http://localhost:5173`. Use this to manage Customers and Products.
4. **POS Panel:** Available at `http://localhost:5174`. Use this for fast checkout operations and point of sale.
5. **Backend API:** The FastAPI server will be available at `http://localhost:8000`. You can view the automatic Swagger UI documentation at `http://localhost:8000/docs`.
6. **Database:** The PostgreSQL database is mapped to port `5432` on your host machine, using the credentials `admin`:`password123` with a database named `pos_db`.

To stop the containers and remove them (without destroying your data, since volumes persist):
```bash
docker compose down
```

To destroy the database volume (wipe all data):
```bash
docker compose down -v
```