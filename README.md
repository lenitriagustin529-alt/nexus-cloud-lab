# NEXUS Cloud Lab — Advanced Docker Compose

NEXUS Cloud Lab merupakan proyek implementasi **Advanced Docker Compose** yang mengintegrasikan empat layanan utama, yaitu Flask Web Application, PostgreSQL, Redis, dan Nginx Reverse Proxy.

Proyek ini dibuat untuk memenuhi tugas praktikum Docker Compose dengan lingkungan pengembangan macOS pada perangkat MacBook Air M3 (Apple Silicon).

Aplikasi dilengkapi dashboard modern dengan navigasi multi-halaman untuk menampilkan informasi sistem, layanan aplikasi, database, cache, dan aktivitas.

**Akses aplikasi:** http://localhost:8081

**Repository GitHub:**  
https://github.com/lenitriagustin529-alt/nexus-cloud-lab

---

## 1. Arsitektur Sistem

NEXUS Cloud Lab menggunakan arsitektur multi-container yang dikelola menggunakan Docker Compose. Setiap container memiliki fungsi berbeda dan saling berkomunikasi melalui jaringan internal Docker.

### Komponen layanan

| Service | Image/Teknologi | Fungsi |
|---|---|---|
| Web | Flask + Gunicorn | Menjalankan backend dan dashboard aplikasi |
| Database | PostgreSQL 16 Alpine | Menyimpan data aplikasi secara permanen |
| Cache | Redis 7 Alpine | Menyimpan cache untuk mempercepat akses data |
| Nginx | Nginx 1.27 Alpine | Reverse proxy dan pintu masuk aplikasi |

### Penjelasan setiap service

**1. Nginx Reverse Proxy**

- Menerima HTTP request dari browser melalui port 8081.
- Meneruskan request ke Flask Web Application melalui `web:5000`.
- Menjadi pintu masuk utama untuk mengakses aplikasi.
- Membantu memisahkan akses pengguna dari service backend.

**2. Flask Web Application**

- Menjalankan aplikasi menggunakan Flask dan Gunicorn.
- Menyediakan dashboard multi-halaman.
- Mengelola komunikasi dengan PostgreSQL dan Redis.
- Menyediakan endpoint API untuk pemeriksaan kesehatan, catatan, dan statistik aplikasi.

**3. PostgreSQL Database**

- Menggunakan PostgreSQL 16 Alpine.
- Menyimpan data catatan aplikasi.
- Menggunakan named volume agar data tetap tersedia ketika container dibuat ulang.

**4. Redis Cache**

- Menggunakan Redis 7 Alpine.
- Menyimpan cache daftar catatan aplikasi.
- Menggunakan TTL 30 detik.
- Membantu mempercepat akses data yang sering diminta.
- Redis digunakan sebagai cache, bukan sumber penyimpanan data permanen.

### Alur komunikasi sistem

Alur komunikasi aplikasi:

`Browser → Nginx → Flask/Gunicorn → PostgreSQL dan Redis`

Nginx meneruskan request ke service Web melalui DNS internal Docker Compose. Flask kemudian berkomunikasi dengan PostgreSQL melalui service `db` dan Redis melalui service `redis`.

### Dashboard NEXUS Cloud Lab

Aplikasi memiliki lima halaman utama yang dapat diakses melalui menu navigasi.

| No. | Halaman | URL | Keterangan |
|---|---|---|---|
| 1 | Overview | `/` | Menampilkan ringkasan dashboard |
| 2 | Services | `/services` | Menampilkan informasi layanan aplikasi |
| 3 | Database | `/database` | Menampilkan informasi PostgreSQL |
| 4 | Cache Monitor | `/cache` | Menampilkan informasi Redis dan cache |
| 5 | Activity | `/activity` | Menampilkan informasi aktivitas aplikasi |

Seluruh halaman dapat diakses melalui alamat utama:

`http://localhost:8081`

### Network

Proyek menggunakan dua Docker Network:

- `advanced_frontend`: menghubungkan Nginx dengan Web.
- `advanced_backend`: jaringan internal untuk komunikasi Web dengan PostgreSQL dan Redis.

Nginx tidak tergabung ke jaringan backend. PostgreSQL dan Redis tidak memublikasikan port ke host.

### Volume

Proyek menggunakan named volume untuk menjaga persistensi data:

