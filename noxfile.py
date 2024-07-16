"""Nox sessions."""

import nox


@nox.session(python=["3.7", "3.9", "3.11"])
def tests(session):
    """Run tests."""
    session.run("make", "testdeps", external=True)
    session.run("make", "test", external=True)


@nox.session(python=["3.11"])
def lint(session):
    """Run linting."""
    session.run("make", "lintdeps", external=True)
    session.run("make", "lint", external=True)
