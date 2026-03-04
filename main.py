from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import database
import providers

app = FastAPI(title="CloudBridge Manager")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(database.get_db)):
    """Renders the main dashboard."""
    # 1. Fetch connected accounts from DB
    accounts = db.query(database.CloudAccount).all()
    
    all_files = []
    connected_providers = []

    # 2. Fetch files from each connected cloud using our OOP classes
    for acc in accounts:
        connected_providers.append(acc.provider_name)
        try:
            provider = providers.get_provider_instance(acc.provider_name, acc.access_token)
            files = provider.get_files()
            all_files.extend(files)
        except Exception as e:
            print(f"Error loading {acc.provider_name}: {e}")

    # 3. Send data to the HTML template
    return templates.TemplateResponse("index.html", {
        "request": request,
        "files": all_files,
        "connected": connected_providers
    })

@app.post("/link")
async def link_account(provider: str = Form(...), db: Session = Depends(database.get_db)):
    """Simulates the OAuth linking process."""
    # Check if already linked
    existing = db.query(database.CloudAccount).filter_by(provider_name=provider).first()
    if not existing:
        # In a real app, this redirects to Google/Dropbox OAuth URLs.
        # Here, we instantly save a mock token to the DB.
        new_account = database.CloudAccount(
            provider_name=provider, 
            access_token=f"mock_token_{provider}_892374"
        )
        db.add(new_account)
        db.commit()
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/unlink")
async def unlink_account(provider: str = Form(...), db: Session = Depends(database.get_db)):
    """Removes a cloud provider from the database."""
    account = db.query(database.CloudAccount).filter_by(provider_name=provider).first()
    if account:
        db.delete(account)
        db.commit()
    return RedirectResponse(url="/", status_code=303)