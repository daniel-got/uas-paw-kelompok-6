# Tour Guide Setup Documentation

---

## 1. Database Migration


### Add 'guide' Role to Database Enum

add guide ke role enum 
```bash
docker exec -it uas-pengweb-db psql -U postgres -d uas_pengweb -c "ALTER TYPE user_role ADD VALUE 'guide';"
```

### Create Tour Guide assignment table 


```bash
# Generate migration file
docker exec -it uas-pyramid-backend alembic revision --autogenerate -m "add tour guide assignment"

# Apply migration
docker exec -it uas-pyramid-backend alembic upgrade head
```

---

## 2. Register a Tour Guide


```bash
curl -X POST http://localhost:6543/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Budi Guide",
    "email": "budi@mail.com",
    "password": "password123",
    "role": "guide"
  }'
```

### Login as Tour Guide


```bash
curl -X POST http://localhost:6543/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "budi@mail.com",
    "password": "password123"
  }'
```


---

## 3. Assign Guide to Booking

**Prerequisites:** 
- Complete the booking process until payment is confirmed
- Have both `ID_BOOKING` and `ID_GUIDE` available

Only agents can assign guides to bookings using this endpoint:

```bash
curl -X POST http://localhost:6543/api/assignments \
  -H "Authorization: Bearer TOKEN_AGENT" \
  -H "Content-Type: application/json" \
  -d '{
    "bookingId": "ID_BOOKING",
    "guideId": "ID_GUIDE"
  }'
```

**Note:** Save the `ID_ASSIGNMENT` from the response for status updates.

---

## 4. Update Assignment Status

hanya guide bisa update status
### Start the Tour (Update to 'on_duty')


```bash
curl -X PATCH http://localhost:6543/api/assignments/ID_ASSIGNMENT/status \
  -H "Authorization: Bearer TOKEN_GUIDE" \
  -H "Content-Type: application/json" \
  -d '{"status": "on_duty"}'
```

### Complete the Tour (Update to 'completed')


```bash
curl -X PATCH http://localhost:6543/api/assignments/ID_ASSIGNMENT/status \
  -H "Authorization: Bearer TOKEN_GUIDE" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

---

## Status Flow Summary

1. **Initial:** Guide is assigned to booking
2. **on_duty:** Guide starts the tour
3. **completed:** Tour is finished

---

## tugas agent dan guide  

| Agent | Register guides, assign guides to bookings |
| Guide | Login, update own assignment status |

### Required Tokens

- `TOKEN_AGENT` - For assigning guides
- `TOKEN_GUIDE` - For guide status updates
- `ID_GUIDE` - Guide's user ID
- `ID_BOOKING` - Booking ID (must be payment confirmed)
- `ID_ASSIGNMENT` - Assignment ID (from assignment response)
