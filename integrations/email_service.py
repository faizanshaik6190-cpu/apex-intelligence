import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from app.config import settings

class EmailService:
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.username = settings.smtp_username
        self.password = settings.smtp_password
    
    def send_outreach_email(self, to_email: str, business_name: str, message: str) -> bool:
        """
        Send a personalized outreach email to a business.
        """
        try:
            subject = f"Growth Opportunity for {business_name}"
            body = f"""Hi {business_name},

{message}

Best regards,
Apex Intelligence
Growth & Consulting Agency"""
            
            return self.send_email(to_email, subject, body)
        except Exception as e:
            print(f"Error sending outreach email: {e}")
            return False
    
    def send_audit_delivery_email(self, to_email: str, business_name: str, audit_content: str) -> bool:
        """
        Send the growth audit to the client.
        """
        try:
            subject = f"{business_name} - Growth Audit Report"
            body = f"""Hi {business_name},

Please find your professional growth audit report below:

{audit_content}

Best regards,
Apex Intelligence
Growth & Consulting Agency"""
            
            return self.send_email(to_email, subject, body)
        except Exception as e:
            print(f"Error sending audit email: {e}")
            return False
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Generic email sending function.
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
