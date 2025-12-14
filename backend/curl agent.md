# 👨‍💼 Agent API Curl Commands

Agent dapat:

- Register & Login
- Create Destinations & Packages
- Create/Update/Delete Packages
- Monitor Bookings dari Tourists
- Verify/Reject Payment Proofs
- Manage QRIS Payment Methods
- View Agent Analytics

---

## ==================== WORKFLOW ORDER ====================

### Agent Workflow:

1. **Register & Login** → Get `YOUR_JWT_TOKEN`
2. **Create Destinations** (if needed) → Get `DESTINATION_ID`
3. **Create Packages** for Destinations → Get `PACKAGE_ID`
4. **Monitor Bookings** from Tourists → Get `BOOKING_ID`
5. **Verify Payment Proofs** from Tourists
6. **Update Booking Status** to confirmed/completed
7. **View Analytics** of Your Performance

---

## ==================== AUTH ====================

### Register as Agent

```bash
curl -X POST http://localhost:6543/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "YOUR_AGENT_EMAIL@example.com",
    "password": "YOUR_PASSWORD",
    "name": "Your Agent Name",
    "role": "agent"
  }'
```

**Response includes `token` - Save this as `YOUR_JWT_TOKEN`**

### Login as Agent

```bash
curl -X POST http://localhost:6543/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "YOUR_AGENT_EMAIL@example.com",
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

## ==================== DESTINATIONS ====================

### Create Destination - REQUIRES JWT (Agent Only)

```bash
curl -X POST http://localhost:6543/api/destinations \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "name=Destination Name" \
  -F "description=Beautiful destination description" \
  -F "country=Country Name" \
  -F "photo=@/path/to/destination_image.jpg"
```

**Response includes `id` - Save this as `DESTINATION_ID`**

### Get All Destinations (Public)

```bash
curl -X GET "http://localhost:6543/api/destinations"
```

### Get Destination Detail (Public)

```bash
curl -X GET http://localhost:6543/api/destinations/DESTINATION_ID
```

### Update Destination - REQUIRES JWT (Agent Only)

```bash
curl -X PUT http://localhost:6543/api/destinations/DESTINATION_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Updated Destination Name",
    "description": "Updated description",
    "country": "Country Name"
  }'
```

### Delete Destination - REQUIRES JWT (Agent Only)

```bash
curl -X DELETE http://localhost:6543/api/destinations/DESTINATION_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## ==================== PACKAGES ====================

### Create Package - REQUIRES JWT (Agent Only)

**Prerequisites: Must have DESTINATION_ID from Create Destination step**

```bash
curl -X POST http://localhost:6543/api/packages \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "destinationId=DESTINATION_ID" \
  -F "name=Package Name" \
  -F "duration=5" \
  -F "price=3500000" \
  -F "itinerary=Day 1: Arrival. Day 2: Beach tour. Day 3: Temple visit. Day 4: Adventure. Day 5: Return." \
  -F "maxTravelers=20" \
  -F "contactPhone=08123456789" \
  -F "images=@/path/to/image1.jpg" \
  -F "images=@/path/to/image2.jpg"
```

**Response includes `id` - Save this as `PACKAGE_ID`**

### Get All Packages (Public)

```bash
curl -X GET "http://localhost:6543/api/packages?page=1&limit=10&destination=DESTINATION_ID"
```

### Get Package Detail (Public)

```bash
curl -X GET http://localhost:6543/api/packages/PACKAGE_ID
```

### Get Own Packages - REQUIRES JWT (Agent Only)

```bash
curl -X GET "http://localhost:6543/api/packages/agent?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update Own Package - REQUIRES JWT (Agent Only)

```bash
curl -X PUT http://localhost:6543/api/packages/PACKAGE_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Updated Package Name",
    "duration": 7,
    "price": 4500000,
    "maxTravelers": 25
  }'
```

### Delete Own Package - REQUIRES JWT (Agent Only)

```bash
curl -X DELETE http://localhost:6543/api/packages/PACKAGE_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## ==================== BOOKINGS MANAGEMENT ====================

### Get All Bookings - REQUIRES JWT (Agent Only)

```bash
curl -X GET "http://localhost:6543/api/bookings?status=pending&page=1&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Booking Detail - REQUIRES JWT (Agent Only)

```bash
curl -X GET http://localhost:6543/api/bookings/BOOKING_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Bookings by Package - REQUIRES JWT (Agent Only)

```bash
curl -X GET "http://localhost:6543/api/bookings/package/PACKAGE_ID?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Bookings by Tourist - REQUIRES JWT (Agent Only)

```bash
curl -X GET "http://localhost:6543/api/bookings/tourist/TOURIST_ID" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update Booking Status - REQUIRES JWT (Agent Only)

**Status can be: pending, confirmed, completed, cancelled**

```bash
curl -X PUT http://localhost:6543/api/bookings/BOOKING_ID/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "status": "confirmed"
  }'
```

---

## ==================== PAYMENT VERIFICATION ====================

### Get Pending Payment Verifications - REQUIRES JWT (Agent Only)

**This shows bookings waiting for payment verification**

```bash
curl -X GET "http://localhost:6543/api/bookings/payment/pending?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Verify Payment - REQUIRES JWT (Agent Only)

**After tourist uploads payment proof, agent verifies it**

```bash
curl -X PUT http://localhost:6543/api/bookings/BOOKING_ID/payment-verify \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "verificationNotes": "Payment verified from bank transfer"
  }'
