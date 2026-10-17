"""
Пример поиска по индексу FAISS.

Запуск:
    python3 scripts/query_index.py "Who is Lyra Vale?"
"""

import sys
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

BASE = Path(__file__).resolve().parent.parent
INDEX_DIR = BASE / "index"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main() -> None:
    if len(sys.argv) < 2:
        print('Использование: python3 scripts/query_index.py "текст запроса"')
        return

    query = sys.argv[1]

    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    store = FAISS.load_local(
        str(INDEX_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    results = store.similarity_search(query, k=3)

    print(f"\nQuery: {query}\n")
    for i, doc in enumerate(results, start=1):
        print(f"Результат #{i}")
        print(f"Заголовок: {doc.metadata.get('title')}")
        print(f"Источник: {doc.metadata.get('source')}")
        print(doc.page_content[:700])
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()
