# Requirement: Pagination & Sorting

The system SHALL support pagination and sorting.

---

## Scenario: Pagination
- WHEN GET /tasks?page=1&size=10
- THEN system SHALL return paginated results

---

## Scenario: Sorting
- WHEN GET /tasks?sort=created_at
- THEN system SHALL return sorted results