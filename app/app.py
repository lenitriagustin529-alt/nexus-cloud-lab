import os
import time
from flask import Flask, jsonify, render_template_string, request
import psycopg
import redis

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
<meta name="theme-color" content="#0a1020"><title>{{ title }} · {{ app_name }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#0a1020;--panel:#111b30;--panel2:#0d1729;--line:rgba(151,170,205,.14);--muted:#8796b2;--text:#edf3ff;--cyan:#62e6ef;--blue:#7d9cff;--green:#42d6a0;--red:#ff718b;--sidebar:250px}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:Manrope,system-ui,sans-serif;min-height:100vh}a{color:inherit}
.sidebar{position:fixed;inset:0 auto 0 0;width:var(--sidebar);padding:27px 18px;background:#0c1426;border-right:1px solid var(--line);display:flex;flex-direction:column;z-index:5}
.brand{display:flex;align-items:center;gap:12px;padding:0 10px 30px}.logo{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;background:linear-gradient(135deg,var(--cyan),#7c8dff);color:#07101d;font-size:21px;font-weight:900}.brand-name{font-weight:800;letter-spacing:.08em}.brand-name span{color:var(--cyan)}.brand small{display:block;color:var(--muted);font:9px 'DM Mono',monospace;letter-spacing:.16em;margin-top:4px}
.nav-label{padding:12px 12px 9px;color:#61718f;font:10px 'DM Mono',monospace;letter-spacing:.16em}.nav{display:grid;gap:6px}.nav a{display:flex;align-items:center;gap:12px;padding:13px 12px;border-radius:11px;color:#9eacc5;text-decoration:none;font-size:12px;font-weight:700;transition:.2s}.nav a:hover,.nav a.active{background:linear-gradient(100deg,#18314b,#17243b);color:#eafaff}.nav a.active{box-shadow:inset 3px 0 var(--cyan)}.nav-icon{width:20px;text-align:center;font-size:16px;color:var(--cyan)}
.side-status{margin-top:auto;padding:15px;background:#111e32;border:1px solid var(--line);border-radius:14px}.side-status small{display:block;color:var(--muted);font:9px 'DM Mono',monospace;letter-spacing:.12em}.side-status strong{display:flex;align-items:center;gap:8px;margin-top:10px;font-size:12px}.pulse{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 12px var(--green)}
.main{margin-left:var(--sidebar);padding:28px clamp(20px,3vw,46px) 35px;max-width:1700px}.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:34px}.crumb{font-size:11px;color:var(--muted)}.crumb b{color:var(--text)}.live{padding:8px 12px;border:1px solid #42d6a033;background:#42d6a00c;border-radius:99px;color:var(--green);font:10px 'DM Mono',monospace;letter-spacing:.08em}
.welcome{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin-bottom:26px}.eyebrow{color:var(--cyan);font:10px 'DM Mono',monospace;letter-spacing:.2em;text-transform:uppercase}.welcome h1{font-size:clamp(29px,3.4vw,43px);letter-spacing:-.05em;margin:10px 0 8px}.welcome h1 span{color:var(--cyan)}.welcome p{margin:0;color:var(--muted);font-size:12px;line-height:1.7;max-width:760px}.owner,.panel,.metric,.service-card{background:linear-gradient(150deg,#15223a,#101a2d);border:1px solid var(--line);border-radius:15px}.owner{padding:13px 16px;min-width:205px}.owner small,.tiny{color:var(--muted);font:9px 'DM Mono',monospace;letter-spacing:.12em}.owner strong{display:block;font-size:12px;margin:6px 0}.owner span{color:var(--cyan);font:10px 'DM Mono',monospace}
.section-head{display:flex;justify-content:space-between;align-items:center;margin:27px 0 13px}.section-head h2,.panel h2{font-size:13px;margin:0}.section-head span{color:var(--muted);font:9px 'DM Mono',monospace;letter-spacing:.1em}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px}.metric{padding:18px;min-height:120px}.metric small{color:var(--muted);font:9px 'DM Mono',monospace;letter-spacing:.1em}.metric b{display:block;font-size:19px;margin-top:14px}.subline{font:9px 'DM Mono',monospace;color:var(--green);margin-top:5px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.panel{padding:19px;min-width:0}.panel p{color:var(--muted);font-size:11px;line-height:1.7}.service-card{padding:17px;background:#0b1527}.service-card h3{font-size:13px;margin:0 0 7px}.service-card p{margin:0}.tag{display:inline-block;margin-top:12px;color:var(--green);font:9px 'DM Mono',monospace}
.rows{display:grid;gap:8px}.rowitem{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px;background:#0b1527;border:1px solid var(--line);border-radius:10px;font-size:11px}.rowitem span{color:var(--muted)}.rowitem b{font:10px 'DM Mono',monospace}
.form{display:flex;gap:8px;margin:14px 0}.form input{flex:1;min-width:0;background:#091324;border:1px solid #2b3b57;color:var(--text);padding:12px;border-radius:10px;font-size:11px}.btn{border:0;border-radius:10px;padding:0 16px;background:linear-gradient(100deg,var(--cyan),#8ca5ff);color:#07101d;font-size:10px;font-weight:800;cursor:pointer}.btn:hover{filter:brightness(1.08)}.notes{display:grid;gap:8px}.note{display:flex;justify-content:space-between;gap:10px;padding:12px;background:#0b1527;border:1px solid var(--line);border-radius:10px;font-size:10px}.note time{color:var(--muted);font:8px 'DM Mono',monospace;white-space:nowrap}.empty{padding:18px;text-align:center;color:var(--muted);font-size:11px;border:1px dashed #34445f;border-radius:10px}
.activity{display:grid;gap:0}.event{display:flex;gap:12px;padding:16px 0;border-bottom:1px solid var(--line)}.event:last-child{border:0}.dot{width:8px;height:8px;border-radius:50%;background:var(--cyan);margin-top:5px;flex:none}.event strong{font-size:11px}.event p{margin:5px 0 0}.footer{margin-top:28px;padding-top:16px;border-top:1px solid var(--line);color:#64748b;font:8px 'DM Mono',monospace;letter-spacing:.1em}.toast{position:fixed;right:22px;bottom:22px;background:#152641;border:1px solid #62e6ef66;padding:12px 16px;border-radius:11px;font-size:11px;display:none;z-index:10}
@media(max-width:1050px){.metrics{grid-template-columns:repeat(2,1fr)}}@media(max-width:720px){.sidebar{position:static;width:auto;padding:15px 17px}.brand{padding:0 0 14px}.nav-label{display:none}.nav{display:flex;overflow:auto}.nav a{white-space:nowrap;padding:10px}.side-status{display:none}.main{margin:0;padding:20px 16px}.welcome{align-items:flex-start;flex-direction:column}.owner{width:100%}.grid{grid-template-columns:1fr}}@media(max-width:440px){.metrics{gap:8px}.metric{padding:13px}.metric b{font-size:15px}.form{flex-direction:column}.btn{padding:12px}}
</style></head>
<body>
<aside class="sidebar">
 <div class="brand"><div class="logo">N</div><div class="brand-name">NEXUS<span>.</span><small>CLOUD OPERATIONS</small></div></div>
 <div class="nav-label">WORKSPACE</div>
 <nav class="nav">
  <a href="{{ url_for('index') }}" class="{{ 'active' if page=='overview' else '' }}"><span class="nav-icon">⌂</span>Overview</a>
  <a href="{{ url_for('services_page') }}" class="{{ 'active' if page=='services' else '' }}"><span class="nav-icon">◈</span>Services</a>
  <a href="{{ url_for('database_page') }}" class="{{ 'active' if page=='database' else '' }}"><span class="nav-icon">▤</span>Database</a>
  <a href="{{ url_for('cache_page') }}" class="{{ 'active' if page=='cache' else '' }}"><span class="nav-icon">ϟ</span>Cache Monitor</a>
  <a href="{{ url_for('activity_page') }}" class="{{ 'active' if page=='activity' else '' }}"><span class="nav-icon">≋</span>Activity</a>
 </nav>
 <div class="side-status"><small>ENVIRONMENT STATUS</small><strong><i class="pulse"></i> Monitoring enabled</strong></div>
</aside>
<main class="main">
 <header class="topbar"><div class="crumb">Workspace&nbsp; / &nbsp;<b>{{ title }}</b></div><div class="live">● LIVE MONITORING</div></header>
 <section class="welcome"><div><div class="eyebrow">● CLOUD INFRASTRUCTURE / CONTROL CENTER</div><h1>{{ heading|safe }}</h1><p>{{ description }}</p></div><div class="owner"><small>PROJECT OWNER</small><strong>{{ student_name }}</strong><span>NPM // {{ student_npm }}</span></div></section>
 {% if page=='overview' %}
 <div class="section-head"><h2>Infrastructure Summary</h2><span>DOCKER COMPOSE STACK</span></div>
 <section class="metrics">
  <div class="metric"><small>WEB APPLICATION</small><b>Flask + Gunicorn</b><div class="subline">● APPLICATION SERVICE</div></div>
  <div class="metric"><small>DATABASE ENGINE</small><b>PostgreSQL 16</b><div class="subline" id="dbMetric">● CHECKING</div></div>
  <div class="metric"><small>CACHE ENGINE</small><b>Redis 7</b><div class="subline" id="redisMetric">● CHECKING</div></div>
  <div class="metric"><small>REVERSE PROXY</small><b>Nginx</b><div class="subline">● GATEWAY SERVICE</div></div>
 </section>
 <div class="section-head"><h2>Quick Access</h2><span>OPEN MODULE</span></div>
 <section class="grid">
  <a class="service-card" href="{{ url_for('services_page') }}"><h3>Service Observability →</h3><p>Lihat detail empat layanan utama dan status koneksi backend.</p><span class="tag">VIEW SERVICES</span></a>
  <a class="service-card" href="{{ url_for('database_page') }}"><h3>Persistent Database →</h3><p>Kelola catatan uji yang disimpan secara persisten di PostgreSQL.</p><span class="tag">OPEN DATABASE</span></a>
  <a class="service-card" href="{{ url_for('cache_page') }}"><h3>Redis Cache Monitor →</h3><p>Periksa status cache, cache hit/miss, dan waktu TTL.</p><span class="tag">MONITOR CACHE</span></a>
  <a class="service-card" href="{{ url_for('activity_page') }}"><h3>Activity Center →</h3><p>Lihat aktivitas sistem dan ringkasan komponen aplikasi.</p><span class="tag">VIEW ACTIVITY</span></a>
 </section>
 {% elif page=='services' %}
 <div class="section-head"><h2>Container Services</h2><span>4 CORE SERVICES</span></div>
 <section class="grid">
  <div class="service-card"><h3>◈ Web Application</h3><p>Flask application served by Gunicorn on internal port 5000.</p><span class="tag">APPLICATION · WEB</span></div>
  <div class="service-card"><h3>▤ PostgreSQL 16</h3><p>Relational database service for persistent notes storage.</p><span class="tag" id="dbStatus">CHECKING</span></div>
  <div class="service-card"><h3>ϟ Redis 7</h3><p>In-memory cache layer with configured expiration policy.</p><span class="tag" id="redisStatus">CHECKING</span></div>
  <div class="service-card"><h3>⌘ Nginx</h3><p>Reverse proxy gateway exposed to the host on port 8081.</p><span class="tag">GATEWAY · PORT 80</span></div>
 </section>
 <div class="panel" style="margin-top:14px"><h2>Connection diagnostics</h2><p id="healthInfo">Checking database and Redis connectivity...</p><button class="btn" onclick="checkHealth()" type="button">Refresh status</button></div>
 {% elif page=='database' %}
 <div class="grid">
  <div class="panel"><h2>Persistent Data Workspace</h2><p>Tambahkan catatan pengujian. Data disimpan di PostgreSQL dan tetap tersedia setelah container dibuat ulang selama named volume tidak dihapus.</p>
   <form class="form" id="noteForm"><input id="noteInput" maxlength="180" placeholder="Tulis data uji..." required><button class="btn" type="submit">Simpan data ↗</button></form>
   <div class="notes" id="notes"><div class="empty">Memuat data dari database...</div></div>
  </div>
  <div class="panel"><h2>Database Information</h2><div class="rows" style="margin-top:14px"><div class="rowitem"><span>Engine</span><b>POSTGRESQL 16</b></div><div class="rowitem"><span>Internal port</span><b>5432</b></div><div class="rowitem"><span>Storage</span><b>NAMED VOLUME</b></div><div class="rowitem"><span>Connection</span><b id="dbMetric">CHECKING</b></div><div class="rowitem"><span>Total records</span><b id="totalNotes">—</b></div></div></div>
 </div>
 {% elif page=='cache' %}
 <section class="grid">
  <div class="panel"><h2>Redis Cache Monitor</h2><p>Memantau cache catatan yang digunakan aplikasi NEXUS.</p><div class="rows"><div class="rowitem"><span>Cache engine</span><b>REDIS 7</b></div><div class="rowitem"><span>Connection</span><b id="redisStatus">CHECKING</b></div><div class="rowitem"><span>Cache result</span><b id="cacheBadge">WAITING</b></div><div class="rowitem"><span>Configured TTL</span><b>{{ cache_ttl }} SECONDS</b></div></div></div>
  <div class="panel"><h2>Cache Insight</h2><p id="cacheInfo">Memuat informasi cache dari backend aplikasi...</p><button class="btn" type="button" onclick="loadData()">Refresh cache data</button></div>
 </section>
 {% elif page=='activity' %}
 <section class="panel"><h2>Recent Activity</h2><p>Informasi aktivitas antarmuka dan komponen aplikasi.</p><div class="activity">
  <div class="event"><i class="dot"></i><div><strong>Dashboard initialized</strong><p>Frontend monitoring interface loaded.</p></div></div>
  <div class="event"><i class="dot"></i><div><strong>API polling enabled</strong><p>Service status can be refreshed from backend API.</p></div></div>
  <div class="event"><i class="dot"></i><div><strong>Persistent storage configured</strong><p>Notes are stored through PostgreSQL.</p></div></div>
  <div class="event"><i class="dot"></i><div><strong>Cache layer configured</strong><p>Redis cache uses a {{ cache_ttl }} second TTL policy.</p></div></div>
 </div></section>
 {% endif %}
 <footer class="footer">NEXUS CLOUD LAB · ADVANCED DOCKER COMPOSE</footer>
</main><div class="toast" id="toast"></div>
<script>
const $=id=>document.getElementById(id);
function toast(msg){if(!$('toast'))return;$('toast').textContent=msg;$('toast').style.display='block';setTimeout(()=>$('toast').style.display='none',2600)}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
async function loadData(){
 try{
  const r=await fetch('/api/notes');if(!r.ok)throw new Error('API unavailable');const d=await r.json();
  if($('notes'))$('notes').innerHTML=d.notes.length?d.notes.map(n=>`<div class="note"><span>${escapeHtml(n.content)}</span><time>${escapeHtml(n.created_at)}</time></div>`).join(''):'<div class="empty">Belum ada data. Tambahkan catatan pertamamu.</div>';
  if($('dbMetric'))$('dbMetric').textContent='CONNECTED';
  if($('redisMetric'))$('redisMetric').textContent=d.redis_connected?'CONNECTED':'OFFLINE';
  if($('dbStatus'))$('dbStatus').textContent='CONNECTED';
  if($('redisStatus'))$('redisStatus').textContent=d.redis_connected?'CONNECTED':'OFFLINE';
  if($('cacheBadge'))$('cacheBadge').textContent=d.cache;
  if($('cacheInfo'))$('cacheInfo').textContent=`Cache ${d.cache} · Redis ${d.redis_connected?'AVAILABLE':'UNAVAILABLE / DATABASE FALLBACK'} · TTL ${d.ttl}s · ${d.notes.length} records returned`;
 }catch(e){['dbMetric','redisMetric','dbStatus','redisStatus'].forEach(id=>{if($(id))$(id).textContent='OFFLINE'});if($('cacheInfo'))$('cacheInfo').textContent='API tidak tersedia. Periksa service Docker.'}
}
async function checkHealth(){try{const r=await fetch('/api/health');const d=await r.json();if($('healthInfo'))$('healthInfo').textContent=`Database: ${d.services.database?'CONNECTED':'OFFLINE'} · Redis: ${d.services.redis?'CONNECTED':'OFFLINE'} · Overall: ${d.status.toUpperCase()}`;loadData()}catch(e){if($('healthInfo'))$('healthInfo').textContent='Health endpoint unavailable'}}
if($('noteForm'))$('noteForm').addEventListener('submit',async e=>{e.preventDefault();const content=$('noteInput').value.trim();if(!content)return;try{const r=await fetch('/api/notes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({content})});const d=await r.json();if(r.ok){$('noteInput').value='';toast('Data berhasil disimpan ke PostgreSQL');loadData()}else toast(d.error||'Gagal menyimpan data')}catch(e){toast('Tidak dapat menghubungi API aplikasi')}});
loadData();if($('healthInfo'))checkHealth();
</script></body></html>"""

def render_page(page, title, heading, description):
    return render_template_string(
        PAGE, page=page, title=title, heading=heading,
        description=description, app_name=APP_NAME,
        student_name=STUDENT_NAME, student_npm=STUDENT_NPM,
        cache_ttl=CACHE_TTL,
    )

@app.get("/")
def index():
    return render_page("overview", "Overview", "System <span>Overview.</span>",
        "Selamat datang di pusat monitoring NEXUS Cloud Lab. Pilih modul pada navigasi untuk melihat detail setiap komponen.")

@app.get("/services")
def services_page():
    return render_page("services", "Services", "Service <span>Observability.</span>",
        "Pantau komponen utama Docker Compose dan periksa konektivitas PostgreSQL serta Redis.")

@app.get("/database")
def database_page():
    return render_page("database", "Database", "Persistent <span>Database.</span>",
        "Kelola catatan pengujian dan lihat informasi penyimpanan PostgreSQL.")

@app.get("/cache")
def cache_page():
    return render_page("cache", "Cache Monitor", "Redis <span>Cache Monitor.</span>",
        "Pantau koneksi Redis, hasil cache, dan kebijakan time-to-live aplikasi.")

@app.get("/activity")
def activity_page():
    return render_page("activity", "Activity", "System <span>Activity.</span>",
        "Lihat ringkasan aktivitas dan konfigurasi komponen NEXUS Cloud Lab.")

def db_conn():
    return psycopg.connect(DATABASE_URL, connect_timeout=3)

def redis_conn():
    return redis.Redis.from_url(
        REDIS_URL, socket_connect_timeout=2, socket_timeout=2, decode_responses=True
    )

def init_db():
    with db_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id BIGSERIAL PRIMARY KEY,
                content VARCHAR(180) NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)

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
    return jsonify(
        status="ok" if all(checks.values()) else "degraded",
        services=checks,
    ), (200 if all(checks.values()) else 503)


@app.get("/api/notes")
def get_notes():
    cache_status = "MISS"
    notes = None
    client = None
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
                "SELECT id, content, to_char(created_at AT TIME ZONE 'UTC', "
                "'YYYY-MM-DD HH24:MI:SS') AS created_at "
                "FROM notes ORDER BY id DESC LIMIT 8"
            ).fetchall()
        notes = [
            {"id": r[0], "content": r[1], "created_at": r[2] + " UTC"}
            for r in rows
        ]
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
        redis_connected=(client is not None),
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
                (content,),
            ).fetchone()
        try:
            redis_conn().delete("nexus:notes")
        except Exception:
            pass
        return jsonify(message="created", id=row[0]), 201
    except Exception:
        return jsonify(
            error="Database tidak dapat dihubungi. Periksa service PostgreSQL."
        ), 503


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
