from fastapi import APIRouter
from src.infrastructure.dependencies.database import get_database

router = APIRouter()


@router.get("/health")
async def health_check():
    try:
        db = await get_database()
        # Test database connection
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
