import grpc
from sqlmodel import select, Session
from sqlalchemy.exc import IntegrityError
from devices.devices_pb2_grpc import DeviceServiceServicer
from devices.devices_pb2 import GetDevicesResponse, CreateDeviceResponse  # noqa
from devices.models import DBDevice
from core.database import engine
import logging
import json

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
            response.devices.add(**json.loads(device.model_dump_json(exclude={'user_id'})))
        return response

    def CreateDevice(self, request, context):
        logger.info(f"Creating device for user_id: {context.user_id}")
        user_id = context.user_id

        new_device = DBDevice(
            user_id=user_id,
            mac_address=request.mac_address,
            name=request.name,
        )

        try:
            self.db_session.add(new_device)
            self.db_session.commit()
            self.db_session.refresh(new_device)

            response = CreateDeviceResponse()
            response.device.id = str(new_device.id)
            response.device.name = new_device.name
            response.device.mac_address = new_device.mac_address
            response.device.is_active = new_device.is_active
            # response.device.last_read = new_device.last_read
            return response
        except IntegrityError as e:
            self.db_session.rollback()
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Device with the same MAC address already exists.")
            logger.error(f"Error creating device: {e}")
            return CreateDeviceResponse()

    def __del__(self):
        self.db_session.close()