```

### Reject Payment - REQUIRES JWT (Agent Only)

**If payment proof is invalid or amount doesn't match**

```bash
curl -X PUT http://localhost:6543/api/bookings/BOOKING_ID/payment-reject \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "rejectionReason": "Amount not matching booking price"
  }'
```

---

## ==================== QRIS PAYMENT METHODS ====================

### Get All QRIS Methods (Public)

```bash
curl -X GET "http://localhost:6543/api/qris?page=1&limit=10"
```

### Get QRIS Detail (Public)

```bash
curl -X GET http://localhost:6543/api/qris/QRIS_ID
```

### Create QRIS - REQUIRES JWT (Agent Only)

```bash
curl -X POST http://localhost:6543/api/qris \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "foto_qr=@/path/to/qris_image.png" \
  -F "fee_type=rupiah" \
  -F "fee_value=10000"
```

**Response includes `id` - Save this as `QRIS_ID`**

### Delete QRIS - REQUIRES JWT (Agent Only)

```bash
curl -X DELETE http://localhost:6543/api/qris/QRIS_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### QRIS Preview (Generate) - REQUIRES JWT

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

## ==================== REVIEWS MANAGEMENT ====================

### Get All Reviews - REQUIRES JWT (Agent Only)

```bash
curl -X GET "http://localhost:6543/api/reviews?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Reviews by Package (Public)

```bash
curl -X GET "http://localhost:6543/api/reviews/package/PACKAGE_ID?page=1&limit=10"
```

### Get Reviews by Tourist - REQUIRES JWT

```bash
curl -X GET "http://localhost:6543/api/reviews/tourist/TOURIST_ID" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## ==================== ANALYTICS ====================

### Get Agent Stats - REQUIRES JWT (Agent Only)

```bash
curl -X GET http://localhost:6543/api/analytics/agent/stats \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response includes:**

- Total Packages
- Total Bookings
- Total Revenue
- Average Rating
- Pending Payment Verifications

### Get Agent Package Performance - REQUIRES JWT (Agent Only)

```bash
curl -X GET "http://localhost:6543/api/analytics/agent/package-performance" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Shows performance metrics for each package:**

- Package ID & Name
- Bookings Count
- Revenue
- Average Rating

---

## � Complete Agent Workflow Example

### Step 1: Register & Login

```bash
# Register
curl -X POST http://localhost:6543/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "YOUR_AGENT_EMAIL@example.com",
    "password": "YOUR_PASSWORD",
    "name": "Your Agent Name",
    "role": "agent"
  }'

# Login and save token
TOKEN=$(curl -X POST http://localhost:6543/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "YOUR_AGENT_EMAIL@example.com",
    "password": "YOUR_PASSWORD"
  }' | jq -r '.token')
```

### Step 2: Create Destination

```bash
DEST=$(curl -X POST http://localhost:6543/api/destinations \
  -H "Authorization: Bearer $TOKEN" \
  -F "name=Bali" \
  -F "description=Island of Gods with stunning beaches" \
  -F "country=Indonesia" \
  -F "photo=@/path/to/destination_image.jpg" | jq -r '.id')
```

### Step 3: Create Package

```bash
PKG=$(curl -X POST http://localhost:6543/api/packages \
  -H "Authorization: Bearer $TOKEN" \
  -F "destinationId=$DEST" \
  -F "name=Bali Adventure 5 Days" \
  -F "duration=5" \
  -F "price=3500000" \
  -F "itinerary=Day 1: Arrival at airport. Day 2: Beach tour. Day 3: Temple visit. Day 4: Adventure activities. Day 5: Return home." \
  -F "maxTravelers=20" \
  -F "contactPhone=08123456789" \
  -F "images=@/path/to/image1.jpg" | jq -r '.id')
```

### Step 4: Monitor Pending Bookings

```bash
curl -X GET "http://localhost:6543/api/bookings?status=pending&page=1&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### Step 5: Verify Payment for Booking

```bash
curl -X PUT http://localhost:6543/api/bookings/BOOKING_ID/payment-verify \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "verificationNotes": "Payment verified from bank account"
  }'
```

### Step 6: Update Booking Status to Confirmed

```bash
curl -X PUT http://localhost:6543/api/bookings/BOOKING_ID/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "confirmed"
  }'
```

### Step 7: View Your Analytics

```bash
curl -X GET http://localhost:6543/api/analytics/agent/stats \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📝 Important Tips

1. **Save JWT Token**: After login, save the token:

   ```bash
   TOKEN=$(curl ... | jq -r '.token')
   ```

2. **Replace Placeholders**:

   - `YOUR_JWT_TOKEN` → Token from login response
   - `DESTINATION_ID` → ID from create destination response
   - `PACKAGE_ID` → ID from create package response
   - `BOOKING_ID` → ID from get bookings response
   - `TOURIST_ID` → Tourist's user ID
   - `QRIS_ID` → ID from create QRIS response

3. **Workflow Order**:

   ```
   Auth → Create Destination → Create Package
   → Monitor Bookings → Verify Payments → Update Status → View Analytics
   ```

4. **Booking Status Values**: `pending`, `confirmed`, `completed`, `cancelled`

5. **For Testing**: Use environment variables:

   ```bash
   DEST_ID=$(curl ... | jq -r '.id')
   PKG_ID=$(curl ... -d '{"destinationId": "'$DEST_ID'"}' | jq -r '.id')
   ```

6. **File Upload**: Use `-F` flag for multipart form data (images, photos, QRIS)

7. **Only Manage Your Own Packages**: Agents can only create and manage packages they own
