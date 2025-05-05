package com.loan.service;

import com.loan.model.dto.*;
import com.loan.model.entity.Applicant;
import com.loan.model.entity.Business;
import com.loan.model.entity.LoanApplication;
import com.loan.model.entity.LoanStatus;
import com.loan.repository.ApplicantRepository;
import com.loan.repository.BusinessRepository;
import com.loan.repository.LoanApplicationRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor; // Lombok for constructor injection
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional; // For DB transactions

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor // Creates constructor with final fields (Autowired equivalent)
public class ApplicationService {

    private final ApplicantRepository applicantRepository;
    private final BusinessRepository businessRepository;
    private final LoanApplicationRepository loanApplicationRepository;
    private final DtoMapperService dtoMapperService; // Inject mapper service

    @Transactional // Ensure all DB operations within this method are atomic
    public SubmissionResponseDTO submitApplication(LoanApplicationDTO applicationDTO) {

        // Map DTOs to Entities
        // Consider checking if applicant/business already exist based on email/EIN
        // For this example, we create new ones each time as per cascade settings.
        Applicant applicant = dtoMapperService.toApplicantEntity(applicationDTO.getApplicant());
        Business business = dtoMapperService.toBusinessEntity(applicationDTO.getBusiness());

        // Create LoanApplication Entity
        LoanApplication loanApplication = new LoanApplication();
        loanApplication.setApplicant(applicant); // JPA will handle saving due to CascadeType.PERSIST
        loanApplication.setBusiness(business);   // JPA will handle saving due to CascadeType.PERSIST
        loanApplication.setLoanAmount(applicationDTO.getLoanDetails().getAmount());
        loanApplication.setLoanPurpose(applicationDTO.getLoanDetails().getPurpose());
        loanApplication.setSubmittedAt(OffsetDateTime.now()); // Set submission time

        // Determine Status (same logic as mock)
        BigDecimal revenue = business.getAnnualRevenue();
        int yearsInOperation = business.getYearsInOperation();
        BigDecimal loanAmount = loanApplication.getLoanAmount();
        BigDecimal fiftyK = new BigDecimal("50000");
        BigDecimal twoHundredK = new BigDecimal("200000");
        BigDecimal pointFive = new BigDecimal("0.5");

        if (revenue.compareTo(fiftyK) < 0 || yearsInOperation < 1) {
            loanApplication.setStatus(LoanStatus.DECLINED);
        } else if (revenue.compareTo(twoHundredK) >= 0 && yearsInOperation >= 3 && loanAmount.compareTo(revenue.multiply(pointFive)) <= 0) {
            loanApplication.setStatus(LoanStatus.APPROVED);
        } else {
            loanApplication.setStatus(LoanStatus.NEEDS_REVIEW);
        }

        // Save the application (which cascades saves to applicant and business)
        LoanApplication savedApplication = loanApplicationRepository.save(loanApplication);

        // Return the generated ID
        return new SubmissionResponseDTO(savedApplication.getId());
    }

    @Transactional(readOnly = true) // Read-only transaction for fetching data
    public LoanApplicationDTO getApplication(UUID applicationId) {
        // Use findByIdWithDetails if you defined it for eager fetching, otherwise findById is fine.
         LoanApplication application = loanApplicationRepository.findByIdWithDetails(applicationId)
        // LoanApplication application = loanApplicationRepository.findById(applicationId)
                .orElseThrow(() -> new EntityNotFoundException("LoanApplication not found with id: " + applicationId));

        // Map Entity back to DTO
        return dtoMapperService.toLoanApplicationDTO(application);
    }
}