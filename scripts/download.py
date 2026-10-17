import json
import re
import html
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://winx.fandom.com/api.php"
OUT_DIR = Path(__file__).resolve().parent.parent / "knowledge_base" / "_raw"
MAX_CHARS = 7000

BLOCK = [
    "for other uses",
    "this article",
    "talk page",
    "please help",
    "fandom",
    "community content",
    "disambiguation",
    "out of universe",
    "stub",
    "expand",
    "featured article",
    "trivia",
    "gallery",
    "appearances",
    "navigation",
    "editor discretion",
]


def is_bad_paragraph(text: str) -> bool:
    lower = text.lower()
    if len(text) < 40:
        return True
    if any(bad in lower for bad in BLOCK):
        return True
    commas = text.count(",")
    periods = text.count(".")
    if commas >= 15 and commas / (periods + 1) >= 6:
        return True
    return False


ENTITIES = {
    "characters": [
        "Bloom",
        "Stella",
        "Flora",
        "Musa",
        "Tecna",
        "Aisha",
        "Roxy",
        "Icy",
        "Darcy",
        "Stormy",
    ],
    "places": [
        "Alfea",
        "Cloud Tower",
        "Red Fountain",
        "Domino",
        "Solaria",
        "Melody",
        "Andros",
        "Magix",
    ],
    "magic": [
        "Charmix_(Form)",
        "Enchantix_(Form)",
        "Believix_(Form)",
        "Harmonix_(Form)",
        "Sirenix_(Form)",
        "Bloomix_(Form)",
        "Mythix",
        "Tynix_(Form)",
        "Cosmix",
    ],
    "groups": [
        "Winx_(Group)",
        "Trix_(Group)",
        "Specialists_(Group)",
    ],
}


def fetch_clean(title: str) -> str:
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "format": "json",
        "redirects": "1",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "rag-kb-builder/1.0 (educational project)"}
    )

    with urllib.request.urlopen(request, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    if "parse" not in data:
        return ""

    raw = data["parse"]["text"]["*"]

    paragraphs = re.findall(r"<p>(.*?)</p>", raw, flags=re.S)
    cleaned = []

    for para in paragraphs:
        text = re.sub(r"<[^>]+>", "", para)
        text = html.unescape(text)
        text = re.sub(r"\[\d+\]", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        if is_bad_paragraph(text):
            continue

        cleaned.append(text)

    result = "\n\n".join(cleaned)

    if len(result) > MAX_CHARS:
        result = result[:MAX_CHARS].rsplit("\n\n", 1)[0]

    return result


def slugify(title: str) -> str:
    slug = title.lower().replace(" ", "-")
    return re.sub(r"[^a-z0-9-]", "", slug)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total = 0

    for category, titles in ENTITIES.items():
        for title in titles:
            try:
                text = fetch_clean(title)
            except Exception as err:
                print(f"Fail {title}: {err}")
                continue

            if len(text) < 200:
                print(f"Skip {title}: слишком короткий ({len(text)})")
                continue

            path = OUT_DIR / f"{category}__{slugify(title)}.md"
            path.write_text(f"# {title}\n\n{text}\n", encoding="utf-8")
            total += 1
            print(f"OK {path.name} ({len(text)} chars)")
            time.sleep(0.3)

    print(f"\nСохранено {total} документов в {OUT_DIR}")


if __name__ == "__main__":
    main()

