package com.yourcompany.loanapplication.repository;

import com.yourcompany.loanapplication.model.entity.LoanApplication;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;
import java.util.UUID;

public interface LoanApplicationRepository extends JpaRepository<LoanApplication, UUID> {

    // Override findById to fetch Applicant and Business eagerly if needed for the GET request
    // Otherwise, default lazy loading is fine, and the service layer will trigger loading when mapping to DTO.
    // For explicit fetching:
    @Query("SELECT la FROM LoanApplication la JOIN FETCH la.applicant JOIN FETCH la.business WHERE la.id = :id")
    Optional<LoanApplication> findByIdWithDetails(@Param("id") UUID id);
}