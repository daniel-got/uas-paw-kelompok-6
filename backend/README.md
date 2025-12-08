# Backend Python Pyramid
> Kode utama backend python pyramid tugas besar Pemrograman Aplikasi Web

## Installation
1. postgres
2. python314+

### Setup postgres:
1. Masuk ke shell psql dan buat database
```sh
CREATE DATABASE uas_pengweb;
```
2. Buat user/role
```sh
CREATE USER alembic_user WITH PASSWORD '12345';
CREATE USER app_prod_user WITH PASSWORD '12345';
```
3. Berikan hak akses koneksi database tadi ke semua user diatas
```sh
GRANT CONNECT ON DATABASE uas_pengweb TO alembic_user;
GRANT CONNECT ON DATABASE uas_pengweb TO app_prod_user;
```
4. Masuk ke database
```sh
\c uas_pengweb
```
5. (Setup user alembic) Berikan akses ke alembic_user, line 2 dan 3 opsional jika db kosong
```sh
GRANT USAGE, CREATE ON SCHEMA public TO alembic_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO alembic_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO alembic_user;
```
6. (Setup user prod) Berikan akses ke user prod
```sh
GRANT USAGE ON SCHEMA public TO app_prod_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_prod_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_prod_user;
```
7. Beri akses tabel yang dibuat alembic nanti ke user prod
```sh
ALTER DEFAULT PRIVILEGES FOR ROLE alembic_user IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_prod_user;

ALTER DEFAULT PRIVILEGES FOR ROLE alembic_user IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO app_prod_user;
```

### Setup Python
1. Clone repository
```sh
git clone https://github.com/Tugas-Besar-Pemrograman-Aplikasi-Web/Pyramid-Backend.git
```
2. Masuk ke root repository
```sh
cd Pyramid-Backend/
```
3. Buat virtual env
```sh
python -m venv env
```
4. Source activate
```sh
source env/bin/activate
```
5. Install dependensi
```sh
pip install -r requirements.txt
```

### Setup Alembic:
1. Autogenerate migration
```sh
alembic revision --autogenerate -m "initiate"
```
2. Upgrade head
```sh
alembic upgrade head
```

### Run aplikasi:
1. Run main.py
```sh
python main.py
```

