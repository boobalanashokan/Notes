const express = require('express'), fs = require('fs'), path = require('path');
const app = express();
app.use(express.json({ limit: '20mb' }));
app.use(express.static(path.join(__dirname, 'public')));

const DIR = path.join(__dirname, 'data');
const DB = path.join(DIR, 'db.json'), SEED = path.join(DIR, 'seed.json');
fs.mkdirSync(DIR, { recursive: true });

app.get('/api/data', (req, res) => {
  if (!fs.existsSync(DB)) {
    if (fs.existsSync(SEED)) fs.copyFileSync(SEED, DB);
    else fs.writeFileSync(DB, JSON.stringify({ areas: [] }));
  }
  res.sendFile(DB);
});

app.put('/api/data', (req, res) => {
  fs.writeFileSync(DB + '.tmp', JSON.stringify(req.body, null, 1));
  fs.renameSync(DB + '.tmp', DB);
  res.json({ ok: true });
});

app.listen(3000, '0.0.0.0', () => console.log('Running on http://localhost:3000'));