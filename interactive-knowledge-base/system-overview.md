# System Overview

## Quick Loan - Online Platform for Small Business Loan Application Intake

A streamlined web-based platform for small business loan applications, featuring a ReactJS frontend, a Java Spring Boot backend with decisioning logic, and PostgreSQL for data persistence.

## Architecture

A standard three-tier architecture:
*   **Presentation Tier (Frontend):** ReactJS single-page application (SPA) running in the user's browser. Responsible for rendering the UI, capturing user input, client-side validation, and communicating with the backend API.
*   **Application Tier (Backend):** Java/Spring Boot RESTful API. Responsible for handling requests, server-side validation, executing business logic (including loan decisioning), and interacting with the persistence layer.
*   **Data Tier (Persistence):** PostgreSQL relational database. Responsible for storing and retrieving application details and decision outcomes.

## Workflow

1. **User fills out the multi-step form on the frontend.**
2. **Frontend validates and submits data to the backend API.**
3. **Backend validates, persists data, and runs decisioning logic.**
4. **Decision and application status are stored in PostgreSQL.**
5. **Frontend polls or queries for application status updates.**

