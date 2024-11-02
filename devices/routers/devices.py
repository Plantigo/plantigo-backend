from fastapi import APIRouter, Depends
from devices.schemas.devices import DeviceCreate, Device
from devices.services.devices import create_device, get_all_devices
from devices.core.database import get_session
from devices.core.dependencies import get_current_user
from devices.schemas.token import TokenData
from sqlmodel import Session

router = APIRouter(
    prefix="/devices",
)


@router.get("/")
def read_all(current_user: TokenData = Depends(get_current_user),
             db: Session = Depends(get_session)) -> list[Device]:
    """
    Retrieve all devices for the current authenticated user.

    Args:
        current_user (TokenData): The current authenticated user.
        db (Session): The database session.

    Returns:
        list[Device]: A list of devices associated with the current user.
    """
    response = get_all_devices(current_user, db)
    return [Device(**device.dict()) for device in response]


@router.post("/")
def create(device: DeviceCreate, db: Session = Depends(get_session)) -> Device:
    """
    Create a new device.

    Args:
        device (DeviceCreate): The device data to create.
        db (Session): The database session.

    Returns:
        Device: The created device.
    """
    response = create_device(device, db)
    return Device(**response.dict())