| Volume | Mount Path | Fungsi |
|---|---|---|
| `advanced_postgres_data` | `/var/lib/postgresql/data` | Menyimpan data PostgreSQL |
| `advanced_redis_data` | `/data` | Menyimpan data Redis |

Redis menggunakan konfigurasi AOF untuk mendukung persistensi data cache.

---

## 2. Persiapan dan Instalasi

### Persyaratan sistem

- macOS.
- MacBook Air M3 atau perangkat yang mendukung Docker Desktop.
- Docker Desktop.
- Docker CLI.
- Docker Compose.
- Git untuk pengelolaan repository.

### Konfigurasi environment

Buka direktori proyek:

```bash
cd ~/Downloads/advanced-docker-compose
```

Buat file environment berdasarkan template:

```bash
cp .env.example .env
```

Edit file `.env` dan sesuaikan konfigurasi database, terutama `DB_PASSWORD`, menggunakan password lokal yang kuat.

**Catatan keamanan:** File `.env` tidak boleh diunggah ke repository publik karena berisi konfigurasi sensitif.

### Validasi konfigurasi

Jalankan perintah:

```bash
docker compose config
```

Periksa daftar service:

```bash
docker compose config --services
```

### Build dan menjalankan aplikasi

```bash
docker compose build
docker compose up -d
```

Periksa status container:

```bash
docker compose ps
```

Jika seluruh service berjalan dengan baik, aplikasi dapat diakses melalui:

http://localhost:8081

---

## 3. Pengujian Aplikasi dan Antarcontainer

Pengujian dilakukan untuk memastikan aplikasi, database, cache, reverse proxy, dan komunikasi antarcontainer berjalan sesuai fungsinya.

### A. Pemeriksaan kesehatan aplikasi

```bash
curl -i http://localhost:8081/api/health
```

Endpoint ini digunakan untuk memeriksa kondisi kesehatan aplikasi dan layanan pendukungnya.

### B. Pemeriksaan statistik aplikasi

```bash
curl -s http://localhost:8081/api/stats
```

Perintah ini digunakan untuk melihat informasi statistik yang disediakan backend aplikasi.

### C. Pemeriksaan koneksi PostgreSQL

```bash
docker compose exec db pg_isready -U nexus_user -d nexus_db
```

Perintah ini digunakan untuk memastikan PostgreSQL siap menerima koneksi.

Nama database dan user mengikuti konfigurasi pada file `.env`.

### D. Pemeriksaan koneksi Redis

```bash
docker compose exec redis redis-cli ping
```

Hasil yang diharapkan:

```text
PONG
```

### E. Pemeriksaan DNS antarcontainer

```bash
docker compose exec web python -c "import socket; print('db:', socket.gethostbyname('db')); print('redis:', socket.gethostbyname('redis'))"
```

Pengujian ini memastikan container Web dapat menemukan service PostgreSQL dan Redis melalui DNS internal Docker Compose.

### F. Pemeriksaan Docker Network dan Volume

```bash
docker network ls
docker volume ls
```

Perintah tersebut digunakan untuk memeriksa jaringan dan volume yang digunakan oleh proyek.

### G. Pengujian navigasi dashboard

Pengujian dilakukan dengan membuka setiap menu navigasi pada browser.

| No. | Halaman | URL | Hasil |
|---|---|---|---|
| 1 | Overview | `http://localhost:8081/` | Berfungsi |
| 2 | Services | `http://localhost:8081/services` | Berfungsi |
| 3 | Database | `http://localhost:8081/database` | Berfungsi |
| 4 | Cache Monitor | `http://localhost:8081/cache` | Berfungsi |
| 5 | Activity | `http://localhost:8081/activity` | Berfungsi |

Hasil pengujian menunjukkan bahwa kelima halaman dashboard dapat diakses melalui menu navigasi aplikasi.

### H. Pengujian API catatan dan cache

Endpoint catatan dapat diperiksa menggunakan:

```bash
curl -i http://localhost:8081/api/notes
```

Pengujian cache dilakukan dengan mengakses endpoint catatan beberapa kali. Respons pertama dapat menunjukkan `MISS`, sedangkan permintaan berikutnya dapat menunjukkan `HIT` selama cache masih berlaku.

Ketika catatan baru ditambahkan melalui aplikasi, cache dihapus agar data terbaru dapat ditampilkan.

---

## 4. Dokumentasi Pengujian Tantangan Wajib A–D

