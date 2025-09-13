"""
Health check API endpoints.
"""
from fastapi import APIRouter
from typing import Dict, Any

from core.health import health_checker

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint providing system status and configuration."""
    return health_checker.get_health_status()
