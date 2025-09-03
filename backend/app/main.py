from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import openai
import io
import os
import traceback
from dotenv import load_dotenv
from textblob import TextBlob
import re
import random

# Load environment variables 
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load BLIP model once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Rewrites a raw caption to 3 expressive ones using GPT
def rewrite_caption_with_gpt(raw_caption: str) -> list:
    try:
        prompt = (
            f"Here is a literal image description: '{raw_caption}'.\n\n"
            "Imagine this is a viral Instagram post. Write 3 different creative, emotionally expressive, and aesthetic captions someone might actually use to post this photo.\n"
            "Avoid using literal descriptions or repetitive phrases. Focus on the *mood*, *feeling*, and *vibe* of the image. Use poetic language, metaphors, and sensory details to evoke emotions.\n"
            "Make the captions playful, nostalgic, or thought-provoking. Use emojis tastefully to enhance the mood."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.95,
        )

        full_response = response['choices'][0]['message']['content'].strip()
        captions = [line.strip("- ").strip() for line in full_response.split("\n") if line.strip()]
        return captions[:3] if captions else [raw_caption]

    except Exception as e:
        print("GPT Caption Error:", e)
        return [raw_caption]  # fallback list

# 🎨 Generate expressive captions using predefined templates
def generate_expressive_captions(raw_caption: str) -> list:
    templates = [
        f"Lost in the moment, where dreams meet reality. 🌟",
        f"Chasing the light, embracing the magic. ✨",
        f"Every snapshot tells a story waiting to be told. 💖",
        f"Moments like these are what life is all about. 🌅",
        f"Finding beauty in the ordinary. 🌸",
        f"Here’s to the adventures that make us feel alive. 📖",
        f"Capturing the essence of joy in a single frame. 🌈",
        f"Let the colors of this moment paint your soul. 🌠",
    ]
    return random.sample(templates, 3)  # Return 3 random captions

# Adjust the tone of the captions
def adjust_tone(caption: str) -> str:
    # Example of tone adjustment using TextBlob for sentiment analysis
    blob = TextBlob(caption)
    if blob.sentiment.polarity < 0:
        return f"🌧️ {caption} (A little gloomy, but still beautiful.)"
    elif blob.sentiment.polarity > 0:
        return f"🌞 {caption} (Bright and uplifting!)"
    return caption  # Neutral tone

# Main API endpoint
@app.post("/generate-caption/")
async def generate_caption(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Step 1: Generate raw caption using BLIP
        inputs = processor(images=image, return_tensors="pt")
        out = model.generate(inputs['pixel_values'])
        raw_caption = processor.decode(out[0], skip_special_tokens=True)

        # Step 2: Rewrite the caption using GPT
        gpt_captions = rewrite_caption_with_gpt(raw_caption)

        # Step 3: Generate expressive captions using predefined templates
        expressive_captions = generate_expressive_captions(raw_caption)

        # Step 4: Adjust tone and remove unwanted phrases
        adjusted_captions = [adjust_tone(caption) for caption in gpt_captions + expressive_captions]

        return JSONResponse(content={"captions": adjusted_captions})

    except Exception as e:
        print("Error in caption generation:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
