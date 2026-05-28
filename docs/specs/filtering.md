# Requirement: Task Filtering

The system SHALL support filtering tasks.

---

## Scenario: Filter by status
- WHEN GET /tasks?status=todo
- THEN system SHALL return matching tasks

---

## Scenario: Filter by priority
- WHEN GET /tasks?priority=high
- THEN system SHALL return high priority tasks

---

## Scenario: Filter by time range
- WHEN GET /tasks?start_date=...&end_date=...
- THEN system SHALL return tasks in range