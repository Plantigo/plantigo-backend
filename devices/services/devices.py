from sqlalchemy import ScalarResult
from devices.schemas.devices import DeviceCreate
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
