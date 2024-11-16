

class TelemetryDataDispatcherService:
    def __init__(self, config: Config, telemetry_data: TelemetryData):
        self.config = config
        self.telemetry_data = telemetry_data

    async def dispatch(self, telemetry_data: dict):
        # Dispatch the telemetry data to the appropriate handler
        handler = self.config.get_handler(telemetry_data)
        await handler.handle(telemetry_data, self.telemetry_data)
