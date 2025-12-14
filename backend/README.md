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
cd backend
```

3. Buat virtual env

```sh
python -m venv env
```

4. Source activate

```sh
.\env\Scripts\activate
```

5. Install dependensi

```sh
pip install -r requirements.txt
```

### Setup Alembic:

1. Upgrade head

```sh
alembic upgrade head
```

2. Autogenerate migration

```sh
alembic revision --autogenerate -m "initiate"
```

### Run aplikasi:

1. Run main.py

```sh
python main.py
```

# Dokumentasi API

> Ini adalah dokumentasi utama dari semua api yang tersedia di backend python pyramid tugas besar Pemrograman Aplikasi Web

## Auth

### POST /api/auth/register

**Register/signup user baru (tourist atau agent)**
**Request Body:**

```json
{
  "name": "John Doe", //string
  "email": "john@example.com", //string
  "password": "password123", //string
  "role": "tourist" // or "agent" //string
}
```

**Response (201 Created):**

```json
{
  "user": {
    "id": "uuid-here",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "tourist"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### POST /api/auth/login

**Login user**
**Request Body:**

```json
{
  "email": "john@example.com", //string
  "password": "password123", //string
  "role": "tourist" // validate user has this role //string
}
```

**Response (200 OK):**

```json
{
  "user": {
    "id": "uuid-here",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "tourist"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### GET /api/auth/me

**Get current authenticated user**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "tourist"
}
```

---

## Packages

### GET /api/packages

**Get all packages**
**Query Parameters:**

- `destination` (optional): Filter by destination ID
- `minPrice` (optional): Minimum price filter
- `maxPrice` (optional): Maximum price filter
- `search` (optional): Search by package name
- `sort` (optional): `price` or `duration`
- `page` (optional, default: 1): Page number
- `limit` (optional, default: 9): Items per page
  **Response (200 OK):**

```json
{
  "id": "uuid-here",
  "agentId": "uuid-here",
  "destinationId": "uuid-here",
  "name": "Maldives Paradise Retreat",
  "duration": 7,
  "price": 3500.0,
  "itinerary": "Day 1-2: Arrival...",
  "maxTravelers": 4,
  "contactPhone": "+62 812-3456-7890",
  "images": ["url1", "url2"],
  "rating": 4.8,
  "reviewsCount": 245,
  "destinationName": Bali,
  "country": Indonesia
}
```

---

## Packages

### POST /api/packages

**Create new package (agent only)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "destinationId": "uuid-here", //string
  "name": "Bali Adventure Package", //string
  "duration": 5, //number
  "price": 2500.0, //number
  "itinerary": "Day 1: Arrival...", //string
  "maxTravelers": 8, //number
  "contactPhone": "+62 812-3456-7890", //string
  "images": ["url1", "url2"] //array of string
}
```

**Response (201 Created):**

```json
{
  "id": "uuid-here",
  "agentId": "uuid-from-token",
  "destinationId": "uuid-here",
  "name": "Bali Adventure Package",
  "duration": 5,
  "price": 2500.0,
  "itinerary": "Day 1: Arrival...",
  "maxTravelers": 8,
  "contactPhone": "+62 812-3456-7890",
  "images": ["url1", "url2"],
  "rating": null,
  "reviewsCount": 0,
  "destinationName": "Bali",
  "country": Indonesia
}
```

**Validation:**

- `duration` must be > 0
- `price` must be > 0
- `maxTravelers` must be > 0
- `images` array must have at least 1 image

---

## QRIS & Payment API Endpoints

### 1️⃣ POST /api/qris - Upload Static QRIS

```bash
curl -X POST "http://localhost:6543/api/qris" \
  -F "foto_qr=@C:\path\to\qris_image.png" \
  -F "fee_type=rupiah" \
  -F "fee_value=10000"
```

### 2️⃣ GET /api/qris - List All QRIS

```bash
curl -X GET "http://localhost:6543/api/qris?page=1&limit=10" \
  -H "Content-Type: application/json"
```

### 3️⃣ GET /api/qris/{id} - Get QRIS Detail

```bash
curl -X GET "http://localhost:6543/api/qris/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json"
```

### 4️⃣ DELETE /api/qris/{id} - Delete QRIS

```bash
curl -X DELETE "http://localhost:6543/api/qris/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json"
```

### 5️⃣ POST /api/payment/generate - Generate Dynamic Payment

```bash
curl -X POST "http://localhost:6543/api/payment/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1000000
  }'
```

---
