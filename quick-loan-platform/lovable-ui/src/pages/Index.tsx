
import React from "react";
import { FormProvider } from "@/contexts/FormContext";
import { ApplicationForm } from "@/components/ApplicationForm";

const Index: React.FC = () => {
  return (
    <div className="min-h-screen">
      <header className="bg-primary text-white py-6">
        <div className="container max-w-6xl mx-auto px-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold">Quick Loan Gateway</h1>
              <p className="text-primary-foreground/90 text-sm md:text-base">
                Small Business Loan Application
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container max-w-6xl mx-auto py-8 px-4">
        <div className="mb-10 max-w-3xl mx-auto text-center">
          <h2 className="text-2xl md:text-3xl font-bold mb-3">Apply for a Business Loan</h2>
          <p className="text-muted-foreground">
            Complete the application below to request funding for your business.
            The process typically takes less than 10 minutes.
          </p>
        </div>

        <FormProvider>
          <ApplicationForm />
        </FormProvider>
      </main>

      <footer className="bg-muted py-6">
        <div className="container max-w-6xl mx-auto px-4 text-center text-sm text-muted-foreground">
          <p className="mb-2">
            &copy; {new Date().getFullYear()} Quick Loan Gateway. All rights reserved.
          </p>
          <p>
            <a href="#" className="text-primary hover:underline mx-2">Privacy Policy</a>
            <span className="text-muted-foreground mx-1">|</span>
            <a href="#" className="text-primary hover:underline mx-2">Terms of Service</a>
            <span className="text-muted-foreground mx-1">|</span>
            <a href="#" className="text-primary hover:underline mx-2">Contact Us</a>
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
