# Shakey-Verse Sound Lab — Melody Maker (MVP)

AI-assisted melody generator and vocal preset toolbox for producers.

What this scaffold contains
- frontend/: Next.js app (UI + Tone.js playback, MIDI export link)
- backend/: FastAPI app with /generate endpoint that returns note JSON and a generated .mid file
- presets/: vocal_presets.json with 5 example presets

Quick start (on your machine)

Prerequisites
- Node.js 18+
- Python 3.10+
- git

Run backend

cd backend
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn main:app --reload --port 8000

Run frontend

cd frontend
npm install
npm run dev

Open http://localhost:3000

Notes
- The backend serves generated MIDI files under /generated.
- This scaffold uses an algorithmic melody generator; later we can wire a hosted model (Hugging Face) or self-hosted Music Transformer.

Next teaching steps I will walk you through after this push:
1) Run the backend and frontend locally and test generation
2) Inspect the backend code to see how notes are created and converted to MIDI
3) Inspect frontend code to learn how Tone.js plays MIDI-pitched notes and how MIDI export works
4) Swap the generator for a hosted model (optional)

If anything breaks when you run it, tell me the exact error and I'll guide you step-by-step.
