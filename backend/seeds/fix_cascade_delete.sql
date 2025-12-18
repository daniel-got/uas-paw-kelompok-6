-- Fix CASCADE DELETE for packages
-- Run this SQL directly in PostgreSQL to add CASCADE delete to foreign keys

BEGIN;

-- Drop existing foreign key constraints
ALTER TABLE bookings DROP CONSTRAINT IF EXISTS bookings_package_id_fkey;
ALTER TABLE reviews DROP CONSTRAINT IF EXISTS reviews_package_id_fkey;
ALTER TABLE reviews DROP CONSTRAINT IF EXISTS reviews_booking_id_fkey;

-- Recreate foreign key constraints with CASCADE delete
ALTER TABLE bookings 
    ADD CONSTRAINT bookings_package_id_fkey 
    FOREIGN KEY (package_id) 
    REFERENCES packages(id) 
    ON DELETE CASCADE;

ALTER TABLE reviews 
    ADD CONSTRAINT reviews_package_id_fkey 
    FOREIGN KEY (package_id) 
    REFERENCES packages(id) 
    ON DELETE CASCADE;

ALTER TABLE reviews 
    ADD CONSTRAINT reviews_booking_id_fkey 
    FOREIGN KEY (booking_id) 
    REFERENCES bookings(id) 
    ON DELETE CASCADE;

COMMIT;

-- Verify the constraints
SELECT 
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    confdeltype AS delete_action
FROM pg_constraint 
WHERE conname IN ('bookings_package_id_fkey', 'reviews_package_id_fkey', 'reviews_booking_id_fkey')
ORDER BY conname;
