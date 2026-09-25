from twilio.rest import Client as TwilioClient
from typing import Dict, Any
from app.config import settings

class TwilioService:
    def __init__(self):
        self.client = TwilioClient(settings.twilio_account_sid, settings.twilio_auth_token)
        self.phone_number = settings.twilio_phone_number
    
    def send_sms(self, to_number: str, message: str) -> bool:
        """
        Send an SMS message to a business contact.
        """
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            return message.sid is not None
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
    
    def send_outreach_sms(self, to_number: str, business_name: str) -> bool:
        """
        Send an outreach SMS to a business.
        """
        message = f"Hi {business_name}, Apex Intelligence here! We provide professional growth audits for businesses like yours. Interested in learning how to improve your visibility and leads? Reply YES or visit our website."
        return self.send_sms(to_number, message)
    
    def make_voice_call(self, to_number: str, message: str) -> bool:
        """
        Make a voice call with a message.
        """
        try:
            call = self.client.calls.create(
                to=to_number,
                from_=self.phone_number,
                url="http://demo.twilio.com/docs/voice.xml"  # Replace with actual TwiML
            )
            return call.sid is not None
        except Exception as e:
            print(f"Error making voice call: {e}")
            return False
