# LAPORAN PENGUMPULAN PRAKTIKUM ADVANCED DOCKER COMPOSE

## 1. Identitas Mahasiswa

- **Nama:** Leni Tri Agustin
- **NPM:** 2024606601020
- **Semester:** 5
- **Nama Proyek:** NEXUS Cloud Lab

## 2. Repository Proyek

**Repository GitHub:**

https://github.com/lenitriagustin529-alt/nexus-cloud-lab

**Dokumentasi Screenshot Pengujian:**

https://github.com/lenitriagustin529-alt/nexus-cloud-lab/tree/main/bukti-pengujian/screenshot

**Dokumentasi Analisis Arsitektur:**

`ANALISIS-ARSITEKTUR.md`

## 3. Deskripsi Proyek

NEXUS Cloud Lab merupakan proyek implementasi aplikasi berbasis multi-container menggunakan Docker Compose. Proyek ini mengintegrasikan empat service utama yang saling berkomunikasi untuk membangun lingkungan aplikasi yang terstruktur dan mudah dikelola.

Teknologi yang digunakan meliputi:

1. **Nginx:** Sebagai reverse proxy dan pintu masuk akses aplikasi.
2. **Flask dan Gunicorn:** Sebagai Web Application yang menangani permintaan pengguna.
3. **PostgreSQL:** Sebagai sistem manajemen basis data untuk menyimpan data aplikasi.
4. **Redis:** Sebagai cache untuk membantu mempercepat akses data.

Implementasi juga menggunakan Docker Network untuk komunikasi antarkontainer dan named volume untuk menjaga persistensi data.

## 4. Arsitektur dan Fitur Aplikasi

Aplikasi NEXUS Cloud Lab menyediakan dashboard yang terdiri dari lima halaman utama:

| Halaman | Fungsi |
|---|---|
| Overview | Menampilkan ringkasan kondisi aplikasi dan service |
| Services | Menampilkan informasi status layanan |
| Database | Menampilkan informasi dan aktivitas PostgreSQL |
| Cache Monitor | Memantau aktivitas Redis Cache |
| Activity | Menampilkan aktivitas aplikasi |

Aplikasi dapat diakses melalui Nginx pada alamat lokal:

`http://localhost:8081`

Dokumentasi lebih lengkap mengenai arsitektur, fungsi setiap service, komunikasi antarkontainer, Docker Network, dan Docker Volume tersedia pada file `ANALISIS-ARSITEKTUR.md`.

## 5. Implementasi dan Hasil Pengujian

Implementasi dan pengujian yang telah dilakukan mencakup:

1. Menjalankan empat service menggunakan Docker Compose.
2. Memeriksa status container dan healthcheck.
3. Menguji komunikasi antarkontainer.
4. Memeriksa konfigurasi Docker Network.
5. Memeriksa penggunaan Docker Volume.
6. Menguji penyimpanan data PostgreSQL.
7. Menguji persistensi data setelah container database dibuat ulang.
8. Menguji mekanisme Redis Cache MISS dan Cache HIT.
9. Menguji Cache Invalidation.
10. Menguji gangguan pada Redis dan Web Application.
11. Menguji kesalahan konfigurasi upstream Nginx yang menghasilkan HTTP 502.
12. Memperbaiki konfigurasi Nginx dan memastikan aplikasi kembali dapat diakses dengan HTTP 200.
13. Menguji restart resilience dan memeriksa kondisi service setelah restart.

Berdasarkan pengujian yang telah dilakukan, aplikasi dapat dijalankan menggunakan Docker Compose, service dapat berkomunikasi sesuai konfigurasi, dan data PostgreSQL tetap tersedia setelah container database dibuat ulang melalui named volume.

## 6. Dokumentasi Challenge D16–D20

### D16 – Application Inaccessible

Melakukan simulasi gangguan pada Web Application untuk mengamati dampaknya terhadap akses aplikasi melalui Nginx.

### D17 – Volume dan Data Persistence

Menguji persistensi data PostgreSQL dengan membuat ulang container database dan memastikan data sebelumnya tetap tersedia melalui named volume.

### D18 – Redis Cache

Menguji mekanisme Redis Cache yang meliputi Cache MISS, Cache HIT, Cache Invalidation, serta dampak gangguan Redis terhadap aplikasi.

### D19 – Service Configuration

Melakukan kesalahan konfigurasi upstream Nginx secara sengaja sehingga menghasilkan HTTP 502. Selanjutnya konfigurasi diperbaiki dan aplikasi dipastikan kembali dapat diakses dengan HTTP 200.

### D20 – Restart Resilience

Menguji kemampuan service untuk berjalan kembali setelah proses restart, memeriksa status kesehatan container, serta memastikan data PostgreSQL tetap tersedia.

## 7. Dokumentasi Screenshot

Dokumentasi implementasi dan pengujian disimpan dalam folder:

`bukti-pengujian/screenshot/`

Berdasarkan daftar file pada komputer, terdapat **29 screenshot** yang terdiri dari:

- 5 screenshot halaman dashboard terbaru: Overview, Services, Database, Cache Monitor, dan Activity.
- 23 screenshot dokumentasi implementasi, konfigurasi, pengujian, serta troubleshooting.
- 1 screenshot status akhir Docker Compose.

Dokumentasi tersebut mencakup bukti kondisi container, pengujian Redis, persistensi PostgreSQL, gangguan service, pemulihan Nginx, restart resilience, konfigurasi Docker, komunikasi antarkontainer, dan tampilan dashboard aplikasi.

## 8. Kesimpulan

Berdasarkan implementasi dan pengujian yang telah dilakukan, proyek NEXUS Cloud Lab berhasil membangun aplikasi berbasis Docker Compose yang terdiri dari empat service utama, yaitu Nginx sebagai reverse proxy, Web Application menggunakan Flask dan Gunicorn, PostgreSQL sebagai database, serta Redis sebagai cache.

Implementasi ini menerapkan Docker Network untuk komunikasi antarkontainer dan named volume untuk menjaga persistensi data. Aplikasi juga menyediakan dashboard dengan lima halaman utama untuk menampilkan informasi dan aktivitas sistem.

Pengujian mencakup pemeriksaan kesehatan container, komunikasi antarlayanan, penyimpanan dan persistensi data PostgreSQL, mekanisme Redis Cache, simulasi gangguan service, kesalahan konfigurasi upstream Nginx, serta restart resilience.

Hasil implementasi dan pengujian didokumentasikan melalui screenshot dan file analisis arsitektur yang tersedia pada repository GitHub.

Dengan demikian, proyek ini memberikan pengalaman praktis dalam membangun, mengelola, menguji, dan melakukan troubleshooting aplikasi multi-container menggunakan Docker Compose.