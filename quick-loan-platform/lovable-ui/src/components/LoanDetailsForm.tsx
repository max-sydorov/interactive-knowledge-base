
import React, { useState, useEffect } from "react";
import { useFormContext } from "@/contexts/FormContext";
import { validateLoanDetails } from "@/utils/validation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";

export const LoanDetailsForm: React.FC = () => {
  const { loanDetails, setLoanDetails, setCurrentStep } = useFormContext();
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  // Format currency input
  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  // Parse currency input
  const parseCurrency = (value: string): number => {
    return Number(value.replace(/[^0-9.-]+/g, ''));
  };

  const handleInputChange = (field: keyof typeof loanDetails, value: string | number) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    
    setLoanDetails(prev => ({
      ...prev,
      [field]: field === "amount" && typeof value === "string" 
        ? parseCurrency(value) 
        : value
    }));
  };

  // Validate fields when their values change
  useEffect(() => {
    const validationErrors = validateLoanDetails(loanDetails);
    setErrors(validationErrors);
  }, [loanDetails]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Mark all fields as touched
    const allTouched = Object.keys(loanDetails).reduce(
      (acc, key) => ({ ...acc, [key]: true }),
      {}
    );
    setTouched(allTouched);
    
    // Validate all fields
    const validationErrors = validateLoanDetails(loanDetails);
    setErrors(validationErrors);
    
    // Proceed if no errors
    if (Object.keys(validationErrors).length === 0) {
      setCurrentStep(4);
    } else {
      // Scroll to the first error
      const firstErrorField = document.querySelector('[aria-invalid="true"]');
      if (firstErrorField) {
        firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  };

  const goBack = () => {
    setCurrentStep(2);
  };

  return (
    <Card className="animate-fade-in">
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Loan Amount */}
          <div className="space-y-2">
            <Label htmlFor="loanAmount">
              Loan Amount <span className="text-destructive">*</span>
            </Label>
            <Input
              id="loanAmount"
              value={loanDetails.amount ? formatCurrency(loanDetails.amount) : ""}
              onChange={(e) => handleInputChange("amount", e.target.value)}
              onFocus={(e) => {
                // When focused, if the value is $0, clear it
                if (parseCurrency(e.target.value) === 0) {
                  handleInputChange("amount", "");
                }
              }}
              onBlur={(e) => {
                // When blurred, if the value is empty, set it to $0
                if (e.target.value === "") {
                  handleInputChange("amount", 0);
                }
              }}
              placeholder="$0"
              aria-invalid={touched.amount && !!errors.amount}
              aria-describedby={errors.amount ? "loanAmount-error" : undefined}
            />
            {touched.amount && errors.amount && (
              <p id="loanAmount-error" className="text-sm text-destructive">
                {errors.amount}
              </p>
            )}
          </div>

          {/* Loan Purpose */}
          <div className="space-y-2">
            <Label htmlFor="loanPurpose">
              Loan Purpose <span className="text-destructive">*</span>
            </Label>
            <Textarea
              id="loanPurpose"
              value={loanDetails.purpose}
              onChange={(e) => handleInputChange("purpose", e.target.value)}
              placeholder="Please describe how you plan to use the loan funds..."
              className="min-h-[120px]"
              aria-invalid={touched.purpose && !!errors.purpose}
              aria-describedby={errors.purpose ? "loanPurpose-error" : undefined}
            />
            {touched.purpose && errors.purpose && (
              <p id="loanPurpose-error" className="text-sm text-destructive">
                {errors.purpose}
              </p>
            )}
          </div>

          <div className="flex justify-between pt-4">
            <Button type="button" variant="outline" onClick={goBack}>Back</Button>
            <Button type="submit">Review Application</Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};
