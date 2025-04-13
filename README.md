# AI Image Caption Generator

Generate meaningful captions for images using deep learning, FastAPI, and a modern frontend.

## Features

- Upload image or paste URL
- AI-generated captions using deep learning (CNN + RNN / transformer models)
- FastAPI backend with Uvicorn server
- Modern frontend with React (or other JS framework)

---

## Tech Stack

- **Backend:** FastAPI, Uvicorn, Python, Torch/TensorFlow
- **Frontend:** React.js / Vite / TailwindCSS
- **Model:** CNN (ResNet) + RNN (LSTM) or Transformer-based (e.g., BLIP)
- **Serving:** REST API

---

## Setup Instructions

### Backend (FastAPI + Uvicorn) | Frontend(React + Vite)

```bash
# Go to backend directory
cd backend/

# Create and activate virtual environment (optional)
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload

# Go to frontend directory
cd frontend/

# Install dependencies
npm install

# Start development server
npm run dev
