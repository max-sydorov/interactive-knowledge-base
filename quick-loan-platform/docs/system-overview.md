# System Overview

## Quick Loan - Online Platform for Small Business Loan Application Intake

A streamlined web-based platform for small business loan applications, featuring a ReactJS frontend, a Java Spring Boot backend with decisioning logic, and PostgreSQL for data persistence.

---

## 1. Frontend (ReactJS)

### Features
- **Multi-step Application Form**: 
  - Step 1: Personal Information (name, contact, SSN, address)
  - Step 2: Business Information (business name, EIN, address, type, years in operation, revenue)
  - Step 3: Loan Details (amount requested, purpose)
  - Step 4: Review & Submit

- **Validation**: 
  - Client-side validation for required fields, formats, and logical checks.

- **Status Tracking**: 
  - After submission, applicants can check the status of their application.

- **User Experience**: 
  - Responsive design, clear progress indicators, and error handling.

- **API Integration**: 
  - Communicates with backend via RESTful endpoints for submission and status retrieval.

---

## 2. Backend (Java, Spring Boot)

### Core Components
- **REST API Endpoints**:
  - `POST /applications`: Accepts new loan applications.
  - `GET /applications/{id}`: Retrieves application and decision status.

- **Application Processing**:
  - Receives and validates incoming data.
  - Triggers decisioning logic upon application submission.

- **Decisioning Logic**:
  - Simple rule-based engine (e.g., minimum revenue, years in business, credit score threshold).
  - Assigns status: Approved, Declined, or Needs Review.
  - Stores decision outcome and rationale.

- **Security**:
  - Input sanitization, authentication (optional for MVP), and secure data handling.

- **Error Handling**:
  - Returns meaningful error messages and HTTP status codes.

---

## 3. Persistence Layer (PostgreSQL)

### Database Design
- **Tables**:
  - `applicants`: Stores personal information.
  - `businesses`: Stores business details.
  - `applications`: Links applicant, business, and loan request.
  - `decisions`: Stores decision status, rationale, and timestamps.

- **Relationships**:
  - One-to-many: Applicant to Applications.
  - One-to-one: Application to Decision.

- **Data Integrity**:
  - Use of foreign keys, constraints, and indexing for performance.

---

## 4. Workflow

1. **User fills out the multi-step form on the frontend.**
2. **Frontend validates and submits data to the backend API.**
3. **Backend validates, persists data, and runs decisioning logic.**
4. **Decision and application status are stored in PostgreSQL.**
5. **Frontend polls or queries for application status updates.**

---

## 5. Deployment & Operations

- **Frontend**: Deployed on a static hosting service (e.g., Vercel, Netlify).
- **Backend**: Deployed on a cloud platform (e.g., AWS, Heroku) with environment variables for DB credentials.
- **Database**: Managed PostgreSQL instance with secure access controls.
- **Monitoring**: Basic logging and error tracking for backend and database.

