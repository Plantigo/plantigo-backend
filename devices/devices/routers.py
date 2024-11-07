from fastapi import APIRouter, Depends, HTTPException
from devices.schemas import DeviceCreate, Device, DeviceUpdate
from devices.services import create_device, get_all_devices, update_device, delete_device
from core.database import get_session
from core.dependencies import get_current_user
from auth_token.schemas import TokenData
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
def create(
        device: DeviceCreate,
        current_user: TokenData = Depends(get_current_user),
        db: Session = Depends(get_session)
) -> Device:
    """
        Create a new device.

        Args:
            device (DeviceCreate): The device data to create.
            current_user (TokenData): The current authenticated user.
            db (Session): The database session.

        Returns:
            Device: The created device.
        """
    response = create_device(device, current_user, db)
    print(response)
    return Device(**response.dict())


@router.put("/{device_id}")
def update(device_id: int, device_data: DeviceUpdate, db: Session = Depends(get_session)) -> Device:
    """
    Update a device by its ID.

    Args:
        device_id (int): The ID of the device to update.
        device_data (DeviceUpdate): The new device data.
        db (Session): The database session.

    Returns:
        Device: The updated device.
    """
    db_device = update_device(device_id, device_data, db)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return Device(**db_device.dict())


@router.delete("/{device_id}")
def delete(device_id: int, db: Session = Depends(get_session)) -> dict:
    """
    Delete a device by its ID.

    Args:
        device_id (int): The ID of the device to delete.
        db (Session): The database session.

    Returns:
        dict: A message indicating the deletion status.
    """
    delete_status = delete_device(device_id, db)
    if not delete_status:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}
