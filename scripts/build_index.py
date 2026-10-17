import time
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

BASE = Path(__file__).resolve().parent.parent
KB_DIR = BASE / "knowledge_base"
INDEX_DIR = BASE / "index"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def load_documents() -> list[Document]:
    documents = []

    for path in sorted(KB_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue

        lines = text.splitlines()
        title = path.stem
        if lines and lines[0].startswith("# "):
            title = lines[0][2:].strip()

       
           

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": path.name,
                    "title": title,
                    
                },
            )
        )

    return documents


def main() -> None:

    documents = load_documents()
    print(f"Loaded documents: {len(documents)}")


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index


    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)


    build_start = time.time()
    store = FAISS.from_documents(chunks, embeddings)
    build_elapsed = time.time() - build_start

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    store.save_local(str(INDEX_DIR))


    print("\nГотово.")
    print(f"Документы: {len(documents)}")
    print(f"Чанки: {len(chunks)}")
    print(f"Index время: {build_elapsed:.1f} s")



if __name__ == "__main__":
    main()
