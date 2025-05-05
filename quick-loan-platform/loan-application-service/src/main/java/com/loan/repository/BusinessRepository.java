package com.yourcompany.loanapplication.repository;

import com.yourcompany.loanapplication.model.entity.Business;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface BusinessRepository extends JpaRepository<Business, UUID> {
     // Optional: Add methods like findByEin if needed for checking duplicates later
     // Optional<Business> findByEin(String ein);
}