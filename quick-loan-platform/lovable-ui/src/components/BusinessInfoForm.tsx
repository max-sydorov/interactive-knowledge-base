
import React, { useState, useEffect } from "react";
import { useFormContext } from "@/contexts/FormContext";
import { validateBusiness } from "@/utils/validation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export const BusinessInfoForm: React.FC = () => {
  const { business, setBusiness, setCurrentStep } = useFormContext();
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  // Format EIN as user types (XX-XXXXXXX)
  const formatEIN = (input: string): string => {
    const digitsOnly = input.replace(/\D/g, '');
    let formatted = '';
    
    if (digitsOnly.length > 0) {
      formatted += digitsOnly.substring(0, Math.min(2, digitsOnly.length));
    }
    if (digitsOnly.length > 2) {
      formatted += '-' + digitsOnly.substring(2, Math.min(9, digitsOnly.length));
    }
    
    return formatted;
  };

  const handleInputChange = (field: keyof typeof business, value: string | number) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    
    // Apply formatting for specific fields
    if (field === 'ein') {
      value = formatEIN(value as string);
    }

    setBusiness(prev => ({
      ...prev,
      [field]: value
    }));
  };

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

  // Validate fields when their values change
  useEffect(() => {
    const validationErrors = validateBusiness(business);
    setErrors(validationErrors);
  }, [business]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Mark all fields as touched
    const allTouched = Object.keys(business).reduce(
      (acc, key) => ({ ...acc, [key]: true }),
      {}
    );
    setTouched(allTouched);
    
    // Validate all fields
    const validationErrors = validateBusiness(business);
    setErrors(validationErrors);
    
    // Proceed if no errors
    if (Object.keys(validationErrors).length === 0) {
      setCurrentStep(3);
    } else {
      // Scroll to the first error
      const firstErrorField = document.querySelector('[aria-invalid="true"]');
      if (firstErrorField) {
        firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  };

  const goBack = () => {
    setCurrentStep(1);
  };

  const businessTypes = [
    "Sole Proprietorship", 
    "Partnership", 
    "Limited Liability Company (LLC)", 
    "Corporation", 
    "S Corporation", 
    "Nonprofit Organization"
  ];

  return (
    <Card className="animate-fade-in">
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Business Name */}
            <div className="space-y-2">
              <Label htmlFor="businessName">
                Business Name <span className="text-destructive">*</span>
              </Label>
              <Input
                id="businessName"
                value={business.name}
                onChange={(e) => handleInputChange("name", e.target.value)}
                aria-invalid={touched.name && !!errors.name}
                aria-describedby={errors.name ? "businessName-error" : undefined}
              />
              {touched.name && errors.name && (
                <p id="businessName-error" className="text-sm text-destructive">
                  {errors.name}
                </p>
              )}
            </div>

            {/* EIN */}
            <div className="space-y-2">
              <Label htmlFor="ein">
                Employer Identification Number (EIN) <span className="text-destructive">*</span>
              </Label>
              <Input
                id="ein"
                value={business.ein}
                placeholder="XX-XXXXXXX"
                onChange={(e) => handleInputChange("ein", e.target.value)}
                maxLength={10}
                aria-invalid={touched.ein && !!errors.ein}
                aria-describedby={errors.ein ? "ein-error" : undefined}
              />
              {touched.ein && errors.ein && (
                <p id="ein-error" className="text-sm text-destructive">
                  {errors.ein}
                </p>
              )}
            </div>

            {/* Business Type */}
            <div className="space-y-2">
              <Label htmlFor="businessType">
                Business Type <span className="text-destructive">*</span>
              </Label>
              <Select 
                value={business.type} 
                onValueChange={(value) => handleInputChange("type", value)}
              >
                <SelectTrigger 
                  id="businessType"
                  aria-invalid={touched.type && !!errors.type}
                  aria-describedby={errors.type ? "businessType-error" : undefined}
                >
                  <SelectValue placeholder="Select business type" />
                </SelectTrigger>
                <SelectContent>
                  {businessTypes.map((type) => (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {touched.type && errors.type && (
                <p id="businessType-error" className="text-sm text-destructive">
                  {errors.type}
                </p>
              )}
            </div>

            {/* Years in Operation */}
            <div className="space-y-2">
              <Label htmlFor="yearsInOperation">
                Years in Operation <span className="text-destructive">*</span>
              </Label>
              <Input
                id="yearsInOperation"
                type="number"
                min="0"
                step="0.5"
                value={business.yearsInOperation || ""}
                onChange={(e) => handleInputChange("yearsInOperation", Number(e.target.value))}
                aria-invalid={touched.yearsInOperation && !!errors.yearsInOperation}
                aria-describedby={errors.yearsInOperation ? "yearsInOperation-error" : undefined}
              />
              {touched.yearsInOperation && errors.yearsInOperation && (
                <p id="yearsInOperation-error" className="text-sm text-destructive">
                  {errors.yearsInOperation}
                </p>
              )}
            </div>

            {/* Annual Revenue */}
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="annualRevenue">
                Annual Revenue <span className="text-destructive">*</span>
              </Label>
              <Input
                id="annualRevenue"
                value={business.annualRevenue ? formatCurrency(business.annualRevenue) : ""}
                onChange={(e) => handleInputChange("annualRevenue", parseCurrency(e.target.value))}
                onFocus={(e) => {
                  // When focused, if the value is $0, clear it
                  if (parseCurrency(e.target.value) === 0) {
                    handleInputChange("annualRevenue", "");
                  }
                }}
                onBlur={(e) => {
                  // When blurred, if the value is empty, set it to $0
                  if (e.target.value === "") {
                    handleInputChange("annualRevenue", 0);
                  }
                }}
                placeholder="$0"
                aria-invalid={touched.annualRevenue && !!errors.annualRevenue}
                aria-describedby={errors.annualRevenue ? "annualRevenue-error" : undefined}
              />
              {touched.annualRevenue && errors.annualRevenue && (
                <p id="annualRevenue-error" className="text-sm text-destructive">
                  {errors.annualRevenue}
                </p>
              )}
            </div>
          </div>

          <h3 className="text-lg font-semibold mt-6">Business Address</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Street Address */}
            <div className="md:col-span-2 space-y-2">
              <Label htmlFor="businessAddress">
                Street Address <span className="text-destructive">*</span>
              </Label>
              <Input
                id="businessAddress"
                value={business.streetAddress}
                onChange={(e) => handleInputChange("streetAddress", e.target.value)}
                aria-invalid={touched.streetAddress && !!errors.streetAddress}
                aria-describedby={errors.streetAddress ? "businessAddress-error" : undefined}
              />
              {touched.streetAddress && errors.streetAddress && (
                <p id="businessAddress-error" className="text-sm text-destructive">
                  {errors.streetAddress}
                </p>
              )}
            </div>

            {/* City */}
            <div className="space-y-2">
              <Label htmlFor="businessCity">
                City <span className="text-destructive">*</span>
              </Label>
              <Input
                id="businessCity"
                value={business.city}
                onChange={(e) => handleInputChange("city", e.target.value)}
                aria-invalid={touched.city && !!errors.city}
                aria-describedby={errors.city ? "businessCity-error" : undefined}
              />
              {touched.city && errors.city && (
                <p id="businessCity-error" className="text-sm text-destructive">
                  {errors.city}
                </p>
              )}
            </div>

            {/* State and Zip */}
            <div className="grid grid-cols-2 gap-4">
              {/* State */}
              <div className="space-y-2">
                <Label htmlFor="businessState">
                  State <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="businessState"
                  value={business.state}
                  onChange={(e) => handleInputChange("state", e.target.value.toUpperCase())}
                  maxLength={2}
                  placeholder="CA"
                  className="uppercase"
                  aria-invalid={touched.state && !!errors.state}
                  aria-describedby={errors.state ? "businessState-error" : undefined}
                />
                {touched.state && errors.state && (
                  <p id="businessState-error" className="text-sm text-destructive">
                    {errors.state}
                  </p>
                )}
              </div>

              {/* Zip Code */}
              <div className="space-y-2">
                <Label htmlFor="businessZipCode">
                  Zip Code <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="businessZipCode"
                  value={business.zipCode}
                  onChange={(e) => handleInputChange("zipCode", e.target.value)}
                  aria-invalid={touched.zipCode && !!errors.zipCode}
                  aria-describedby={errors.zipCode ? "businessZipCode-error" : undefined}
                />
                {touched.zipCode && errors.zipCode && (
                  <p id="businessZipCode-error" className="text-sm text-destructive">
                    {errors.zipCode}
                  </p>
                )}
              </div>
            </div>
          </div>

          <div className="flex justify-between pt-4">
            <Button type="button" variant="outline" onClick={goBack}>Back</Button>
            <Button type="submit">Continue</Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};
