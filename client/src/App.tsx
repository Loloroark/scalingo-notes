import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL;

type Note = { id: number; content: string };

export default function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [content, setContent] = useState("");
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const res = await fetch(`${API}/notes`);
      setNotes(await res.json());
      setError("");
    } catch {
      setError(`API injoignable : ${API}/notes`);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const add = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch(`${API}/notes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });
    setContent("");
    load();
  };

  return (
    <main>
      <h1>Notes</h1>
      <form onSubmit={add}>
        <input value={content} onChange={(e) => setContent(e.target.value)} required />
        <button>Ajouter</button>
      </form>
      {error && <p>{error}</p>}
      <ul>
        {notes.map((n) => (
          <li key={n.id}>{n.content}</li>
        ))}
      </ul>
    </main>
  );
}
