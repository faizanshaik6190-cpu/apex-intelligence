from typing import Any, Dict

from app.agents.base import BaseAgent

class OutreachDealDeskAgent(BaseAgent):
    name = "Apex Outreach & Deal Desk"

    def run(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        offer = {
            "business_name": lead.get("business_name"),
            "price": 1200.0,
            "status": "negotiating",
            "message": (
                f"Hi {lead.get('business_name')}, we provide a professional growth audit "
                "to improve visibility, lead flow, and conversion performance. "
                "We can help identify the biggest opportunities for growth and provide a clear plan."
            ),
            "notes": "Initial offer prepared. Human approval required before final deal."
        }
        return offer
