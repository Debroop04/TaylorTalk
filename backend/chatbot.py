from agent import get_drive_query
from drive_tool import search_drive
from tools import DriveSearchTool

def chat(user_message):

    query = get_drive_query(user_message)

    print("Generated query:")
    print(query)

    files = DriveSearchTool.invoke(query)

    if not files:
        return "No files found"

    result="Found files:\n\n"

    for file in files:

        result += f"{file['name']}\n"

    return result


message=input("Ask: ")

response=chat(message)

print(response)