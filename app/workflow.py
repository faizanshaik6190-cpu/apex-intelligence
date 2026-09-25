from typing import List

from sqlalchemy.orm import Session

from app.agents.ceo import CEOAgent
from app.agents.client_care import ClientCareAgent
from app.agents.delivery_guide import DeliveryGuideAgent
from app.agents.growth_auditor import GrowthAuditorAgent
from app.agents.lead_hunter import LeadHunterAgent
from app.models import ApprovalRequest, Audit, Client, Deal, DeliveryPlan, Lead, Ticket

class WorkflowEngine:
    def __init__(self, db: Session):
        self.db = db

    def generate_leads(self, city: str, category: str, limit: int = 10):
        hunter = LeadHunterAgent()
        leads = hunter.run(city, category, limit)
        created = []

        for lead in leads:
            new_lead = Lead(
                business_name=lead["business_name"],
                city=lead["city"],
                category=lead["category"],
                website=lead.get("website"),
                phone=lead.get("phone"),
                email=lead.get("email"),
                rating=lead.get("rating", 0.0),
                score=lead.get("score", 0.0),
                source=lead.get("source", "google_maps"),
                notes=lead.get("notes", ""),
                status="new"
            )
            self.db.add(new_lead)
            self.db.commit()
            self.db.refresh(new_lead)
            created.append(new_lead)

        return created

    def approve_leads(self, lead_ids: List[int]):
        for lead_id in lead_ids:
            lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
            if lead:
                lead.status = "approved_for_outreach"
                self.db.add(ApprovalRequest(
                    task_type="lead_list",
                    target_id=lead.id,
                    status="approved",
                    notes="Lead approved by owner"
                ))
        self.db.commit()

    def create_deal(self, lead_id: int, price: float, notes: str = ""):
        lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise ValueError("Lead not found")

        deal = Deal(
            lead_id=lead.id,
            price=price,
            status="negotiating",
            owner_approved=False,
            notes=notes
        )
        self.db.add(deal)
        self.db.commit()
        self.db.refresh(deal)

        lead.status = "deal_created"
        self.db.commit()

        return deal

    def approve_deal(self, deal_id: int):
        deal = self.db.query(Deal).filter(Deal.id == deal_id).first()
        if not deal:
            raise ValueError("Deal not found")

        deal.owner_approved = True
        deal.status = "accepted"

        client = Client(
            deal_id=deal.id,
            business_name=deal.lead.business_name,
            city=deal.lead.city,
            contact_name="Owner",
            contact_email=deal.lead.email,
            status="active"
        )
        self.db.add(client)
        self.db.commit()

        self.db.add(ApprovalRequest(
            task_type="deal_offer",
            target_id=deal.id,
            status="approved",
            notes="Deal approved by owner"
        ))
        self.db.commit()

        return client

    def create_audit(self, client_id: int):
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ValueError("Client not found")

        auditor = GrowthAuditorAgent()
        audit_data = auditor.run(client.business_name, client.city, "")
        audit = Audit(
            client_id=client.id,
            title=audit_data["title"],
            content=audit_data["content"],
            owner_approved=False
        )
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(audit)

        client.status = "audit_started"
        self.db.commit()
        return audit

    def approve_audit(self, audit_id: int):
        audit = self.db.query(Audit).filter(Audit.id == audit_id).first()
        if not audit:
            raise ValueError("Audit not found")

        audit.owner_approved = True
        self.db.add(ApprovalRequest(
            task_type="audit_send",
            target_id=audit.id,
            status="approved",
            notes="Audit approved by owner"
        ))
        self.db.commit()
        return audit

    def create_delivery_plan(self, client_id: int):
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ValueError("Client not found")

        guide = DeliveryGuideAgent()
        plan_data = guide.run(client.business_name)
        plan = DeliveryPlan(
            client_id=client.id,
            title=plan_data["title"],
            content=plan_data["content"],
            owner_approved=False
        )
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)

        client.status = "delivery_started"
        self.db.commit()
        return plan

    def approve_delivery(self, plan_id: int):
        plan = self.db.query(DeliveryPlan).filter(DeliveryPlan.id == plan_id).first()
        if not plan:
            raise ValueError("Delivery plan not found")

        plan.owner_approved = True
        self.db.add(ApprovalRequest(
            task_type="delivery_send",
            target_id=plan.id,
            status="approved",
            notes="Delivery plan approved by owner"
        ))
        self.db.commit()
        return plan

    def create_ticket(self, client_id: int, title: str, description: str):
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ValueError("Client not found")

        ticket = Ticket(
            client_id=client.id,
            title=title,
            description=description,
            status="open"
        )
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)

        return ticket

    def ceo_summary(self):
        leads = self.db.query(Lead).all()
        deals = self.db.query(Deal).all()
        audits = self.db.query(Audit).all()
        tickets = self.db.query(Ticket).all()

        ceo = CEOAgent()
        return ceo.run(
            leads=[{"id": l.id, "business_name": l.business_name, "status": l.status} for l in leads],
            deals=[{"id": d.id, "price": d.price, "status": d.status, "owner_approved": d.owner_approved} for d in deals],
            audits=[{"id": a.id, "title": a.title, "owner_approved": a.owner_approved} for a in audits],
            tickets=[{"id": t.id, "title": t.title, "status": t.status} for t in tickets],
        )
