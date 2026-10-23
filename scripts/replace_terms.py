import json
import re
from pathlib import Path

RAW_DIR = Path("knowledge_base/_raw")
OUT_DIR = Path("knowledge_base")
MAP_FILE = Path("knowledge_base/terms_map.json")

OUT_DIR.mkdir(parents=True, exist_ok=True)

terms_map = json.loads(MAP_FILE.read_text(encoding="utf-8"))
sorted_terms = sorted(terms_map.items(), key=lambda x: len(x[0]), reverse=True)


def replace_terms(text: str) -> str:
    for src, dst in sorted_terms:
        if re.fullmatch(r"[A-Za-z0-9 ]+", src):
            pattern = r"\b" + re.escape(src) + r"\b"
        else:
            pattern = re.escape(src)
        text = re.sub(pattern, dst, text)
    return text


def slugify(text: str) -> str:
    text = text.lower()
    text = text.replace(" ", "-")
    text = text.replace("_", "-")
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


for file_path in RAW_DIR.glob("*.md"):
    text = file_path.read_text(encoding="utf-8")
    updated = replace_terms(text)

    # category из имени файла: groups__trixgroup.md -> groups
    if "__" in file_path.stem:
        category, _ = file_path.stem.split("__", 1)
    else:
        category = "unknown"

    lines = updated.splitlines()
    if lines and lines[0].startswith("# "):
        old_title = lines[0][2:].strip()
        new_title = replace_terms(old_title)
        lines[0] = f"# {new_title}"
        updated = "\n".join(lines)
    else:
        if "__" in file_path.stem:
            _, original_slug = file_path.stem.split("__", 1)
            new_title = replace_terms(original_slug)
        else:
            new_title = replace_terms(file_path.stem)

    new_slug = slugify(new_title)
    new_file_name = f"{category}__{new_slug}.md"
    out_path = OUT_DIR / new_file_name

    out_path.write_text(updated, encoding="utf-8")
    print(f"OK {file_path.name} -> {out_path.name}")

print("Готово")
