"""Calculator tool."""

import ast
import operator

from ..core.tool import Tool


class CalculatorTool(Tool):
    """Safe calculator: numbers and arithmetic only, no eval()."""

    name = "calculator"
    description = (
        "Calculates an arithmetic expression. Use it for any calculations "
        "instead of doing the math in your head."
    )
    parameters = {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "An expression such as '(12.5 + 7) * 3 / 2'",
            }
        },
        "required": ["expression"],
    }

    _OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }

    def run(self, expression: str) -> str:
        result = self._eval(ast.parse(expression, mode="eval").body)
        if isinstance(result, int):
            return str(result)  # integers — unchanged: 2**100 will remain exact
        return f"{result:.10g}"  # 25.200000000000003 → 25.2

    def _eval(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in self._OPS:
            return self._OPS[type(node.op)](self._eval(node.left), self._eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._OPS:
            return self._OPS[type(node.op)](self._eval(node.operand))
        raise ValueError("Only numbers and '+ - * / ** %' are allowed.")
