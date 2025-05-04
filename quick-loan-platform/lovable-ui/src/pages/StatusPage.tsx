
import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { apiService, LoanApplication } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { ArrowLeft, Clock, CheckCircle, XCircle, AlertCircle, Loader2 } from "lucide-react";

const StatusPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [application, setApplication] = useState<LoanApplication | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchApplication = async () => {
      if (!id) {
        setError("No application ID provided");
        setLoading(false);
        return;
      }

      try {
        const data = await apiService.getApplication(id);
        setApplication(data);
      } catch (err) {
        setError("Failed to load application data");
        console.error("Error fetching application:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchApplication();
  }, [id]);

  // Format date
  const formatDate = (dateString?: string) => {
    if (!dateString) return "N/A";
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  // Format currency
  const formatCurrency = (value?: number): string => {
    if (value === undefined) return "N/A";
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  // Get status details based on status
  const getStatusDetails = (status?: string) => {
    switch (status) {
      case "APPROVED":
        return {
          icon: <CheckCircle className="h-8 w-8 text-success" />,
          color: "success",
          message: "Your loan application has been approved! Our team will contact you soon with next steps.",
          badgeVariant: "secondary" as const,
        };
      case "DECLINED":
        return {
          icon: <XCircle className="h-8 w-8 text-destructive" />,
          color: "destructive",
          message: "Unfortunately, your loan application has been declined. Please contact our support team for more information.",
          badgeVariant: "destructive" as const,
        };
      case "NEEDS_REVIEW":
        return {
          icon: <AlertCircle className="h-8 w-8 text-amber-500" />,
          color: "amber-500",
          message: "Your application requires additional review. Our team may contact you for more information.",
          badgeVariant: "outline" as const,
        };
      case "PENDING":
      default:
        return {
          icon: <Clock className="h-8 w-8 text-primary" />,
          color: "primary",
          message: "Your application is currently being processed. This typically takes 1-2 business days.",
          badgeVariant: "default" as const,
        };
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-[70vh] items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto text-primary" />
          <h2 className="mt-4 text-xl font-semibold">Loading application data...</h2>
        </div>
      </div>
    );
  }

  if (error || !application) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-10">
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Application Not Found</CardTitle>
            <CardDescription>
              {error || "We couldn't find the application you're looking for."}
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <p className="mb-6">Please check the application ID and try again.</p>
            <Link to="/">
              <Button>
                <ArrowLeft className="mr-2 h-4 w-4" />
                Return to Home
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  const statusDetails = getStatusDetails(application.status);

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <Link to="/" className="inline-flex items-center text-primary mb-6">
        <ArrowLeft className="mr-1 h-4 w-4" />
        Back to Home
      </Link>
      
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="text-2xl">Application Status</CardTitle>
              <CardDescription>
                Application ID: <span className="font-mono">{application.id}</span>
              </CardDescription>
            </div>
            <Badge variant={statusDetails.badgeVariant}>
              {application.status?.replace("_", " ")}
            </Badge>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {/* Status Message */}
          <div className="flex items-start space-x-4 p-4 bg-muted/50 rounded-lg">
            {statusDetails.icon}
            <div>
              <h3 className="font-semibold">Status Update</h3>
              <p>{statusDetails.message}</p>
            </div>
          </div>
          
          {/* Application Details */}
          <div>
            <h3 className="text-lg font-semibold mb-2">Application Details</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Applicant</p>
                <p className="font-medium">{application.applicant.firstName} {application.applicant.lastName}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Business Name</p>
                <p className="font-medium">{application.business.name}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Loan Amount</p>
                <p className="font-medium">{formatCurrency(application.loanDetails.amount)}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Submitted On</p>
                <p className="font-medium">{formatDate(application.submittedAt)}</p>
              </div>
            </div>
          </div>
          
          <Separator />
          
          {/* Contact Information */}
          <div>
            <h3 className="text-lg font-semibold mb-2">Need Assistance?</h3>
            <p>
              If you have questions about your application, please contact our support team at <a href="mailto:support@quickloan.example" className="text-primary font-medium">support@quickloan.example</a> or call <a href="tel:8005551234" className="text-primary font-medium">800-555-1234</a>.
            </p>
            <p className="mt-2">
              Be sure to have your application ID ready: <span className="font-mono">{application.id}</span>
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default StatusPage;
