---
description: Create a complete feature specification through discovery, requirements, design, and tasks
argument-hint: [feature description]
---

# Feature Specification Orchestrator

This command runs the complete feature specification workflow through 4 phases:

**Phase 0: Discovery** (@feature-discovery)
- Understand the problem and business value
- Research existing solutions
- Decide on approach (custom/integrate/hybrid)

**Phase 1: Requirements** (@feature-requirements)
- Gather detailed requirements
- Create user stories with acceptance criteria
- Document integration points

**Phase 2: Design** (@feature-design)
- Design architecture and components
- Define interfaces and data models
- Plan error handling and testing

**Phase 3: Tasks** (@feature-tasks)
- Break design into sequenced tasks
- Create actionable implementation plan
- Link tasks to requirements

---

## User Request

Feature to implement: $ARGUMENTS

---

## Instructions for Claude

You are orchestrating a multi-phase feature specification process. You will run 4 specialized agents in sequence, allowing the user to approve each phase before proceeding.

### Your Role

1. **Explain the process** to the user
2. **Run each agent** using the Task tool
3. **Wait for user approval** between phases
4. **Pass context** between agents by referencing created documents

### Process Flow

**Step 1: Introduce the Process**

Say:
```
I'll help you create a complete feature specification for: $ARGUMENTS

This process has 4 phases:
0. Discovery - Understand the problem and explore solutions
1. Requirements - Document what needs to be built
2. Design - Plan how to build it
3. Tasks - Create implementation checklist

I'll run a specialized agent for each phase and wait for your approval before moving forward.

Let's start with Phase 0: Discovery...
```

**Step 2: Run Discovery Agent**

Use the SlashCommand tool to invoke the /feature-discovery command:
```
/feature-discovery $ARGUMENTS
```

This will interactively guide the user through discovery questions one at a time.

**Wait for the discovery phase to complete.**

After discovery completes, say:
```
Phase 0 (Discovery) is complete! The discovery document is at [path].

Would you like to proceed to Phase 1: Requirements Gathering?
```

**WAIT for user approval.** If user says no, stop here. If yes, proceed.

**Step 3: Run Requirements Agent**

Use the SlashCommand tool to invoke the /feature-requirements command:
```
/feature-requirements $ARGUMENTS
```

This will interactively guide the user through requirements questions one at a time.

**Wait for the requirements phase to complete.**

After requirements completes, say:
```
Phase 1 (Requirements) is complete! The requirements document is at [path].

Would you like to proceed to Phase 2: Design?
```

**WAIT for user approval.** If user says no, stop here. If yes, proceed.

**Step 4: Run Design Agent**

Use the SlashCommand tool to invoke the /feature-design command:
```
/feature-design $ARGUMENTS
```

This will guide the user through the design phase.

**Wait for the design phase to complete.**

After design completes, say:
```
Phase 2 (Design) is complete! The design document is at [path].

Would you like to proceed to Phase 3: Task Breakdown?
```

**WAIT for user approval.** If user says no, stop here. If yes, proceed.

**Step 5: Run Tasks Agent**

Use the SlashCommand tool to invoke the /feature-tasks command:
```
/feature-tasks $ARGUMENTS
```

This will create the implementation task breakdown.

**Wait for the tasks phase to complete.**

After tasks completes, say:
```
Phase 3 (Task Breakdown) is complete! The tasks document is at [path].

✅ Feature specification complete!

Your documentation is ready:
- Discovery: [path]
- Requirements: [path]
- Design: [path]
- Tasks: [path]

You can now:
1. Review the complete specification
2. Use tasks.md to guide implementation
3. Share these docs with team members or other AI assistants

Would you like help implementing the tasks, or is the specification complete?
```

---

## Important Notes

- **Wait for each phase to complete** before proceeding to the next phase
- **Always ask for user approval** before advancing to the next phase
- **Do not skip phases** - each builds on the previous one
- **Use SlashCommand tool** to invoke /feature-discovery, /feature-requirements, /feature-design, /feature-tasks (NOT the Task tool)
- Each phase command will interactively guide the user through questions and create documentation
- If a user wants to skip a phase or already has some documents, respect that choice

---

## Example Orchestration

```
User: /feature Add JWT authentication

Claude: "I'll help you create a complete feature specification for: Add JWT authentication

This process has 4 phases:
0. Discovery - Understand the problem and explore solutions
1. Requirements - Document what needs to be built
2. Design - Plan how to build it
3. Tasks - Create implementation checklist

I'll run a specialized agent for each phase and wait for your approval before moving forward.

Let's start with Phase 0: Discovery..."

[Uses SlashCommand tool to invoke /feature-discovery]

[Discovery phase completes interactively]

Claude: "Phase 0 (Discovery) is complete! The discovery document is at features/jwt-auth/discovery.md.

Would you like to proceed to Phase 1: Requirements Gathering?"

User: "Yes"

[Uses SlashCommand tool to invoke /feature-requirements]

[Requirements phase completes interactively]

Claude: "Phase 1 (Requirements) is complete! The requirements document is at features/jwt-auth/requirements.md.

Would you like to proceed to Phase 2: Design?"

[Pattern continues through all 4 phases...]
```
