from typing import Any, Dict

from app.agents.base import BaseAgent

class ClientCareAgent(BaseAgent):
    name = "Apex Client Care"

    def run(self, client_name: str, issue: str) -> Dict[str, Any]:
        return {
            "title": f"{client_name} Support Ticket",
            "description": issue,
            "status": "open",
            "priority": "medium"
        }
