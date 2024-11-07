from core.settings import settings

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.app_host or "0.0.0.0",
        port=settings.app_port or 8000,
        log_level="debug",
        reload=settings.debug,
    )
