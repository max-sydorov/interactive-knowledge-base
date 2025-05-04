
import React from "react";
import { CheckIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface StepIndicatorProps {
  currentStep: number;
  totalSteps: number;
}

export const StepIndicator: React.FC<StepIndicatorProps> = ({ 
  currentStep, 
  totalSteps 
}) => {
  const steps = [
    { number: 1, title: "Personal Information" },
    { number: 2, title: "Business Information" },
    { number: 3, title: "Loan Details" },
    { number: 4, title: "Review & Submit" },
  ];

  return (
    <div className="w-full py-4">
      <div className="flex justify-between items-center mb-4">
        {steps.map((step, index) => {
          const isCompleted = currentStep > step.number;
          const isActive = currentStep === step.number;
          
          return (
            <React.Fragment key={step.number}>
              {/* Step circle */}
              <div className="flex flex-col items-center relative">
                <div
                  className={cn(
                    "flex items-center justify-center w-10 h-10 rounded-full border-2 transition-colors",
                    isCompleted ? "border-primary bg-primary text-primary-foreground" : 
                    isActive ? "border-primary bg-accent text-primary" : 
                    "border-gray-300 bg-white text-gray-400"
                  )}
                >
                  {isCompleted ? (
                    <CheckIcon className="w-5 h-5" />
                  ) : (
                    <span className="text-sm font-medium">{step.number}</span>
                  )}
                </div>
                <span className={cn(
                  "mt-2 text-xs font-medium whitespace-nowrap",
                  isCompleted || isActive ? "text-primary" : "text-gray-400"
                )}>
                  {step.title}
                </span>
              </div>
              
              {/* Connector line */}
              {index < steps.length - 1 && (
                <div
                  className={cn(
                    "flex-1 h-0.5 mx-2",
                    currentStep > index + 1 ? "bg-primary" : "bg-gray-300"
                  )}
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
