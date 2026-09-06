import ast
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[2]

GUEST_DIR = ROOT_DIR / "src" / "guest"
TRUSTED_BASE_DIR = ROOT_DIR / "src" / "host" / "trusted_base"

GUEST_NAMESPACE = "src.guest"
TRUSTED_BASE_NAMESPACE = "src.host.trusted_base"


def guest_files() -> tuple[Path, ...]:
    return tuple(sorted(GUEST_DIR.rglob("*.py")))


def parse(
    path: Path,
) -> ast.Module:
    return ast.parse(
        path.read_text("utf-8"),
        str(path),
    )


def imports(
    path: Path,
) -> tuple[ast.Import | ast.ImportFrom, ...]:
    return tuple(
        node
        for node in ast.walk(parse(path))
        if isinstance(node, (ast.Import, ast.ImportFrom))
    )


def imported_modules(
    node: ast.Import | ast.ImportFrom,
) -> tuple[str, ...]:
    if isinstance(node, ast.Import):
        return tuple(alias.name for alias in node.names)

    if node.module is None:
        return ()

    return (node.module,)


def fail_if_violations(
    violations: list[str],
    description: str,
) -> None:
    if not violations:
        return

    pytest.fail(
        f"{len(violations)} {description} found.\n\n"
        + "\n".join(f"- {violation}" for violation in violations),
        pytrace=False,
    )
