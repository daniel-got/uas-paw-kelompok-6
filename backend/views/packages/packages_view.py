from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import select, asc, desc
from sqlalchemy.exc import NoResultFound, IntegrityError
from db import Session
from models.package_model import Package
from models.destination_model import Destination
from helpers.jwt_validate_helper import jwt_validate
from pydantic import BaseModel, Field, ValidationError
from typing import List
from . import serialization_data
import uuid
import json
from pathlib import Path


class PackageRequest(BaseModel):
    destinationId: str
    name: str
    duration: int = Field(gt=0)
    price: float = Field(gt=0)
    itinerary: str
    maxTravelers: int = Field(gt=0)
    contactPhone: str
    images: List[str]


@view_config(route_name="packages", request_method="GET", renderer="json")
def get_packages(request):
    destination_id = request.params.get("destination")
    search_query = request.params.get("q") or request.params.get("search")
    min_price = request.params.get("minPrice")
    max_price = request.params.get("maxPrice")
    sort_by = request.params.get("sortBy")
    order = request.params.get("order", "asc")

    with Session() as session:
        stmt = select(Package)

        if destination_id and destination_id != "all":
            try:
                uuid.UUID(destination_id)
                stmt = stmt.where(Package.destination_id == destination_id)
            except ValueError:
                pass

        if search_query:
            stmt = stmt.where(Package.name.ilike(f"%{search_query}%"))

        if min_price:
            stmt = stmt.where(Package.price >= float(min_price))

        if max_price:
            stmt = stmt.where(Package.price <= float(max_price))

        if sort_by == "price":
            sort_column = Package.price
        elif sort_by == "duration":
            sort_column = Package.duration
        else:
            sort_column = Package.created_at

        if order == "desc":
            stmt = stmt.order_by(desc(sort_column))
        else:
            stmt = stmt.order_by(asc(sort_column))

        try:
            results = session.execute(stmt).scalars().all()
            return [serialization_data(pkg) for pkg in results]
        except Exception as e:
            print(f"Error fetching packages : {e}")
            return Response(json_body={"error": "Internal server error"}, status=500)


@view_config(route_name="packages", request_method="POST", renderer="json")
@jwt_validate
def create_package(request):
    if request.jwt_claims["role"] != "agent":
        return Response(
            json_body={"error": "Forbidden : Only agent can access"}, status=403
        )

    # Create storage directory if it doesn't exist
    storage_dir = Path("storage/packages")
    storage_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Get form data
        destination_id = request.POST.get("destinationId")
        name = request.POST.get("name")
        duration = request.POST.get("duration")
        price = request.POST.get("price")
        itinerary = request.POST.get("itinerary")
        max_travelers = request.POST.get("maxTravelers")
        contact_phone = request.POST.get("contactPhone")
        
        # Validate required fields
        if not all([destination_id, name, duration, price, itinerary, max_travelers, contact_phone]):
            return Response(json_body={"error": "Missing required fields"}, status=400)
        
        # Parse numeric fields
        try:
            duration = int(duration)
            price = float(price)
            max_travelers = int(max_travelers)
        except ValueError:
            return Response(json_body={"error": "Invalid numeric values for duration, price, or maxTravelers"}, status=400)
        
        # Handle image uploads
        image_urls = []
        images_field = request.POST.getall("images")
        
        if images_field:
            for image_file in images_field:
                try:
                    filename = image_file.filename
                    if not filename or filename == '':
                        continue
                    
                    # Validate file extension
                    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
                    file_ext = Path(filename).suffix.lower()
                    
                    if file_ext not in allowed_extensions:
                        return Response(json_body={"error": f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"}, status=400)
                    
                    # Check file size (max 5MB)
                    file_content = image_file.file.read()
                    if len(file_content) > 5 * 1024 * 1024:
                        return Response(json_body={"error": "File size exceeds 5MB limit"}, status=400)
                    
                    # Generate unique filename
                    unique_filename = f"{uuid.uuid4()}{file_ext}"
                    file_path = storage_dir / unique_filename
                    
                    # Save file
                    with open(file_path, 'wb') as f:
                        f.write(file_content)
                    
                    image_urls.append(f"/packages/{unique_filename}")
                except AttributeError:
                    continue

        with Session() as session:
            dest_stmt = select(Destination).where(Destination.id == destination_id)
            try:
                session.execute(dest_stmt).scalars().one()
            except NoResultFound:
                return Response(json_body={"error": "Destination id not found"}, status=400)

            try:
                agent_uuid = uuid.UUID(request.jwt_claims["sub"])
                dest_uuid = uuid.UUID(destination_id)
            except ValueError:
                return Response(json_body={"error": "Invalid UUID format"}, status=400)

            new_package = Package(
                agent_id=agent_uuid,
                destination_id=dest_uuid,
                name=name,
                duration=duration,
                price=price,
                itinerary=itinerary,
                max_travelers=max_travelers,
                contact_phone=contact_phone,
                images=image_urls
            )

            try:
                session.add(new_package)
                session.commit()
                session.refresh(new_package)
                return serialization_data(new_package)
            except IntegrityError as err:
                session.rollback()
                return Response(json_body={"error": str(err.orig)}, status=409)
            except Exception as e:
                session.rollback()
                print(f"CRITICAL ERROR: {e}")
                return Response(json_body={"error": f"Internal Server Error: {str(e)}"}, status=500)
                
    except Exception as e:
        print(f"Error creating package: {e}")
        return Response(json_body={"error": "Internal server error"}, status=500)
