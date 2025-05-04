
import React, { useState, useEffect } from "react";
import { useFormContext } from "@/contexts/FormContext";
import { validateApplicant } from "@/utils/validation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";

export const PersonalInfoForm: React.FC = () => {
  const { applicant, setApplicant, setCurrentStep } = useFormContext();
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  // Format SSN as user types (XXX-XX-XXXX)
  const formatSSN = (input: string): string => {
    const digitsOnly = input.replace(/\D/g, '');
    let formatted = '';
    
    if (digitsOnly.length > 0) {
      formatted += digitsOnly.substring(0, Math.min(3, digitsOnly.length));
    }
    if (digitsOnly.length > 3) {
      formatted += '-' + digitsOnly.substring(3, Math.min(5, digitsOnly.length));
    }
    if (digitsOnly.length > 5) {
      formatted += '-' + digitsOnly.substring(5, Math.min(9, digitsOnly.length));
    }
    
    return formatted;
  };

  // Format phone as user types (XXX-XXX-XXXX)
  const formatPhone = (input: string): string => {
    const digitsOnly = input.replace(/\D/g, '');
    let formatted = '';
    
    if (digitsOnly.length > 0) {
      formatted += digitsOnly.substring(0, Math.min(3, digitsOnly.length));
    }
    if (digitsOnly.length > 3) {
      formatted += '-' + digitsOnly.substring(3, Math.min(6, digitsOnly.length));
    }
    if (digitsOnly.length > 6) {
      formatted += '-' + digitsOnly.substring(6, Math.min(10, digitsOnly.length));
    }
    
    return formatted;
  };

  const handleInputChange = (field: keyof typeof applicant, value: string) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    
    // Apply formatting for specific fields
    if (field === 'ssn') {
      value = formatSSN(value);
    } else if (field === 'phone') {
      value = formatPhone(value);
    }
    
    setApplicant(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Validate fields when their values change
  useEffect(() => {
    const validationErrors = validateApplicant(applicant);
    setErrors(validationErrors);
  }, [applicant]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Mark all fields as touched
    const allTouched = Object.keys(applicant).reduce(
      (acc, key) => ({ ...acc, [key]: true }),
      {}
    );
    setTouched(allTouched);
    
    // Validate all fields
    const validationErrors = validateApplicant(applicant);
    setErrors(validationErrors);
    
    // Proceed if no errors
    if (Object.keys(validationErrors).length === 0) {
      setCurrentStep(2);
    } else {
      // Scroll to the first error
      const firstErrorField = document.querySelector('[aria-invalid="true"]');
      if (firstErrorField) {
        firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  };

  return (
    <Card className="animate-fade-in">
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* First Name */}
            <div className="space-y-2">
              <Label htmlFor="firstName">
                First Name <span className="text-destructive">*</span>
              </Label>
              <Input
                id="firstName"
                value={applicant.firstName}
                onChange={(e) => handleInputChange("firstName", e.target.value)}
                aria-invalid={touched.firstName && !!errors.firstName}
                aria-describedby={errors.firstName ? "firstName-error" : undefined}
              />
              {touched.firstName && errors.firstName && (
                <p id="firstName-error" className="text-sm text-destructive">
                  {errors.firstName}
                </p>
              )}
            </div>

            {/* Last Name */}
            <div className="space-y-2">
              <Label htmlFor="lastName">
                Last Name <span className="text-destructive">*</span>
              </Label>
              <Input
                id="lastName"
                value={applicant.lastName}
                onChange={(e) => handleInputChange("lastName", e.target.value)}
                aria-invalid={touched.lastName && !!errors.lastName}
                aria-describedby={errors.lastName ? "lastName-error" : undefined}
              />
              {touched.lastName && errors.lastName && (
                <p id="lastName-error" className="text-sm text-destructive">
                  {errors.lastName}
                </p>
              )}
            </div>

            {/* Email */}
            <div className="space-y-2">
              <Label htmlFor="email">
                Email <span className="text-destructive">*</span>
              </Label>
              <Input
                id="email"
                type="email"
                value={applicant.email}
                onChange={(e) => handleInputChange("email", e.target.value)}
                aria-invalid={touched.email && !!errors.email}
                aria-describedby={errors.email ? "email-error" : undefined}
              />
              {touched.email && errors.email && (
                <p id="email-error" className="text-sm text-destructive">
                  {errors.email}
                </p>
              )}
            </div>

            {/* Phone */}
            <div className="space-y-2">
              <Label htmlFor="phone">
                Phone <span className="text-destructive">*</span>
              </Label>
              <Input
                id="phone"
                value={applicant.phone}
                placeholder="XXX-XXX-XXXX"
                onChange={(e) => handleInputChange("phone", e.target.value)}
                maxLength={12}
                aria-invalid={touched.phone && !!errors.phone}
                aria-describedby={errors.phone ? "phone-error" : undefined}
              />
              {touched.phone && errors.phone && (
                <p id="phone-error" className="text-sm text-destructive">
                  {errors.phone}
                </p>
              )}
            </div>

            {/* SSN */}
            <div className="space-y-2">
              <Label htmlFor="ssn">
                Social Security Number <span className="text-destructive">*</span>
              </Label>
              <Input
                id="ssn"
                value={applicant.ssn}
                placeholder="XXX-XX-XXXX"
                onChange={(e) => handleInputChange("ssn", e.target.value)}
                maxLength={11}
                aria-invalid={touched.ssn && !!errors.ssn}
                aria-describedby={errors.ssn ? "ssn-error" : undefined}
              />
              {touched.ssn && errors.ssn && (
                <p id="ssn-error" className="text-sm text-destructive">
                  {errors.ssn}
                </p>
              )}
            </div>
          </div>

          <h3 className="text-lg font-semibold mt-6">Address</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Street Address */}
            <div className="md:col-span-2 space-y-2">
              <Label htmlFor="streetAddress">
                Street Address <span className="text-destructive">*</span>
              </Label>
              <Input
                id="streetAddress"
                value={applicant.streetAddress}
                onChange={(e) => handleInputChange("streetAddress", e.target.value)}
                aria-invalid={touched.streetAddress && !!errors.streetAddress}
                aria-describedby={errors.streetAddress ? "streetAddress-error" : undefined}
              />
              {touched.streetAddress && errors.streetAddress && (
                <p id="streetAddress-error" className="text-sm text-destructive">
                  {errors.streetAddress}
                </p>
              )}
            </div>

            {/* City */}
            <div className="space-y-2">
              <Label htmlFor="city">
                City <span className="text-destructive">*</span>
              </Label>
              <Input
                id="city"
                value={applicant.city}
                onChange={(e) => handleInputChange("city", e.target.value)}
                aria-invalid={touched.city && !!errors.city}
                aria-describedby={errors.city ? "city-error" : undefined}
              />
              {touched.city && errors.city && (
                <p id="city-error" className="text-sm text-destructive">
                  {errors.city}
                </p>
              )}
            </div>

            {/* State and Zip */}
            <div className="grid grid-cols-2 gap-4">
              {/* State */}
              <div className="space-y-2">
                <Label htmlFor="state">
                  State <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="state"
                  value={applicant.state}
                  onChange={(e) => handleInputChange("state", e.target.value.toUpperCase())}
                  maxLength={2}
                  placeholder="CA"
                  className="uppercase"
                  aria-invalid={touched.state && !!errors.state}
                  aria-describedby={errors.state ? "state-error" : undefined}
                />
                {touched.state && errors.state && (
                  <p id="state-error" className="text-sm text-destructive">
                    {errors.state}
                  </p>
                )}
              </div>

              {/* Zip Code */}
              <div className="space-y-2">
                <Label htmlFor="zipCode">
                  Zip Code <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="zipCode"
                  value={applicant.zipCode}
                  onChange={(e) => handleInputChange("zipCode", e.target.value)}
                  aria-invalid={touched.zipCode && !!errors.zipCode}
                  aria-describedby={errors.zipCode ? "zipCode-error" : undefined}
                />
                {touched.zipCode && errors.zipCode && (
                  <p id="zipCode-error" className="text-sm text-destructive">
                    {errors.zipCode}
                  </p>
                )}
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4">
            <Button type="submit">Continue</Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};
