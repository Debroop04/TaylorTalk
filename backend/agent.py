from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv("../.env")

llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You convert user requests into Google Drive API q parameters.

Return ONLY the query.
No explanations.
No markdown.
No extra text.

Examples:

find reports
name contains 'report'

find reports uploaded after 10 AM
name contains 'report' and modifiedTime > '2025-05-15T10:00:00'

find reports from yesterday
name contains 'report' and modifiedTime > '2025-05-14T00:00:00'

find PDFs uploaded today
mimeType='application/pdf' and modifiedTime > '2025-05-15T00:00:00'

find pdf reports
name contains 'report' and mimeType='application/pdf'

find spreadsheets
mimeType contains 'spreadsheet'

find png images
mimeType='image/png'

find images
mimeType contains 'image/'
                                          
find videos
mimeType contains 'video/'

User request:
{input}
""")

chain = prompt | llm


def get_drive_query(user_input):

    response = chain.invoke(
        {"input": user_input}
    )

    query = response.content.strip()

    query = query.split("\n")[0]

    return query