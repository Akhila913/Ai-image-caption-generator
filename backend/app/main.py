# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from transformers import BlipProcessor, BlipForConditionalGeneration
# from PIL import Image
# import openai
# import torch
# import io
# import os
# import traceback
# from dotenv import load_dotenv

# # Load environment variables (e.g., OpenAI API key)
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# app = FastAPI()

# # Allow CORS for frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load BLIP model once for image captioning
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# # ✨ Generate expressive social-style captions using GPT
# def rewrite_caption_with_gpt(raw_caption: str) -> list:
#     try:
#         prompt = (
#             f"You are a poetic, emotionally intelligent Instagram caption writer.\n"
#             f"The following is a literal image description: '{raw_caption}'\n\n"
#             "Now turn this into 3 different creative, emotionally expressive, and aesthetic captions for someone posting this photo on Instagram or social media.\n"
#             "Avoid repeating literal words like 'a man', 'a woman', 'sitting', etc. Instead, focus on the *vibe*, *emotion*, *moment*, and *story* behind it.\n"
#             "Make the captions sound human — they can be poetic, nostalgic, witty, or romantic.\n"
#             "Use emojis only when they enhance the mood. Keep them short and scroll-stopping.\n\n"
#             "Example:\n"
#             "Literal: a couple walking under street lights\n"
#             "Captions:\n"
#             "- City lights, quiet hearts 🏙️❤️\n"
#             "- Late night talks and long walks\n"
#             "- Us, under the same stars ✨\n\n"
#             f"Now give 3 captions for: '{raw_caption}'"
#         )

#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=180,
#             temperature=0.95,
#         )

#         full_response = response['choices'][0]['message']['content'].strip()

#         # Handle both bullet point and numbered list formats
#         captions = []
#         for line in full_response.split("\n"):
#             line = line.strip()
#             if line.startswith(("-", "*", "•")):
#                 captions.append(line[1:].strip())
#             elif line[:2].isdigit() or line[:1].isdigit():
#                 captions.append(line.split(".", 1)[-1].strip())
#             elif line:
#                 captions.append(line.strip())

#         return captions[:3] if captions else [raw_caption]

#     except Exception as e:
#         print("🔴 GPT Caption Error:", e)
#         return [raw_caption]  # fallback

# # 🚀 Main caption generation endpoint
# @app.post("/generate-caption/")
# async def generate_caption(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         image = Image.open(io.BytesIO(contents)).convert('RGB')

#         # Step 1: Generate raw literal caption using BLIP
#         inputs = processor(images=image, return_tensors="pt")
#         out = model.generate(**inputs)
#         raw_caption = processor.decode(out[0], skip_special_tokens=True)

#         # Step 2: Enhance it with expressive social-style captions
#         styled_captions = rewrite_caption_with_gpt(raw_caption)

#         return {"captions": styled_captions}

#     except Exception as e:
#         print("🔥 Backend Error:", e)
#         traceback.print_exc()
#         return JSONResponse(status_code=500, content={"captions": ["Error generating captions."]})



# @app.post("/generate-caption/")
# async def generate_caption(file: UploadFile = File(...)):
#     # Save and load image as needed
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents))

#     # Get literal caption from your model
#     raw_caption = generate_caption_from_model(image)

#     # Rewrite with GPT
#     final_captions = rewrite_caption_with_gpt(raw_caption)

#     return {"captions": final_captions}  # ✅ NOT 'caption': raw_caption












# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from transformers import BlipProcessor, BlipForConditionalGeneration
# from PIL import Image
# import openai
# import torch
# import io
# import os
# import traceback
# from dotenv import load_dotenv
# from textblob import TextBlob

# # Load environment variables (e.g., OpenAI API key)
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# app = FastAPI()

