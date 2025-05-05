package com.loan.model.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class LoanDetailsDTO {
    @NotNull(message = "Loan amount cannot be null")
    @Positive(message = "Loan amount must be positive")
    private BigDecimal amount;

    private String purpose;
}