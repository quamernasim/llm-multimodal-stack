"""
Application runner for Wan Image-to-Video service.
"""

import uvicorn
from config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level=settings.log_level.lower()
    )
