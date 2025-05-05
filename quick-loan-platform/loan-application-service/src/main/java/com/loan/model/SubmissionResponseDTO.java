package com.yourcompany.loanapplication.model.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SubmissionResponseDTO {
    private UUID applicationId; // Use UUID
}