# 👤 Tourist API Curl Commands

Tourist dapat:

- Register & Login
- Browse Packages & Destinations
- Create Bookings
- Upload Payment Proof
- Create Reviews
- View Own Bookings
- View Own Reviews
- View Tourist Analytics

---

## ==================== AUTH ====================

### Register as Tourist

```bash
curl -X POST http://localhost:6543/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "YOUR_EMAIL@example.com",
    "password": "YOUR_PASSWORD",
    "name": "Your Name",
    "role": "tourist"
  }'
```

**Response includes `token` - Save this as `YOUR_JWT_TOKEN`**

### Login as Tourist

```bash
curl -X POST http://localhost:6543/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "YOUR_EMAIL@example.com",
    "password": "YOUR_PASSWORD"
  }'
```

**Response includes `token` - Use this for all authenticated requests**

### Get Current Profile - REQUIRES JWT

```bash
curl -X GET http://localhost:6543/api/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## ==================== DESTINATIONS (Public) ====================

### Get All Destinations (Public - Browse)

```bash
curl -X GET "http://localhost:6543/api/destinations?page=1&limit=10"
```

### Get Destination Detail (Public)

```bash
curl -X GET http://localhost:6543/api/destinations/DESTINATION_ID
```

---

## ==================== PACKAGES (Public Browse) ====================

### Get All Packages (Public - Browse)

```bash
curl -X GET "http://localhost:6543/api/packages?page=1&limit=10&destination=DESTINATION_ID&minPrice=100000&maxPrice=5000000&sortBy=price&order=asc"
```

### Search Packages (Public)

```bash
curl -X GET "http://localhost:6543/api/packages/search?q=Bali"
```

### Get Package Detail (Public)

```bash
curl -X GET http://localhost:6543/api/packages/PACKAGE_ID
```

---

## ==================== BOOKINGS ====================

### Get Own Bookings - REQUIRES JWT

```bash
curl -X GET "http://localhost:6543/api/bookings?status=pending&page=1&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Booking Detail - REQUIRES JWT

```bash
curl -X GET http://localhost:6543/api/bookings/BOOKING_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Create Booking - REQUIRES JWT (Tourist Only)

```bash
curl -X POST http://localhost:6543/api/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "packageId": "PACKAGE_ID",
    "numberOfTravelers": 5,
    "totalPrice": 17500000,
    "departureDate": "2025-02-15",
    "notes": "Special request: vegetarian meals"
  }'
```

**Response includes `id` - Save this as `BOOKING_ID`**

### Get Own Bookings by Tourist - REQUIRES JWT

```bash
curl -X GET http://localhost:6543/api/bookings/tourist/TOURIST_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## ==================== PAYMENT ====================

### Upload Payment Proof - REQUIRES JWT

```bash
curl -X POST http://localhost:6543/api/bookings/BOOKING_ID/payment-proof \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "proof=@/path/to/payment_proof.jpg"
```

### Generate Payment (Auto QRIS) - REQUIRES JWT

```bash
curl -X POST http://localhost:6543/api/payment/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "amount": 2500000
  }'
```

---

## ==================== REVIEWS ====================

### Get Reviews by Package (Public)

```bash
curl -X GET "http://localhost:6543/api/reviews/package/PACKAGE_ID?page=1&limit=10"
```

### Create Review - REQUIRES JWT (Tourist Only, After Completed Trip)

```bash
curl -X POST http://localhost:6543/api/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "bookingId": "BOOKING_ID",
    "packageId": "PACKAGE_ID",
    "rating": 5,
    "comment": "Amazing experience! Highly recommended."
  }'
```

### Get Own Reviews - REQUIRES JWT

```bash
curl -X GET http://localhost:6543/api/reviews/tourist/TOURIST_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## ==================== QRIS (Payment Methods) ====================

### Get All QRIS (Public)

```bash
curl -X GET "http://localhost:6543/api/qris?page=1&limit=10"
```

### Get QRIS Detail (Public)

```bash
curl -X GET http://localhost:6543/api/qris/QRIS_ID
```

### QRIS Preview (Generate Preview) - REQUIRES JWT

```bash
curl -X POST http://localhost:6543/api/qris/preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "static_qris_string": "00020126450014com.midtrans...",
    "jumlah_bayar": 1000000
  }'
```

---

## ==================== ANALYTICS (Tourist Dashboard) ====================

### Get Tourist Stats - REQUIRES JWT

```bash
curl -X GET http://localhost:6543/api/analytics/tourist/stats \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Response includes:

- totalBookings
- confirmedBookings
- pendingBookings
- completedBookings
- cancelledBookings
- totalSpent
- reviewsGiven

---

## 📋 Booking Flow Example

### 1. Browse Packages

```bash
curl -X GET "http://localhost:6543/api/packages?destination=UUID&maxPrice=5000000"
```

### 2. View Package Detail

