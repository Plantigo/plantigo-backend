

from core.settings import DEBUG, APP_HOST, APP_PORT





if __name__ == "__main__":
    import uvicorn


    uvicorn.run(
        "app:app",
        host=APP_HOST or "0.0.0.0",
        port=APP_PORT or 8000,
        log_level="debug",
        reload=DEBUG,
    )
