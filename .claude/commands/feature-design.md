---
description: Run design phase only - create design.md with architecture and components
argument-hint: [feature description]
---

Run the feature-design agent to create detailed design documentation.

Feature description: $ARGUMENTS

Guide the user through:
1. Read discovery.md and requirements.md if they exist
2. Explore codebase to understand existing patterns
3. Ask design questions if needed (one at a time with confirmation)
4. Create design.md with architecture, components, interfaces, error handling, and testing strategy

@feature-design $ARGUMENTS
