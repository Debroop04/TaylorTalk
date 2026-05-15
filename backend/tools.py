from langchain.tools import tool
from drive_tool import search_drive


@tool
def DriveSearchTool(query: str):

    """
    Search Google Drive files using a Google Drive API q parameter.
    """

    return search_drive(query)