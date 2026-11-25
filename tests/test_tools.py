import re

import pytest

from tooled_ai_agent.core.tool import Tool, ToolRegistry
from tooled_ai_agent.tools import CalculatorTool, CurrentTimeTool


def test_calculator_arithmetic():
    calc = CalculatorTool()
    assert calc.run("(12.5 + 7) * 3 / 2") == "29.25"
    assert calc.run("2 ** 100") == str(2**100)
    assert calc.run("-5 % 3") == "1"


def test_calculator_rejects_code():
    with pytest.raises(ValueError):
        CalculatorTool().run("__import__('os').getcwd()")


def test_current_time_format():
    # "2026-11-25 21:42:00 EET (Wednesday)"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \S+ \(\w+\)",
                        CurrentTimeTool().run("Europe/Kyiv"))


def test_registry_executes_and_reports_errors():
    reg = ToolRegistry([CalculatorTool()])
    assert reg.execute("calculator", {"expression": "1 + 1"}) == "2"
    assert "unknown tool" in reg.execute("nope", {})
    assert "Execution error" in reg.execute("calculator", {"expression": "x"})


def test_registry_rejects_duplicates():
    with pytest.raises(ValueError):
        ToolRegistry([CalculatorTool(), CalculatorTool()])


def test_schema_format():
    schema = CalculatorTool().schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "calculator"
    assert issubclass(CalculatorTool, Tool)
