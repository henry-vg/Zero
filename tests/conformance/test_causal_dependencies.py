import re
from collections import defaultdict
from pathlib import Path

from tests.conformance._helpers import (
    GUEST_DIR,
    GUEST_NAMESPACE,
    fail_if_violations,
    guest_files,
    imported_modules,
    imports,
)

_CAUSAL_NAME_PATTERN = re.compile(r"^n(?P<position>\d{3})_.+$")


def _causal_position(
    path: Path,
) -> tuple[int, ...] | None:
    position = []

    for part in path.relative_to(GUEST_DIR).parts:
        match = _CAUSAL_NAME_PATTERN.fullmatch(Path(part).stem)

        if match is None:
            return None

        position.append(int(match.group("position")))

    return tuple(position)


def _guest_module_path(
    module: str,
) -> Path | None:
    if not module.startswith(f"{GUEST_NAMESPACE}."):
        return None

    relative_module = module.removeprefix(f"{GUEST_NAMESPACE}.")
    path = GUEST_DIR.joinpath(*relative_module.split(".")).with_suffix(".py")

    return path if path.is_file() else None


def _guest_units() -> tuple[Path, ...]:
    return tuple(
        sorted(
            path
            for path in GUEST_DIR.rglob("*")
            if "__pycache__" not in path.parts
            and (path.is_dir() or path.suffix == ".py")
        )
    )


def test_every_guest_unit_has_a_causal_position():
    violations = []

    for path in _guest_units():
        name = path.stem if path.is_file() else path.name

        if _CAUSAL_NAME_PATTERN.fullmatch(name) is None:
            violations.append(str(path.relative_to(GUEST_DIR)))

    fail_if_violations(
        violations,
        "GUEST units without a valid 'nDDD_' causal position",
    )


def test_sibling_causal_positions_are_unique():
    violations = []
    parents = (
        GUEST_DIR,
        *(path for path in _guest_units() if path.is_dir()),
    )

    for parent in parents:
        by_position: dict[int, list[str]] = defaultdict(list)

        for child in parent.iterdir():
            if not (child.is_dir() or child.suffix == ".py"):
                continue

            name = child.stem if child.is_file() else child.name
            match = _CAUSAL_NAME_PATTERN.fullmatch(name)

            if match is None:
                continue

            by_position[int(match.group("position"))].append(child.name)

        for position, names in by_position.items():
            if len(names) > 1:
                relative_parent = parent.relative_to(GUEST_DIR)
                violations.append(
                    f"{relative_parent or '.'}: "
                    f"n{position:03d}_ -> {', '.join(sorted(names))}"
                )

    fail_if_violations(
        violations,
        "duplicate sibling causal positions",
    )


def test_guest_dependencies_only_point_to_the_causal_past():
    violations = []

    for source in guest_files():
        source_position = _causal_position(source)

        if source_position is None:
            continue

        for node in imports(source):
            for module in imported_modules(node):
                if not module.startswith(f"{GUEST_NAMESPACE}."):
                    continue

                target = _guest_module_path(module)

                if target is None:
                    violations.append(
                        f"{source.relative_to(GUEST_DIR)}:{node.lineno} -> "
                        f"{module} does not resolve to a concrete GUEST module"
                    )
                    continue

                target_position = _causal_position(target)

                if target_position is None:
                    continue

                if target_position >= source_position:
                    violations.append(
                        f"{source.relative_to(GUEST_DIR)}:{node.lineno} -> "
                        f"{module} ({target_position} >= {source_position})"
                    )

    fail_if_violations(
        violations,
        "invalid GUEST causal dependencies",
    )
