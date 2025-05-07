export interface Applicant {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  ssn: string;
  streetAddress: string;
  city: string;
  state: string;
  zipCode: string;
}

export interface Business {
  name: string;
  ein: string;
  streetAddress: string;
  city: string;
  state: string;
  zipCode: string;
  type: string;
  yearsInOperation: number;
  annualRevenue: number;
}

export interface LoanDetails {
  amount: number; // Frontend might use number, backend uses BigDecimal
  purpose: string;
}

export interface LoanApplication {
  id?: string; // Changed to string to match UUID from backend
  applicant: Applicant;
  business: Business;
  loanDetails: LoanDetails;
  status?: 'PENDING' | 'APPROVED' | 'DECLINED' | 'NEEDS_REVIEW'; // Ensure this matches backend LoanStatus Enum
  submittedAt?: string; // Backend sends string (ISO format), keep as string or convert to Date
} 