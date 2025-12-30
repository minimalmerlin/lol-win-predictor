"""
Backend Server Runner
Run from project root: python backend/run.py
Or from backend dir: python run.py
"""

import uvicorn
import sys
from pathlib import Path

# Add parent directory to path (for accessing models/ and data/)
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    print(f"🚀 Starting LoL Coach Backend on port {settings.PORT}")
    print(f"📍 Environment: {settings.ENV}")
    print(f"🔄 Auto-reload: {not settings.IS_PRODUCTION}")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=not settings.IS_PRODUCTION,
        log_level="info"
    )
