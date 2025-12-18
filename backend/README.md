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
##### Windows

```sh
.\env\Scripts\activate
```
##### Unix
```sh
source env/bin/activate
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

2. Autogenerate migration (optional jika menambah/mengedit model)

```sh
alembic revision --autogenerate -m "initiate"
```

### Run aplikasi:

1. Run main.py

```sh
python main.py
```

---

## Docker/Podman Setup

### Requirements:
- Docker
- Docker Compose
###### atau
- Podman
- Podman Compose

### Quick Start dengan Docker Compose

1. Masuk ke folder backend

```sh
cd backend
```

2. Build dan jalankan containers

```sh
docker-compose up --build
```

3. Cek apakah service berjalan

```bash
docker-compose ps
```

Output yang diharapkan (jika menggunakan docker compose):
```
NAME              STATUS
uas-pengweb-db    Up (healthy)
uas-pyramid-backend  Up
```

4. Test API

```bash
curl http://localhost:6543/api/auth/me
```

### Docker Compose Services

#### PostgreSQL Service (uas-pengweb-db)
- Image: `postgres:15-alpine`
- Port: `5432`
- Database: `uas_pengweb`
- Users: `alembic_user`, `app_prod_user` (auto-created)
- Initialization: `init-db.sql`
- Storage: `postgres_data` volume (persistent)

#### Pyramid Backend Service (uas-pyramid-backend)
- Image: Built from `Dockerfile`
- Port: `6543`
- Environment: `DATABASE_URL=postgresql+psycopg2://app_prod_user:12345@postgres:5432/uas_pengweb`
- Startup: Runs `alembic upgrade head && python main.py`
- Volumes:
  - `./storage:/app/storage` - Application storage (persistent)
  - `.:/app` - Code mount for development

### Useful Docker Commands

**View logs**

```bash
docker-compose logs pyramid-backend
docker-compose logs postgres
docker-compose logs -f  # Follow logs
```

**Stop containers**

```bash
docker-compose down
```

**Stop and remove all data (volumes)**

```bash
docker-compose down -v
```

**Rebuild image**

```bash
docker-compose up --build
```

**Access PostgreSQL inside container**

```bash
docker-compose exec postgres psql -U app_prod_user -d uas_pengweb
```

**Access Pyramid container shell**

```bash
docker-compose exec pyramid-backend bash
```

**Run Alembic migration inside container**

```bash
docker-compose exec pyramid-backend alembic upgrade head
```

### Troubleshooting

**Issue: "connection refused"**
- Pastikan PostgreSQL service sudah healthy: `docker-compose ps`
- Tunggu healthcheck pass (5-10 detik)

**Issue: "permission denied for schema public"**
- Database users belum ter-setup
- Jalankan `docker-compose down -v` dan rebuild: `docker-compose up --build`

**Issue: Alembic migration error**
- Check logs: `docker-compose logs pyramid-backend`
- Ensure `DATABASE_URL` environment variable format benar
- Database user harus punya CREATE privilege pada public schema

**Issue: Port 6543 already in use**
- Change port di `docker-compose.yml`:
  ```yaml
  ports:
    - "8000:6543"  # Maps localhost:8000 to container:6543
  ```

---

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
  "message": "User Registered",
  "user": {
    "id": "uuid-here",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "tourist"
  }
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

### PUT /api/auth/profile

**Change profile info**
**Headers:**
```
Authorization: Bearer {token}
```
**Request Body:**

```json
{
  "name": "Fqwawa", //string | optional
  "email": "john@example.com" //string | optional
}
```
**Response (200 OK):**

```json
{
  "message": "Profile updated successfully",
  "user": {
  	"id": "5066b09f-e0f9-4229-ac75-3d396cb6c0fc",
  	"name": "Fqwawa",
	  "email": "faiq@gmail.com",
	  "role": "agent"
  }
}
```

---

### PUT /api/auth/change-password

**Change user password**
**Headers:**
```
Authorization: Bearer {token}
```
**Request Body:**

```json
{
  "currentPassword": "Fqwawa", //string
  "newPassword": "john@example.com" //string
}
```
**Response (200 OK):**

```json
{
	"message": "Password changed successfully"
}
```

---

## Destinations

### GET /api/destinations

**Get all destinations**
**Query Parameters:**