# # Allow CORS for frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load BLIP model once
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# # ✨ Rewrites a raw caption to 3 expressive ones using GPT
# def rewrite_caption_with_gpt(raw_caption: str) -> list:
#     try:
#         prompt = (
#             f"Here is a literal image description: '{raw_caption}'.\n\n"
#             "Imagine this is a viral Instagram post. Write 3 different creative, emotionally expressive, and aesthetic captions someone might actually use to post this photo.\n"
#             "Focus on the *mood*, *feeling*, and *vibe* of the image. Use poetic language, metaphors, and sensory details to evoke emotions.\n"
#             "Make the captions playful, nostalgic, or thought-provoking. Use emojis tastefully to enhance the mood.\n"
#             "Example:\n"
#             "1. 'Lost in the golden hues of sunset, where time stands still. 🌅✨ #GoldenHour'\n"
#             "2. 'Chasing dreams and catching sunsets. 🌄💭 #Wanderlust'\n"
#             "3. 'The sky painted in colors of hope and serenity. 🌌💖 #NatureLover'"
#         )

#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=200,
#             temperature=0.95,
#         )

#         full_response = response['choices'][0]['message']['content'].strip()
#         captions = [line.strip("- ").strip() for line in full_response.split("\n") if line.strip()]
#         return captions[:3] if captions else [raw_caption]

#     except Exception as e:
#         print("🔴 GPT Caption Error:", e)
#         return [raw_caption]  # fallback list

# # 🎨 Generate expressive captions using predefined templates
# def generate_expressive_captions(raw_caption: str) -> list:
#     templates = [
#         f"Lost in the moment: {raw_caption} 🌟",
#         f"Chasing dreams, catching vibes. {raw_caption} ✨",
#         f"Where the heart feels at home. {raw_caption} 💖",
#         f"Golden hour, golden memories. {raw_caption} 🌅",
#         f"Living for these little moments. {raw_caption} 🌸",
#         f"Every picture tells a story. {raw_caption} 📖",
#         f"Here’s to the magic of now. {raw_caption} 🌈",
#         f"Feeling the vibes, living the dream. {raw_caption} 🌠",
#     ]
#     return templates[:3]  # Return the first 3 captions

# # 🎭 Adjust caption tone based on sentiment
# def adjust_tone(caption: str) -> str:
#     analysis = TextBlob(caption)
#     if analysis.sentiment.polarity > 0.5:
#         return f"Feeling blessed and grateful. {caption} 🙏"
#     elif analysis.sentiment.polarity < -0.5:
#         return f"Sometimes, it’s okay to feel low. {caption} 🌧️"
#     else:
#         return f"Every moment has its own story. {caption} 📸"

# # 🚀 Main API endpoint
# @app.post("/generate-caption/")
# async def generate_caption(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         image = Image.open(io.BytesIO(contents)).convert('RGB')

#         # Step 1: Generate raw caption using BLIP
#         inputs = processor(images=image, return_tensors="pt")
#         out = model.generate(**inputs)
#         raw_caption = processor.decode(out[0], skip_special_tokens=True)

#         # Step 2: Rewrite it into 3 expressive captions using GPT
#         styled_captions = rewrite_caption_with_gpt(raw_caption)

#         # Step 3: If GPT fails, fall back to predefined templates
#         if styled_captions == [raw_caption]:
#             styled_captions = generate_expressive_captions(raw_caption)

#         # Step 4: Adjust tone based on sentiment
#         styled_captions = [adjust_tone(caption) for caption in styled_captions]

#         return {"captions": styled_captions}

#     except Exception as e:
#         print("🔥 Backend Error:", e)
#         traceback.print_exc()
#         return JSONResponse(status_code=500, content={"captions": ["Error generating captions."]})






# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from transformers import BlipProcessor, BlipForConditionalGeneration
# from PIL import Image
# import openai
# import io
# import os
# import traceback
# from dotenv import load_dotenv
# from textblob import TextBlob
# import re

# # Load environment variables (e.g., OpenAI API key)
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# app = FastAPI()

