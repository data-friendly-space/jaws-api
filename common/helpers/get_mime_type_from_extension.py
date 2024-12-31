"""Contains a method for getting a mimetype from a file extension"""
import mimetypes

def get_mimetype_from_extension(filename: str) -> str:
    """Retrieve a mimetype from a given filename"""
    mimetype, _ = mimetypes.guess_type(filename)
    return mimetype
