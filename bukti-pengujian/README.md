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

Dokumentasi screenshot disimpan dalam folder `bukti-pengujian/screenshot/`.

### A. Dashboard Aplikasi

1. `01-dashboard-overview.png` – Tampilan halaman Overview.
2. `01-dashboard-services.png` – Tampilan halaman Services.
3. `01-dashboard-database.png` – Tampilan halaman Database.
4. `01-dashboard-cache-monitor.png` – Tampilan halaman Cache Monitor.
5. `01-dashboard-activity.png` – Tampilan halaman Activity.

### B. Implementasi dan Pengujian Service

6. `02-container-healthy.png` – Status container dan healthcheck.
7. `03-redis-cache-miss.png` – Pengujian Redis Cache MISS.
8. `04-redis-cache-hit.png` – Pengujian Redis Cache HIT.
9. `05-postgresql-save-note.png` – Pengujian penyimpanan data PostgreSQL.
10. `06-postgresql-persistence.png` – Pengujian persistensi PostgreSQL.
11. `07-api-health-stats.png` – Pengujian API Health dan Stats.
12. `08-redis-cache-invalidation.png` – Pengujian Cache Invalidation.

### C. Pengujian Gangguan dan Pemulihan

13. `09-redis-outage.png` – Pengujian gangguan Redis.
14. `10-web-outage.png` – Pengujian gangguan Web Application.
15. `11-nginx-upstream-error-502.png` – Pengujian kesalahan konfigurasi upstream Nginx dengan HTTP 502.
16. `12-nginx-recovery-200.png` – Bukti pemulihan Nginx dengan HTTP 200.
17. `13-restart-resilience.png` – Pengujian Restart Resilience.
18. `14-container-healthy-after-restart.png` – Status container setelah restart.
19. `15-postgresql-data-after-restart.png` – Pemeriksaan data PostgreSQL setelah restart.
20. `16-postgresql-persistence-after-container-recreation.png` – Pengujian persistensi PostgreSQL setelah container dibuat ulang.

### D. Konfigurasi dan Infrastruktur Docker

21. `17-arsitektur-docker-compose.png` – Dokumentasi arsitektur Docker Compose.
22. `18-dockerfile-configuration.png` – Dokumentasi konfigurasi Dockerfile.
23. `19-compose-configuration.png` – Dokumentasi konfigurasi Docker Compose.
24. `20-docker-network.png` – Dokumentasi Docker Network.
25. `21-docker-volume.png` – Dokumentasi Docker Volume.
26. `22-inter-container-communication.png` – Pengujian komunikasi antarkontainer.
27. `23-nginx-troubleshooting-logs.png` – Dokumentasi troubleshooting Nginx.

### E. Status Akhir Implementasi

28. `docker-compose-status-final.png` – Status akhir seluruh service Docker Compose.

**Catatan:** Dokumentasi lokal yang diperiksa berisi 28 file screenshot setelah pembaruan dashboard dan penambahan screenshot status akhir. Checklist ini mencantumkan file bukti yang tersedia dan tidak menggantikan hasil pengujian sebenarnya.