Pengujian tantangan A–D telah dilaksanakan sebagai bagian dari praktikum Advanced Docker Compose. Bagian ini merupakan dokumentasi hasil pengerjaan, bukan instruksi untuk mengulang seluruh pengujian.

### Uji A — Persistensi Data Setelah Container Dihapus

**Tujuan:** Membuktikan bahwa data PostgreSQL tetap tersimpan meskipun container dihapus dan dibuat kembali.

Pengujian dilakukan dengan menambahkan catatan unik melalui aplikasi, memeriksa data menggunakan PostgreSQL, kemudian menghentikan dan membuat ulang container tanpa menghapus named volume.

Perintah pemeriksaan data:

```bash
docker compose exec db psql -U nexus_user -d nexus_db -c "SELECT id, content, created_at FROM notes ORDER BY id DESC;"
```

Perintah untuk membuat ulang container:

```bash
docker compose down
docker compose up -d
docker compose ps
```

**Hasil pengujian:** Data tetap tersedia setelah container dibuat ulang karena PostgreSQL menggunakan named volume `advanced_postgres_data`.

### Uji B — Menghentikan Service

**Tujuan:** Mengamati dampak ketika salah satu service tidak tersedia.

Pengujian dilakukan dengan menghentikan service Redis dan mengamati kondisi aplikasi. Pengujian juga mencakup penghentian service Web untuk memperlihatkan dampak ketika backend tidak tersedia.

Perintah pengujian Redis:

```bash
docker compose stop redis
curl -i http://localhost:8081/api/health
curl -i http://localhost:8081/api/notes
```

Pemulihan Redis:

```bash
docker compose start redis
```

Perintah pengujian Web:

```bash
docker compose stop web
```

Setelah pengamatan selesai, service dipulihkan:

```bash
docker compose start web
docker compose ps
```

**Hasil pengujian:** Gangguan service dapat diamati melalui respons aplikasi dan status container. Ketika backend Web berhenti, Nginx tidak dapat meneruskan request ke aplikasi. Setelah service dipulihkan, aplikasi dapat diakses kembali.

### Uji C — Kesalahan Konfigurasi dan Perbaikan Nginx

**Tujuan:** Memperlihatkan dampak kesalahan konfigurasi reverse proxy dan proses perbaikannya.

Pengujian dilakukan dengan membuat salinan konfigurasi Nginx:

```bash
cp nginx/default.conf nginx/default.conf.bak
```

Kemudian konfigurasi `proxy_pass` diubah sementara dari:

```nginx
proxy_pass http://web:5000;
```

Menjadi:

```nginx
proxy_pass http://web:5999;
```

Konfigurasi yang salah diterapkan dengan:

```bash
docker compose restart nginx
```

Kemudian dilakukan pemeriksaan:

```bash
curl -i http://localhost:8081
docker compose logs --tail=30 nginx
```

**Hasil pengujian:** Nginx tidak dapat terhubung ke port backend yang salah sehingga menghasilkan respons `502 Bad Gateway`.

Konfigurasi kemudian dipulihkan:

```bash
mv nginx/default.conf.bak nginx/default.conf
docker compose restart nginx
```

Pemeriksaan pemulihan:

```bash
curl -i http://localhost:8081/api/health
```

Setelah konfigurasi diperbaiki, aplikasi kembali dapat diakses.

### Uji D — Restart Resilience

**Tujuan:** Memastikan layanan dapat berjalan kembali setelah dilakukan restart.

Pengujian dilakukan dengan menjalankan:

```bash
docker compose restart
```

Kemudian memeriksa status seluruh container:

```bash
docker compose ps
```

Pemeriksaan kesehatan aplikasi:

```bash
curl -i http://localhost:8081/api/health
```

**Hasil pengujian:** Service dapat dijalankan kembali setelah restart dan kondisi aplikasi diperiksa melalui status container serta endpoint kesehatan.

Pengujian ini juga mendokumentasikan penerapan mekanisme:

- `restart: unless-stopped`
- Healthcheck pada service.
- `depends_on` dengan kondisi `service_healthy`.

**Catatan penting:** Jangan menggunakan `docker compose down -v` pada pengujian persistensi karena perintah tersebut menghapus named volume dan data di dalamnya.

---

## 5. Troubleshooting

### A. Port 8081 sudah digunakan

