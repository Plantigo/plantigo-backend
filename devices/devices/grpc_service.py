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
        """
        Fetches all devices for the given user.

        Args:
            request (GetDevicesRequest): The request object.
            context: The context object providing RPC-specific information.

        Returns:
            GetDevicesResponse: The response object containing the list of devices.
        """
        logger.info(f"Fetching devices for user_id: {context.user_id}")
        user_id = context.user_id

        statement = select(DBDevice).where(DBDevice.user_id == user_id)
        devices = self.db_session.exec(statement)

        response = GetDevicesResponse()

        for device in devices:
            response.devices.add(**json.loads(device.model_dump_json(exclude={'user_id'})))
        return response

    def CreateDevice(self, request, context):
        """
        Creates a new device for the user.

        Args:
            request (CreateDeviceRequest): The request object containing the device details.
            context: The context object providing RPC-specific information.

        Returns:
            CreateDeviceResponse: The response object containing the created device details.

        Raises:
            grpc.StatusCode.INVALID_ARGUMENT: If required arguments are missing.
            grpc.StatusCode.ALREADY_EXISTS: If a device with the same MAC address already exists.
        """
        if not request.name or not request.mac_address:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Name and MAC address are required.")
            return CreateDeviceResponse()

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

            response = CreateDeviceResponse(
                device=json.loads(new_device.model_dump_json(exclude={'user_id'}))
            )
            return response
        except IntegrityError as e:
            self.db_session.rollback()
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Device with the same MAC address already exists.")
            logger.error(f"Error creating device: {e}")
            return CreateDeviceResponse()

    def __del__(self):
        self.db_session.close()
