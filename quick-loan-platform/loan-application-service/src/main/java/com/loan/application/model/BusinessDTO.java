package com.loan.application.model;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class BusinessDTO {
    @NotBlank(message = "Business name cannot be blank")
    private String name;

    @NotBlank(message = "EIN cannot be blank")
    // Add pattern validation for EIN if needed: @Pattern(regexp="^\\d{2}-\\d{7}$")
    private String ein;

    private String streetAddress;
    private String city;
    private String state;
    private String zipCode;
    private String type;

    @NotNull(message = "Years in operation cannot be null")
    @Min(value = 0, message = "Years in operation must be zero or positive")
    private Integer yearsInOperation;

    @NotNull(message = "Annual revenue cannot be null")
    @PositiveOrZero(message = "Annual revenue must be zero or positive")
    private BigDecimal annualRevenue;
}