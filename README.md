# AI Integration Mini-Lab: AI Document Assistant

## Project Overview
This project is a Streamlit mini-chatbot that allows a user to upload a small PDF or TXT document and ask questions about its contents. The chatbot uses Google’s Gemini API through the Google Gen AI Python SDK to generate responses based only on the uploaded document.

This mini-lab demonstrates a simple but meaningful AI task: document-based question answering. It also introduces concepts related to retrieval-augmented generation (RAG), since the user provides a source document and the chatbot uses that document as the context for answering questions.

---

## Model Name & Source
- **Model:** Gemini 3 Flash Preview
- **Source:** Google Gemini API
- **SDK:** Google Gen AI Python SDK

---

## Rationale for Model Selection
I selected Gemini 3 Flash Preview because it supports document-based interactions and is designed for fast response times in interactive applications. It is a strong choice for a mini-chatbot because it can process uploaded files and answer user questions in natural language. This makes it suitable for a simple document assistant built with Streamlit. The model also works well for prototyping early RAG-style applications, which connects directly to the larger course project.

---

## How the App Works
1. The user opens the Streamlit app.
2. The user uploads a PDF or TXT document.
3. The app uploads the file to the Gemini API.
4. The user enters a question in the chat box.
5. The chatbot answers using only the uploaded document.
6. If the answer is not in the document, the chatbot says it does not know based on the uploaded document.

---

## API Usage
This project uses the Google Gen AI Python SDK to connect to the Gemini API.

Main steps:
- Create a client using the API key from the `.env` file
- Upload the user’s document with the Files API
- Create a chat session with a system instruction
- Send the uploaded document and user question to the model
- Display the returned response in Streamlit

---

## Installation Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
