from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import numpy as np
import pretty_midi
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve generated midi files
os.makedirs("generated", exist_ok=True)
app.mount("/generated", StaticFiles(directory="generated"), name="generated")

class GenerateRequest(BaseModel):
    style: str = "pop"
    key: str = "C"
    scale: str = "major"
    tempo: int = 100
    bars: int = 4
    seed: Optional[int] = None
    temperature: float = 1.0

def scale_degrees_for(scale_name: str):
    if scale_name.lower() == "minor":
        return [0, 2, 3, 5, 7, 8, 10]
    return [0, 2, 4, 5, 7, 9, 11]  # major

note_name_to_midi = {
    "C": 0, "C#":1, "D":2, "D#":3, "E":4, "F":5, "F#":6, "G":7, "G#":8, "A":9, "A#":10, "B":11
}

def generate_melody(req: GenerateRequest):
    if req.seed is not None:
        np.random.seed(req.seed)
    tempo = req.tempo
    beats_per_bar = 4
    total_beats = req.bars * beats_per_bar
    beat_duration = 60.0 / tempo

    root = note_name_to_midi.get(req.key.upper(), 0)
    scale = scale_degrees_for(req.scale)
    notes = []
    t = 0.0
    while t < total_beats:
        dur_beats = np.random.choice([0.5, 1.0, 1.5, 2.0], p=[0.2,0.6,0.1,0.1])
        dur = float(min(dur_beats, total_beats - t)) * beat_duration
        degree = int(np.clip(int(np.random.normal(len(scale)/2, req.temperature)), 0, len(scale)-1))
        pitch = 60 + root + scale[degree]  # center around MIDI 60 (C4)
        notes.append({
            "pitch": int(pitch),
            "start": round(t * beat_duration, 4),
            "duration": round(dur, 4),
            "velocity": int(np.random.randint(80, 120))
        })
        t += dur_beats
    return notes


def notes_to_midi_file(notes, tempo, filename):
    pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    piano = pretty_midi.Instrument(program=0)
    for n in notes:
        note = pretty_midi.Note(
            velocity=int(n["velocity"]),
            pitch=int(n["pitch"]),
            start=float(n["start"]),
            end=float(n["start"]) + float(n["duration"]) 
        )
        piano.notes.append(note)
    pm.instruments.append(piano)
    path = os.path.join("generated", filename)
    pm.write(path)
    return path

@app.post("/generate")
async def generate(req: GenerateRequest):
    try:
        notes = generate_melody(req)
        filename = f"melody_{uuid.uuid4().hex}.mid"
        path = notes_to_midi_file(notes, req.tempo, filename)
        midi_url = f"/generated/{filename}"
        return {"notes": notes, "midi_url": midi_url, "tempo": req.tempo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
