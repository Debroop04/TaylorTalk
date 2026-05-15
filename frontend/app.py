import streamlit as st

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from google.oauth2 import service_account
from googleapiclient.discovery import build


# -----------------------------
# LOAD ENV
# -----------------------------

load_dotenv()


# -----------------------------
# STREAMLIT CONFIG
# -----------------------------

st.set_page_config(
    page_title="TailorTalk AI",
    page_icon="🤖"
)

st.title("🤖 TailorTalk AI")

st.write(
    "Search your Google Drive using natural language."
)


# -----------------------------
# GOOGLE DRIVE SETUP
# -----------------------------

SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    'service_account.json',
    scopes=SCOPES
)

service = build(
    'drive',
    'v3',
    credentials=credentials
)


def search_drive(query):

    results = service.files().list(
        q=query,
        fields="files(id,name,mimeType)"
    ).execute()

    return results.get('files', [])


# -----------------------------
# LLM SETUP
# -----------------------------

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


# -----------------------------
# UI
# -----------------------------

with st.form("search_form"):

    user_input = st.text_input(
        "Ask something",
        placeholder="Examples: Find reports, Find spreadsheets, Find videos"
    )

    submitted = st.form_submit_button("Search")


if submitted and user_input:

    query = get_drive_query(user_input)

    st.subheader("Generated Query")

    st.code(query)

    files = search_drive(query)

    st.subheader("Results")

    if files:

        for file in files:

            file_id = file["id"]

            mime_type = file["mimeType"]

            if "google-apps.spreadsheet" in mime_type:

                link = f"https://docs.google.com/spreadsheets/d/{file_id}"

            elif "spreadsheetml" in mime_type:

                link = f"https://drive.google.com/file/d/{file_id}/view"

            elif "document" in mime_type:

                link = f"https://docs.google.com/document/d/{file_id}"

            elif "presentation" in mime_type:

                link = f"https://docs.google.com/presentation/d/{file_id}"

            else:

                link = f"https://drive.google.com/file/d/{file_id}/view"

            st.markdown(
                f"📄 [{file['name']}]({link})"
            )

    else:

        st.warning("No files found")