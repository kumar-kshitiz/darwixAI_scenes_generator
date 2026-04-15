import re

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def split_into_sentences(text: str):
    text = clean_text(text)
    if not text:
        return []
    # Basic sentence splitter
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip(" \"'") for p in parts if p.strip()]

def split_into_clauses(sentence: str):
    # Fallback for short input or long sentences
    parts = re.split(r"\s*(?:,|;|\band then\b|\bthen\b|\bso\b|\bbecause\b|\bwhile\b|\bafter\b)\s*",
                     sentence, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]

def segment_story(text: str, min_scenes: int = 3, max_scenes: int = 5):
    """
    Returns 3-5 logical scenes.
    Works well for 3-5 sentence paragraphs, and still falls back gracefully.
    """
    sentences = split_into_sentences(text)

    # Best case: already 3-5 sentences
    if min_scenes <= len(sentences) <= max_scenes:
        return sentences

    # Too many sentences -> merge into max_scenes panels
    if len(sentences) > max_scenes:
        k = max_scenes
        base, extra = divmod(len(sentences), k)
        scenes = []
        i = 0
        for idx in range(k):
            size = base + (1 if idx < extra else 0)
            chunk = " ".join(sentences[i:i + size]).strip()
            if chunk:
                scenes.append(chunk)
            i += size
        return scenes

    # Too few sentences -> try clause splitting
    clauses = []
    for sentence in sentences:
        clauses.extend(split_into_clauses(sentence))

    clauses = [c for c in clauses if len(c.split()) >= 3]

    if len(clauses) >= min_scenes:
        return clauses[:max_scenes]

    # Final fallback: split by approximate word chunks
    words = clean_text(text).split()
    if not words:
        return []

    target = max(1, len(words) // min_scenes)
    scenes = []
    for i in range(0, len(words), target):
        chunk = " ".join(words[i:i + target]).strip()
        if chunk:
            scenes.append(chunk)

    # Ensure at least 3 scenes if possible
    return scenes[:max_scenes]