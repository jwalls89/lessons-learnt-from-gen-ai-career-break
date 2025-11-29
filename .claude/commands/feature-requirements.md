---
description: Run requirements phase only - gather detailed requirements and create requirements.md
argument-hint: [feature description]
---

Run the feature-requirements agent to gather detailed requirements.

Feature description: $ARGUMENTS

Guide the user through requirements questions one at a time:
1. Check for existing discovery.md for context
2. Ask questions about functionality, users, integration, errors, configuration
3. Confirm each answer before recording
4. Create requirements.md with user stories and acceptance criteria

@feature-requirements $ARGUMENTS
