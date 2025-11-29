"""Devcontainer verification tasks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context

from project.utils import get_current_working_directory


@task
def check(context: Context, *, build_only: bool = False, run_project_check: bool = False) -> None:
    """Verify the devcontainer builds and runs correctly in headless mode.

    Args:
        context: The invoke context.
        build_only: Only build the image, skip up and exec (fast check).
        run_project_check: Run 'invoke project.check' inside container instead of 'invoke --list'.

    """
    workspace_path = get_current_working_directory()

    # Verify Docker is available
    context.run("docker info", hide=True)

    # Build the devcontainer image
    context.run(
        f"npx @devcontainers/cli build --workspace-folder {workspace_path}",
        echo=True,
    )

    if build_only:
        return

    # Start container in headless mode
    context.run(
        f"npx @devcontainers/cli up --workspace-folder {workspace_path}",
        echo=True,
    )

    # Verify inside the container
    verify_cmd = "poetry run invoke project.check" if run_project_check else "poetry run invoke --list"
    context.run(
        f"npx @devcontainers/cli exec --workspace-folder {workspace_path} {verify_cmd}",
        echo=True,
    )


collection = Collection("devcontainer")
collection.add_task(check)
