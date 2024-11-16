from sqlmodel import select, Session
from devices.devices_pb2_grpc import DeviceServiceServicer
from devices.devices_pb2 import GetDevicesResponse  # noqa
from devices.models import DBDevice
from core.settings import settings
from sqlmodel import create_engine
import logging

engine = create_engine(settings.database_url, echo=True)

logger = logging.getLogger(__name__)


class DeviceGRPCService(DeviceServiceServicer):
    def __init__(self):
        self.db_session = Session(engine)

    def GetAllDevices(self, request, context):
        logger.info(f"Fetching devices for user_id: {context.user_id}")
        user_id = context.user_id

        statement = select(DBDevice).where(DBDevice.user_id == user_id)
        devices = self.db_session.exec(statement)

        response = GetDevicesResponse()

        for device in devices:
            response.devices.add(
                id=str(device.id),
                name=device.name,
                mac_address=device.mac_address
            )
        return response

    def __del__(self):
        self.db_session.close()
