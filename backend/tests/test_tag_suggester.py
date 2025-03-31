# backend/tests/test_tag_suggester.py

# backend/utils/tag_suggester.py
def suggest_tags(text: str) -> list[str]:
    tags = []
    if "documentation" in text.lower():
        tags.append("docs")
    if "bug" in text.lower():
        tags.append("bugfix")
    return tags
