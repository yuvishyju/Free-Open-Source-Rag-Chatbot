import streamlit as st
import os
import time
import base64 

from modules.indexer import DocumentIndexer
from modules.rag_engine import RAGEngine


st.set_page_config(
    page_title="Free RAG Chatbot",
    page_icon="📚",
    layout="wide"
)
# -----------------------------
# LOCAL BACKGROUND FUNCTION
# -----------------------------
# def set_local_background(image_path):
#     """Sets a local image as the app background with an 85% dark readability overlay."""
#     if not os.path.exists(image_path):
#         return  # Gracefully skip if image file is not found yet

#     with open(image_path, "rb") as file:
#         encoded_string = base64.b64encode(file.read()).decode()

#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("data:image/png;base64,{encoded_string}");
#             background-size: cover;
#             background-position: center;
#             background-attachment: fixed;
#         }}
#         /* Modern card styling for chat messages */
#         [data-testid="stChatMessage"] {{
#             background-color: rgba(255, 255, 255, 0.05);
#             border-radius: 12px;
#             padding: 14px;
#             margin-bottom: 12px;
#             border: 1px solid rgba(255, 255, 255, 0.1);
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # Apply your local image (adjust filename if you use .png):
# set_local_background("assets/cute.jpg")

UPLOAD_FOLDER = "data/uploaded_documents"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("📚 Free RAG Document Chatbot")

st.write(
    "Ask questions about your uploaded documents "
    "using a local RAG pipeline."
)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("📄 Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)


if uploaded_files:

    for uploaded_file in uploaded_files:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as file:
            file.write(
                uploaded_file.getbuffer()
            )

if uploaded_files:

    if st.sidebar.button("🔄 Process Documents"):

        indexer = DocumentIndexer()

        progress = st.sidebar.empty()

        for uploaded_file in uploaded_files:

            file_path = os.path.join(
                UPLOAD_FOLDER,
                uploaded_file.name
            )

            progress.write(
                f"Processing {uploaded_file.name}..."
            )

            try:

                chunk_count = indexer.index_document(
                    file_path,
                    uploaded_file.name
                )

                st.success(
                    f"✅ {uploaded_file.name} "
                    f"indexed successfully "
                    f"({chunk_count} chunks)"
                )

            except Exception as e:

                st.error(
                    f"❌ Error processing "
                    f"{uploaded_file.name}: {e}"
                )

        progress.empty()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

question = st.chat_input(
    "Ask a question about your documents..."
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        answer_placeholder = st.empty()

        with st.spinner("Searching documents..."):
            start_time = time.time()

            rag = RAGEngine()

            result = rag.ask(question)

            answer = result["answer"]

            end_time = time.time()

            response_time = end_time - start_time

        answer_placeholder.markdown(answer)
        st.caption(
            f"⏱️ Response time: {response_time:.2f} seconds"
        )
        # -------------------------
        # SOURCES
        # -------------------------
        if result["results"] is not None:
            metadatas = result["results"]["metadatas"][0]
            distances = result["results"]["distances"][0]

            for i in range(len(metadatas)):

                metadata = metadatas[i]

                filename = metadata["filename"]
                page = metadata["page_number"]

                if page is not None:
                    st.write(
                        f"📄 {filename} — Page {page}"
                    )

                else:
                    st.write(
                        f"📄 {filename}"
                    )

            # -------------------------
            # RETRIEVED CHUNKS
            # -------------------------

            with st.expander("🔍 View Retrieved Passages"):

                documents = result["results"]["documents"][0]
                distances = result["results"]["distances"][0]

                for i in range(len(documents)):

                    st.markdown(
                        f"**Retrieved Chunk {i + 1}**"
                    )

                    st.write(
                        f"Similarity distance: "
                        f"{distances[i]:.4f}"
                    )

                    st.write(
                        documents[i]
                    )

                    st.divider()

        else:

            st.info(
                "🔎 No sufficiently similar information "
                "was found in the uploaded documents."
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })