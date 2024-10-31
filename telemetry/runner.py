import uvicorn
import logging
import sys
from core.settings import DEBUG, APP_HOST, APP_PORT

# Configure logging
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting application...")

    uvicorn.run(
        "app:app",
        host=APP_HOST or "0.0.0.0",
        port=APP_PORT or 8000,
        log_level="debug",
        reload=DEBUG,
    )


if __name__ == "__main__":
    main()