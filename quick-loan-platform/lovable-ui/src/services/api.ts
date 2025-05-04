
export interface Applicant {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  ssn: string;
  streetAddress: string;
  city: string;
  state: string;
  zipCode: string;
}

export interface Business {
  name: string;
  ein: string;
  streetAddress: string;
  city: string;
  state: string;
  zipCode: string;
  type: string;
  yearsInOperation: number;
  annualRevenue: number;
}

export interface LoanDetails {
  amount: number;
  purpose: string;
}

export interface LoanApplication {
  id?: string;
  applicant: Applicant;
  business: Business;
  loanDetails: LoanDetails;
  status?: 'PENDING' | 'APPROVED' | 'DECLINED' | 'NEEDS_REVIEW';
  submittedAt?: string;
}

// This is a mock API service for demo purposes
// In a real application, this would make actual HTTP requests to your backend
class ApiService {
  private applications: LoanApplication[] = [];
  
  // Simulate submitting an application to the backend
  async submitApplication(application: LoanApplication): Promise<{ applicationId: string }> {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Generate a fake application ID
    const applicationId = Math.random().toString(36).substring(2, 15);
    
    // Add timestamp
    const submittedAt = new Date().toISOString();
    
    // Determine status based on simple rules
    let status: 'PENDING' | 'APPROVED' | 'DECLINED' | 'NEEDS_REVIEW';
    const revenue = application.business.annualRevenue;
    const yearsInOperation = application.business.yearsInOperation;
    const loanAmount = application.loanDetails.amount;
    
    if (revenue < 50000 || yearsInOperation < 1) {
      status = 'DECLINED';
    } else if (revenue >= 200000 && yearsInOperation >= 3 && loanAmount <= revenue * 0.5) {
      status = 'APPROVED';
    } else {
      status = 'NEEDS_REVIEW';
    }
    
    // Store the application with the generated ID and status
    this.applications.push({
      ...application,
      id: applicationId,
      status,
      submittedAt
    });
    
    // Return the application ID
    return { applicationId };
  }
  
  // Simulate retrieving an application by ID
  async getApplication(applicationId: string): Promise<LoanApplication | null> {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Find the application
    const application = this.applications.find(app => app.id === applicationId);
    
    return application || null;
  }
}

export const apiService = new ApiService();
