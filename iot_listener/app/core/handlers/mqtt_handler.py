import logging
import re

from app.core.interfaces.db import DatabaseInterface


class TelemetryHandler:
    def __init__(self, db: DatabaseInterface, topic_handlers: dict[str, callable]):
        self.db = db
        self.logger = logging.getLogger("TelemetryHandler")
        self.handlers = self._compile_handlers(topic_handlers)

    @staticmethod
    def _compile_handlers(topic_handlers: dict) -> list:

        compiled = []
        for topic_pattern, handler in topic_handlers.items():
            pattern = topic_pattern.replace('+', r'([^/]+)').replace('#', r'.*')
            compiled.append((re.compile(f"^{pattern}$"), handler))
        return compiled

    def parse_and_dispatch(self, topic: str, payload: dict):
        for pattern, handler in self.handlers:
            match = pattern.match(topic)
            if match:
                variables = match.groups()
                self.logger.info(f"Matched topic: {topic} with handler: {handler.__class__.__name__}")
                handler.handle(topic, variables, payload)
                return

        self.logger.warning(f"No handler found for topic: {topic}")
