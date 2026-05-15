import streamlit as st
import requests

st.set_page_config(
    page_title="TailorTalk",
    page_icon="🤖"
)

st.title("🤖 TailorTalk AI")

st.write(
    "Search your Google Drive using natural language.  \n by Debroop"
)

with st.form("search_form"):

    user_input = st.text_input(
        "Ask something",
        placeholder="Examples: Find reports, Find spreadsheets, Find png images"
    )

    submitted = st.form_submit_button("Search")

if submitted and user_input:

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={
            "message": user_input
        }
    )

    data = response.json()

    st.subheader("Generated Query")

    st.code(data["query"])

    st.subheader("Results")

    if "files" in data:

        for file in data["files"]:

            file_id = file["id"]

            mime_type = file["mimeType"]

            if "spreadsheet" in mime_type:

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