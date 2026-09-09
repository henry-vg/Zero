import ast

from tests.conformance._helpers import (
    GUEST_DIR,
    fail_if_violations,
    guest_files,
    parse,
)

_ANNOTATION_FIELDS = frozenset(
    {
        "annotation",
        "returns",
    }
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

_FORBIDDEN_CONTEXTUAL_NODES = {
    ast.Attribute: "attribute access",
    ast.Dict: "dict literal",
    ast.List: "list literal",
    ast.Set: "set literal",
    ast.Subscript: "subscript",
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
    "dict",
    "eval",
    "exec",
    "getattr",
    "int",
    "len",
    "list",
    "set",
    "sum",
    "tuple",
}

_FORBIDDEN_CONTEXTUAL_CALLS = {
    "Bit": "Bit() construction",
}


def _walk_with_context(
    node: ast.AST,
    in_annotation: bool = False,
) -> tuple[tuple[ast.AST, bool], ...]:
    nodes = [(node, in_annotation)]

    for field, value in ast.iter_fields(node):
        child_in_annotation = in_annotation or field in _ANNOTATION_FIELDS

        if isinstance(value, ast.AST):
            nodes.extend(_walk_with_context(value, child_in_annotation))
            continue

        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    nodes.extend(_walk_with_context(item, child_in_annotation))

    return tuple(nodes)


def _forbidden_reason(
    node: ast.AST,
    in_annotation: bool,
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

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id in _FORBIDDEN_BUILTINS:
            return f"builtin {node.func.id}()"

        if not in_annotation and node.func.id in _FORBIDDEN_CONTEXTUAL_CALLS:
            return _FORBIDDEN_CONTEXTUAL_CALLS[node.func.id]

    if in_annotation:
        return None

    reason = _FORBIDDEN_CONTEXTUAL_NODES.get(type(node))

    if reason is not None:
        return reason

    if isinstance(node, ast.Constant) and type(node.value) is int:
        return "integer literal"

    return None


def _forbidden_reasons(
    source: str,
) -> tuple[str, ...]:
    reasons = []

    for node, in_annotation in _walk_with_context(ast.parse(source)):
        reason = _forbidden_reason(node, in_annotation)

        if reason is not None:
            reasons.append(reason)

    return tuple(reasons)


def test_guest_does_not_use_native_python_computation():
    violations = []

    for source in guest_files():
        for node, in_annotation in _walk_with_context(parse(source)):
            reason = _forbidden_reason(node, in_annotation)

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
