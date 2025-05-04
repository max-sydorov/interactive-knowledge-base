
import React from "react";
import { useFormContext } from "@/contexts/FormContext";
import { PersonalInfoForm } from "./PersonalInfoForm";
import { BusinessInfoForm } from "./BusinessInfoForm";
import { LoanDetailsForm } from "./LoanDetailsForm";
import { ReviewAndSubmit } from "./ReviewAndSubmit";
import { SubmissionSuccess } from "./SubmissionSuccess";
import { StepIndicator } from "./StepIndicator";

export const ApplicationForm: React.FC = () => {
  const { currentStep } = useFormContext();

  // Render the appropriate form based on the current step
  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return <PersonalInfoForm />;
      case 2:
        return <BusinessInfoForm />;
      case 3:
        return <LoanDetailsForm />;
      case 4:
        return <ReviewAndSubmit />;
      case 5:
        return <SubmissionSuccess />;
      default:
        return <PersonalInfoForm />;
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-6">
      {currentStep < 5 && <StepIndicator currentStep={currentStep} totalSteps={4} />}
      <div className="mt-6">
        {renderStep()}
      </div>
    </div>
  );
};
