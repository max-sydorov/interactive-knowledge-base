
import React from "react";
import { useFormContext } from "@/contexts/FormContext";
import { apiService } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/components/ui/use-toast";
import { CheckCircle } from "lucide-react";

export const ReviewAndSubmit: React.FC = () => {
  const { 
    applicant, 
    business, 
    loanDetails, 
    setCurrentStep, 
    setApplicationId,
    isSubmitting,
    setIsSubmitting
  } = useFormContext();
  const { toast } = useToast();

  // Format currency
  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    
    try {
      const result = await apiService.submitApplication({
        applicant,
        business,
        loanDetails
      });
      
      setApplicationId(result.applicationId);
      setCurrentStep(5);
      
      toast({
        title: "Application Submitted Successfully",
        description: `Your application ID is ${result.applicationId}`,
      });
    } catch (error) {
      console.error("Error submitting application:", error);
      toast({
        variant: "destructive",
        title: "Submission Failed",
        description: "There was an error submitting your application. Please try again.",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const goBack = () => {
    setCurrentStep(3);
  };

  return (
    <Card className="animate-fade-in">
      <CardHeader>
        <CardTitle className="text-2xl">Review Your Application</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Personal Information Section */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold flex items-center">
            <CheckCircle className="mr-2 h-5 w-5 text-primary" />
            Personal Information
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">Full Name</p>
              <p>{applicant.firstName} {applicant.lastName}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Email</p>
              <p>{applicant.email}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Phone</p>
              <p>{applicant.phone}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">SSN</p>
              <p>XXX-XX-{applicant.ssn.slice(-4)}</p>
            </div>
            <div className="md:col-span-2">
              <p className="text-sm text-muted-foreground">Address</p>
              <p>
                {applicant.streetAddress},<br />
                {applicant.city}, {applicant.state} {applicant.zipCode}
              </p>
            </div>
          </div>
        </div>
        
        <Separator />
        
        {/* Business Information Section */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold flex items-center">
            <CheckCircle className="mr-2 h-5 w-5 text-primary" />
            Business Information
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">Business Name</p>
              <p>{business.name}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">EIN</p>
              <p>{business.ein}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Business Type</p>
              <p>{business.type}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Years in Operation</p>
              <p>{business.yearsInOperation}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Annual Revenue</p>
              <p>{formatCurrency(business.annualRevenue)}</p>
            </div>
            <div className="md:col-span-2">
              <p className="text-sm text-muted-foreground">Business Address</p>
              <p>
                {business.streetAddress},<br />
                {business.city}, {business.state} {business.zipCode}
              </p>
            </div>
          </div>
        </div>
        
        <Separator />
        
        {/* Loan Details Section */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold flex items-center">
            <CheckCircle className="mr-2 h-5 w-5 text-primary" />
            Loan Details
          </h3>
          <div className="grid grid-cols-1 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">Loan Amount</p>
              <p className="font-semibold text-lg">{formatCurrency(loanDetails.amount)}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Loan Purpose</p>
              <p className="whitespace-pre-line">{loanDetails.purpose}</p>
            </div>
          </div>
        </div>

        <div className="bg-muted p-4 rounded-md mt-6">
          <p className="text-sm">
            By submitting this application, you certify that all information provided is accurate and complete.
            You authorize us to verify the information and obtain credit reports. Terms and conditions apply.
          </p>
        </div>

        <div className="flex justify-between pt-4">
          <Button type="button" variant="outline" onClick={goBack}>Back</Button>
          <Button 
            onClick={handleSubmit} 
            disabled={isSubmitting}
          >
            {isSubmitting ? "Submitting..." : "Submit Application"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
