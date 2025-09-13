"""
Health check API endpoints.
"""

from fastapi import APIRouter
from typing import Dict, Any

from core.health import health_checker

router = APIRouter(tags=["health"])

@router.get("/health")
async def get_health() -> Dict[str, Any]:
    """Get service health status."""
    return health_checker.get_health_status()
