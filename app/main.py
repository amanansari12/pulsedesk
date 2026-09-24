from fastapi import FastAPI

from app.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health_check():
    return {"status": "ok", "Environment": settings.environment}


# if __name__ == "__main__":
#     pass
