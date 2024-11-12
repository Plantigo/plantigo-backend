from sqlmodel import select, Session
from devices.devices_pb2_grpc import DeviceServiceServicer
from devices.devices_pb2 import GetDevicesResponse  # noqa
from devices.models import DBDevice
from core.settings import settings
from sqlmodel import create_engine

engine = create_engine(settings.database_url, echo=True)


class DeviceGRPCService(DeviceServiceServicer):
    def __init__(self):
        self.db_session = Session(engine)

    def GetAllDevices(self, request, context):
        user_id = request.user_id

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
