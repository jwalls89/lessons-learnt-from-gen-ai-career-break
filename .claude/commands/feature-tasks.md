---
description: Run task breakdown phase only - create tasks.md with sequenced implementation steps
argument-hint: [feature description]
---

Run the feature-tasks agent to create implementation task breakdown.

Feature description: $ARGUMENTS

Guide the user through:
1. Read discovery.md, requirements.md, and design.md if they exist
2. Break design into discrete, sequenced tasks
3. Create tasks.md with:
   - Actionable implementation steps
   - Dependencies and sequencing
   - Time estimates
   - Links to requirements

@feature-tasks $ARGUMENTS
