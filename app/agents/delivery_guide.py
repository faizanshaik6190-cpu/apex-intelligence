from typing import Any, Dict

from app.agents.base import BaseAgent

class DeliveryGuideAgent(BaseAgent):
    name = "Apex Delivery Guide"

    def run(self, business_name: str) -> Dict[str, Any]:
        steps = f"""IMPLEMENTATION ROADMAP - {business_name}

=== WEEK 1: FOUNDATION ===

Task 1: Review Growth Audit
- Read through all findings
- Identify top 3 priorities
- Schedule team alignment meeting

Task 2: Define Target Customer
- Document ideal customer profile
- List pain points they experience
- Map to your solution

Task 3: Clarify Your Offer
- Write single-sentence value proposition
- Create 3-benefit summary
- Identify unique differentiators

=== WEEK 2-3: QUICK WINS ===

Task 4: Fix High-Impact Website Issues
- Improve headline on homepage
- Add social proof/testimonials
- Create clear CTA above the fold

Task 5: Improve Local Search
- Optimize Google Business Profile
- Add 50+ customer reviews target
- Build local citations

Task 6: Launch Measurement
- Set up Google Analytics 4
- Create dashboard for key metrics
- Define success metrics

=== WEEK 4-6: SCALE ===

Task 7: Lead Generation Testing
- Run 2-3 lead gen experiments
- Test messaging and channels
- Measure cost per qualified lead

Task 8: Conversion Optimization
- A/B test key pages
- Implement chat/contact system
- Create email follow-up sequence

Task 9: Revisit Results
- Analyze performance after 30 days
- Iterate on top performers
- Plan next phase improvements

=== ONGOING: OPTIMIZATION ===

- Monthly performance review
- Quarterly strategy sessions
- Continuous A/B testing
- Regular team updates
"""

        return {
            "title": f"{business_name} Delivery Roadmap",
            "content": steps
        }