Periksa apakah port 8081 sedang digunakan oleh aplikasi lain. Jika diperlukan, sesuaikan port mapping Nginx pada file Compose, kemudian jalankan:

```bash
docker compose up -d
```

### B. Container Web Unhealthy

Periksa log Web:

```bash
docker compose logs web
```

Pastikan konfigurasi `.env` benar dan service database serta Redis dapat diakses.

### C. Terjadi 502 Bad Gateway

Periksa status container:

```bash
docker compose ps
```

Periksa log Nginx dan Web:

```bash
docker compose logs nginx web
```

Pastikan konfigurasi upstream Nginx mengarah ke:

```nginx
proxy_pass http://web:5000;
```

Pastikan juga Nginx dan Web terhubung ke network yang sesuai.

### D. Database Gagal Login

Pastikan nilai berikut sesuai dengan konfigurasi pada `.env`:

- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

Jangan menghapus volume database sebelum data diamankan.

### E. Build Gagal

Jalankan build ulang tanpa menggunakan cache:

```bash
docker compose build --no-cache web
```

Kemudian jalankan:

```bash
docker compose up -d
```

---

## 6. Perintah Demonstrasi

Berikut kumpulan perintah yang digunakan untuk demonstrasi proyek:

### Menjalankan aplikasi

```bash
docker compose config
docker compose config --services
docker compose build
docker compose up -d
docker compose ps
```

### Memeriksa log

```bash
docker compose logs --tail=30
```

### Memeriksa API

```bash
curl -i http://localhost:8081/api/health
curl -s http://localhost:8081/api/stats
```

### Memeriksa Network

```bash
docker network inspect advanced_frontend
docker network inspect advanced_backend
```

### Memeriksa Volume

```bash
docker volume inspect advanced_postgres_data
```

### Restart aplikasi

```bash
docker compose restart
docker compose ps
```

### Menghentikan aplikasi

```bash
docker compose down
```

Perintah tersebut menghapus container dan network proyek, tetapi mempertahankan named volume selama tidak menggunakan opsi `-v`.

---

## 7. Catatan Keamanan dan Batasan

1. File `.env` digunakan untuk konfigurasi lokal dan tidak boleh diunggah ke repository publik.
2. Gunakan password yang kuat untuk konfigurasi database.
3. Named volume digunakan untuk menjaga persistensi data PostgreSQL.
4. Redis digunakan sebagai cache, bukan sebagai sumber data permanen.
5. Pada lingkungan produksi diperlukan secret management, TLS, pembatasan akses, backup database, serta pengaturan resource.
6. Aplikasi menggunakan Google Fonts apabila koneksi internet tersedia. Aplikasi tetap dapat dijalankan tanpa font eksternal.
7. Proyek dikembangkan dan diuji pada lingkungan praktikum lokal menggunakan Docker Desktop.

---

## 8. Identitas dan Pengumpulan

**Nama:** Leni Tri Agustin  
**NPM:** 2024606601020  
**Kelas/Semester:** Semester 5  
**Judul video:** `TKA_2024606601020_ADVANCED_DOCKER`

**Repository GitHub:**

https://github.com/lenitriagustin529-alt/nexus-cloud-lab

**Kode tantangan dosen:** Diisi sesuai kode yang benar-benar diberikan oleh dosen.

---

## 9. Kesimpulan

NEXUS Cloud Lab merupakan implementasi Advanced Docker Compose yang mengintegrasikan Flask Web Application, PostgreSQL, Redis, dan Nginx Reverse Proxy dalam lingkungan multi-container.

Proyek ini menerapkan pemisahan layanan, komunikasi antarcontainer menggunakan Docker Network, penyimpanan data menggunakan named volume, healthcheck, serta pengelolaan layanan menggunakan Docker Compose.

Dashboard multi-halaman menyediakan lima menu utama, yaitu Overview, Services, Database, Cache Monitor, dan Activity, sehingga informasi aplikasi dapat diakses melalui navigasi yang terstruktur.

Melalui pengujian aplikasi dan tantangan A–D, proyek mendemonstrasikan persistensi data, penanganan gangguan service, perbaikan kesalahan konfigurasi reverse proxy, serta pemulihan layanan setelah restart.

Dengan demikian, proyek NEXUS Cloud Lab menjadi demonstrasi penerapan konsep containerization dan orkestrasi layanan menggunakan Docker Compose pada lingkungan praktikum.