-- Remove ENUM type if it exists (run this separately if migrating an existing DB)
-- DROP TYPE IF EXISTS loan_status;

-- Create Applicants table (no changes here)
CREATE TABLE IF NOT EXISTS applicants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    ssn VARCHAR(11) UNIQUE,
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Businesses table (no changes here)
CREATE TABLE IF NOT EXISTS businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    ein VARCHAR(10) NOT NULL UNIQUE,
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    type VARCHAR(100),
    years_in_operation INTEGER NOT NULL CHECK (years_in_operation >= 0),
    annual_revenue NUMERIC(19, 2) NOT NULL CHECK (annual_revenue >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Loan Applications table (status column changed)
CREATE TABLE IF NOT EXISTS loan_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    applicant_id UUID NOT NULL,
    business_id UUID NOT NULL,
    loan_amount NUMERIC(19, 2) NOT NULL CHECK (loan_amount > 0),
    loan_purpose TEXT,
    -- Changed status to VARCHAR and added a CHECK constraint
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING'
        CHECK (status IN ('PENDING', 'APPROVED', 'DECLINED', 'NEEDS_REVIEW')),
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_applicant
        FOREIGN KEY(applicant_id)
        REFERENCES applicants(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_business
        FOREIGN KEY(business_id)
        REFERENCES businesses(id)
        ON DELETE RESTRICT
);

-- Add Indexes (no changes here, but ensure they exist)
CREATE INDEX IF NOT EXISTS idx_applicants_email ON applicants(email);
CREATE INDEX IF NOT EXISTS idx_applicants_ssn ON applicants(ssn);
CREATE INDEX IF NOT EXISTS idx_businesses_ein ON businesses(ein);
CREATE INDEX IF NOT EXISTS idx_loan_applications_applicant_id ON loan_applications(applicant_id);
CREATE INDEX IF NOT EXISTS idx_loan_applications_business_id ON loan_applications(business_id);
CREATE INDEX IF NOT EXISTS idx_loan_applications_status ON loan_applications(status);
CREATE INDEX IF NOT EXISTS idx_loan_applications_submitted_at ON loan_applications(submitted_at);