from typing import Any, Dict, List

from app.agents.base import BaseAgent

class LeadHunterAgent(BaseAgent):
    name = "Apex Lead Hunter"

    def run(self, city: str, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        sample_businesses = [
            {
                "business_name": "Bright Path Dental",
                "city": city,
                "category": category,
                "website": "https://example.com/brightpathdental",
                "phone": "+1-555-0101",
                "email": "hello@brightpathdental.com",
                "rating": 4.8,
                "score": 92,
                "source": "google_maps",
                "notes": "Strong local presence, weak online conversion funnel"
            },
            {
                "business_name": "Harbor Auto Care",
                "city": city,
                "category": category,
                "website": "https://example.com/harborautocare",
                "phone": "+1-555-0102",
                "email": "service@harborautocare.com",
                "rating": 4.6,
                "score": 89,
                "source": "google_maps",
                "notes": "Needs lead generation and local trust improvements"
            },
            {
                "business_name": "Summit Wellness Studio",
                "city": city,
                "category": category,
                "website": "https://example.com/summitwellness",
                "phone": "+1-555-0103",
                "email": "hello@summitwellness.com",
                "rating": 4.9,
                "score": 95,
                "source": "google_maps",
                "notes": "Good brand, low conversion from website"
            }
        ]

        return sample_businesses[:limit]