- `country` (optional): Filter by country
- `search` (optional): Search by name or description
  **Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "name": "Maldives",
    "description": "Crystal clear waters and luxurious overwater villas...",
    "photoUrl": "https://example.com/image.jpg",
    "country": "Maldives"
  }
]
```

---

### GET /api/destinations/:id

**Get destination by ID**
**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "name": "Maldives",
  "description": "Crystal clear waters...",
  "photoUrl": "https://example.com/image.jpg",
  "country": "Maldives"
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
  "destinationName": "Bali",
  "country": "Indonesia"
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

### GET /api/packages/{id}

**Get package detail**
**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "agentId": "uuid-here",
  "destinationId": "uuid-here",
  "name": "Bali Adventure Package",
  "duration": 5,
  "price": 2500.0,
  "itinerary": "Day 1: Arrival...",
  "maxTravelers": 8,
  "contactPhone": "+62 812-3456-7890",
  "images": ["url1", "url2"],
  "rating": 4.8,
  "reviewsCount": 45,
  "destinationName": "Bali",
  "country": "Indonesia"
}
```

---

### GET /api/packages/search

**Search packages by query**
**Query Parameters:**

- `q` (required): Search query (package name)
- `page` (optional, default: 1): Page number
- `limit` (optional, default: 10): Items per page

**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "agentId": "uuid-here",
    "destinationId": "uuid-here",
    "name": "Bali Adventure Package",
    "duration": 5,
    "price": 2500.0,
    "itinerary": "Day 1: Arrival...",
    "maxTravelers": 8,
    "contactPhone": "+62 812-3456-7890",
    "images": ["url1", "url2"],
    "rating": 4.8,
    "reviewsCount": 45,
    "destinationName": "Bali",
    "country": "Indonesia"
  }
]
```

---

### GET /api/packages/agent/{agentId}

**Get all packages by specific agent**
**Headers:**

```
Authorization: Bearer {token}
```

**Query Parameters:**

- `page` (optional, default: 1): Page number
- `limit` (optional, default: 10): Items per page

**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "agentId": "uuid-here",
    "destinationId": "uuid-here",
    "name": "Bali Adventure Package",
    "duration": 5,
    "price": 2500.0,
    "itinerary": "Day 1: Arrival...",
    "maxTravelers": 8,
    "contactPhone": "+62 812-3456-7890",
    "images": ["url1", "url2"],
    "rating": 4.8,
    "reviewsCount": 45,
    "destinationName": "Bali",
    "country": "Indonesia"
  }
]
```

---

### PUT /api/packages/{id}

**Update package (agent only)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "Updated Bali Adventure Package",
  "duration": 7,
  "price": 3500.0,
  "itinerary": "Updated itinerary...",
  "maxTravelers": 10,
  "contactPhone": "+62 812-9876-5432"
}
```

**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "agentId": "uuid-here",
  "destinationId": "uuid-here",
  "name": "Updated Bali Adventure Package",
  "duration": 7,
  "price": 3500.0,
  "itinerary": "Updated itinerary...",
  "maxTravelers": 10,
  "contactPhone": "+62 812-9876-5432",
  "images": ["url1", "url2"],
  "rating": 4.8,
  "reviewsCount": 45,
  "destinationName": "Bali",
  "country": "Indonesia"
}
```

---

### DELETE /api/packages/{id}

**Delete package (agent only)**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "message": "Package deleted successfully"
}
```

---

## Destinations

### GET /api/destinations

**Get all destinations**
**Query Parameters:**

- `page` (optional, default: 1): Page number
- `limit` (optional, default: 10): Items per page

**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "name": "Bali",
    "description": "Island of Gods with stunning beaches",
    "country": "Indonesia",
    "photo": "url-to-image",
    "createdAt": "2024-01-01T00:00:00Z"
  }
]
```

---

### GET /api/destinations/{id}

**Get destination detail**
**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "name": "Bali",
  "description": "Island of Gods with stunning beaches",
  "country": "Indonesia",
  "photo": "url-to-image",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

---

### POST /api/destinations

**Create new destination (agent only)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Request Body:**

```
- name: "Bali" (string)
- description: "Island of Gods with stunning beaches" (string)
- country: "Indonesia" (string)
- photo: <binary file> (image file)
```

**Response (201 Created):**

```json
{
  "id": "uuid-here",
  "name": "Bali",
  "description": "Island of Gods with stunning beaches",
  "country": "Indonesia",
  "photo": "url-to-image",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

---

### PUT /api/destinations/{id}

**Update destination (agent only)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "Bali Updated",
  "description": "Updated description",
  "country": "Indonesia"
}
```

**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "name": "Bali Updated",
  "description": "Updated description",
  "country": "Indonesia",
  "photo": "url-to-image",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

---

### DELETE /api/destinations/{id}

