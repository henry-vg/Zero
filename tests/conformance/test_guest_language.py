import ast

from tests.conformance._helpers import (
    GUEST_DIR,
    fail_if_violations,
    guest_files,
    parse,
)

_FORBIDDEN_NODES = {
    ast.BoolOp: "boolean operator",
    ast.BinOp: "binary operator",
    ast.Compare: "comparison",
    ast.If: "if",
    ast.IfExp: "conditional expression",
    ast.For: "for",
    ast.AsyncFor: "async for",
    ast.While: "while",
    ast.Match: "match",
    ast.ListComp: "list comprehension",
    ast.SetComp: "set comprehension",
    ast.DictComp: "dict comprehension",
    ast.GeneratorExp: "generator expression",
}

_FORBIDDEN_UNARY_OPERATORS = (
    ast.Not,
    ast.UAdd,
    ast.USub,
    ast.Invert,
)

_FORBIDDEN_BUILTINS = {
    "__import__",
    "all",
    "any",
    "bool",
    "eval",
    "exec",
    "int",
    "len",
    "sum",
}


def _forbidden_reason(
    node: ast.AST,
) -> str | None:
    reason = _FORBIDDEN_NODES.get(type(node))

    if reason is not None:
        return reason

    if isinstance(node, ast.Constant) and type(node.value) is bool:
        return "boolean literal"

    if isinstance(node, ast.UnaryOp) and isinstance(
        node.op,
        _FORBIDDEN_UNARY_OPERATORS,
    ):
        return "unary operator"

    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in _FORBIDDEN_BUILTINS
    ):
        return f"builtin {node.func.id}()"

    return None


def test_guest_does_not_use_native_python_computation():
    violations = []

    for source in guest_files():
        for node in ast.walk(parse(source)):
            reason = _forbidden_reason(node)

            if reason is None:
                continue

            violations.append(
                f"{source.relative_to(GUEST_DIR)}:{getattr(node, 'lineno', '?')} -> "
                f"{reason}"
            )

    fail_if_violations(
        violations,
        "native Python computations in GUEST",
    )
