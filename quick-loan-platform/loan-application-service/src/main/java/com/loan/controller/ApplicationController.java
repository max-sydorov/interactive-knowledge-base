package com.loan.controller;

import com.loan.model.dto.LoanApplicationDTO;
import com.loan.model.dto.SubmissionResponseDTO;
import com.loan.service.ApplicationService;
import jakarta.persistence.EntityNotFoundException;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;


import java.util.UUID;

@RestController
@RequestMapping("/api/applications") // Base path for this controller
@RequiredArgsConstructor
// @CrossOrigin(origins = "http://localhost:xxxx") // Allow frontend (replace xxxx with frontend port if needed) - See CORS config below for better approach
public class ApplicationController {

    private final ApplicationService applicationService;

    @PostMapping
    public ResponseEntity<SubmissionResponseDTO> submitApplication(@Valid @RequestBody LoanApplicationDTO applicationDTO) {
        // Basic validation happens automatically due to @Valid
        SubmissionResponseDTO response = applicationService.submitApplication(applicationDTO);
        // Return 201 Created status
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/{id}")
    public ResponseEntity<LoanApplicationDTO> getApplication(@PathVariable UUID id) {
        try {
            LoanApplicationDTO applicationDTO = applicationService.getApplication(id);
            return ResponseEntity.ok(applicationDTO);
        } catch (EntityNotFoundException e) {
            // Return 404 Not Found
             throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Application not found", e);
        }
        // Add more robust error handling if needed (e.g., using @ControllerAdvice)
    }
}