
import React from "react";
import { useFormContext } from "@/contexts/FormContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { CheckCircle } from "lucide-react";
import { Link } from "react-router-dom";

export const SubmissionSuccess: React.FC = () => {
  const { applicationId } = useFormContext();

  return (
    <Card className="animate-fade-in">
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-success/20">
          <CheckCircle className="h-10 w-10 text-success" />
        </div>
        <CardTitle className="text-2xl">Application Submitted!</CardTitle>
        <CardDescription className="text-lg">
          Thank you for your business loan application
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="rounded-lg border bg-card p-6">
          <h3 className="mb-2 font-semibold">Application ID</h3>
          <p className="text-2xl font-bold text-primary">{applicationId}</p>
          <p className="mt-2 text-sm text-muted-foreground">
            Please save this ID for your records. You'll need it to check the status of your application.
          </p>
        </div>
        
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">What happens next?</h3>
          <ol className="list-decimal list-inside space-y-2 ml-2">
            <li>Our team will review your application (typically within 1-2 business days).</li>
            <li>You may be contacted for additional information or documentation.</li>
            <li>Once a decision is made, you'll be notified via email.</li>
            <li>If approved, we'll work with you to complete the loan process.</li>
          </ol>
        </div>
        
        <div className="rounded-lg border bg-accent/50 p-4">
          <p className="text-sm">
            <strong>Questions?</strong> Contact our support team at 
            <a href="mailto:support@quickloan.example" className="text-primary font-medium"> support@quickloan.example</a>
          </p>
        </div>
        
        <div className="flex justify-center pt-4">
          <Link to={`/status/${applicationId}`}>
            <Button>Check Application Status</Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
};
