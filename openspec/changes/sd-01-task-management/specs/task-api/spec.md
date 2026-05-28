## ADDED Requirements

### Requirement: Task CRUD
The system SHALL support the full lifecycle (CRUD) of tasks in the database.

#### Scenario: Create Task Successfully
- **GIVEN** a valid payload containing title, priority, and status
- **WHEN** POST /api/v1/tasks is called
- **THEN** the system SHALL persist the task and return HTTP 201 with the created task details (including the generated unique ID)

#### Scenario: Create Task with Invalid Data
- **GIVEN** a task payload with a missing required field or an empty title
- **WHEN** POST /api/v1/tasks is called
- **THEN** the system SHALL return HTTP 422 with a structured JSON containing validation error details

#### Scenario: Get Existing Task by ID
- **GIVEN** a task with a specific ID exists in the database
- **WHEN** GET /api/v1/tasks/{id} is called
- **THEN** the system SHALL return HTTP 200 with the requested task's details

#### Scenario: Get Non-existent Task
- **GIVEN** no task with the specified ID exists in the database
- **WHEN** GET /api/v1/tasks/{id} is called
- **THEN** the system SHALL return HTTP 404 with a structured error response: "Task not found"

#### Scenario: Update Task Successfully
- **GIVEN** a task with a specific ID exists in the database
- **WHEN** PUT /api/v1/tasks/{id} is called with valid updated fields
- **THEN** the system SHALL update the task in the database and return HTTP 200 with the fully updated task details

#### Scenario: Update Non-existent Task
- **GIVEN** no task with the specified ID exists in the database
- **WHEN** PUT /api/v1/tasks/{id} is called with valid updated fields
- **THEN** the system SHALL return HTTP 404 with a structured error response: "Task not found"

#### Scenario: Delete Task Successfully
- **GIVEN** a task with a specific ID exists in the database
- **WHEN** DELETE /api/v1/tasks/{id} is called
- **THEN** the system SHALL remove the task from the database and return HTTP 204 (No Content)

#### Scenario: Delete Non-existent Task
- **GIVEN** no task with the specified ID exists in the database
- **WHEN** DELETE /api/v1/tasks/{id} is called
- **THEN** the system SHALL return HTTP 404 with a structured error response: "Task not found"


### Requirement: Task Filtering
The system SHALL support filtering tasks by multiple conditions such as status, priority, and creation time range.

#### Scenario: Filter tasks by status and priority
- **GIVEN** multiple tasks exist in the database with various statuses ('todo', 'in_progress', 'done') and priorities ('low', 'medium', 'high')
- **WHEN** GET /api/v1/tasks?status=in_progress&priority=high is called
- **THEN** the system SHALL return HTTP 200 with a list of tasks matching both high priority and in_progress status

#### Scenario: Filter tasks with invalid status or priority
- **GIVEN** the database is running
- **WHEN** GET /api/v1/tasks?status=unknown_status or GET /api/v1/tasks?priority=critical is called
- **THEN** the system SHALL return HTTP 422 with a structured JSON containing validation error details

#### Scenario: Filter tasks by creation time range
- **GIVEN** multiple tasks exist in the database with different creation dates
- **WHEN** GET /api/v1/tasks?start_date=2026-05-01&end_date=2026-05-31 is called
- **THEN** the system SHALL return HTTP 200 with all tasks created within that inclusive range


### Requirement: Task Pagination and Sorting
The system SHALL support paginating and sorting the returned list of tasks.

#### Scenario: Paginate task list successfully
- **GIVEN** multiple tasks exist in the database
- **WHEN** GET /api/v1/tasks?skip=0&limit=5 is called
- **THEN** the system SHALL return HTTP 200 with a structured paginated response containing a list of up to 5 tasks and the total count of matching tasks

#### Scenario: Paginate with invalid limit or skip values
- **GIVEN** the database is running
- **WHEN** GET /api/v1/tasks?limit=-5 or GET /api/v1/tasks?limit=500 is called
- **THEN** the system SHALL return HTTP 422 with a structured validation error response

#### Scenario: Sort task list ascending
- **GIVEN** multiple tasks exist in the database with different creation times
- **WHEN** GET /api/v1/tasks?sort_by=created_at&sort_order=asc is called
- **THEN** the system SHALL return HTTP 200 with the task list ordered by their creation time ascending

#### Scenario: Sort task list descending
- **GIVEN** multiple tasks exist in the database
- **WHEN** GET /api/v1/tasks?sort_by=priority&sort_order=desc is called
- **THEN** the system SHALL return HTTP 200 with the task list ordered by their priority descending (high > medium > low)


### Requirement: Validation and Error Handling
The system SHALL validate all inputs and return structured error responses for bad requests.

#### Scenario: Invalid status value in creation payload
- **GIVEN** a task creation payload containing an invalid status (e.g. 'not_started')
- **WHEN** POST /api/v1/tasks is called
- **THEN** the system SHALL return HTTP 422 with a validation error detailing that status must be one of 'todo', 'in_progress', or 'done'

#### Scenario: Invalid priority value in creation payload
- **GIVEN** a task creation payload containing an invalid priority (e.g. 'critical')
- **WHEN** POST /api/v1/tasks is called
- **THEN** the system SHALL return HTTP 422 with a validation error detailing that priority must be one of 'low', 'medium', or 'high'

#### Scenario: Title length exceeds bounds
- **GIVEN** a task creation payload containing a title that exceeds 100 characters
- **WHEN** POST /api/v1/tasks is called
- **THEN** the system SHALL return HTTP 422 with a validation error indicating that title length must be between 1 and 100 characters
