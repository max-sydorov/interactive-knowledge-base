
import { Applicant, Business, LoanDetails } from "../services/api";

export const validateApplicant = (applicant: Applicant): Record<string, string> => {
  const errors: Record<string, string> = {};

  // First Name validation
  if (!applicant.firstName.trim()) {
    errors.firstName = "First name is required";
  }

  // Last Name validation
  if (!applicant.lastName.trim()) {
    errors.lastName = "Last name is required";
  }

  // Email validation
  if (!applicant.email.trim()) {
    errors.email = "Email is required";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(applicant.email)) {
    errors.email = "Invalid email format";
  }

  // Phone validation
  if (!applicant.phone.trim()) {
    errors.phone = "Phone number is required";
  } else if (!/^\d{10}$/.test(applicant.phone.replace(/\D/g, ''))) {
    errors.phone = "Phone must be 10 digits";
  }

  // SSN validation
  if (!applicant.ssn.trim()) {
    errors.ssn = "SSN is required";
  } else if (!/^\d{9}$/.test(applicant.ssn.replace(/\D/g, ''))) {
    errors.ssn = "SSN must be 9 digits";
  }

  // Address validation
  if (!applicant.streetAddress.trim()) {
    errors.streetAddress = "Street address is required";
  }

  // City validation
  if (!applicant.city.trim()) {
    errors.city = "City is required";
  }

  // State validation
  if (!applicant.state.trim()) {
    errors.state = "State is required";
  } else if (applicant.state.length !== 2) {
    errors.state = "Please use 2-letter state code";
  }

  // Zip Code validation
  if (!applicant.zipCode.trim()) {
    errors.zipCode = "Zip code is required";
  } else if (!/^\d{5}(-\d{4})?$/.test(applicant.zipCode)) {
    errors.zipCode = "Invalid zip code format";
  }

  return errors;
};

export const validateBusiness = (business: Business): Record<string, string> => {
  const errors: Record<string, string> = {};

  // Business name validation
  if (!business.name.trim()) {
    errors.name = "Business name is required";
  }

  // EIN validation
  if (!business.ein.trim()) {
    errors.ein = "EIN is required";
  } else if (!/^\d{9}$/.test(business.ein.replace(/\D/g, ''))) {
    errors.ein = "EIN must be 9 digits";
  }

  // Address validation
  if (!business.streetAddress.trim()) {
    errors.streetAddress = "Street address is required";
  }

  // City validation
  if (!business.city.trim()) {
    errors.city = "City is required";
  }

  // State validation
  if (!business.state.trim()) {
    errors.state = "State is required";
  } else if (business.state.length !== 2) {
    errors.state = "Please use 2-letter state code";
  }

  // Zip Code validation
  if (!business.zipCode.trim()) {
    errors.zipCode = "Zip code is required";
  } else if (!/^\d{5}(-\d{4})?$/.test(business.zipCode)) {
    errors.zipCode = "Invalid zip code format";
  }

  // Business type validation
  if (!business.type.trim()) {
    errors.type = "Business type is required";
  }

  // Years in operation validation
  if (business.yearsInOperation <= 0) {
    errors.yearsInOperation = "Years in operation must be greater than 0";
  } else if (business.yearsInOperation > 100) {
    errors.yearsInOperation = "Please enter a valid number of years";
  }

  // Annual revenue validation
  if (business.annualRevenue <= 0) {
    errors.annualRevenue = "Annual revenue must be greater than 0";
  }

  return errors;
};

export const validateLoanDetails = (loanDetails: LoanDetails): Record<string, string> => {
  const errors: Record<string, string> = {};

  // Loan amount validation
  if (loanDetails.amount <= 0) {
    errors.amount = "Loan amount must be greater than 0";
  } else if (loanDetails.amount > 5000000) {
    errors.amount = "Loan amount cannot exceed $5,000,000";
  }

  // Loan purpose validation
  if (!loanDetails.purpose.trim()) {
    errors.purpose = "Loan purpose is required";
  } else if (loanDetails.purpose.length < 10) {
    errors.purpose = "Please provide more detail about the purpose";
  }

  return errors;
};
