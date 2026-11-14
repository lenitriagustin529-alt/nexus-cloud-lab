import os
import time
from datetime import datetime, timezone

import psycopg
import redis
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)
DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ["REDIS_URL"]
CACHE_TTL = int(os.getenv("CACHE_TTL", "30"))
APP_NAME = os.getenv("APP_NAME", "NEXUS | Cloud Operations")
STUDENT_NAME = os.getenv("STUDENT_NAME", "Mahasiswa")
STUDENT_NPM = os.getenv("STUDENT_NPM", "-")

PAGE = r"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#080d1c">
<title>{{ app_name }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#080d1c;--panel:#111a2d;--panel2:#0d1527;--line:rgba(148,163,184,.15);--muted:#8b9ab5;--text:#edf4ff;--cyan:#5ee7f5;--violet:#a78bfa;--green:#50e3a4;--red:#fb7185}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 12% 0%,rgba(49,89,170,.22),transparent 34%),radial-gradient(ellipse at 90% 8%,rgba(124,58,237,.16),transparent 28%),var(--bg);color:var(--text);font-family:Manrope,system-ui,sans-serif;min-height:100vh}
.wrap{max-width:1180px;margin:auto;padding:30px 24px 56px}.top{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:48px}.brand{display:flex;align-items:center;gap:12px;font-weight:800;letter-spacing:.04em}.logo{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;background:linear-gradient(135deg,#5ee7f5,#8b5cf6);color:#07101d;font-size:22px;box-shadow:0 8px 30px #5ee7f533}.tag{font:11px 'DM Mono',monospace;color:var(--cyan);border:1px solid #5ee7f544;padding:8px 11px;border-radius:99px;letter-spacing:.12em}
.hero{display:grid;grid-template-columns:1.25fr .75fr;gap:28px;align-items:end;margin-bottom:30px}.eyebrow{color:var(--cyan);font:12px 'DM Mono',monospace;letter-spacing:.2em;text-transform:uppercase}.hero h1{font-size:clamp(38px,6vw,68px);line-height:1.02;letter-spacing:-.055em;margin:14px 0 18px}.hero h1 span{background:linear-gradient(90deg,var(--cyan),#b5a2ff);-webkit-background-clip:text;background-clip:text;color:transparent}.sub{color:var(--muted);line-height:1.8;max-width:650px;font-size:15px}.identity{background:linear-gradient(145deg,#172541,#111a2d);border:1px solid var(--line);border-radius:20px;padding:22px}.identity small,.metric small{color:var(--muted);font:11px 'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase}.identity strong{display:block;font-size:18px;margin:9px 0 4px}.identity p{margin:0;color:var(--muted);font:12px 'DM Mono',monospace}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:28px 0}.metric{background:linear-gradient(150deg,rgba(20,32,54,.96),rgba(13,21,39,.96));border:1px solid var(--line);border-radius:18px;padding:20px;min-height:130px}.metric-head{display:flex;justify-content:space-between;align-items:center}.metric .ico{font-size:20px}.metric b{display:block;font-size:22px;margin-top:16px;letter-spacing:-.04em}.metric .state{font:11px 'DM Mono',monospace;color:var(--green);margin-top:5px}.layout{display:grid;grid-template-columns:1.1fr .9fr;gap:16px}.card{background:rgba(17,26,45,.88);border:1px solid var(--line);border-radius:20px;padding:24px;box-shadow:0 18px 50px #0002}.card h2{font-size:17px;margin:0 0 7px}.hint{color:var(--muted);font-size:12px;line-height:1.7;margin:0 0 20px}.form{display:flex;gap:10px;margin:16px 0 20px}.form input{min-width:0;flex:1;background:#080f20;border:1px solid #293852;color:var(--text);padding:13px 14px;border-radius:12px;font:13px Manrope;outline:none}.form input:focus{border-color:var(--cyan);box-shadow:0 0 0 3px #5ee7f51c}.btn{border:0;border-radius:12px;padding:0 18px;background:linear-gradient(100deg,#5ee7f5,#9c8cff);color:#07101d;font-weight:800;cursor:pointer}.btn:hover{filter:brightness(1.08)}.notes{display:grid;gap:9px}.note{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:12px 14px;background:#0b1425;border:1px solid var(--line);border-radius:12px}.note span{font-size:13px;overflow-wrap:anywhere}.note time{color:var(--muted);font:10px 'DM Mono',monospace;white-space:nowrap}.empty{padding:18px;text-align:center;color:var(--muted);font-size:12px;border:1px dashed #34445f;border-radius:12px}.stack{display:grid;gap:12px}.service{display:flex;align-items:center;justify-content:space-between;padding:14px;background:#0b1425;border:1px solid var(--line);border-radius:13px}.service-left{display:flex;align-items:center;gap:12px}.dot{width:9px;height:9px;border-radius:50%;background:var(--green);box-shadow:0 0 12px #50e3a4aa}.service strong{font-size:13px}.service small{display:block;color:var(--muted);font:10px 'DM Mono',monospace;margin-top:4px}.online{font:10px 'DM Mono',monospace;color:var(--green)}.cache{margin-top:16px;border:1px solid #8b5cf644;background:#8b5cf611;border-radius:13px;padding:14px;color:#c8bbff;font-size:12px;line-height:1.7}.foot{display:flex;justify-content:space-between;gap:14px;margin-top:28px;padding-top:18px;border-top:1px solid var(--line);color:#64748b;font:10px 'DM Mono',monospace;letter-spacing:.08em}
.toast{position:fixed;right:22px;bottom:22px;background:#13233b;border:1px solid #5ee7f566;padding:13px 17px;border-radius:12px;font-size:13px;display:none;box-shadow:0 12px 40px #0008}
@media(max-width:850px){.hero,.layout{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}.top{margin-bottom:34px}}@media(max-width:480px){.wrap{padding:20px 15px 40px}.metrics{gap:9px}.metric{padding:15px;min-height:112px}.metric b{font-size:18px}.form{flex-direction:column}.btn{padding:13px}.tag{font-size:9px}}
</style></head>
<body><main class="wrap">
<header class="top"><div class="brand"><div class="logo">N</div><div>NEXUS<span style="color:var(--cyan)">.</span> STACK</div></div><div class="tag">DOCKER COMPOSE / LIVE</div></header>
<section class="hero"><div><div class="eyebrow">● SYSTEM ONLINE · CLOUD LAB</div><h1>One stack.<br><span>Four services.</span></h1><p class="sub">Aplikasi demonstrasi arsitektur container modern. Kelola data, uji cache, dan pantau komunikasi antarlayanan dalam satu dashboard.</p></div>
<div class="identity"><small>PROJECT OWNER</small><strong>{{ student_name }}</strong><p>NPM // {{ student_npm }}</p></div></section>
<section class="metrics">
<div class="metric"><div class="metric-head"><small>WEB APPLICATION</small><span class="ico">◈</span></div><b>Flask + Gunicorn</b><div class="state">● RUNNING</div></div>
<div class="metric"><div class="metric-head"><small>DATABASE</small><span class="ico">▤</span></div><b>PostgreSQL 16</b><div class="state">● CONNECTED</div></div>
<div class="metric"><div class="metric-head"><small>CACHE ENGINE</small><span class="ico">ϟ</span></div><b>Redis 7</b><div class="state">● CONNECTED</div></div>
<div class="metric"><div class="metric-head"><small>GATEWAY</small><span class="ico">⌘</span></div><b>Nginx Proxy</b><div class="state">● ROUTING</div></div>
</section>
<section class="layout">
<div class="card"><h2>Persistent Data Workspace</h2><p class="hint">Tambahkan catatan uji. Data disimpan ke PostgreSQL dan tetap tersedia setelah container dibuat ulang selama named volume tidak dihapus.</p>
<form class="form" id="noteForm"><input id="noteInput" maxlength="180" placeholder="Tulis data uji, mis. Data praktikum pertama..." required><button class="btn" type="submit">Simpan data ↗</button></form>
<div class="notes" id="notes"><div class="empty">Memuat data dari database…</div></div></div>
<div class="card"><h2>Service Observability</h2><p class="hint">Status koneksi aktual yang diperiksa oleh backend aplikasi.</p>
<div class="stack">
<div class="service"><div class="service-left"><i class="dot"></i><div><strong>PostgreSQL</strong><small>DATABASE / PORT 5432</small></div></div><span class="online" id="dbStatus">CHECKING</span></div>
<div class="service"><div class="service-left"><i class="dot"></i><div><strong>Redis Cache</strong><small>IN-MEMORY / PORT 6379</small></div></div><span class="online" id="redisStatus">CHECKING</span></div>
<div class="service"><div class="service-left"><i class="dot"></i><div><strong>Application API</strong><small>GUNICORN / PORT 5000</small></div></div><span class="online">ONLINE</span></div>
</div><div class="cache" id="cacheInfo">Cache Redis akan menampilkan status HIT atau MISS saat data dimuat.</div></div>
</section>
<footer class="foot"><span>NEXUS CLOUD LAB · ADVANCED DOCKER</span><span>REVERSE PROXY → APP → DATA LAYER</span></footer>
</main><div class="toast" id="toast"></div>
<script>
const $=id=>document.getElementById(id);
function toast(msg){$('toast').textContent=msg;$('toast').style.display='block';setTimeout(()=>$('toast').style.display='none',2600)}
async function loadNotes(){try{const r=await fetch('/api/notes');const d=await r.json();$('notes').innerHTML=d.notes.length?d.notes.map(n=>`<div class="note"><span>${escapeHtml(n.content)}</span><time>${n.created_at}</time></div>`).join(''):'<div class="empty">Belum ada data. Tambahkan catatan pertamamu.</div>';$('dbStatus').textContent='CONNECTED';$('redisStatus').textContent=d.redis_connected?'CONNECTED':'OFFLINE';$('redisStatus').style.color=d.redis_connected?'var(--green)':'var(--red)';$('cacheInfo').textContent=`REDIS CACHE: ${d.cache} · ${d.redis_connected?'AVAILABLE':'UNAVAILABLE / FALLBACK TO DATABASE'} · TTL ${d.ttl}s · ${d.notes.length} data ditampilkan`;}catch(e){$('cacheInfo').textContent='Koneksi API gagal. Periksa status service.'}}
function escapeHtml(s){return s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
$('noteForm').addEventListener('submit',async e=>{e.preventDefault();const content=$('noteInput').value.trim();if(!content)return;const r=await fetch('/api/notes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({content})});const d=await r.json();if(r.ok){$('noteInput').value='';toast('Data berhasil disimpan ke PostgreSQL');loadNotes()}else toast(d.error||'Gagal menyimpan data')});
loadNotes();setInterval(loadNotes,15000);
</script></body></html>"""


def db_conn():
    return psycopg.connect(DATABASE_URL, connect_timeout=3)


def redis_conn():
    return redis.Redis.from_url(REDIS_URL, socket_connect_timeout=2, socket_timeout=2, decode_responses=True)


def init_db():
    with db_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id BIGSERIAL PRIMARY KEY,
                content VARCHAR(180) NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)


@app.get("/")
def index():
    return render_template_string(PAGE, app_name=APP_NAME, student_name=STUDENT_NAME, student_npm=STUDENT_NPM)


@app.get("/api/health")
def health():
    checks = {"database": False, "redis": False}
    try:
        with db_conn() as conn:
            conn.execute("SELECT 1")
        checks["database"] = True
    except Exception:
        pass
    try:
        checks["redis"] = bool(redis_conn().ping())
    except Exception:
        pass
    return jsonify(status="ok" if all(checks.values()) else "degraded", services=checks), (200 if all(checks.values()) else 503)


@app.get("/api/notes")
def get_notes():
    cache_status = "MISS"
    notes = None
    try:
        client = redis_conn()
        cached = client.get("nexus:notes")
        if cached:
            import json
            notes = json.loads(cached)
            cache_status = "HIT"
    except Exception:
        client = None

    if notes is None:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, content, to_char(created_at AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI:SS') AS created_at FROM notes ORDER BY id DESC LIMIT 8"
            ).fetchall()
        notes = [{"id": r[0], "content": r[1], "created_at": r[2] + " UTC"} for r in rows]
        if client:
            import json
            try:
                client.setex("nexus:notes", CACHE_TTL, json.dumps(notes))
            except Exception:
                pass
    return jsonify(
        notes=notes,
        cache=cache_status,
        ttl=CACHE_TTL,
        redis_connected=(client is not None)
    )


@app.post("/api/notes")
def create_note():
    payload = request.get_json(silent=True) or {}
    content = str(payload.get("content", "")).strip()
    if not content or len(content) > 180:
        return jsonify(error="Isi catatan wajib 1–180 karakter."), 400
    try:
        with db_conn() as conn:
            row = conn.execute(
                "INSERT INTO notes (content) VALUES (%s) RETURNING id",
                (content,)
            ).fetchone()
        try:
            redis_conn().delete("nexus:notes")
        except Exception:
            pass
        return jsonify(message="created", id=row[0]), 201
    except Exception:
        return jsonify(error="Database tidak dapat dihubungi. Periksa service PostgreSQL."), 503


@app.get("/api/stats")
def stats():
    try:
        with db_conn() as conn:
            count = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        return jsonify(total_notes=count, database="connected")
    except Exception:
        return jsonify(error="database unavailable"), 503


@app.errorhandler(404)
def not_found(_):
    return jsonify(error="endpoint not found"), 404


# Initialize schema with a short retry window while PostgreSQL becomes ready.
for attempt in range(15):
    try:
        init_db()
        break
    except Exception:
        if attempt == 14:
            raise
        time.sleep(2)
