package com.loan.application.model;

import com.loan.application.entity.LoanStatus; // Use the enum
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.OffsetDateTime; // Use OffsetDateTime for timezone
import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class LoanApplicationDTO {
    private UUID id; // Use UUID

    @NotNull(message = "Applicant details cannot be null")
    @Valid // Enable validation on nested ApplicantDTO
    private ApplicantDTO applicant;

    @NotNull(message = "Business details cannot be null")
    @Valid // Enable validation on nested BusinessDTO
    private BusinessDTO business;

    @NotNull(message = "Loan details cannot be null")
    @Valid // Enable validation on nested LoanDetailsDTO
    private LoanDetailsDTO loanDetails;

    private LoanStatus status; // Use the Enum type
    private OffsetDateTime submittedAt; // Use OffsetDateTime
}