from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Audit, Client, Deal, DeliveryPlan, Lead, Ticket
from app.workflow import WorkflowEngine
from integrations.google_maps_service import GoogleMapsService
from integrations.email_service import EmailService
from integrations.twilio_service import TwilioService
from integrations.voice_service import VoiceService
from integrations.celery_tasks import send_outreach_email_task, send_sms_task

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Apex Intelligence API",
    description="AI-powered growth agency with 6 specialized agents + integrations",
    version="2.0.0"
)

# Request models
class LeadCreateRequest(BaseModel):
    city: str
    category: str
    limit: int = 10

class ApproveLeadRequest(BaseModel):
    lead_ids: List[int]

class DealCreateRequest(BaseModel):
    lead_id: int
    price: float
    notes: str = ""

class AuditCreateRequest(BaseModel):
    client_id: int

class DeliveryPlanCreateRequest(BaseModel):
    client_id: int

class TicketCreateRequest(BaseModel):
    client_id: int
    title: str
    description: str

class OutreachEmailRequest(BaseModel):
    lead_id: int
    message: str = ""

class OutreachSMSRequest(BaseModel):
    lead_id: int

class VoiceCommandRequest(BaseModel):
    command: str

# Health & Status endpoints
@app.get("/")
def root():
    return {
        "message": "Apex Intelligence is online.",
        "company": "Apex Intelligence",
        "status": "operational",
        "version": "2.0.0",
        "agents": [
            "Apex Lead Hunter",
            "Apex Outreach & Deal Desk",
            "Apex Growth Auditor",
            "Apex Delivery Guide",
            "Apex Client Care",
            "Apex CEO"
        ],
        "integrations": [
            "Google Maps",
            "Email Service",
            "Twilio (SMS/Voice)",
            "OpenAI Voice",
            "Celery (Background Tasks)",
            "React Dashboard"
        ]
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

# Lead endpoints
@app.post("/leads/generate")
def generate_leads(payload: LeadCreateRequest, db: Session = Depends(get_db)):
    try:
        # Use Google Maps if configured, otherwise use sample data
        workflow = WorkflowEngine(db)
        leads = workflow.generate_leads(payload.city, payload.category, payload.limit)
        return {
            "message": "Leads generated",
            "count": len(leads),
            "leads": [{"id": l.id, "business_name": l.business_name, "score": l.score} for l in leads]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/leads/approve")
def approve_leads(payload: ApproveLeadRequest, db: Session = Depends(get_db)):
    workflow = WorkflowEngine(db)
    workflow.approve_leads(payload.lead_ids)
    return {"message": "Leads approved", "lead_ids": payload.lead_ids}

@app.get("/leads")
def list_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()
    return [{"id": l.id, "business_name": l.business_name, "city": l.city, "status": l.status, "score": l.score} for l in leads]

# Deal endpoints
@app.post("/deals/create")
def create_deal(payload: DealCreateRequest, db: Session = Depends(get_db)):
    try:
        workflow = WorkflowEngine(db)
        deal = workflow.create_deal(payload.lead_id, payload.price, payload.notes)
        return {"message": "Deal created", "deal_id": deal.id, "price": deal.price, "status": deal.status}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/deals/approve")
def approve_deal(deal_id: int, db: Session = Depends(get_db)):
    try:
        workflow = WorkflowEngine(db)
        client = workflow.approve_deal(deal_id)
        return {"message": "Deal approved and client created", "client_id": client.id, "business_name": client.business_name}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/deals")
def list_deals(db: Session = Depends(get_db)):
    deals = db.query(Deal).all()
    return [{"id": d.id, "lead_id": d.lead_id, "price": d.price, "status": d.status, "owner_approved": d.owner_approved} for d in deals]

# Client endpoints
@app.get("/clients")
def list_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return [{"id": c.id, "business_name": c.business_name, "city": c.city, "status": c.status} for c in clients]

# Audit endpoints
@app.post("/audits/create")
def create_audit(payload: AuditCreateRequest, db: Session = Depends(get_db)):
    try:
        workflow = WorkflowEngine(db)
        audit = workflow.create_audit(payload.client_id)
        return {"message": "Audit created", "audit_id": audit.id, "title": audit.title}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/audits/approve")
def approve_audit(audit_id: int, db: Session = Depends(get_db)):
    try:
        workflow = WorkflowEngine(db)
        audit = workflow.approve_audit(audit_id)
        return {"message": "Audit approved", "audit_id": audit.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/audits")
def list_audits(db: Session = Depends(get_db)):
    audits = db.query(Audit).all()
    return [{"id": a.id, "client_id": a.client_id, "title": a.title, "owner_approved": a.owner_approved} for a in audits]

# Delivery endpoints
@app.post("/delivery/create")
def create_delivery(payload: DeliveryPlanCreateRequest, db: Session = Depends(get_db)):
    try:
        workflow = WorkflowEngine(db)
        plan = workflow.create_delivery_plan(payload.client_id)
        return {"message": "Delivery plan created", "plan_id": plan.id, "title": plan.title}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/delivery/approve")
def approve_delivery(plan_id: int, db: Session = Depends(get_db)):
    try:
        workflow = WorkflowEngine(db)
        plan = workflow.approve_delivery(plan_id)
        return {"message": "Delivery approved", "plan_id": plan.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delivery")
def list_delivery_plans(db: Session = Depends(get_db)):
    plans = db.query(DeliveryPlan).all()
    return [{"id": p.id, "client_id": p.client_id, "title": p.title, "owner_approved": p.owner_approved} for p in plans]

# Customer Care endpoints
@app.post("/customers/tickets/create")
def create_ticket(payload: TicketCreateRequest, db: Session = Depends(get_db)):
    try:
        workflow = WorkflowEngine(db)
        ticket = workflow.create_ticket(payload.client_id, payload.title, payload.description)
        return {"message": "Ticket created", "ticket_id": ticket.id, "status": ticket.status}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/tickets")
def list_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    return [{"id": t.id, "client_id": t.client_id, "title": t.title, "status": t.status} for t in tickets]

# CEO endpoints
@app.get("/ceo/summary")
def ceo_summary(db: Session = Depends(get_db)):
    workflow = WorkflowEngine(db)
    summary = workflow.ceo_summary()
    return summary

@app.get("/ceo/voice/summary")
def ceo_voice_summary(db: Session = Depends(get_db)):
    workflow = WorkflowEngine(db)
    summary = workflow.ceo_summary()
    voice_service = VoiceService()
    audio = voice_service.speak_company_summary(summary)
    return {"message": "Voice summary generated", "summary": summary}

@app.post("/ceo/voice/command")
def ceo_voice_command(payload: VoiceCommandRequest):
    voice_service = VoiceService()
    response = voice_service.get_voice_command_response(payload.command)
    return {"command": payload.command, "response": response}

# Outreach endpoints
@app.post("/outreach/email")
def send_outreach_email(payload: OutreachEmailRequest, db: Session = Depends(get_db)):
    try:
        lead = db.query(Lead).filter(Lead.id == payload.lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Queue background task
        message = payload.message or f"We provide professional growth audits for businesses like {lead.business_name}. Interested?"
        send_outreach_email_task.delay(lead.email, lead.business_name, message)
        
        return {"message": "Email queued for sending", "lead_id": payload.lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/outreach/sms")
def send_outreach_sms(payload: OutreachSMSRequest, db: Session = Depends(get_db)):
    try:
        lead = db.query(Lead).filter(Lead.id == payload.lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Queue background task
        send_sms_task.delay(lead.phone, f"Hi {lead.business_name}, Apex Intelligence here!")
        
        return {"message": "SMS queued for sending", "lead_id": payload.lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
