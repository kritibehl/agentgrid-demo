export default async function handler(req, res) {
  try {
    const r = await fetch("https://autoops-api-126325674316.us-central1.run.app/support/ingest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });
    const data = await r.json();
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.status(r.status).json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
