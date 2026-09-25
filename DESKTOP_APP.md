# Apex Intelligence - Desktop App

## Simple Windows/Mac/Linux Desktop Application

This is a **desktop GUI app** that controls the entire Apex Intelligence private server.

### Installation (Windows)

1. Open PowerShell in the `apex-intelligence` folder
2. Run:
   ```powershell
   python -m pip install -r app_requirements.txt
   ```
3. Then run:
   ```powershell
   python apex_app.py
   ```

### Installation (Mac/Linux)

1. Open Terminal in the `apex-intelligence` folder
2. Run:
   ```bash
   chmod +x run_app.sh
   ./run_app.sh
   ```
3. Then run:
   ```bash
   python3 apex_app.py
   ```

### What the App Does

The desktop app has 4 tabs:

#### 1. **Dashboard**
- Start/Stop/Restart the server with one click
- View real-time logs
- See server status
- Open API docs

#### 2. **API Tester**
- Test API endpoints
- View responses in JSON format
- No command line needed

#### 3. **Lead Generator**
- Generate leads by city and category
- Set number of leads to find
- View results instantly

#### 4. **Services**
- Quick links to all services
- API Docs
- Supervisor
- Celery Flower
- CEO Summary

### Features

✅ Start/Stop/Restart server with buttons
✅ Real-time logs and status
✅ Automatic Docker management
✅ Test API without terminal
✅ Generate leads with a form
✅ Quick links to all services
✅ Clean, simple GUI
✅ Works on Windows, Mac, Linux

### System Requirements

- Python 3.8+
- Docker Desktop installed
- 4GB+ RAM
- 10GB+ free disk space

### Troubleshooting

If the app won't start:

1. Make sure Docker Desktop is running
2. Run: `docker ps` in PowerShell to verify
3. If Docker isn't installed, download from: https://www.docker.com/products/docker-desktop

If you get a "module not found" error:

```powershell
python -m pip install PyQt6 requests
```

Then try again:

```powershell
python apex_app.py
```

### That's It!

You now have a complete GUI app to manage your Apex Intelligence server.
