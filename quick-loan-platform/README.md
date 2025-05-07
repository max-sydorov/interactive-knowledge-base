# Quick Loan Platform

A modern loan application platform built with Spring Boot and React.

## Project Structure

```
quick-loan-platform/
├── docs/                      # Project documentation
├── db/                        # Database scripts and migrations
│   └── schema.sql            # Database schema definition
├── loan-application-service/  # Backend Spring Boot service
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/        # Java source code
│   │   │   └── resources/   # Configuration files
│   │   └── test/            # Test files
│   └── pom.xml              # Maven configuration
└── lovable-ui/              # Frontend React application
    ├── src/
    │   ├── components/      # React components
    │   ├── services/        # API services
    │   ├── pages/          # Page components
    │   └── styles/         # CSS and styling
    └── package.json        # NPM configuration
```

## Documentation

For detailed documentation about the platform architecture, API specifications, and development guidelines, please visit our [Documentation](./docs/README.md).

## Prerequisites

Before you begin, ensure you have the following installed:

### Backend Requirements
- Java 17 or higher
- Maven 3.6 or higher
- PostgreSQL 15 or higher

### Frontend Requirements
- Node.js 18 or higher
- npm 9 or higher

## Installation

### 1. Database Setup

1. Install PostgreSQL if you haven't already:
   ```bash
   # For macOS using Homebrew
   brew install postgresql@15
   ```

2. Start PostgreSQL service:
   ```bash
   brew services start postgresql@15
   ```

3. Create the user and database:
   ```bash
   psql -d postgres -f db/setup.sql
   ```

4. Run the database schema:
   ```bash
   psql -h localhost -U loan_application_user -d loan_application -f db/schema.sql
   ```

### 2. Backend Service Setup

1. Navigate to the backend service directory:
   ```bash
   cd loan-application-service
   ```

2. Install dependencies:
   ```bash
   mvn clean install
   ```


### 3. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd lovable-ui
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

### 1. Start the Backend Service

```bash
cd loan-application-service
mvn spring-boot:run
```

The backend service will start on `http://localhost:8080`

### 2. Start the Frontend Development Server

```bash
cd lovable-ui
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Development

### Backend Development
- The backend is built with Spring Boot 3.2.3
- Uses Spring Data JPA for database operations
- Follows RESTful API design principles

### Frontend Development
- Built with React 18 and TypeScript
- Uses Vite as the build tool
- Implements modern UI components with Radix UI
- Styled with Tailwind CSS

## Testing

### Backend Tests
```bash
cd loan-application-service
mvn test
```

### Frontend Tests
```bash
cd lovable-ui
npm test
```