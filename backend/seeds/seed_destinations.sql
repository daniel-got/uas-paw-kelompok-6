-- Seed destinations data
-- Run this in PostgreSQL to add sample destinations

INSERT INTO
    destinations (
        id,
        name,
        description,
        photo_url,
        country,
        created_at
    )
VALUES (
        'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
        'Bali',
        'Beautiful island known for beaches, temples, and vibrant culture.',
        'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800',
        'Indonesia',
        NOW()
    ),
    (
        'b2c3d4e5-f6a7-8901-bcde-f12345678901',
        'Yogyakarta',
        'Cultural heart of Java with ancient temples like Borobudur and Prambanan.',
        'https://images.unsplash.com/photo-1584810359583-96fc3448beaa?w=800',
        'Indonesia',
        NOW()
    ),
    (
        'c3d4e5f6-a7b8-9012-cdef-123456789012',
        'Raja Ampat',
        'Paradise for diving and snorkeling with pristine marine biodiversity.',
        'https://images.unsplash.com/photo-1516690561799-46d8f74f9abf?w=800',
        'Indonesia',
        NOW()
    ),
    (
        'd4e5f6a7-b8c9-0123-def1-234567890123',
        'Lombok',
        'Stunning beaches, Mount Rinjani, and laid-back island vibes.',
        'https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=800',
        'Indonesia',
        NOW()
    ),
    (
        'e5f6a7b8-c9d0-1234-ef12-345678901234',
        'Komodo Island',
        'Home to the famous Komodo dragons and amazing diving spots.',
        'https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=800',
        'Indonesia',
        NOW()
    ),
    (
        'f6a7b8c9-d0e1-2345-f123-456789012345',
        'Bandung',
        'Cool highland city surrounded by tea plantations and volcanic landscapes.',
        'https://images.unsplash.com/photo-1555899434-94d1368aa7af?w=800',
        'Indonesia',
        NOW()
    ),
    (
        'a7b8c9d0-e1f2-3456-0123-567890123456',
        'Bromo',
        'Iconic volcanic landscape perfect for sunrise views and adventure.',
        'https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?w=800',
        'Indonesia',
        NOW()
    ),
    (
        'b8c9d0e1-f2a3-4567-1234-678901234567',
        'Lake Toba',
        'Largest volcanic lake in the world with beautiful Batak culture.',
        'https://images.unsplash.com/photo-1570789210967-2cac24834d46?w=800',
        'Indonesia',
        NOW()
    )
ON CONFLICT (id) DO NOTHING;