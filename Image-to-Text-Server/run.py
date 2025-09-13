"""
Application runner script.
"""

import uvicorn
from config.constants import DEFAULT_HOST, DEFAULT_PORT

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        log_level="info",
        reload=False
    )