**Delete destination (agent only)**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "message": "Destination deleted successfully"
}
```

---

## Bookings

### GET /api/bookings

**Get all bookings (agent) or own bookings (tourist)**
**Headers:**

```
Authorization: Bearer {token}
```

**Query Parameters:**

- `status` (optional): `pending`, `confirmed`, `completed`, `cancelled`
- `page` (optional, default: 1): Page number
- `limit` (optional, default: 10): Items per page

**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "touristId": "uuid-here",
    "packageId": "uuid-here",
    "status": "pending",
    "numberOfTravelers": 2,
    "totalPrice": 5000000,
    "departureDate": "2025-02-15",
    "notes": "Special requests",
    "paymentProofUrl": null,
    "paymentStatus": "pending",
    "createdAt": "2024-01-01T00:00:00Z"
  }
]
```

---

### GET /api/bookings/{id}

**Get booking detail**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "touristId": "uuid-here",
  "packageId": "uuid-here",
  "status": "pending",
  "numberOfTravelers": 2,
  "totalPrice": 5000000,
  "departureDate": "2025-02-15",
  "notes": "Special requests",
  "paymentProofUrl": null,
  "paymentStatus": "pending",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

---

### POST /api/bookings

**Create new booking (tourist only)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "packageId": "uuid-here",
  "numberOfTravelers": 2,
  "totalPrice": 5000000,
  "departureDate": "2025-02-15",
  "notes": "Special requests"
}
```

**Response (201 Created):**

```json
{
  "id": "uuid-here",
  "touristId": "uuid-from-token",
  "packageId": "uuid-here",
  "status": "pending",
  "numberOfTravelers": 2,
  "totalPrice": 5000000,
  "departureDate": "2025-02-15",
  "notes": "Special requests",
  "paymentProofUrl": null,
  "paymentStatus": "pending",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

---

### PUT /api/bookings/{id}/status

**Update booking status (agent only)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "status": "confirmed"
}
```

**Valid status values:** `pending`, `confirmed`, `completed`, `cancelled`

**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "status": "confirmed",
  "updatedAt": "2024-01-02T00:00:00Z"
}
```

---

### POST /api/bookings/{id}/payment-proof

**Upload payment proof (tourist only)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Request Body:**

```
- proof: <binary file> (image file of payment proof)
```

**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "paymentProofUrl": "url-to-proof",
  "paymentStatus": "waiting_verification"
}
```

---

### PUT /api/bookings/{id}/payment-verify

**Verify payment (agent only)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "verificationNotes": "Payment verified from bank transfer"
}
```

**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "paymentStatus": "verified",
  "paymentVerificationDate": "2024-01-02T00:00:00Z"
}
```

---

### PUT /api/bookings/{id}/payment-reject

**Reject payment (agent only)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "rejectionReason": "Amount does not match booking price"
}
```

**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "paymentStatus": "rejected",
  "rejectionReason": "Amount does not match booking price"
}
```

---

### GET /api/bookings/tourist/{touristId}

**Get bookings by specific tourist**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "touristId": "uuid-here",
    "packageId": "uuid-here",
    "status": "pending",
    "numberOfTravelers": 2,
    "totalPrice": 5000000,
    "departureDate": "2025-02-15"
  }
]
```

---

### GET /api/bookings/package/{packageId}

**Get all bookings for a specific package**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "touristId": "uuid-here",
    "packageId": "uuid-here",
    "status": "confirmed",
    "numberOfTravelers": 2,
    "totalPrice": 5000000,
    "departureDate": "2025-02-15"
  }
]
```

---

### GET /api/bookings/payment/pending

**Get all bookings with pending payment verification (agent only)**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "touristId": "uuid-here",
    "packageId": "uuid-here",
    "paymentProofUrl": "url-to-proof",
    "paymentStatus": "waiting_verification",
    "totalPrice": 5000000
  }
]
```

---

## Reviews

### GET /api/reviews

**Get all reviews**
**Query Parameters:**

- `page` (optional, default: 1): Page number
- `limit` (optional, default: 10): Items per page

**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "touristId": "uuid-here",
    "bookingId": "uuid-here",
    "packageId": "uuid-here",
    "rating": 5,
    "comment": "Amazing experience!",
    "createdAt": "2024-01-05T00:00:00Z"
  }
]
```

---

### GET /api/reviews/package/{packageId}

**Get reviews by specific package**
**Query Parameters:**

- `page` (optional, default: 1): Page number
- `limit` (optional, default: 10): Items per page

**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "touristId": "uuid-here",
    "bookingId": "uuid-here",
    "packageId": "uuid-here",
    "rating": 5,
    "comment": "Amazing experience!",
    "createdAt": "2024-01-05T00:00:00Z"
  }
]
```

---

### GET /api/reviews/tourist/{touristId}

**Get reviews by specific tourist**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "touristId": "uuid-here",
    "bookingId": "uuid-here",
    "packageId": "uuid-here",
    "rating": 5,
    "comment": "Amazing experience!",
    "createdAt": "2024-01-05T00:00:00Z"
  }
]
```

---

### POST /api/reviews

**Create new review (tourist only, after completed booking)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "bookingId": "uuid-here",
  "packageId": "uuid-here",
  "rating": 5,
  "comment": "Amazing experience! Highly recommended."
}
```

