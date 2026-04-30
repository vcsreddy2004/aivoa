// services/api.ts
export const generateForm = async (text: string) => {
  const res = await fetch("http://localhost:8000/generate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ text }),
  });
  return res.json();
};