# # Allow CORS for frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load BLIP model once
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# # ✨ Rewrites a raw caption to 3 expressive ones using GPT
# def rewrite_caption_with_gpt(raw_caption: str) -> list:
#     try:
#         prompt = (
#             f"Here is a literal image description: '{raw_caption}'.\n\n"
#             "Imagine this is a viral Instagram post. Write 3 different creative, emotionally expressive, and aesthetic captions someone might actually use to post this photo.\n"
#             "Focus on the *mood*, *feeling*, and *vibe* of the image. Use poetic language, metaphors, and sensory details to evoke emotions.\n"
#             "Make the captions playful, nostalgic, or thought-provoking. Use emojis tastefully to enhance the mood.\n"
#             "Example:\n"
#             "1. 'Lost in the golden hues of sunset, where time stands still. 🌅✨ #GoldenHour'\n"
#             "2. 'Chasing dreams and catching sunsets. 🌄💭 #Wanderlust'\n"
#             "3. 'The sky painted in colors of hope and serenity. 🌌💖 #NatureLover'"
#         )

#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=200,
#             temperature=0.95,
#         )

#         full_response = response['choices'][0]['message']['content'].strip()
#         captions = [line.strip("- ").strip() for line in full_response.split("\n") if line.strip()]
#         return captions[:3] if captions else [raw_caption]

#     except Exception as e:
#         print("🔴 GPT Caption Error:", e)
#         return [raw_caption]  # fallback list

# # 🎨 Generate expressive captions using predefined templates
# def generate_expressive_captions(raw_caption: str) -> list:
#     templates = [
#         f"Lost in the moment: {raw_caption} 🌟",
#         f"Chasing dreams, catching vibes. {raw_caption} ✨",
#         f"Where the heart feels at home. {raw_caption} 💖",
#         f"Golden hour, golden memories. {raw_caption} 🌅",
#         f"Living for these little moments. {raw_caption} 🌸",
#         f"Every picture tells a story. {raw_caption} 📖",
#         f"Here’s to the magic of now. {raw_caption} 🌈",
#         f"Feeling the vibes, living the dream. {raw_caption} 🌠",
#     ]
#     return templates[:3]  # Return the first 3 captions

# # 🎭 Adjust caption tone based on sentiment and remove unwanted phrases
# def adjust_tone(caption: str) -> str:
#     # Remove specific unwanted phrases
#     caption = re.sub(r'a girl looking at the sunset', '', caption, flags=re.IGNORECASE).strip()
    
#     analysis = TextBlob(caption)
#     if analysis.sentiment.polarity > 0.5:
#         return f"Feeling blessed and grateful. {caption} 🙏"
#     elif analysis.sentiment.polarity < -0.5:
#         return f"Sometimes, it’s okay to feel low. {caption} 🌧️"
#     else:
#         return f"Every moment has its own story. {caption} 📸"

# # 🚀 Main API endpoint
# @app.post("/generate-caption/")
# async def generate_caption(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         image = Image.open(io.BytesIO(contents)).convert('RGB')

#         # Step 1: Generate raw caption using BLIP
#         inputs = processor(images=image, return_tensors="pt")
#         out = model.generate (inputs['pixel_values'])
#         raw_caption = processor.decode(out[0], skip_special_tokens=True)

#         # Step 2: Rewrite the caption using GPT
#         gpt_captions = rewrite_caption_with_gpt(raw_caption)

#         # Step 3: Generate expressive captions using predefined templates
#         expressive_captions = generate_expressive_captions(raw_caption)

#         # Step 4: Adjust tone and remove unwanted phrases
#         adjusted_captions = [adjust_tone(caption) for caption in gpt_captions + expressive_captions]

#         return JSONResponse(content={"captions": adjusted_captions})

#     except Exception as e:
#         print("🔴 Error in caption generation:", e)
#         return JSONResponse(content={"error": str(e)}, status_code=500)












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

# Load environment variables (e.g., OpenAI API key)
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

# ✨ Rewrites a raw caption to 3 expressive ones using GPT
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
        print("🔴 GPT Caption Error:", e)
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

# 🛠️ Adjust the tone of the captions
def adjust_tone(caption: str) -> str:
    # Example of tone adjustment using TextBlob for sentiment analysis
    blob = TextBlob(caption)
    if blob.sentiment.polarity < 0:
        return f"🌧️ {caption} (A little gloomy, but still beautiful.)"
    elif blob.sentiment.polarity > 0:
        return f"🌞 {caption} (Bright and uplifting!)"
    return caption  # Neutral tone

# 🚀 Main API endpoint
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
        print("🔴 Error in caption generation:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)