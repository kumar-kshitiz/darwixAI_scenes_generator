from flask import Flask, render_template, request
from story_utils import segment_story
from prompt_engine import enhance_prompt, build_character_profile
from image_generator import generate_image
import re

app = Flask(__name__)

#  Action + Scene Detection Logic

ACTION_VERBS = {
    "walks", "runs", "jumps", "enters", "leaves", "sees", "finds",
    "opens", "closes", "starts", "stops", "looks", "turns", "falls",
    "goes", "comes", "takes", "brings", "hears", "watches"
}

SCENE_BREAKERS = {
    "suddenly", "later", "meanwhile", "after", "before",
    "next", "then", "at night", "in the morning", "instantly"
}


def estimate_scenes_by_actions(text: str):
    tokens = re.findall(r"[a-zA-Z']+", text.lower())
    return sum(1 for word in tokens if word in ACTION_VERBS)


def detect_scene_shifts(text: str):
    text = text.lower()
    count = 1
    for phrase in SCENE_BREAKERS:
        if phrase in text:
            count += 1
    return count


def count_sentences(text: str):
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    return len(sentences)


#  UPDATED: dynamic scene count (min=3, max=7)
def decide_scene_count(text: str):
    sentences = count_sentences(text)
    actions = estimate_scenes_by_actions(text)
    shifts = detect_scene_shifts(text)

    score = max(sentences, actions, shifts)

    #  dynamic clamp
    return max(3, min(9, score))


#  Route

@app.route("/", methods=["GET", "POST"])
def index():
    storyboard = []
    error = None

    if request.method == "POST":
        user_text = request.form.get("story", "").strip()
        style = request.form.get("style", "digital art").strip()

        if not user_text:
            return render_template(
                "index.html",
                storyboard=[],
                error="Please enter a story paragraph."
            )

        #  Hybrid scene count
        scene_count = decide_scene_count(user_text)

        character = build_character_profile(user_text)

        scenes = segment_story(
            user_text,
            min_scenes=scene_count,
            max_scenes=scene_count
        )

        if len(scenes) < 3:
            error = "The text was too short to form enough scenes. Please enter a richer paragraph."

        for i, scene in enumerate(scenes, start=1):
            prompt = enhance_prompt(
                scene,
                character=character,
                style=style,
                scene_no=i,
                total_scenes=len(scenes)
            )

            image_path = generate_image(prompt)

            storyboard.append({
                "scene_no": i,
                "text": scene,
                "prompt": prompt,
                "image": image_path
            })

    return render_template("index.html", storyboard=storyboard, error=error)


if __name__ == "__main__":
    app.run(debug=True)