# NEXUS Cloud Lab — Advanced Docker Compose

Proyek demonstrasi empat service: Flask Web Application, PostgreSQL, Redis, dan Nginx Reverse Proxy. Dibuat untuk praktikum Docker Compose pada macOS (Apple Silicon/M3).

## 1. Arsitektur

- **Nginx** menerima HTTP dari host pada `http://localhost:8081` lalu meneruskan request ke `web:5000`.
- **Web** menjalankan Flask melalui Gunicorn. Backend berkomunikasi dengan PostgreSQL dan Redis menggunakan nama DNS service Compose (`db`, `redis`).
- **PostgreSQL** menyimpan catatan secara permanen pada named volume `advanced_postgres_data`.
- **Redis** menyimpan cache daftar catatan dengan TTL 30 detik. Cache bukan sumber data permanen.

### Network

- `advanced_frontend`: Nginx ↔ Web.
- `advanced_backend` (internal): Web ↔ PostgreSQL dan Redis. Nginx tidak tergabung ke backend; database/cache tidak dipublikasikan ke host.

### Volume

- `advanced_postgres_data`: `/var/lib/postgresql/data`.
- `advanced_redis_data`: `/data` (Redis AOF aktif).

## 2. Persiapan

```bash
cp .env.example .env
```

Edit `.env`, ganti `DB_PASSWORD` dengan password lokal yang kuat. Jangan commit `.env` ke repository.

Validasi dan build:

```bash
docker compose config
docker compose config --services
docker compose build
docker compose up -d
docker compose ps
```

Buka `http://localhost:8081`.

## 3. Pengujian aplikasi dan antarkontainer

```bash
curl -i http://localhost:8081/api/health
curl -s http://localhost:8081/api/stats
docker compose exec db pg_isready -U nexus_user -d nexus_db
docker compose exec redis redis-cli ping
docker compose exec web python -c "import socket; print('db:', socket.gethostbyname('db')); print('redis:', socket.gethostbyname('redis'))"
docker network ls
docker volume ls
```

Sesuaikan nama DB/user dengan `.env` bila diubah.

Uji cache: buka `/api/notes` dua kali. Respons pertama umumnya `MISS`, berikutnya `HIT` selama cache masih valid. Tambah catatan melalui web; aplikasi menghapus cache agar data baru segera terlihat.

## 4. Tantangan wajib

### Uji A — Hapus container, data tetap ada

1. Tambah catatan unik melalui browser, misalnya `DATA-PERSIST-2026-01`.
2. Buktikan data tersimpan:
   ```bash
   docker compose exec db psql -U nexus_user -d nexus_db -c "SELECT id, content, created_at FROM notes ORDER BY id DESC;"
   ```
3. Hapus container dan buat ulang tanpa menghapus volume:
   ```bash
   docker compose down
   docker compose up -d
   docker compose ps
   ```
4. Muat ulang browser dan jalankan SELECT lagi. Catatan harus tetap ada.

**Penting:** `docker compose down -v` menghapus named volume dan data. Jangan jalankan perintah itu pada pengujian persistensi.

### Uji B — Hentikan service

Gunakan Redis agar efek degradasi cache mudah diamati:

```bash
docker compose stop redis
curl -i http://localhost:8081/api/health
curl -i http://localhost:8081/api/notes
docker compose start redis
docker compose ps
```

Halaman dan pembacaan data tetap berfungsi karena PostgreSQL adalah sumber data utama. Status health menjadi `degraded` saat Redis berhenti. Catatan baru tetap dapat disimpan; cache dilewati sampai Redis aktif kembali.

Alternatif demonstrasi dampak yang lebih jelas: jalankan `docker compose stop web`, lalu akses `http://localhost:8081`. Pada pengujian ini, Nginx menghasilkan respons HTTP 504 Gateway Time-out. Log Nginx juga menunjukkan respons HTTP 502 Bad Gateway ketika koneksi menuju backend tidak tersedia. Hasil dapat berbeda bergantung pada kondisi koneksi dan waktu respons. Pulihkan layanan dengan `docker compose start web`, kemudian pastikan seluruh container kembali sehat menggunakan `docker compose ps`. Setelah pemulihan, akses aplikasi kembali dan pastikan menghasilkan HTTP 200 OK.

### Uji C — Salah konfigurasi sengaja, lalu perbaiki

1. Simpan konfigurasi:
   ```bash
   cp nginx/default.conf nginx/default.conf.bak
   ```
2. Ubah sementara `proxy_pass http://web:5000;` menjadi `proxy_pass http://web:5999;`.
3. Terapkan dan amati error:
   ```bash
   docker compose restart nginx
   curl -i http://localhost:8081
   docker compose logs --tail=30 nginx
   ```
   Nama service `web` tetap dapat ditemukan, tetapi port 5999 tidak menyediakan layanan sehingga Nginx mengembalikan 502 Bad Gateway. Log menunjukkan connection refused.
4. Pulihkan:
   ```bash
   mv nginx/default.conf.bak nginx/default.conf
   docker compose restart nginx
   curl -i http://localhost:8081/api/health
   ```

### Uji D — Restart resilience (tantangan tambahan)

```bash
docker compose restart
docker compose ps
curl -i http://localhost:8081/api/health
```

Tunjukkan `restart: unless-stopped`, healthcheck, dan `depends_on: condition: service_healthy`.

## 5. Troubleshooting umum

- **Port 8081 sudah digunakan:** ubah mapping Nginx di Compose menjadi `"8081:80"`, lalu `docker compose up -d`.
- **Container web unhealthy:** `docker compose logs web`; pastikan `.env` benar dan DB/Redis healthy.
- **502 Bad Gateway:** `docker compose ps`, `docker compose logs nginx web`; periksa upstream `web:5000` dan network `frontend`.
- **Database gagal login:** samakan `DB_NAME`, `DB_USER`, `DB_PASSWORD` di `.env`; bila volume lama dibuat dengan kredensial berbeda, jangan hapus volume sebelum data diamankan.
- **Build gagal:** `docker compose build --no-cache web`.

## 6. Perintah demonstrasi ringkas

```bash
docker compose config
docker compose build
docker compose up -d
docker compose ps
docker compose logs --tail=30
curl -i http://localhost:8081/api/health
docker network inspect advanced_frontend
docker network inspect advanced_backend
docker volume inspect advanced_postgres_data
docker compose down
docker compose up -d
```

## 7. Catatan keamanan dan batasan

Password `.env` hanya untuk lingkungan praktikum lokal. Jangan unggah `.env` ke GitHub. Pada produksi gunakan secret management, TLS, pembatasan akses, backup database, dan kebijakan resource. UI memakai Google Fonts bila internet tersedia; aplikasi tetap berfungsi tanpa font eksternal.

## 8. Identitas dan pengumpulan

Nama: Leni Tri Agustin  
NPM: 2024606601020  
Kelas: Semester 5  
Judul video: `TKA_2024606601020_ADVANCED_DOCKER`  
Kode tantangan dosen: isi sesuai kode yang benar-benar diberikan dosen. Jangan menebak atau menggunakan kode tugas lain.
