package com.loan.application.repository;

import com.loan.application.entity.Business;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface BusinessRepository extends JpaRepository<Business, UUID> {
     // Optional: Add methods like findByEin if needed for checking duplicates later
     // Optional<Business> findByEin(String ein);
}