def generate_mongo_uri(host: str, port: int, user: str = None, password: str = None) -> str:
    """
    Generates a MongoDB URI.

    Parameters:
    - host (str): The hostname of the MongoDB server.
    - port (int): The port of the MongoDB server.
    - user (str): The username for MongoDB authentication (optional).
    - password (str): The password for MongoDB authentication (optional).

    Returns:
    - str: The generated MongoDB URI.
    """
    if user and password:
        uri = f"mongodb://{user}:{password}@{host}:{port}"
    else:
        uri = f"mongodb://{host}:{port}"

    return uri
