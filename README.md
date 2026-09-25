# Apex Intelligence

An AI-powered growth and consulting company that uses 6 specialized agents to:

- Generate leads from local businesses
- Negotiate service contracts
- Create professional 3-page growth audits
- Deliver implementation roadmaps
- Handle customer support
- Report to the CEO/owner

## Company Structure

The company is run by 6 main AI agents:

1. **Apex Lead Hunter** - Generates qualified leads from local businesses
2. **Apex Outreach & Deal Desk** - Handles outreach and price negotiation
3. **Apex Growth Auditor** - Creates professional 3-page business audits
4. **Apex Delivery Guide** - Builds implementation roadmaps
5. **Apex Client Care** - Handles customer support and issues
6. **Apex CEO** - Central reporting and approval authority

## Core Features

- ✅ Lead generation with scoring
- ✅ Deal creation and negotiation workflow
- ✅ Professional audit report generation
- ✅ Implementation roadmap delivery
- ✅ Customer support ticketing
- ✅ Owner approval gates on all major actions
- ✅ Executive CEO summary dashboard
- ✅ **NEW: Google Maps lead generation**
- ✅ **NEW: Email & SMS outreach automation**
- ✅ **NEW: Twilio voice integration**
- ✅ **NEW: Voice interface for CEO agent**
- ✅ **NEW: React dashboard**
- ✅ **NEW: Background job processing with Celery**

## Business Rules

1. All major actions require owner approval:
   - Lead approval before outreach
   - Deal approval before client acceptance
   - Audit approval before delivery
   - Delivery plan approval before sending to client

2. All reports flow through the Apex CEO agent

3. The owner remains the final decision-maker

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Create `.env` file from `.env.example` and add your API keys:

```bash
cp .env.example .env
# Edit .env with your:
# - Google Maps API key
# - Twilio credentials
# - OpenAI API key
# - Email credentials
# - Redis URL
```

### Start Redis (for background tasks)

```bash
redis-server
```

### Run Celery worker (in separate terminal)

```bash
celery -A integrations.celery_tasks worker --loglevel=info
```

### Run the FastAPI application

```bash
uvicorn app.main:app --reload
```

### Start React Dashboard (in separate terminal)

```bash
cd dashboard
npm install
npm start
```

The dashboard will open at `http://localhost:3000`

## API Endpoints

### Leads
- `POST /leads/generate` - Generate new leads from Google Maps
- `POST /leads/approve` - Approve leads for outreach
- `GET /leads` - List all leads

### Deals
- `POST /deals/create` - Create a deal for a lead
- `POST /deals/approve` - Approve a deal and create client
- `GET /deals` - List all deals

### Clients
- `GET /clients` - List all clients

### Audits
- `POST /audits/create` - Create a growth audit for a client
- `POST /audits/approve` - Approve audit for delivery
- `GET /audits` - List all audits

### Delivery
- `POST /delivery/create` - Create delivery/implementation plan
- `POST /delivery/approve` - Approve delivery for sending
- `GET /delivery` - List all delivery plans

### Customer Care
- `POST /customers/tickets/create` - Create support ticket
- `GET /tickets` - List all support tickets

### Executive
- `GET /ceo/summary` - Get full company status and summary
- `GET /ceo/voice/summary` - Get voice version of summary
- `POST /ceo/voice/command` - Send a voice command
- `GET /health` - Health check

### Outreach (Background Tasks)
- `POST /outreach/email` - Send outreach email
- `POST /outreach/sms` - Send SMS message
- `POST /outreach/bulk-email` - Send bulk email campaign

## Integration Features

### Google Maps Integration

```python
from integrations.google_maps_service import GoogleMapsService

service = GoogleMapsService()
businesses = service.find_businesses("Austin, TX", "dental clinic")
```

### Email Outreach

```python
from integrations.email_service import EmailService

service = EmailService()
service.send_outreach_email("contact@business.com", "Business Name", "Your message")
```

### SMS & Voice (Twilio)

```python
from integrations.twilio_service import TwilioService

service = TwilioService()
service.send_outreach_sms("+1234567890", "Business Name")
```

### Voice Interface

```python
from integrations.voice_service import VoiceService

service = VoiceService()
audio = service.speak_company_summary(summary_dict)
response = service.get_voice_command_response("Show me the leads")
```

### Background Tasks (Celery)

```python
from integrations.celery_tasks import send_outreach_email_task

# Non-blocking email sending
send_outreach_email_task.delay("email@example.com", "Business", "Message")
```

## Example Workflow

1. Generate leads for Austin, dental category
2. Owner reviews and approves leads via dashboard
3. System sends personalized emails and SMS to approved leads
4. Responses are tracked and logged
5. Create deals for interested leads with pricing
6. Owner approves pricing and deal via dashboard
7. System creates client and starts audit research
8. Auditor generates 3-page audit report
9. Owner reviews and approves audit via dashboard
10. System creates delivery roadmap
11. Owner approves delivery package
12. Delivery sent to client via email
13. Client support tickets handled by Apex Client Care
14. CEO provides real-time status updates
15. Owner can ask voice commands to get company status

## Architecture

```
Apex Intelligence
├── FastAPI Backend (app/)
│   ├── 6 AI Agents
│   ├── Database Models
│   ├── Workflow Engine
│   └── API Endpoints
├── Integrations (integrations/)
│   ├── Google Maps
│   ├── Email Service
│   ├── Twilio (SMS/Voice)
│   ├── Voice Service (OpenAI)
│   ├── Celery (Background Tasks)
│   └── Task Models
├── React Dashboard (dashboard/)
│   ├── Real-time Status
│   ├── Lead Management
│   ├── Deal Tracking
│   ├── Voice Interface
│   └── Analytics
└── Configuration
    ├── .env
    ├── requirements.txt
    └── Redis/Celery Setup
```

## Next Steps

- [ ] Deploy to production (AWS/GCP/Heroku)
- [ ] Add advanced analytics
- [ ] Implement multi-user support
- [ ] Add payment processing
- [ ] Build mobile app
- [ ] Add more integrations (Slack, HubSpot, etc.)
- [ ] Implement AI-powered lead scoring
- [ ] Add CRM features
- [ ] Build reporting system

## License

MIT
