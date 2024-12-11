from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from pathlib import Path
from urllib.parse import unquote
import shutil
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Create necessary directories and copy static files
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
ICON_DIR = STATIC_DIR / "icon"
SCHOOL_ICON_DIR = STATIC_DIR / "school_icon"

# Ensure directories exist
STATIC_DIR.mkdir(parents=True, exist_ok=True)
ICON_DIR.mkdir(parents=True, exist_ok=True)
SCHOOL_ICON_DIR.mkdir(parents=True, exist_ok=True)

# Copy static files from app directory if they don't exist in static
APP_STATIC = BASE_DIR / "app" / "static"
if APP_STATIC.exists():
    for item in APP_STATIC.glob("**/*"):
        if item.is_file():
            relative_path = item.relative_to(APP_STATIC)
            target_path = STATIC_DIR / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if not target_path.exists():
                shutil.copy2(item, target_path)

# Mount static files directory
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ontrack-zh.onrender.com",
        "https://ontrack-zh-front.onrender.com",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file handlers
@app.get("/api/survey/icon/{icon_id}")
async def get_icon(icon_id: str):
    try:
        icon_path = ICON_DIR / f"{icon_id}.png"
        print(f"Looking for icon at: {icon_path}")
        if icon_path.exists():
            return FileResponse(str(icon_path))
        default_icon = ICON_DIR / "default.png"
        if default_icon.exists():
            print("Using default icon")
            return FileResponse(str(default_icon))
        raise HTTPException(status_code=404, detail="Icon not found")
    except Exception as e:
        print(f"Error serving icon: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/survey/school-icon/{school}")
async def get_school_icon(school: str):
    try:
        school_name = unquote(school)
        icon_path = SCHOOL_ICON_DIR / f"{school_name}.png"
        print(f"Looking for school icon at: {icon_path}")
        if icon_path.exists():
            return FileResponse(str(icon_path))
        default_icon = SCHOOL_ICON_DIR / "default.png"
        if default_icon.exists():
            print("Using default school icon")
            return FileResponse(str(default_icon))
        raise HTTPException(status_code=404, detail="School icon not found")
    except Exception as e:
        print(f"Error serving school icon: {e}")
        raise HTTPException(status_code=404, detail=str(e))

# Root route
@app.get("/")
async def root():
    return {
        "message": "Welcome to OnTrack API",
        "version": "2.0",
        "endpoints": {
            "survey": "/api/survey/questions",
            "submit": "/api/survey/submit",
            "icons": "/api/survey/icon/{icon_id}",
            "school_icons": "/api/survey/school-icon/{school}"
        }
    }

# Include routers
from app.routers import survey
app.include_router(
    survey.router,
    prefix="/api/survey",
    tags=["survey"]
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "static_dirs": {
            "static": str(STATIC_DIR.exists()),
            "icon": str(ICON_DIR.exists()),
            "school_icon": str(SCHOOL_ICON_DIR.exists())
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
