"""
Seed script for destinations table
Run this script to populate the database with sample destinations
Usage: python seed_destinations.py
"""
from db import Session
from models.destination_model import Destination
import uuid

destinations_data = [
    {
        "name": "Bali",
        "description": "Beautiful island known for beaches, temples, and vibrant culture.",
        "photo_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800",
        "country": "Indonesia"
    },
    {
        "name": "Yogyakarta",
        "description": "Cultural heart of Java with ancient temples like Borobudur and Prambanan.",
        "photo_url": "https://images.unsplash.com/photo-1584810359583-96fc3448beaa?w=800",
        "country": "Indonesia"
    },
    {
        "name": "Raja Ampat",
        "description": "Paradise for diving and snorkeling with pristine marine biodiversity.",
        "photo_url": "https://images.unsplash.com/photo-1516690561799-46d8f74f9abf?w=800",
        "country": "Indonesia"
    },
    {
        "name": "Lombok",
        "description": "Stunning beaches, Mount Rinjani, and laid-back island vibes.",
        "photo_url": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=800",
        "country": "Indonesia"
    },
    {
        "name": "Komodo Island",
        "description": "Home to the famous Komodo dragons and amazing diving spots.",
        "photo_url": "https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=800",
        "country": "Indonesia"
    },
    {
        "name": "Bandung",
        "description": "Cool highland city surrounded by tea plantations and volcanic landscapes.",
        "photo_url": "https://images.unsplash.com/photo-1555899434-94d1368aa7af?w=800",
        "country": "Indonesia"
    },
    {
        "name": "Bromo",
        "description": "Iconic volcanic landscape perfect for sunrise views and adventure.",
        "photo_url": "https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?w=800",
        "country": "Indonesia"
    },
    {
        "name": "Lake Toba",
        "description": "Largest volcanic lake in the world with beautiful Batak culture.",
        "photo_url": "https://images.unsplash.com/photo-1570789210967-2cac24834d46?w=800",
        "country": "Indonesia"
    }
]

def seed_destinations():
    with Session() as session:
        # Check if destinations already exist
        existing = session.query(Destination).count()
        if existing > 0:
            print(f"Destinations already exist ({existing} records). Skipping seed.")
            return
        
        # Insert destinations
        for data in destinations_data:
            destination = Destination(
                id=uuid.uuid4(),
                name=data["name"],
                description=data["description"],
                photo_url=data["photo_url"],
                country=data["country"]
            )
            session.add(destination)
        
        session.commit()
        print(f"Successfully seeded {len(destinations_data)} destinations!")

if __name__ == "__main__":
    seed_destinations()
