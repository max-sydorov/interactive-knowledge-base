# Database Setup Instructions

This directory contains the database schema for the Loan Application System. Follow these steps to set up the database on your local PostgreSQL instance.

## Prerequisites

- PostgreSQL installed on your machine
- `psql` command-line tool

## Setup Steps

*   Create the database user and database:
```bash
    psql -d postgres -f setup.sql
```

*   Create schema:
```bash
    psql -h localhost -U loan_application_user -d loan_application -f schema.sql
```