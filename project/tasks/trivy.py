"""Trivy security scanning tasks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context

from project.utils import ensure_directory, get_current_working_directory


@task
def check(context: Context) -> None:
    """Run trivy security scanner using Docker to scan the filesystem for vulnerabilities and security issues."""
    workspace_path = get_current_working_directory()
    cache_path = workspace_path / ".quality" / "trivy"
    ensure_directory(cache_path)

    context.run(
        f"docker run --rm "
        f"-v {workspace_path}:/workspace "
        f"-v {cache_path}:/root/.cache/ "
        f"aquasec/trivy fs "
        f"--scanners vuln,secret,misconfig,license "
        f"--exit-code 1 "
        f"/workspace",
        echo=True,
    )


collection = Collection("trivy")
collection.add_task(check)
