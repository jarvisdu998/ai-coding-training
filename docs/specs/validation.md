# Requirement: Validation & Error Handling

The system SHALL validate input and return structured errors.

---

## Scenario: Invalid input
- WHEN missing required field
- THEN system SHALL return 400 error

---

## Scenario: Invalid enum
- WHEN priority is invalid
- THEN system SHALL return validation error

---

## Scenario: Server error
- WHEN database fails
- THEN system SHALL return 500 structured error