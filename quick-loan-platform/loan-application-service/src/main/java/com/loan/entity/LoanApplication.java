package com.yourcompany.loanapplication.model.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "loan_applications")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class LoanApplication {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.PERSIST) // Cascade PERSIST to save new Applicant/Business with Application
    @JoinColumn(name = "applicant_id", nullable = false)
    private Applicant applicant;

    @ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.PERSIST) // Cascade PERSIST
    @JoinColumn(name = "business_id", nullable = false)
    private Business business;

    @Column(name = "loan_amount", nullable = false, precision = 19, scale = 2)
    private BigDecimal loanAmount;

    @Column(name = "loan_purpose", columnDefinition = "TEXT")
    private String loanPurpose;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20) // Ensure length matches ENUM values
    private LoanStatus status;

    @CreationTimestamp // Or set manually in service layer before save
    @Column(name = "submitted_at", nullable = false, updatable = false)
    private OffsetDateTime submittedAt;
}