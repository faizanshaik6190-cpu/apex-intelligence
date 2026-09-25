from typing import Optional, Dict, Any
from app.config import settings

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class VoiceService:
    def __init__(self):
        if OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model or "gpt-4"
    
    def speak_company_summary(self, summary: Dict[str, Any]) -> str:
        """
        Convert company summary to spoken audio.
        Uses OpenAI Text-to-Speech.
        """
        if not OPENAI_AVAILABLE:
            return "Voice service not available. Install openai package."
        
        try:
            summary_text = self._format_summary_for_speech(summary)
            
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=summary_text
            )
            
            return response
        except Exception as e:
            print(f"Error generating voice: {e}")
            return None
    
    def _format_summary_for_speech(self, summary: Dict[str, Any]) -> str:
        """
        Format the summary for natural speech output.
        """
        text = f"""Good news. Here's your Apex Intelligence company update.
        
You have {summary.get('lead_count', 0)} leads in pipeline.
{summary.get('deal_count', 0)} active deals.
{summary.get('audit_count', 0)} audits in progress.
{summary.get('ticket_count', 0)} customer support tickets.

Pending approvals: {summary.get('pending_approvals', 0)}.

Status: {summary.get('status_message', 'Operational')}.

All major actions await your approval. Report complete.
        """
        return text
    
    def get_voice_command_response(self, user_input: str) -> str:
        """
        Process a voice command and return a response.
        Uses GPT-4 for understanding and responding.
        """
        if not OPENAI_AVAILABLE:
            return "Voice commands not available."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are the CEO of Apex Intelligence, an AI-powered growth agency. Answer questions about the company status, leads, deals, audits, and customer care. Be professional and concise."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error processing voice command: {e}")
            return "I didn't understand that. Could you repeat?"
