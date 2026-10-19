"""Консольный REPL-интерфейс локального RAG-бота.

Запуск:
    python -m rag.bot
"""

from rag.pipeline import RAGPipeline


def main() -> None:
    print("Локальный RAG-бот по knowledge base.")
    print("Введите вопрос. Пустая строка — выход.")

    pipeline = RAGPipeline()

    while True:
        try:
            question = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not question:
            break

        result = pipeline.answer(question)

        print(f"\n{result['answer']}")
        print(f"\nИсточники: {', '.join(result['sources'])}")

    print("\nЗавершение работы.")


if __name__ == "__main__":
    main()
