# AI Image Caption Generator  

Generate expressive captions for your images using **BLIP (image captioning)** + **GPT (caption rewriting)**, powered by a **FastAPI backend** and a **React frontend**.  

---

## Features  

- Upload an image and get **AI-generated captions**.  
- Captions are rewritten into **creative, Instagram-style vibes** using GPT.  
- Predefined **expressive caption templates** for variety.  
- Option to **copy** or **tweak** captions easily in the frontend.  
- **Sentiment-aware tone adjustment** for captions.  

---

## Tech Stack  

**Backend**  
- FastAPI  
- Uvicorn  
- Hugging Face Transformers (BLIP model: `Salesforce/blip-image-captioning-base`)  
- OpenAI GPT (`gpt-3.5-turbo`)  
- TextBlob (sentiment analysis)  
- Pillow (image processing)  
- Python-dotenv (environment variables)  

**Frontend**  
- React.js (CRA setup)  
- CSS  

---

## ⚙️ Setup Instructions  

### 1. Clone Repository 
```bash
git clone https://github.com/Akhila913/ai-image-caption-generator.git
cd ai-image-caption-generator
```

### 2. Backend Setup
```bash
cd backend/
# Create virtual environment
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key in a .env file inside the backend directory:
OPENAI_API_KEY=your_openai_api_key_here
```

### Run the backend server:
```bash
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend/
npm install
npm start   # or npm run dev if using Vite
```

### 4. Access the App
Open your browser at:
http://localhost:3000

### Example Workflow
- Upload an image.
- Backend generates a raw caption using BLIP.
- GPT rewrites it into 3 expressive captions.
- Additional template-based captions are suggested.
- Captions are tone-adjusted and displayed in the UI.

### Future Improvements
- Add support for image URLs.
- Improve UI styling with TailwindCSS.
- Multi-language caption generation.
- Save caption history for each user.
