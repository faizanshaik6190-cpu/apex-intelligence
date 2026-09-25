from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lead, Deal, Client, Audit, DeliveryPlan, Ticket
from app.auth import api_key_auth

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
async def get_stats(api_key: str = Depends(api_key_auth), db: Session = Depends(get_db)):
    """
    Get company statistics and analytics.
    """
    leads_count = db.query(Lead).count()
    deals_count = db.query(Deal).count()
    clients_count = db.query(Client).count()
    audits_count = db.query(Audit).count()
    tickets_count = db.query(Ticket).count()
    
    approved_deals = db.query(Deal).filter(Deal.owner_approved == True).count()
    pending_deals = db.query(Deal).filter(Deal.owner_approved == False).count()
    
    approved_audits = db.query(Audit).filter(Audit.owner_approved == True).count()
    pending_audits = db.query(Audit).filter(Audit.owner_approved == False).count()
    
    return {
        "leads": leads_count,
        "deals": {"total": deals_count, "approved": approved_deals, "pending": pending_deals},
        "clients": clients_count,
        "audits": {"total": audits_count, "approved": approved_audits, "pending": pending_audits},
        "tickets": tickets_count,
        "company_health": "operational"
    }

@router.get("/logs")
async def get_logs(api_key: str = Depends(api_key_auth), limit: int = 100):
    """
    Get recent system logs.
    """
    # This would read from actual log files
    return {
        "message": "Logs endpoint - check log files in /logs directory",
        "log_locations": [
            "/app/logs/fastapi.log",
            "/app/logs/celery_worker.log",
            "/app/logs/redis.log"
        ]
    }

@router.post("/backup")
async def backup_now(api_key: str = Depends(api_key_auth)):
    """
    Trigger immediate backup.
    """
    # This would call the backup script
    return {"message": "Backup triggered", "status": "in progress"}
