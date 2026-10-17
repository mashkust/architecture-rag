# Задание 1. Исследование моделей и инфраструктуры

## Контекст задачи

**QuantumForge Software** — европейская компания, работающая с внутренней технической документацией, архитектурными решениями, регламентами и материалами клиентских проектов. Для такого кейса важно учитывать не только качество ответов, но и конфиденциальность данных.

Основные пользователи RAG-бота:

- разработчики;
- служба поддержки;
- менеджеры и аналитики;
- новые сотрудники.

---

## 1. Сравнение LLM-моделей

### Облачные модели: OpenAI / YandexGPT

**Плюсы:**

- высокое качество ответов;
- быстрый запуск;
- не требуют собственной инфраструктуры.

**Минусы:**

- данные передаются внешнему провайдеру;
- есть риски для конфиденциальных документов;
- стоимость растёт вместе с числом запросов.

**Вывод:** подходят для MVP, но не являются лучшим основным вариантом для корпоративной базы знаний с чувствительными данными.

### Локальные модели: Hugging Face

**Плюсы:**

- данные остаются внутри инфраструктуры компании;
- лучше соответствуют требованиям безопасности и GDPR;
- нет зависимости от внешнего API.

**Минусы:**

- сложнее развернуть и поддерживать;
- нужны собственные вычислительные ресурсы.

**Вывод:** для QuantumForge Software предпочтительнее локальная LLM.

---

## 2. Сравнение моделей эмбеддингов

### OpenAI Embeddings

**Плюсы:**

- хорошее качество;
- простой API.

**Минусы:**

- весь индексируемый текст отправляется внешнему провайдеру;
- регулярные расходы.

### Sentence-Transformers

**Плюсы:**

- локальная индексация;
- документы не передаются наружу;
- низкая стоимость эксплуатации;
- удобно для регулярного обновления индекса.

**Минусы:**

- качество зависит от выбора модели;
- индексация требует локальных ресурсов.

**Вывод:** для проекта лучше использовать локальные эмбеддинги Sentence-Transformers.

---

## 3. Сравнение FAISS и ChromaDB

### FAISS

**Плюсы:**

- очень быстрый поиск;
- простота;
- хорошо подходит для MVP и прототипов.

**Минусы:**

- это **библиотека**, а не полноценная векторная БД;
- менее удобна для работы с метаданными и обновлениями.

### ChromaDB

**Плюсы:**

- хранит векторы и метаданные;
- поддерживает персистентность;
- удобнее для растущей базы знаний и инкрементальных обновлений.

**Минусы:**

- немного сложнее в настройке, чем FAISS.

**Вывод:** для корпоративного решения лучше выбрать ChromaDB, а FAISS использовать на этапе прототипирования.

---

## 4. Рекомендуемая конфигурация сервера

Для локального RAG-бота:

- CPU: 8–16 vCPU
- RAM: 32–64 GB
- GPU: 1 GPU с 24+ GB VRAM
- Disk: от 100 GB SSD

Такой конфигурации достаточно для локальной LLM, локальных эмбеддингов и хранения индекса.

---

## Итог

- локальная LLM (Hugging Face);
- локальные эмбеддинги Sentence-Transformers;
- ChromaDB как основная векторная БД. FAISS будем использовать для локального прототипирования на этапе разработки.

# Задание 2. Подготовка базы знаний

- Выбранная вселенная: Winx.
- Количество документов: 30.
- Скрипт scripts/download.py скачивает страницы через MediaWiki API.
- Скрипт scripts/replace_terms.py читает словарь knowledge_base/terms_map.json (117 пар ).

# Задание 3. Создание векторного индекса базы знаний

`pip install langchain faiss-cpu sentence-transformers langchain-community langchain-core langchain-text-splitters`

- Эмбеддинг-модель `sentence-transformers/all-MiniLM-L6-v2` из Sentence-Transformers  
  (репозиторий: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2, размер эмбеддингов — 384).
- ChromaDB
- Документы: 30
- Чанки: 184
- Index время: 0.5 s

```
Query: Who is Lyra Vale?

Результат #1
Заголовок: Lyra Vale
Источник: characters\_\_lyra-vale.md
Despite her flaws, Lyra Vale still has a heart of gold. She cares for all of her friends, allies, and families (both adopted and biological) deeply, and is always willing to help and fight for a good cause. She has shown herself to be selfless, caring, brave and a true capable leader. Lyra Vale is tough when needed to be and always lends a helping hand to people in need. As she grows in later seasons, she becomes wiser, and a far more focused and effective leader to the Aurora, as a part of maturing over the years, and has (for the most part) learned to reel in her impulsive and temperamental nature. This is especially relevant in World of Aurora and later seasons, where Lyra Vale showcases

Результат #2
Заголовок: Lyra Vale
Источник: characters\_\_lyra-vale.md

# Lyra Vale

Princess Lyra Vale is the Aether of the Phoenix Core. She is Prince Cael Dorian's fiancée, the second princess of Elyndor and its Guardian Aether. She is one of the founding members of the Aurora Circle, where she is recognized as the leader of their group, which also signifies her status as the central protagonist of the Aurora Circle series as a whole. She is also an alumna/student of the Aetheris Academy College for Aethers as of The Secret of the Lost Kingdom. When she was under the influence of Lord Nocthar, who corrupted her mind, she became a dark aether known as Dark Lyra Vale, but Cael Dorian, with the power of his love, purified her, returning her to her former state.


Результат #3
Заголовок: Lyra Vale
Источник: characters\_\_lyra-vale.md
Thanks to Cael Dorian confessing his deep love for her, Lyra Vale manages to use her healing power on everyone affected by Lord Nocthar's magic, including herself, thus freeing herself from Lord Nocthar's control and returning to normal. She returns the Ultimate Power to Relix and joins her friends in a Charmara Convergence that destroys Lord Nocthar and his fortress.

```

# Задание 4. Реализация RAG-бота с техниками промптинга
