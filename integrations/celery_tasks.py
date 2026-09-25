from celery import Celery
from app.config import settings
from integrations.email_service import EmailService
from integrations.twilio_service import TwilioService

celery_app = Celery(
    'apex_intelligence',
    broker=settings.redis_url,
    backend=settings.redis_url
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(name='send_outreach_email_task')
def send_outreach_email_task(to_email: str, business_name: str, message: str):
    """
    Background task to send outreach emails.
    """
    email_service = EmailService()
    result = email_service.send_outreach_email(to_email, business_name, message)
    return {'success': result, 'email': to_email}

@celery_app.task(name='send_audit_delivery_task')
def send_audit_delivery_task(to_email: str, business_name: str, audit_content: str):
    """
    Background task to send audit reports.
    """
    email_service = EmailService()
    result = email_service.send_audit_delivery_email(to_email, business_name, audit_content)
    return {'success': result, 'email': to_email}

@celery_app.task(name='send_sms_task')
def send_sms_task(to_number: str, message: str):
    """
    Background task to send SMS messages.
    """
    twilio_service = TwilioService()
    result = twilio_service.send_sms(to_number, message)
    return {'success': result, 'phone': to_number}

@celery_app.task(name='scrape_business_reviews_task')
def scrape_business_reviews_task(place_id: str, business_name: str):
    """
    Background task to scrape and analyze business reviews.
    """
    # This would integrate with web scraping to gather reviews
    return {'success': True, 'place_id': place_id}

@celery_app.task(name='generate_business_research_task')
def generate_business_research_task(business_name: str, website: str, city: str):
    """
    Background task to research business online.
    """
    # This would scrape the website and gather competitive intelligence
    return {'success': True, 'business': business_name}
