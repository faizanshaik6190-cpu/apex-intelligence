from typing import Any, Dict, List

from app.agents.base import BaseAgent

class CEOAgent(BaseAgent):
    name = "Apex CEO"

    def run(
        self,
        leads: List[Dict[str, Any]],
        deals: List[Dict[str, Any]],
        audits: List[Dict[str, Any]],
        tickets: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        pending_approvals = [
            item for item in leads if not item.get("approved", False)
        ] + [
            item for item in deals if not item.get("owner_approved", False)
        ]

        return {
            "company_name": "Apex Intelligence",
            "company_status": "operational",
            "lead_count": len(leads),
            "deal_count": len(deals),
            "audit_count": len(audits),
            "ticket_count": len(tickets),
            "pending_approvals": len(pending_approvals),
            "status_message": "Company running with owner approval gates",
            "key_notes": [
                "All major actions await approval.",
                "All reports route to the Apex CEO.",
                "The owner remains the final business decision-maker.",
                f"Current pipeline: {len(leads)} leads, {len(deals)} deals, {len(audits)} audits"
            ]
        }
