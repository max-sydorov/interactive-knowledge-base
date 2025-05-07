import { Applicant, Business, LoanDetails, LoanApplication } from './interfaces';

// Define the backend API base URL
const API_BASE_URL = 'http://localhost:8080/api'; // Adjust port if needed

// Define the structure of the submission response from the backend
interface SubmissionResponse {
  applicationId: string; // The backend returns UUID as string
}

// Updated ApiService class using fetch
class ApiService {

  // Submit an application to the real backend
  async submitApplication(application: Omit<LoanApplication, 'id' | 'status' | 'submittedAt'>): Promise<{ applicationId: string }> {
    console.log('Submitting application to backend:', application);
    try {
      const response = await fetch(`${API_BASE_URL}/applications`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add any other headers like Authorization if needed
        },
        body: JSON.stringify(application), // Send the core application data
      });

      if (!response.ok) {
        // Attempt to read error details from backend response
        let errorData = null;
        try {
          errorData = await response.json();
        } catch (e) {
          // Ignore if response body is not JSON
        }
        console.error('Backend submission error:', response.status, response.statusText, errorData);
        throw new Error(`Failed to submit application: ${response.statusText}${errorData ? ' - ' + JSON.stringify(errorData.message || errorData) : ''}`);
      }

      const result: SubmissionResponse = await response.json();
      console.log('Submission successful, Application ID:', result.applicationId);
      // Ensure the returned object matches the expected { applicationId: string } structure
      return { applicationId: result.applicationId };

    } catch (error) {
      console.error('Network error submitting application:', error);
      // Re-throw the error so the calling component can handle it
      throw error;
    }
  }

  // Retrieve an application by ID from the real backend
  async getApplication(applicationId: string): Promise<LoanApplication | null> {
    console.log('Fetching application from backend, ID:', applicationId);
    if (!applicationId) {
       console.warn('getApplication called with invalid ID');
       return null;
    }
    try {
      const response = await fetch(`${API_BASE_URL}/applications/${applicationId}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          // Add any other headers if needed
        },
      });

      if (response.ok) {
        const application: LoanApplication = await response.json();
        console.log('Application fetched successfully:', application);
        // Convert submittedAt string to Date object if needed by frontend components
        if (application.submittedAt) {
           // Backend sends OffsetDateTime (e.g., "2023-10-27T10:15:30+01:00")
           // JavaScript Date can parse this directly
           application.submittedAt = new Date(application.submittedAt).toISOString();
        }
        return application;
      } else if (response.status === 404) {
        console.log('Application not found (404)');
        return null; // Application not found is not necessarily an error in all contexts
      } else {
         // Handle other non-OK statuses as errors
        console.error('Backend fetch error:', response.status, response.statusText);
        throw new Error(`Failed to fetch application: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Network error fetching application:', error);
      // Re-throw or return null based on how you want to handle fetch errors
       throw error; // Or return null;
    }
  }
}

// Export interfaces and the service instance
export * from './interfaces';
export const apiService = new ApiService();