Nama: Leni Tri Agustin  
NPM: 2024606601020  
Proyek: NEXUS Cloud Lab — Advanced Docker Compose

## Checklist Pengujian

- [x] Empat container berhasil dijalankan dan berstatus healthy.
- [x] Dashboard dapat diakses melalui http://localhost:8081.
- [x] Catatan berhasil disimpan pada PostgreSQL.
- [x] Data tetap tersedia setelah container dibuat ulang.
- [x] Redis Cache MISS berhasil.
- [x] Redis Cache HIT berhasil.
- [x] Cache invalidation berhasil setelah penambahan data baru.
- [x] API Health berhasil.
- [x] API Stats berhasil.
- [x] API Notes berhasil.
- [x] Menghentikan service Redis dan mengamati dampaknya.
- [x] Membuat kesalahan konfigurasi upstream Nginx dan memperbaikinya.
- [x] Menguji respons HTTP 502 ketika upstream salah.
- [x] Memastikan aplikasi kembali HTTP 200 setelah konfigurasi diperbaiki.
- [x] Menguji restart resilience seluruh container.
- [x] Memastikan seluruh container kembali healthy setelah restart.
- [x] Memastikan data PostgreSQL tetap tersedia setelah restart.

## Daftar Screenshot

1. Tampilan dashboard NEXUS.
2. Status empat container Docker.
3. Pengujian Redis Cache MISS.
4. Pengujian Redis Cache HIT.
5. Hasil penyimpanan PostgreSQL.
6. Pengujian persistensi setelah container dibuat ulang.
7. Pengujian API Health dan Stats.
8. Pengujian Cache Invalidation.
9. Pengujian Redis Outage.
10. Pengujian Web Outage.
11. Pengujian kesalahan konfigurasi upstream Nginx (HTTP 502).
12. Pemulihan konfigurasi Nginx (HTTP 200).
13. Pengujian Restart Resilience.
14. Status seluruh container setelah restart.
15. Pengujian persistensi data PostgreSQL setelah restart.

Catatan: Checklist hanya menandai pengujian yang sudah benar-benar dilakukan.
