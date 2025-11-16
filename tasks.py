"""Invoke task collections for project development tasks."""

from invoke.collection import Collection

# Import all task modules
from project import (
    actionlint,
    deptry,
    mypy,
    pipaudit,
    precommit,
    ruff,
    testing,
    vulture,
    xenon,
)
from project import project as project_tasks

# Create root namespace
ns = Collection()

# Register all collections
ns.add_collection(actionlint.collection)
ns.add_collection(deptry.collection)
ns.add_collection(mypy.collection)
ns.add_collection(pipaudit.collection)
ns.add_collection(precommit.collection)
ns.add_collection(project_tasks.collection)
ns.add_collection(ruff.collection)
ns.add_collection(testing.collection)
ns.add_collection(vulture.collection)
ns.add_collection(xenon.collection)
