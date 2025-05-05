CREATE USER loan_application_user WITH PASSWORD 'loan_application_password';
CREATE DATABASE loan_application OWNER loan_application_user;
GRANT ALL PRIVILEGES ON DATABASE loan_application TO loan_application_user;