```bash
curl -X GET http://localhost:6543/api/packages/b0efbe2a-2376-41da-a835-1e62370cd53f
```

### 3. View Reviews

```bash
curl -X GET "http://localhost:6543/api/reviews/package/b0efbe2a-2376-41da-a835-1e62370cd53f"
```

### 4. Create Booking

```bash
curl -X POST http://localhost:6543/api/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyYWJlMTliMS00NDQ3LTQ0ZWYtOGY0Yi01OGQ0YzliNmRhNDkiLCJlbWFpbCI6InRvdXJpc3RAZXhhbXBsZS5jb20iLCJyb2xlIjoidG91cmlzdCIsImV4cCI6MTc2NTY4OTAyNywiaWF0IjoxNzY1Njg3MjI3fQ.nzE54Eiaem5lBfCmkfz-xjNFfkbxkYgRs35FBD3d6dw" \
  -d '{
    "packageId": "b0efbe2a-2376-41da-a835-1e62370cd53f",
    "travelersCount": 2,
    "totalPrice": 7000000,
    "travelDate": "2025-02-15"
  }'
```

### 5. Generate Payment

```bash
curl -X POST http://localhost:6543/api/payment/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyYWJlMTliMS00NDQ3LTQ0ZWYtOGY0Yi01OGQ0YzliNmRhNDkiLCJlbWFpbCI6InRvdXJpc3RAZXhhbXBsZS5jb20iLCJyb2xlIjoidG91cmlzdCIsImV4cCI6MTc2NTY4OTAyNywiaWF0IjoxNzY1Njg3MjI3fQ.nzE54Eiaem5lBfCmkfz-xjNFfkbxkYgRs35FBD3d6dw" \
  -d '{
    "amount": 7000000
  }'
```

### 6. Upload Payment Proof

```bash
curl -X POST http://localhost:6543/api/bookings/c5ecd11b-ff25-415b-8a39-b8a2e8ca54f3/payment-proof \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyYWJlMTliMS00NDQ3LTQ0ZWYtOGY0Yi01OGQ0YzliNmRhNDkiLCJlbWFpbCI6InRvdXJpc3RAZXhhbXBsZS5jb20iLCJyb2xlIjoidG91cmlzdCIsImV4cCI6MTc2NTY4OTAyNywiaWF0IjoxNzY1Njg3MjI3fQ.nzE54Eiaem5lBfCmkfz-xjNFfkbxkYgRs35FBD3d6dw" \
  -F "proof=@receipt.jpg"
```

### 7. Wait for Agent to Verify

(Agent akan verify payment melalui endpoint verify)

### 8. After Trip Complete, Create Review

```bash
curl -X POST http://localhost:6543/api/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyYWJlMTliMS00NDQ3LTQ0ZWYtOGY0Yi01OGQ0YzliNmRhNDkiLCJlbWFpbCI6InRvdXJpc3RAZXhhbXBsZS5jb20iLCJyb2xlIjoidG91cmlzdCIsImV4cCI6MTc2NTY4OTAyNywiaWF0IjoxNzY1Njg3MjI3fQ.nzE54Eiaem5lBfCmkfz-xjNFfkbxkYgRs35FBD3d6dw" \
  -d '{
    "bookingId": "c5ecd11b-ff25-415b-8a39-b8a2e8ca54f3",
    "packageId": "b0efbe2a-2376-41da-a835-1e62370cd53f",
    "rating": 5,
    "comment": "Sempurna! Akan booking lagi."
  }'
```

---

## 📝 Tips

1. **Save JWT Token**: After login, save the token:

   ```bash
   TOKEN=$(curl -X POST http://localhost:6543/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{
       "email": "YOUR_EMAIL@example.com",
       "password": "YOUR_PASSWORD"
     }' | jq -r '.token')
   ```

2. **Replace Placeholders**:

   - `YOUR_JWT_TOKEN` → Token from login response
   - `DESTINATION_ID` → ID from get destinations
   - `PACKAGE_ID` → ID from get packages
   - `BOOKING_ID` → ID from create booking response
   - `TOURIST_ID` → Your user ID from profile
   - `QRIS_ID` → ID from get QRIS endpoint

3. **Workflow Order**:

   ```
   Auth → Browse Destinations → Browse Packages → Create Booking
   → Generate Payment → Upload Payment Proof → Wait for Verification
   → After Trip Complete → Create Review
   ```

4. **Booking Status**: `pending`, `confirmed`, `completed`, `cancelled`

5. **File Upload**: Use `-F` flag for multipart form data (payment proof, reviews)

6. **Tourist can only**:

   - Create bookings for themselves
   - Upload payment proofs for their own bookings
   - Create reviews for completed bookings
   - View their own bookings and reviews

7. **Payment Flow**:
   - Create Booking first
   - Generate Payment
   - Upload Payment Proof
   - Wait for Agent to verify
   - Status changes to confirmed
