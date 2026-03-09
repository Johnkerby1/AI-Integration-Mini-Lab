import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="AI Document Assistant", page_icon="📄")
st.title("AI Document Assistant")
st.write("Upload a PDF or TXT file and ask questions about it.")

if not api_key:
    st.error("GOOGLE_API_KEY not found. Add it to your .env file.")
    st.stop()

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Setup")

    uploaded_file_ui = st.file_uploader(
        "Upload your document",
        type=["pdf", "txt"]
    )

    if uploaded_file_ui is not None:
        # Reset state if a new file is uploaded
        if (
            "uploaded_filename" not in st.session_state
            or st.session_state.uploaded_filename != uploaded_file_ui.name
        ):
            st.session_state.uploaded_filename = uploaded_file_ui.name
            st.session_state.messages = []
            st.session_state.pop("doc_ref", None)
            st.session_state.pop("chat", None)

        if "doc_ref" not in st.session_state:
            with st.spinner("Uploading document..."):
                mime_type = uploaded_file_ui.type
                suffix = os.path.splitext(uploaded_file_ui.name)[1] or ".txt"

                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file_ui.getbuffer())
                    temp_path = tmp.name

                try:
                    doc_ref = st.session_state.client.files.upload(
                        file=temp_path,
                        config={"mime_type": mime_type}
                    )
                    st.session_state.doc_ref = doc_ref

                    st.session_state.chat = st.session_state.client.chats.create(
                        model="gemini-3-flash-preview",
                        config=types.GenerateContentConfig(
                            system_instruction=(
                                "You are a helpful document assistant. "
                                "Answer questions ONLY using the uploaded document. "
                                "If the answer is not in the document, say: "
                                "'I don't know based on the uploaded document.'"
                            )
                        )
                    )

                    st.success("Document uploaded successfully.")

                except Exception as e:
                    st.error(f"Upload failed: {e}")

                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask a question about the uploaded document:")

if prompt:
    if "chat" not in st.session_state or "doc_ref" not in st.session_state:
        st.error("Please upload a document first.")
        st.stop()

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(
                message=[st.session_state.doc_ref, prompt]
            )
            answer = response.text if hasattr(response, "text") else str(response)
            st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        st.error(f"Error generating response: {e}")