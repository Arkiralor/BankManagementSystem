# Desc: Boilerplate code for validating request body against request schema
from core import logger

def validate_request_body(request_data: dict, request_schema) -> bool:
    """
    Validates the request body against the request schema.
    """
    try:
        deserialized = request_schema(data=request_data)
    except Exception as ex:
        logger.warn(f"ERROR: {ex}")
        return False
    
    if not deserialized.is_valid():
        logger.warn(f"ERROR: {deserialized.errors}")
        return False
    
    return True