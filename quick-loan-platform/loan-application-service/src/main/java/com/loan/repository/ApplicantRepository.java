package com.loan.repository;

import com.loan.model.entity.Applicant;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface ApplicantRepository extends JpaRepository<Applicant, UUID> {
    // Optional: Add methods like findByEmail if needed for checking duplicates later
    // Optional<Applicant> findByEmail(String email);
}