def serialization_data(destination):
    return {
        "id": str(destination.id),
        "name": destination.name,
        "description": destination.description,
        "photo_url": destination.photo_url,
        "country": destination.country,
    }
