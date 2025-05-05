-- Create ENUM type for Loan Application Status
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'loan_status') THEN
        CREATE TYPE loan_status AS ENUM ('PENDING', 'APPROVED', 'DECLINED', 'NEEDS_REVIEW');
    END IF;
END$$;

-- Create Applicants table
CREATE TABLE IF NOT EXISTS applicants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    ssn VARCHAR(11) UNIQUE, -- Consider encryption or tokenization in a real system
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Businesses table
CREATE TABLE IF NOT EXISTS businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    ein VARCHAR(10) NOT NULL UNIQUE, -- Format: XX-XXXXXXX
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    type VARCHAR(100),
    years_in_operation INTEGER NOT NULL CHECK (years_in_operation >= 0),
    annual_revenue NUMERIC(19, 2) NOT NULL CHECK (annual_revenue >= 0), -- Using NUMERIC for currency
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Loan Applications table
CREATE TABLE IF NOT EXISTS loan_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    applicant_id UUID NOT NULL,
    business_id UUID NOT NULL,
    loan_amount NUMERIC(19, 2) NOT NULL CHECK (loan_amount > 0),
    loan_purpose TEXT,
    status loan_status NOT NULL DEFAULT 'PENDING',
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_applicant
        FOREIGN KEY(applicant_id)
        REFERENCES applicants(id)
        ON DELETE RESTRICT, -- Prevent deleting an applicant if they have applications

    CONSTRAINT fk_business
        FOREIGN KEY(business_id)
        REFERENCES businesses(id)
        ON DELETE RESTRICT -- Prevent deleting a business if it has applications
);

-- Add Indexes for frequently queried columns / foreign keys
CREATE INDEX IF NOT EXISTS idx_applicants_email ON applicants(email);
CREATE INDEX IF NOT EXISTS idx_applicants_ssn ON applicants(ssn); -- If queried often, otherwise maybe remove for security
CREATE INDEX IF NOT EXISTS idx_businesses_ein ON businesses(ein);
CREATE INDEX IF NOT EXISTS idx_loan_applications_applicant_id ON loan_applications(applicant_id);
CREATE INDEX IF NOT EXISTS idx_loan_applications_business_id ON loan_applications(business_id);
CREATE INDEX IF NOT EXISTS idx_loan_applications_status ON loan_applications(status);
CREATE INDEX IF NOT EXISTS idx_loan_applications_submitted_at ON loan_applications(submitted_at);

-- Optional: Grant permissions (replace 'your_app_user' with the actual database user)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON applicants, businesses, loan_applications TO your_app_user;
-- GRANT USAGE, SELECT ON SEQUENCE applicants_id_seq, businesses_id_seq, loan_applications_id_seq TO your_app_user; -- Only if using SERIAL PKs
-- GRANT USAGE ON TYPE loan_status TO your_app_user;