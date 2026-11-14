# Naskah Demonstrasi Video (target 25–30 menit)

**Catatan rekaman:** gunakan OBS/QuickTime dengan layar terminal + browser. Aktifkan webcam sebagai picture-in-picture saat menjelaskan. Jangan hanya membaca slide. Semua hasil harus direkam langsung.

## 1. Opening — 1 menit
"Assalamualaikum warahmatullahi wabarakatuh. Perkenalkan, saya Leni Tri Agustin, NPM 2024606601020, dari kelas semester 5. Pada video ini saya mendemonstrasikan pembangunan aplikasi menggunakan Docker Compose dengan empat service, yaitu Web Application, PostgreSQL, Redis, dan Nginx Reverse Proxy."

## 2. Analisis arsitektur — 3 menit
Tampilkan diagram pada README atau jelaskan alur: Browser → Nginx → Flask/Gunicorn → PostgreSQL dan Redis. Jelaskan Nginx sebagai pintu masuk, Flask sebagai logika aplikasi, PostgreSQL sebagai penyimpanan permanen, Redis sebagai cache. Jelaskan frontend network dan backend internal network serta named volume.

## 3. Dockerfile dan aplikasi — 4 menit
Tampilkan `app/Dockerfile`, `requirements.txt`, dan `app/app.py`. Jelaskan base image Python slim, dependency, user non-root, Gunicorn, endpoint health, query parameterized, dan cache Redis dengan TTL.

## 4. Docker Compose — 5 menit
Tampilkan `compose.yaml`. Jelaskan empat service, build/image, port/expose, environment, `depends_on` dengan healthcheck, restart policy, dua network, dan dua named volume. Jalankan:
```bash
docker compose config
docker compose build
docker compose up -d
docker compose ps
```

## 5. Tampilan dan komunikasi — 3 menit
Buka `http://localhost:8080`, tambahkan catatan dari dashboard. Jalankan:
```bash
curl -i http://localhost:8080/api/health
curl -s http://localhost:8080/api/stats
docker compose exec redis redis-cli ping
docker compose exec db pg_isready -U nexus_user -d nexus_db
docker network ls
docker volume ls
```
Tunjukkan cache MISS/HIT dengan membuka `/api/notes` dua kali melalui browser atau `curl`.

## 6. Tantangan wajib — 6–8 menit
**A. Persistensi:** simpan catatan unik, query PostgreSQL, `docker compose down`, lalu `docker compose up -d`. Buktikan catatan masih ada. Tegaskan tidak menggunakan `-v`.

**B. Stop service:** `docker compose stop redis`. Uji health dan notes. Jelaskan aplikasi masih dapat membaca database namun health berstatus degraded karena cache tidak tersedia. Jalankan `docker compose start redis`. Opsional, stop `web` untuk melihat 502 dari Nginx lalu pulihkan.

**C. Misconfiguration:** ubah port upstream Nginx ke 5999, restart Nginx, tunjukkan 502 dan log connection refused. Kembalikan `web:5000`, restart, lalu buktikan endpoint sehat.

## 7. Tantangan tambahan / restart resilience — 2 menit
Jalankan `docker compose restart`, cek `docker compose ps`, dan endpoint health. Jelaskan `restart: unless-stopped` dan healthcheck. Jika dosen memberi tantangan berbeda, kerjakan sesuai instruksi dosen saat itu.

## 8. Kesimpulan — 1–2 menit
"Praktikum berhasil membangun empat service yang terhubung melalui Docker Compose. Nginx menjadi reverse proxy, Flask menjalankan aplikasi, PostgreSQL menyimpan data persisten melalui named volume, dan Redis mempercepat pembacaan melalui cache. Pengujian membuktikan data tetap tersimpan setelah container dibuat ulang, aplikasi menunjukkan dampak saat service dihentikan, dan kesalahan konfigurasi dapat ditemukan melalui log lalu diperbaiki. Terima kasih."

## Tips teknis rekaman
- Pastikan wajah terlihat saat opening, penjelasan arsitektur, dan kesimpulan.
- Perbesar terminal dan browser agar teks terbaca.
- Uji mikrofon dan lakukan rekaman 20 detik sebelum mulai.
- Upload YouTube dengan status **Unlisted**, bukan Public atau Private.
- Judul: `TKA_2024606601020_ADVANCED_DOCKER`.
