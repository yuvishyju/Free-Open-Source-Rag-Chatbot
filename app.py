import streamlit as st
import os
import time
import base64 
import requests
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
HISTORY_API_URL="http://127.0.0.1:8000"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)
# -----------------------------
# SAVE SEARCH HISTORY
# -----------------------------
def save_search_history(question):

    clean_query = question.strip()
    if not clean_query:
        return

    # Try saving via FastAPI backend
    try:
        response = requests.post(
            f"{HISTORY_API_URL}/history",
            json={"query": clean_query},
            timeout=1
        )
        if response.status_code == 200:
            return
    except requests.exceptions.RequestException:
        pass

    # Direct SQLite fallback if FastAPI backend is not running
    try:
        from backend.database import SessionLocal, SearchHistory
        from datetime import datetime

        db = SessionLocal()

        existing = (
            db.query(SearchHistory)
            .filter(SearchHistory.query == clean_query)
            .first()
        )

        if existing:
            existing.timestamp = datetime.now()
        else:
            history = SearchHistory(query=clean_query)
            db.add(history)

        db.commit()
        db.close()

    except Exception as e:
        print(f"Could not save search history: {e}")


# -----------------------------
# GET RECENT SEARCH HISTORY
# -----------------------------
def get_search_history():

    # Try loading from FastAPI backend
    try:
        response = requests.get(
            f"{HISTORY_API_URL}/history",
            timeout=1
        )
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass

    # Direct SQLite fallback if FastAPI backend is not running
    try:
        from backend.database import SessionLocal, SearchHistory

        db = SessionLocal()

        history = (
            db.query(SearchHistory)
            .order_by(SearchHistory.timestamp.desc())
            .limit(10)
            .all()
        )

        db.close()

        return [
            {
                "id": item.id,
                "query": item.query,
                "timestamp": item.timestamp
            }
            for item in history
        ]

    except Exception as e:
        print(f"Could not load search history: {e}")
        return []


# -----------------------------
# DELETE SINGLE SEARCH HISTORY ITEM
# -----------------------------
def delete_history_item(item_id):

    # Try deleting via FastAPI backend
    try:
        response = requests.delete(
            f"{HISTORY_API_URL}/history/{item_id}",
            timeout=1
        )
        if response.status_code == 200:
            return
    except requests.exceptions.RequestException:
        pass

    # Direct SQLite fallback if FastAPI backend is not running
    try:
        from backend.database import SessionLocal, SearchHistory

        db = SessionLocal()

        item = (
            db.query(SearchHistory)
            .filter(SearchHistory.id == item_id)
            .first()
        )

        if item:
            db.delete(item)
            db.commit()

        db.close()

    except Exception as e:
        print(f"Could not delete search history: {e}")


# -----------------------------
# CLEAR ALL SEARCH HISTORY
# -----------------------------
def clear_all_search_history():

    # Try clearing via FastAPI backend
    try:
        response = requests.delete(
            f"{HISTORY_API_URL}/history",
            timeout=1
        )
        if response.status_code == 200:
            return
    except requests.exceptions.RequestException:
        pass

    # Direct SQLite fallback if FastAPI backend is not running
    try:
        from backend.database import SessionLocal, SearchHistory

        db = SessionLocal()

        db.query(SearchHistory).delete()

        db.commit()

        db.close()

    except Exception as e:
        print(f"Could not clear search history: {e}")


# -----------------------------
# RENDER SIDEBAR SEARCH HISTORY
# -----------------------------
def render_sidebar_history(placeholder):

    history = get_search_history()

    with placeholder.container():

        if history:

            # Option to clear all search history at once
            if st.button("🗑️ Clear All History", key="clear_all_history_btn", use_container_width=True):
                clear_all_search_history()
                st.rerun()

            # Option to selectively click or delete individual searches
            for item in history:

                col1, col2 = st.columns([4, 1])

                with col1:
                    if st.button(
                        f"🔹 {item['query']}",
                        key=f"history_{item['id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_query = item["query"]
                        st.rerun()

                with col2:
                    if st.button(
                        "❌",
                        key=f"delete_{item['id']}",
                        help="Delete this search"
                    ):
                        delete_history_item(item["id"])
                        st.rerun()

        else:

            st.caption(
                "No recent searches."
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

# -----------------------------
# RECENT SEARCH HISTORY
# -----------------------------

st.sidebar.divider()

st.sidebar.header("🕘 Recent Searches")

history_placeholder = st.sidebar.empty()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

# -----------------------------
# CHAT INPUT
# -----------------------------

# Always render chat_input so Streamlit's widget tree stays consistent.
# History queries are injected via session_state and processed on next rerun.
question = st.chat_input(
    "Ask a question about your documents..."
)

# If a history item was clicked, override the question from session_state.
if "selected_query" in st.session_state:
    question = st.session_state.pop("selected_query")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    save_search_history(question)

    render_sidebar_history(history_placeholder)

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

                filename = metadata.get("filename", "Unknown document")
                page_number = metadata.get("page_number", None)

                if page_number is not None:
                    st.write(
                        f"📄 {filename} — Page {page_number}"
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

else:

    render_sidebar_history(history_placeholder)