# Interactive Knowledge Base for Quick Loan Platform

This repository contains a Proof of Concept (POC) for an Interactive Knowledge Base system that provides intelligent assistance for the Quick Loan Platform.

## Project Overview

The project consists of two main components:

1. **Interactive Knowledge Base**: An AI-powered system built with LangChain and OpenAI that can answer questions about the Quick Loan Platform, including its database schema, backend APIs, frontend components, and business processes.

2. **Quick Loan Platform**: A modern loan application platform built with Spring Boot and React, serving as the domain for the knowledge base to operate on.

## Components

### Interactive Knowledge Base

The knowledge base uses a multi-agent architecture to provide comprehensive information about different aspects of the Quick Loan Platform:

- **Knowledge Base Agent**: The main agent that orchestrates queries and responses
- **Database Agent**: Handles database-related questions
- **Backend Agent**: Answers questions about the backend service
- **Frontend Agent**: Provides information about the UI components
- **Database Executor**: Executes SQL queries against the actual database

### Quick Loan Platform

A full-stack application for processing loan applications:

- **Backend**: Spring Boot service for handling loan applications
- **Frontend**: React application with a user-friendly interface
- **Database**: PostgreSQL database for storing application data

## Installation

### Prerequisites

#### For Interactive Knowledge Base
- Python 3.8 or higher
- OpenAI API key

#### For Quick Loan Platform
- Java 17 or higher
- Maven 3.6 or higher
- PostgreSQL 15 or higher
- Node.js 18 or higher
- npm 9 or higher

### Setup Instructions

#### 1. Clone the repository
```bash
git clone https://github.com/yourusername/interactive-knowledge-base.git
cd interactive-knowledge-base
```

#### 2. Set up the Quick Loan Platform

##### Database Setup
```bash
# Install PostgreSQL (if not already installed)
# For macOS using Homebrew
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Create the user and database
psql -d postgres -f quick-loan-platform/db/setup.sql

# Run the database schema
psql -h localhost -U loan_application_user -d loan_application -f quick-loan-platform/db/schema.sql
```

##### Backend Setup
```bash
# Navigate to the backend service directory
cd quick-loan-platform/loan-application-service

# Install dependencies
mvn clean install
```

##### Frontend Setup
```bash
# Navigate to the frontend directory
cd quick-loan-platform/lovable-ui

# Install dependencies
npm install
```

#### 3. Set up the Interactive Knowledge Base

```bash
# Navigate to the knowledge base directory
cd interactive-knowledge-base

# Install dependencies
pip install -r requirements.txt

# Create a .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## Running the Application

### 1. Start the Quick Loan Platform

#### Start the Backend Service
```bash
cd quick-loan-platform/loan-application-service
mvn spring-boot:run
```
The backend service will start on `http://localhost:8080`

#### Start the Frontend Development Server
```bash
cd quick-loan-platform/lovable-ui
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### 2. Start the Interactive Knowledge Base

```bash
cd interactive-knowledge-base
python knowledge_base_agent.py
```

## Usage Examples

The Interactive Knowledge Base can answer questions such as:

- "What is the Quick Loan Platform?"
- "How does our application submission process work?"
- "What tables do we have in the database?"
- "Generate SQL query to get application status by user email"
- "What APIs do we have?"
- "What validation do we have for the Phone field?"
- "What pages do we have on UI?"
- "What is the status of an application for a specific user?"

## Development

### Interactive Knowledge Base
- Built with LangChain and OpenAI
- Uses a ReAct agent pattern for reasoning and acting
- Modular architecture with specialized agents for different domains

### Quick Loan Platform
- Backend: Spring Boot 3.2.3 with Spring Data JPA
- Frontend: React 18 with TypeScript, Vite, Radix UI, and Tailwind CSS
- Database: PostgreSQL

## Testing

### Quick Loan Platform Tests
```bash
# Backend Tests
cd quick-loan-platform/loan-application-service
mvn test

# Frontend Tests
cd quick-loan-platform/lovable-ui
npm test
```

## License

[MIT License](LICENSE)
