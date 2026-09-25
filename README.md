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

### Run the application

```bash
uvicorn app.main:app --reload
```

### Access the API

Open your browser to: `http://localhost:8000/docs`

## API Endpoints

### Leads
- `POST /leads/generate` - Generate new leads
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
- `GET /health` - Health check

## Example Workflow

1. Generate leads for Austin, dental category
2. Owner reviews and approves leads
3. Create deal for approved lead with pricing
4. Owner approves pricing and deal
5. System creates client and starts audit
6. Auditor generates 3-page audit report
7. Owner reviews and approves audit
8. System creates delivery roadmap
9. Owner approves delivery package
10. Delivery sent to client
11. Client support tickets handled by Apex Client Care
12. CEO provides status updates on demand

## Database

Using SQLite by default. Supports any SQLAlchemy-compatible database.

Models:
- Lead
- Deal
- Client
- Audit
- DeliveryPlan
- Ticket
- ApprovalRequest

## Configuration

Create a `.env` file from `.env.example`:

```env
APP_NAME=Apex Intelligence
DATABASE_URL=sqlite:///./apex_intelligence.db
DEBUG=true
OWNER_EMAIL=owner@apexintelligence.com
DEFAULT_MIN_PRICE=500
DEFAULT_MAX_PRICE=5000
```

## Next Steps

- Integrate Google Maps API for real lead generation
- Add web scraping for business research
- Connect real email/SMS outreach tools
- Add voice interface for the CEO agent
- Build React dashboard for owner
- Add background task processing
- Deploy to production

## License

MIT
