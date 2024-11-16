import logging
import sys

from core.logging import configure_logging
from core.server import serve
from core.settings import settings

if __name__ == "__main__":
    logger = configure_logging()

    try:
        logger.info("Starting gRPC server...")
        serve()
    except Exception as e:
        logger.critical(f"Failed to start the gRPC server: {e}", exc_info=True)
        sys.exit(1)
