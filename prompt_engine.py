import re

#  STOPWORDS (fixed: removed gendered pronouns)
STOPWORDS = {
    # Articles
    "a", "an", "the",

    # Conjunctions
    "and", "or", "but", "so", "yet", "nor", "although", "because", "since", "unless",

    # Prepositions
    "to", "of", "in", "on", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "over", "under",
    "again", "further", "off", "near",

    #  Removed gender-related pronouns from here

    # Other pronouns (safe to remove)
    "i", "me", "my", "mine", "myself",
    "we", "us", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "it", "its", "itself",
    "they", "them", "their", "theirs", "themselves",

    # Demonstratives
    "this", "that", "these", "those",

    # Auxiliary verbs
    "is", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "doing",
    "have", "has", "had", "having",

    # Modals
    "can", "could", "should", "would", "may", "might", "must", "shall", "will",

    # Adverbs
    "very", "really", "just", "too", "also", "only", "even", "still", "well",

    # Time
    "then", "now", "when", "while", "after", "before", "once", "soon", "later",

    # Location
    "here", "there", "everywhere", "anywhere",

    # Question words
    "what", "which", "who", "whom", "whose", "why", "how",

    # Quantifiers
    "all", "any", "some", "many", "few", "more", "most", "other", "such",

    # Negations
    "no", "not", "nor", "never",

    # Misc
    "each", "every", "either", "neither",
    "own", "same", "than", "s"
}

#  Detect gender explicitly
def detect_gender(text: str):
    text = text.lower()
    if any(word in text for word in ["she", "her", "hers", "girl", "woman", "female"]):
        return "female"
    elif any(word in text for word in ["he", "him", "his", "boy", "man", "male"]):
        return "male"
    return None

#  NEW: character profile generator
def build_character_profile(text: str):
    gender = detect_gender(text)

    if gender == "female":
        return "a young woman with consistent face, long dark hair, expressive eyes, wearing the same outfit in all scenes"
    elif gender == "male":
        return "a young man with consistent face, short black hair, expressive features, wearing the same outfit in all scenes"

    return "a main character with consistent appearance, same face, same clothes across all scenes"


#  Keyword extraction (cleaner)
def extract_keywords(text: str, limit: int = 6):
    tokens = re.findall(r"[A-Za-z0-9']+", text.lower())
    keywords = []

    for token in tokens:
        if (
            token not in STOPWORDS and
            len(token) > 2 and
            token not in keywords
        ):
            keywords.append(token)

    return keywords[:limit]


#  Enhanced prompt builder
def enhance_prompt(sentence: str, character: str, style: str = "digital art", scene_no: int = 1, total_scenes: int = 3):
    keywords = extract_keywords(sentence)
    keyword_text = ", ".join(keywords) if keywords else "important story details"

    #  Add gender hint
    gender = detect_gender(sentence)
    gender_hint = f"Main character is {gender}. " if gender else ""

    style_bible = (
        "consistent character design, consistent color palette, cinematic continuity, "
        "high detail, ultra sharp focus, polished composition"
    )

    cinematic_boost = (
        "cinematic lighting, volumetric light, depth of field, atmospheric perspective, "
        "dramatic shadows, realistic textures, 4k detail, professional color grading"
    )

    camera_details = (
        "shot composition: rule of thirds, leading lines, dynamic framing, "
        "camera angle: low angle or over-the-shoulder perspective"
    )

    emotion_layer = (
        "clear emotional tone, expressive facial features, strong body language"
    )

    environment_layer = (
        "rich background, immersive environment, layered foreground midground background"
    )

    prompt = (
        f"Storyboard panel {scene_no} of {total_scenes}. "
        f"{sentence}. "
        f"{gender_hint}"
        f"Key elements: {keyword_text}. "

        f"{environment_layer}. "
        f"{emotion_layer}. "
        f"{camera_details}. "
        f"{cinematic_boost}. "

        f"Art style: {style}. "
        f"{style_bible}. "

        f"Highly detailed, cinematic, storytelling illustration. "
        f"No text, no captions, no watermark, no logo."
    )

    return prompt