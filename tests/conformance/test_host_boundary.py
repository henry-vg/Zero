import ast

from tests.conformance._helpers import (
    GUEST_DIR,
    GUEST_NAMESPACE,
    TRUSTED_BASE_DIR,
    TRUSTED_BASE_NAMESPACE,
    fail_if_violations,
    guest_files,
    imported_modules,
    imports,
    parse,
)


def _trusted_base_exports() -> frozenset[str]:
    init = TRUSTED_BASE_DIR / "__init__.py"

    for node in parse(init).body:
        if not isinstance(node, ast.Assign):
            continue

        defines_all = any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        )

        if not defines_all:
            continue

        value = ast.literal_eval(node.value)

        assert isinstance(value, (list, tuple)), (
            "Trusted Base __all__ must be a static list or tuple"
        )
        assert all(isinstance(item, str) for item in value), (
            "Trusted Base __all__ must contain only strings"
        )

        return frozenset(value)

    raise AssertionError("Trusted Base must declare __all__")


def test_guest_imports_respect_host_boundary():
    trusted_base_exports = _trusted_base_exports()
    violations = []

    for source in guest_files():
        for node in imports(source):
            location = f"{source.relative_to(GUEST_DIR)}:{node.lineno}"

            if isinstance(node, ast.Import):
                violations.append(f"{location} -> `import ...` is forbidden")
                continue

            if node.level != 0:
                violations.append(f"{location} -> relative imports are forbidden")
                continue

            if any(alias.name == "*" for alias in node.names):
                violations.append(f"{location} -> wildcard imports are forbidden")
                continue

            module = node.module

            if module is None:
                violations.append(f"{location} -> import has no module")
                continue

            if module.startswith(f"{GUEST_NAMESPACE}."):
                continue

            if module == TRUSTED_BASE_NAMESPACE:
                for alias in node.names:
                    if alias.name not in trusted_base_exports:
                        violations.append(
                            f"{location} -> {alias.name} is not exported "
                            "by the Trusted Base"
                        )
                continue

            violations.append(f"{location} -> {module} crosses the GUEST boundary")

    fail_if_violations(
        violations,
        "invalid GUEST imports",
    )


def test_trusted_base_never_depends_on_guest():
    violations = []

    for source in sorted(TRUSTED_BASE_DIR.rglob("*.py")):
        for node in imports(source):
            for module in imported_modules(node):
                if module == GUEST_NAMESPACE or module.startswith(
                    f"{GUEST_NAMESPACE}."
                ):
                    violations.append(
                        f"{source.relative_to(TRUSTED_BASE_DIR)}:{node.lineno} -> "
                        f"{module}"
                    )

    fail_if_violations(
        violations,
        "Trusted Base -> GUEST dependencies",
    )
