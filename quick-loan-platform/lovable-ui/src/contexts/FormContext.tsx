
import React, { createContext, useContext, useState } from "react";
import { LoanApplication, Applicant, Business, LoanDetails } from "../services/api";

// Define the context type
type FormContextType = {
  currentStep: number;
  setCurrentStep: React.Dispatch<React.SetStateAction<number>>;
  applicant: Applicant;
  setApplicant: React.Dispatch<React.SetStateAction<Applicant>>;
  business: Business;
  setBusiness: React.Dispatch<React.SetStateAction<Business>>;
  loanDetails: LoanDetails;
  setLoanDetails: React.Dispatch<React.SetStateAction<LoanDetails>>;
  applicationId: string | null;
  setApplicationId: React.Dispatch<React.SetStateAction<string | null>>;
  isSubmitting: boolean;
  setIsSubmitting: React.Dispatch<React.SetStateAction<boolean>>;
};

// Create the context
const FormContext = createContext<FormContextType | undefined>(undefined);

// Default values for the form
const defaultApplicant: Applicant = {
  firstName: "",
  lastName: "",
  email: "",
  phone: "",
  ssn: "",
  streetAddress: "",
  city: "",
  state: "",
  zipCode: "",
};

const defaultBusiness: Business = {
  name: "",
  ein: "",
  streetAddress: "",
  city: "",
  state: "",
  zipCode: "",
  type: "",
  yearsInOperation: 0,
  annualRevenue: 0,
};

const defaultLoanDetails: LoanDetails = {
  amount: 0,
  purpose: "",
};

// Create the provider component
export const FormProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [applicant, setApplicant] = useState<Applicant>(defaultApplicant);
  const [business, setBusiness] = useState<Business>(defaultBusiness);
  const [loanDetails, setLoanDetails] = useState<LoanDetails>(defaultLoanDetails);
  const [applicationId, setApplicationId] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const value = {
    currentStep,
    setCurrentStep,
    applicant,
    setApplicant,
    business,
    setBusiness,
    loanDetails,
    setLoanDetails,
    applicationId,
    setApplicationId,
    isSubmitting,
    setIsSubmitting,
  };

  return <FormContext.Provider value={value}>{children}</FormContext.Provider>;
};

// Create a hook for using the context
export const useFormContext = (): FormContextType => {
  const context = useContext(FormContext);
  if (context === undefined) {
    throw new Error("useFormContext must be used within a FormProvider");
  }
  return context;
};
