"""Trivy security scanning tasks."""

from invoke import task
from invoke.collection import Collection
from invoke.context import Context


@task
def check(context: Context) -> None:
    """Run trivy security scanner using Docker to scan the filesystem for vulnerabilities and security issues."""
    context.run("mkdir -p .quality/trivy", echo=True)
    context.run(
        "docker run --rm "
        "-v $(pwd):/workspace "
        "-v $(pwd)/.quality/trivy:/root/.cache/ "
        "aquasec/trivy fs "
        "--scanners vuln,secret,misconfig,license "
        "--exit-code 1 "
        "/workspace",
        echo=True,
    )


collection = Collection("trivy")
collection.add_task(check)
