# Requirement: Task CRUD

The system SHALL support full lifecycle management of tasks.

---

## Scenario: Create Task Successfully
- GIVEN valid task data (title, priority, status)
- WHEN POST /tasks is called
- THEN system SHALL create task and return task ID

---

## Scenario: Create Task Invalid
- GIVEN missing required field
- WHEN POST /tasks is called
- THEN system SHALL return validation error

---

## Scenario: Get Task
- GIVEN valid task ID
- WHEN GET /tasks/{id}
- THEN system SHALL return task details

---

## Scenario: Update Task
- GIVEN valid task ID
- WHEN PUT /tasks/{id}
- THEN system SHALL update task

---

## Scenario: Delete Task
- GIVEN valid task ID
- WHEN DELETE /tasks/{id}
- THEN system SHALL remove task