**Response (201 Created):**

```json
{
  "id": "uuid-here",
  "touristId": "uuid-from-token",
  "bookingId": "uuid-here",
  "packageId": "uuid-here",
  "rating": 5,
  "comment": "Amazing experience! Highly recommended.",
  "createdAt": "2024-01-05T00:00:00Z"
}
```

**Validation:**

- `rating` must be between 1-5
- `comment` must be provided
- Booking must be in `completed` status
- Tourist can only review each booking once

---

## Analytics

### GET /api/analytics/agent/stats

**Get agent statistics (agent only)**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "totalPackages": 5,
  "totalBookings": 45,
  "confirmedBookings": 30,
  "pendingBookings": 10,
  "completedBookings": 5,
  "totalRevenue": 225000000,
  "averageRating": 4.7,
  "pendingPaymentVerifications": 3
}
```

---

### GET /api/analytics/agent/package-performance

**Get agent's package performance (agent only)**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
[
  {
    "packageId": "uuid-here",
    "packageName": "Bali Adventure Package",
    "totalBookings": 15,
    "confirmedBookings": 12,
    "totalRevenue": 75000000,
    "averageRating": 4.8,
    "reviewsCount": 12
  }
]
```

---

### GET /api/analytics/tourist/stats

**Get tourist statistics (tourist only)**
**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "totalBookings": 8,
  "confirmedBookings": 6,
  "pendingBookings": 1,
  "completedBookings": 1,
  "cancelledBookings": 0,
  "totalSpent": 40000000,
  "reviewsGiven": 1
}
```

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

---

### 5️⃣ POST /api/qris/preview - Generate QRIS Preview

```bash
curl -X POST "http://localhost:6543/api/qris/preview" \
  -H "Content-Type: application/json" \
  -d '{
    "static_qris_string": "00020126450014com.midtrans...",
    "jumlah_bayar": 1000000
  }'
```

**Response (200 OK):**

```json
{
  "qr_string": "generated-qr-code-image-url",
  "amount": 1000000,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

### 6️⃣ POST /api/payment/generate - Generate Dynamic Payment

```bash
curl -X POST "http://localhost:6543/api/payment/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1000000
  }'
```

---

### GET /api/packages/{id}

**Get package by ID with full details**
**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "agentId": "uuid-here",
  "destinationId": "uuid-here",
  "name": "Maldives Paradise Retreat",
  "duration": 7,
  "price": 3500.0,
  "itinerary": "Day 1-2: Arrival and resort check-in...",
  "maxTravelers": 4,
  "contactPhone": "+62 812-3456-7890",
  "images": ["url1", "url2", "url3"],
  "rating": 4.8,
  "reviewsCount": 245,
  "destinationName": "Maldives",
  "country": "Indonesia"
}
```

---

### PUT /api/packages/:id

**Update package (Agent only, own packages)**
**Headers:**

```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:** (all fields optional)

```json
{
  "name": "Updated Package Name",
  "duration": 6,
  "price": 2800.0,
  "itinerary": "Updated itinerary...",
  "maxTravelers": 10,
  "contactPhone": "+62 812-9999-9999",
  "images": ["url1", "url2", "url3"]
}
```

**Response (200 OK):**

```json
{
  "id": "uuid-here",
  "agentId": "uuid-here",
  "destinationId": "uuid-here",
  "name": "Maldives Paradise Retreat",
  "duration": 7,
  "price": 3500.0,
  "itinerary": "Day 1-2: Arrival and resort check-in...",
  "maxTravelers": 4,
  "contactPhone": "+62 812-3456-7890",
  "images": ["url1", "url2", "url3"],
  "rating": 4.8,
  "reviewsCount": 245,
  "destinationName": "Maldives",
  "country": "Indonesia"
}
```

### DELETE /api/packages/:id

**Delete package (Agent only, own packages, no bookings)**
**Headers:**

```
Authorization: Bearer {token}
```

## **Response (200 OK)**

### GET /api/packages/agent/:agentId

**Get all packages by agent**
**Response (200 OK):**

```json
[
  {
    "id": "uuid-here",
    "agentId": "uuid-here",
    "destinationId": "uuid-here",
    "name": "Package 1",
    "duration": 7,
    "price": 3500.0,
    "itinerary": "...",
    "maxTravelers": 4,
    "contactPhone": "+62 812-3456-7890",
    "images": ["url1"],
    "rating": 4.8,
    "reviewsCount": 245,
    "destinationName": "Bali"
    "country": "Indonesia"
  }
]
```

---
