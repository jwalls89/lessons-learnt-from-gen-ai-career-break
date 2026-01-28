# Implementation Plan

- [x] 1. Create deptry package structure and basic files




  - Create the `src/python_template_invoke_tasks/deptry/` directory
  - Create `__init__.py` file for the deptry package
  - _Requirements: 2.1, 2.2_

- [x] 2. Implement DeptryCheckTask class





  - Create `check_task.py` with DeptryCheckTask class that extends Task
  - Implement task initialization with correct path and properties (is_check_task=True)
  - Implement invoke_task property that returns an invoke task function
  - Add deptry command execution using `context.run("poetry run deptry")`
  - Include proper error handling and logging using the task framework
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.1, 4.2, 4.3_

- [x] 3. Implement DeptryTaskCollection class





  - Create `task_collection.py` with DeptryTaskCollection class that extends TaskCollection
  - Initialize collection with name "deptry" and appropriate description
  - Implement `_get_requirements_inner()` method returning empty list
  - Implement `_build_tasks_inner()` method returning DeptryCheckTask instance
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 4. Add deptry collection to project configuration



  - Update `penguin.toml` to include deptry collection configuration
  - Set `enabled = true` for the deptry collection
  - _Requirements: 2.4, 3.1, 3.2_

- [x] 5. Register deptry collection in the task system





  - Update the task collection registration to include the new deptry collection
  - Ensure the collection is discoverable by the task collection builder
  - _Requirements: 2.1, 2.4_

- [-] 6. Write unit tests for DeptryCheckTask



  - Create test file for DeptryCheckTask class
  - Test task initialization with correct properties and path
  - Test invoke task creation and basic functionality
  - Test command execution scenarios (success, failure, error handling)
  - Mock context.run calls to test command execution without running actual deptry
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.1, 4.2, 4.3_

- [ ] 7. Write unit tests for DeptryTaskCollection
  - Create test file for DeptryTaskCollection class
  - Test collection initialization with correct name and description
  - Test requirements building returns empty list
  - Test task building returns correct DeptryCheckTask instance
  - _Requirements: 2.1, 2.2, 2.3_

- [ ] 8. Write integration tests for deptry task execution
  - Create integration test that executes the deptry.check task end-to-end
  - Test task appears in available tasks list
  - Test task executes successfully in clean project scenario
  - Test task is included when running project.check command
  - Verify proper exit codes and output formatting
  - _Requirements: 1.1, 1.2, 1.3, 2.4, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3_

- [ ] 9. Test configuration integration
  - Verify deptry respects existing pyproject.toml configuration
  - Test that deptry uses the configured per_rule_ignores settings
  - Ensure task works with default configuration when no custom config exists
  - _Requirements: 3.1, 3.2, 3.3, 5.4_

- [ ] 10. Validate task collection integration
  - Run full task suite to ensure deptry collection integrates properly
  - Verify deptry.check appears in task listings
  - Confirm deptry.check runs as part of project.check
  - Test that logging and output patterns match other check tasks
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 4.1, 4.2, 4.3_
