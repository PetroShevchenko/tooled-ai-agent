"""Tool: current date and time."""

from datetime import datetime
from zoneinfo import ZoneInfo

from ..core.tool import Tool

class CurrentTimeTool(Tool):
    name = "current_time"
    description = (
        "Returns the current date and time. "
        "Use it whenever the answer depends on today's date or the current time."
    )
    parameters = {
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "IANA time zone, e.g. 'Europe/Kyiv' or 'Asia/Tokyo'. "
                               "Omit to use the local time of this computer.",
            }
        },
        "required": [],
    }

    def run(self, timezone: str | None = None) -> str:
        now = datetime.now(ZoneInfo(timezone)) if timezone else datetime.now().astimezone()
        return now.strftime("%Y-%m-%d %H:%M:%S %Z (%A)")