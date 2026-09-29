const express = require('express'), fs = require('fs'), path = require('path');
const app = express();
const ON_VERCEL = !!process.env.VERCEL, LIM = ON_VERCEL ? '4mb' : '50mb';
const PAGES_ORIGIN = process.env.PAGES_ORIGIN || 'https://boobalanashokan.github.io';

app.use((req, res, next) => {
  const origin = req.headers.origin;
  if (origin === PAGES_ORIGIN) {
    res.set('Access-Control-Allow-Origin', origin);
    res.set('Access-Control-Allow-Credentials', 'true');
    res.set('Access-Control-Allow-Headers', 'Authorization, Content-Type');
    res.set('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS');
    res.vary('Origin');
  }
  if (req.method === 'OPTIONS') return origin === PAGES_ORIGIN ? res.sendStatus(204) : res.sendStatus(403);
  next();
});

// Optional password (set APP_PASSWORD). Any username works.
const PASS = process.env.APP_PASSWORD;
if (PASS) app.use((req, res, next) => {
  const [, p] = Buffer.from((req.headers.authorization || '').split(' ')[1] || '', 'base64').toString().split(/:(.*)/s);
  if (p === PASS) return next();
  res.set('WWW-Authenticate', 'Basic realm="Notes"').status(401).send('Login required');
});
app.use(express.json({ limit: LIM }));
app.use(express.static(path.join(__dirname, 'public')));

// ---- storage: a private GitHub repo (GH_TOKEN + GH_REPO), else local files ----
let S;
if (process.env.GH_TOKEN && process.env.GH_REPO) {
  const BR = process.env.GH_BRANCH || 'main', API = `https://api.github.com/repos/${process.env.GH_REPO}/contents/`;
  const H = a => ({ Authorization: 'Bearer ' + process.env.GH_TOKEN, Accept: a || 'application/vnd.github+json', 'User-Agent': 'learning-notes', 'X-GitHub-Api-Version': '2022-11-28' });
  const shaOf = async p => {           // sha comes from the folder listing (works for files > 1 MB too)
    const r = await fetch(API + path.posix.dirname(p) + '?ref=' + BR, { headers: H() });
    if (r.status === 404) return null;
    if (!r.ok) throw new Error('GitHub ' + r.status);
    return ((await r.json()).find(x => x.name === path.posix.basename(p)) || {}).sha || null;
  };
  const putF = async (p, buf, msg) => {
    const sha = await shaOf(p);
    const r = await fetch(API + p, { method: 'PUT', headers: H(), body: JSON.stringify({ message: msg, content: Buffer.from(buf).toString('base64'), branch: BR, ...(sha ? { sha } : {}) }) });
    if (!r.ok) throw new Error('GitHub ' + r.status + ' ' + await r.text());
  };
  const getF = async p => {
    const r = await fetch(API + p + '?ref=' + BR, { headers: H('application/vnd.github.raw+json') });
    if (r.status === 404) return null;
    if (!r.ok) throw new Error('GitHub ' + r.status);
    return Buffer.from(await r.arrayBuffer());
  };
  S = {
    async read() { const b = await getF('data/db.json'); return b && b.toString('utf8'); },
    async write(t) { await putF('data/db.json', Buffer.from(t), 'notes: session save ' + new Date().toISOString()); },
    async put(id, buf) { await putF('data/uploads/' + id, buf, 'attach: ' + id); },
    get: id => getF('data/uploads/' + id),
    async del(id) { const p = 'data/uploads/' + id, sha = await shaOf(p); if (sha) await fetch(API + p, { method: 'DELETE', headers: H(), body: JSON.stringify({ message: 'remove ' + id, sha, branch: BR }) }); },
  };
} else if (ON_VERCEL) {
  throw new Error('Vercel storage is not configured. Set GH_TOKEN and GH_REPO in the Vercel project environment.');
} else {
  const DIR = path.join(__dirname, 'data'), UP = path.join(DIR, 'uploads'), DB = path.join(DIR, 'db.json');
  fs.mkdirSync(UP, { recursive: true });
  S = {
    async read() { return fs.existsSync(DB) ? fs.readFileSync(DB, 'utf8') : null; },
    async write(t) { fs.writeFileSync(DB + '.tmp', t); fs.renameSync(DB + '.tmp', DB); },
    async put(id, buf) { fs.writeFileSync(path.join(UP, id), buf); },
    async get(id) { const p = path.join(UP, id); return fs.existsSync(p) ? fs.readFileSync(p) : null; },
    async del(id) { const p = path.join(UP, id); if (fs.existsSync(p)) fs.unlinkSync(p); },
  };
}

const A = f => (q, r) => f(q, r).catch(e => { console.error(e); r.status(500).send(String(e)); });
app.get('/api/data', A(async (q, r) => { const t = await S.read(); t ? r.type('json').send(t) : r.sendStatus(404); }));
app.put('/api/data', A(async (q, r) => {
  if (!q.query.force) {                // another device saved since this one loaded?
    const cur = await S.read();
    if (cur && (JSON.parse(cur).rev || 0) !== Number(q.query.base || 0)) return r.sendStatus(409);
  }
  await S.write(JSON.stringify(q.body)); r.json({ ok: true });
}));
app.post('/api/upload', express.raw({ type: () => true, limit: LIM }), A(async (q, r) => {
  const name = String(q.query.name || 'file').replace(/[^\w.\-]+/g, '_').slice(-80);
  const file = Date.now().toString(36) + '-' + name;
  await S.put(file, q.body); r.json({ file });
}));
app.get('/files/:f', A(async (q, r) => {
  const f = path.basename(q.params.f), b = await S.get(f);
  b ? r.type(path.extname(f) || 'bin').set('Cache-Control', 'private, max-age=3600').send(b) : r.sendStatus(404);
}));
app.delete('/api/upload/:f', A(async (q, r) => { await S.del(path.basename(q.params.f)); r.json({ ok: true }); }));

if (!ON_VERCEL) app.listen(3000, '0.0.0.0', () => console.log('Running on http://localhost:3000'));
module.exports = app;