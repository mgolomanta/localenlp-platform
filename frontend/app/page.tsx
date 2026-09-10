"use client";

import { ChangeEvent, useEffect, useMemo, useState } from "react";

type Pair = { source: string; target: string; model: string; name: string };
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";
const languageNames: Record<string, string> = {eng: "English", wol: "Wolof", hau: "Hausa"};

export default function Home() {
  const [pairs, setPairs] = useState<Pair[]>([]);
  const [source, setSource] = useState("eng");
  const [target, setTarget] = useState("wol");
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => { fetch(`${API}/languages`).then(r => r.json()).then(data => setPairs(data.pairs || [])).catch(() => setError("Impossible de charger les langues.")); }, []);
  const availableTargets = useMemo(() => [...new Set(pairs.filter(p => p.source === source).map(p => p.target))], [pairs, source]);
  useEffect(() => { if (!availableTargets.includes(target) && availableTargets.length) setTarget(availableTargets[0]); }, [availableTargets, target]);

  function swapLanguages() { const oldSource = source; setSource(target); setTarget(oldSource); setText(result || text); setResult(""); }

  async function translateText() {
    if (!text.trim()) return;
    setLoading(true); setError(""); setResult("");
    try {
      const response = await fetch(`${API}/translate`, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({source_lang: source, target_lang: target, text})});
      const data = await response.json(); if (!response.ok) throw new Error(data.detail || "La traduction a échoué."); setResult(data.translation || "");
    } catch (err) { setError(err instanceof Error ? err.message : "La traduction a échoué."); } finally { setLoading(false); }
  }

  async function translateFile() {
    if (!file) return;
    setLoading(true); setError(""); setResult("");
    const form = new FormData(); form.append("file", file); form.append("source_lang", source); form.append("target_lang", target);
    try {
      const response = await fetch(`${API}/translate/file`, {method: "POST", body: form});
      const data = await response.json(); if (!response.ok) throw new Error(data.detail || "La traduction du fichier a échoué."); setText(data.extracted_text || ""); setResult(data.translation || "");
    } catch (err) { setError(err instanceof Error ? err.message : "La traduction du fichier a échoué."); } finally { setLoading(false); }
  }

  function onFileChange(event: ChangeEvent<HTMLInputElement>) { setFile(event.target.files?.[0] || null); }

  return <main className="page">
    <nav className="nav"><div className="brand"><span className="brand-mark">L</span><span>LocaleNLP</span></div><div className="nav-status"><span className="status-dot" /> Translation API</div></nav>
    <section className="hero"><div className="hero-copy"><p className="kicker">LOCAL LANGUAGES · AI TRANSLATION</p><h1>Translate language.<br /><em>Connect people.</em></h1><p className="hero-text">Translate text and documents between English, Wolof and Hausa using LocaleNLP fine-tuned MarianMT models.</p></div>
      <div className="translator-card"><div className="language-bar"><div className="language-select"><label>FROM</label><select value={source} onChange={e => setSource(e.target.value)}>{Object.entries(languageNames).map(([code, name]) => <option key={code} value={code}>{name}</option>)}</select></div><button className="swap" onClick={swapLanguages} aria-label="Swap languages">⇄</button><div className="language-select right"><label>TO</label><select value={target} onChange={e => setTarget(e.target.value)}>{availableTargets.map(code => <option key={code} value={code}>{languageNames[code]}</option>)}</select></div></div>
        <div className="panels"><div className="panel"><textarea value={text} onChange={e => setText(e.target.value)} placeholder="Type or paste your text here..." /><div className="panel-footer"><span>{text.length.toLocaleString()} characters</span><label className="file-button">Upload file<input type="file" accept=".pdf,.docx,.html,.htm,.md,.srt,.txt,.text" onChange={onFileChange} /></label></div>{file && <div className="file-chip">📄 {file.name}</div>}</div><div className="panel output"><div className="output-label">TRANSLATION</div><div className={`output-text ${result ? "" : "placeholder"}`}>{result || "Your translation will appear here."}</div><div className="panel-footer"><span>{result.length.toLocaleString()} characters</span>{result && <button className="copy" onClick={() => navigator.clipboard.writeText(result)}>Copy</button>}</div></div></div>
        {error && <div className="error">{error}</div>}<div className="actions">{file ? <button className="primary" onClick={translateFile} disabled={loading}>{loading ? "Processing..." : "Translate file →"}</button> : <button className="primary" onClick={translateText} disabled={loading || !text.trim()}>{loading ? "Translating..." : "Translate →"}</button>}</div>
      </div></section>
    <section className="features"><div><strong>4</strong><span>translation models</span></div><div><strong>6+</strong><span>document formats</span></div><div><strong>AI</strong><span>speech transcription ready</span></div></section>
    <footer><span>LocaleNLP</span><span>Built for African language technology.</span></footer>
  </main>;
}
