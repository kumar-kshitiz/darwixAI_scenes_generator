# Pitch Visualizer

Bring your stories to life with AI-generated scenes! Pitch Visualizer is a Flask-based web application that dynamically parses a natural language story, segments it into sequential scenes, and generates high-quality storyboard illustrations using the Hugging Face Inference API (Stable Diffusion). 

## 🚀 Capabilities

- **Intelligent Scene Segmentation**: Uses NLP heuristics (action verbs, scene breakers, and sentence counts) to dynamically divide your text into logical narrative beats (usually 3-9 scenes).
- **Automated Prompt Engineering**: Translates your raw text into highly detailed, optimal image generation prompts with built-in consistency.
- **Character Consistency**: Strives for character continuity across storyboards by analyzing pronouns for implicit or explicit gender cues and injecting consistency parameters.
- **Modern UI/UX**: Includes a gorgeous, glassmorphic UI using custom CSS that features dark aesthetics, vibrant accents, smooth micro-animations, and responsive cards for the final generated storyboard.

---

## 🛠 Setup & Execution

### Prerequisites
- Python 3.8+ 
- A valid [Hugging Face Access Token](https://huggingface.co/settings/tokens) with `read` (or `write`) permissions.

### 1. Installation

Clone or navigate into the project directory, then install the required dependencies:

```bash
pip install -r requirements.txt
```

*(Optional but recommended: use a virtual environment)*

### 2. API Key Management

The image generation uses the `huggingface_hub` client which requires an API key in a `.env` file. 

Create a `.env` file in the root of the project:

```bash
touch .env
```

Add your Hugging Face API key and the intended model (defaults to `stabilityai/stable-diffusion-xl-base-1.0` if not set):

```env
HF_API_KEY=your_huggingface_token_here
```

### 3. Execution

Start the Flask development server:

```bash
python app.py
```

The application will launch on `http://127.0.0.1:5000`. Navigate to this URL in your web browser, enter a story, and watch the visuals generate!

---

## 🎨 Design Choices & Prompt Engineering Methodology

### Pipeline Design
We built the application as a clean, segmented pipeline separating standard Web framework components (`app.py`), the image retrieval service (`image_generator.py`), and the core intelligence (`prompt_engine.py` & `story_utils.py`).

### Prompt Engineering Methodology

Raw user text is typically not optimal for image generation models (like Stable Diffusion), which rely heavily on structural keywords rather than grammatical narrative flow. We implemented an "Enhancement Pipeline" with the following methodology:

1. **Keyword Extraction & Stopword Removal**: 
   The prompt engine filters the raw scene text through an extensive list of structural stopwords (conjunctions, prepositions, adverbs) to isolate the core nouns, verbs, and subjects. This allows the AI model to latch strictly onto the narrative subjects rather than being confused by complex sentence structure.

2. **Implicit Gender Detection for Character Profiling**:
   To pursue consistency, `prompt_engine.py` scans the input for gendered pronouns ("she", "him", "woman"). It then implicitly constructs a standard character profile prompt (`"a young woman with consistent face..."` or `"a young man..."`) and layers it into every scene. 

3. **Cinematic & Environmental Layering**:
   A great storyboard needs excellent composition, not just correct subjects. We automatically embed established "art-direction blocks" into the final prompt sent to the LLM:
   - **Cinematic Boost**: Injects lighting definitions like `"volumetric light, depth of field, dramatic shadows"`.
   - **Camera Details**: Hard-codes compositional standards like `"rule of thirds, leading lines"`.
   - **Style Bible**: Enforces styling traits and overrides like `"consistent color palette, cinematic continuity"`.

4. **Iterative Stability Retrieval**:
   Since API calls might timeout or hit rate limits, `image_generator.py` uses an internal retry mechanism with a backoff. It also implements deterministic file naming using SHA-256 hashes of the prompts. This allows standard browser caching to easily re-map duplicate prompt images without initiating redundant, expensive API calls.
