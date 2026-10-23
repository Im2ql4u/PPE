// Thin wrappers around the local JSON API.
async function req(url, opts) {
  const r = await fetch(url, opts);
  if (!r.ok) {
    let detail = r.statusText;
    try { detail = (await r.json()).detail || detail; } catch { /* not JSON */ }
    throw new Error(detail);
  }
  return r.json();
}
const post = (url, body) => req(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

export const listPieces = () => req("/api/pieces");
export const getPiece = (id) => req(`/api/pieces/${id}`);
export const getScore = (id, { width, transpose, zoom }) =>
  req(`/api/pieces/${id}/score?width=${Math.round(width)}&transpose=${transpose}&scale=${zoom}`);
export const inspect = (id, sel) => post(`/api/pieces/${id}/inspect`, sel.ids ? { ids: sel.ids } : { start: sel.start, end: sel.end });
export const playback = (id, body) => post(`/api/pieces/${id}/playback`, body);
export const alternatives = (id, labelId) => req(`/api/pieces/${id}/labels/${labelId}/alternatives`);
