import { useState } from "react";
import axios from "axios";
import * as Tone from "tone";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [notes, setNotes] = useState([]);
  const [tempo, setTempo] = useState(100);
  const [midiUrl, setMidiUrl] = useState(null);

  async function generate() {
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/generate", {
        style: "pop",
        key: "C",
        scale: "major",
        tempo,
        bars: 4,
        seed: Math.floor(Math.random() * 100000)
      });
      setNotes(res.data.notes);
      setMidiUrl(`http://localhost:8000${res.data.midi_url}`);
    } catch (e) {
      alert("Error generating melody: " + (e.message || e));
    } finally {
      setLoading(false);
    }
  }

  async function play() {
    await Tone.start();
    const synth = new Tone.Synth().toDestination();
    const now = Tone.now();
    notes.forEach(n => {
      const time = now + n.start;
      synth.triggerAttackRelease(Tone.Frequency(n.pitch, "midi"), n.duration, time, n.velocity / 127);
    });
  }

  return (
    <main style={{ padding: 24, fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ fontSize: 22, marginBottom: 8 }}>Shakey‑Verse Sound Lab — Melody Maker (MVP)</h1>
      <div style={{ marginBottom: 12 }}>
        <label style={{ marginRight: 8 }}>Tempo:</label>
        <input type="number" value={tempo} onChange={e => setTempo(Number(e.target.value))} />
      </div>
      <div style={{ marginBottom: 12 }}>
        <button onClick={generate} disabled={loading} style={{ marginRight: 8 }}>
          {loading ? "Generating…" : "Generate Melody"}
        </button>
        <button onClick={play} disabled={!notes.length} style={{ marginRight: 8 }}>Play</button>
        {midiUrl && (
          <a href={midiUrl} style={{ marginLeft: 8 }} target="_blank" rel="noreferrer">Download .mid</a>
        )}
      </div>

      <section>
        <h2>Notes (piano-roll list)</h2>
        <ol>
          {notes.length === 0 && <li>No melody yet — click Generate</li>}
          {notes.map((n, i) => (
            <li key={i}>pitch: {n.pitch}, start: {n.start}s, dur: {n.duration}s, vel: {n.velocity}</li>
          ))}
        </ol>
      </section>

      <section style={{ marginTop: 18 }}>
        <h3>Next steps</h3>
        <ul>
          <li>I can add a MIDI export button (client-side) if you want a direct download without hitting the backend file.</li>
          <li>I can wire a hosted model (Hugging Face) to /generate when you’re ready to spend inference tokens.</li>
        </ul>
      </section>
    </main>
  );
}
