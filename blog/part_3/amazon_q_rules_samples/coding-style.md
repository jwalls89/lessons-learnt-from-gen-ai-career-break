# Coding Style Preferences

## Purpose
This rule defines coding style preferences for Python development to ensure consistent, minimal, and maintainable code.

## Instructions

### Code Structure
- Write only the ABSOLUTE MINIMAL amount of code needed to address requirements correctly
- Avoid verbose implementations and any code that doesn't directly contribute to the solution
- Use command pattern for complex operations - extract focused command classes instead of large methods
- Prefer composition and delegation over inheritance
- Keep classes focused on single responsibilities

### Error Handling
- Create specific exception classes for each command/module (e.g., `CreateChangesetCommandError`)
- Use proper exception chaining with `raise NewError(msg) from e`
- Handle expected errors gracefully, let unexpected errors bubble up

### Type Annotations
- Always use proper type annotations including return types
- Use `TYPE_CHECKING` imports for complex type hints to avoid circular imports
- Use `Literal` types for constrained string values (e.g., CloudFormation capabilities)
- Use union types with `|` syntax (Python 3.10+)

### Method Organization
- Public methods first, private methods last (prefixed with `_`)
- Keep methods short and focused
- Use descriptive method names that explain what they do

### Import Organization
- Group imports: standard library, third-party, local imports
- Use `from typing import TYPE_CHECKING` for type-only imports
- Import specific items rather than entire modules when possible

## Priority
HIGH

## Example
```python
# Good - minimal, focused command
class CreateChangesetCommand:
    def __init__(self, cfn_client: CloudFormationClient, config: Config) -> None:
        self._cfn_client = cfn_client
        self._config = config
    
    def execute(self, parameters: dict[str, str] | None = None) -> str | None:
        try:
            # Focused implementation
            return self._create_changeset(parameters)
        except Exception as e:
            raise CreateChangesetCommandError("Failed to create changeset") from e

# Bad - verbose, unfocused class
class StackManager:
    def create_changeset_with_validation_and_hooks_and_tagging(self, params, validate=True, run_hooks=True):
        # 50+ lines of mixed responsibilities
```
