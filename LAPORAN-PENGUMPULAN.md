
# LAPORAN PENGUMPULAN PRAKTIKUM ADVANCED DOCKER COMPOSE

## 1. Identitas Mahasiswa

- Nama: Leni Tri Agustin
- NPM: 2024606601020
- Kelas: Semester 5
- Nama Proyek: NEXUS Cloud Lab

## 2. Repository Proyek

GitHub:
https://github.com/lenitriagustin529-alt/nexus-cloud-lab

Dokumentasi screenshot:
https://github.com/lenitriagustin529-alt/nexus-cloud-lab/tree/main/bukti-pengujian/screenshot

## 3. Arsitektur Aplikasi

NEXUS Cloud Lab menggunakan Docker Compose dengan empat service utama:

1. Nginx sebagai reverse proxy.
2. Web Application menggunakan Flask dan Gunicorn.
3. PostgreSQL sebagai database.
4. Redis sebagai cache.

Sistem menerapkan Docker Network untuk komunikasi antarkontainer dan named volume untuk persistensi data.

Dokumentasi arsitektur lebih lengkap terdapat pada file ANALISIS-ARSITEKTUR.md.

## 4. Hasil Pengujian

Pengujian yang telah dilakukan meliputi:

- Menjalankan empat service menggunakan Docker Compose.
- Memeriksa status container dan healthcheck.
- Menguji komunikasi antarkontainer.
- Menguji Docker Network dan Docker Volume.
- Menguji penyimpanan data PostgreSQL.
- Menguji persistensi data setelah container database dibuat ulang.
- Menguji Redis Cache MISS dan Cache HIT.
- Menguji Cache Invalidation.
- Menguji gangguan Redis dan Web Application.
- Menguji kesalahan konfigurasi upstream Nginx dan pemulihannya.
- Menguji restart resilience.

## 5. Dokumentasi Challenge D16–D20

### D16 – Application Inaccessible
Melakukan pengujian gangguan Web Application dan mengamati dampaknya terhadap akses aplikasi.

### D17 – Volume dan Data Persistence
Menguji persistensi data PostgreSQL dengan membuat ulang container database dan memastikan data sebelumnya tetap tersedia melalui named volume.

### D18 – Redis Cache
Menguji mekanisme Cache MISS, Cache HIT, Cache Invalidation, serta dampak ketika Redis mengalami gangguan.

### D19 – Service Configuration
Mengubah konfigurasi upstream Nginx secara sengaja sehingga menghasilkan HTTP 502, kemudian memperbaikinya dan memastikan aplikasi kembali menghasilkan HTTP 200.

### D20 – Restart Resilience
Menguji kemampuan service untuk berjalan kembali setelah restart serta memeriksa status kesehatan container dan ketersediaan data.

## 6. Dokumentasi Screenshot

Bukti pengujian tersedia dalam folder:

bukti-pengujian/screenshot/

Folder tersebut berisi 23 screenshot dokumentasi implementasi, konfigurasi, pengujian, dan troubleshooting.

## 7. Kesimpulan

Berdasarkan hasil implementasi dan pengujian, proyek NEXUS Cloud Lab berhasil membangun sistem aplikasi berbasis Docker Compose yang terdiri dari empat service utama, yaitu Web Application menggunakan Flask dan Gunicorn, PostgreSQL sebagai database, Redis sebagai cache, serta Nginx sebagai reverse proxy.

Implementasi ini menerapkan Docker Network untuk komunikasi antarkontainer dan named volume untuk menjaga persistensi data. Pengujian menunjukkan bahwa aplikasi dapat diakses melalui Nginx, data PostgreSQL tetap tersimpan setelah container database dibuat ulang, serta Redis dapat menjalankan fungsi cache melalui mekanisme Cache MISS, Cache HIT, dan Cache Invalidation.

Selain itu, dilakukan pengujian gangguan service, kesalahan konfigurasi upstream Nginx, troubleshooting, dan restart resilience. Hasil pengujian menunjukkan bahwa sistem dapat dipulihkan setelah gangguan dan data tetap tersedia sesuai konfigurasi penyimpanannya.

Dengan demikian, praktikum ini memberikan pemahaman mengenai pembangunan, pengelolaan, komunikasi, penyimpanan data, dan troubleshooting aplikasi multi-container menggunakan Docker Compose.

