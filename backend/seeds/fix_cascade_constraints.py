"""
Run this script to fix CASCADE DELETE constraints on packages
Uses the same database connection as the running application
"""
from db import engine
from sqlalchemy import text

sql_drop = """
ALTER TABLE bookings DROP CONSTRAINT IF EXISTS bookings_package_id_fkey;
ALTER TABLE reviews DROP CONSTRAINT IF EXISTS reviews_package_id_fkey;
ALTER TABLE reviews DROP CONSTRAINT IF EXISTS reviews_booking_id_fkey;
"""

sql_create = """
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
"""

sql_verify = """
SELECT 
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    confdeltype AS delete_action
FROM pg_constraint 
WHERE conname IN ('bookings_package_id_fkey', 'reviews_package_id_fkey', 'reviews_booking_id_fkey')
ORDER BY conname;
"""

try:
    with engine.connect() as conn:
        # Drop existing constraints
        print("Dropping existing foreign key constraints...")
        conn.execute(text(sql_drop))
        conn.commit()
        
        # Create new constraints with CASCADE
        print("Creating new foreign key constraints with CASCADE DELETE...")
        conn.execute(text(sql_create))
        conn.commit()
        
        # Verify
        result = conn.execute(text(sql_verify))
        rows = result.fetchall()
        
        print("\n✅ CASCADE DELETE constraints successfully added!\n")
        print("Verified constraints:")
        for row in rows:
            delete_action = 'CASCADE' if row[2] == 'c' else 'NO ACTION'
            print(f"  - {row[0]} on {row[1]}: ON DELETE {delete_action}")
        
        print("\n✅ Database update complete! Delete package feature should now work.")
        print("   When you delete a package, all related bookings and reviews will be deleted automatically.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nIf the server is running, please stop it first and try again.")
    
