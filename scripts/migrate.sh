#!/bin/bash

# Apex Intelligence - Database Migrations

echo "🔄 Running database migrations..."

# Create tables
python -c "
from app.database import engine, Base
from app.models import *
from integrations.models import *

print('📋 Creating database tables...')
Base.metadata.create_all(bind=engine)
print('✅ Database initialized successfully')
"

echo "✅ Migrations complete"
