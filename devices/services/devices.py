from typing import Optional

from sqlalchemy import ScalarResult
from devices.schemas.devices import DeviceCreate, DeviceUpdate
from devices.schemas.token import TokenData
from sqlmodel import select, Session

from models.devices import DBDevice


def get_all_devices(current_user: TokenData, session: Session) -> ScalarResult[DBDevice]:
    """
    Retrieve all devices for the current user.

    Args:
        current_user (TokenData): The current authenticated user.
        session (Session): The database session.

    Returns:
        list[DBDevice]: A list of devices associated with the current user.
    """

    statement = select(DBDevice).where(DBDevice.user_id == current_user.user_id)
    return session.exec(statement)


def create_device(device: DeviceCreate, session: Session) -> DBDevice:
    """
    Create a new device in the database.

    Args:
        device (DeviceCreate): The device data to create.
        session (Session): The database session.

    Returns:
        DBDevice: The created device.
    """
    db_device = DBDevice(**device.dict())
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device


def update_device(device_id: int, device: DeviceUpdate, session: Session) -> Optional[DBDevice]:
    """
    Update a device by its ID.

    Args:
        device_id (int): The ID of the device to update.
        device (DeviceUpdate): The new device data.
        session (Session): The database session.

    Returns:
        Optional[DBDevice]: The updated device.
    """
    db_device = session.get(DBDevice, device_id)
    if not db_device:
        return None
    for key, value in device.dict().items():
        setattr(db_device, key, value)
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device


def delete_device(device_id: int, session: Session) -> Optional[bool]:
    """
    Delete a device by its ID.

    Args:
        device_id (int): The ID of the device to delete.
        session (Session): The database session.

    Returns:
        Optional[bool]: The deletion status.
    """
    db_device = session.get(DBDevice, device_id)
    if not db_device:
        return None
    session.delete(db_device)
    session.commit()
    return True
