from db import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from typing import Optional
from pyramid.view import view_config
from pydantic import BaseModel, ValidationError
from pyramid.response import Response
from models.destination_model import Destination
from helpers.jwt_validate_helper import jwt_validate
import os
import uuid
from pathlib import Path


class FromRequest(BaseModel):
    country: Optional[str] = None
    name: Optional[str] = None


class CreateDestinationRequest(BaseModel):
    name: str
    description: str
    photo_url: str
    country: str

def serialization_data(destination):
    return {
        "id": str(destination.id),
        "name": destination.name,
        "description": destination.description,
        "photoUrl": destination.photo_url,
        "country": destination.country,
    }


@view_config(route_name="destinations", request_method="GET", renderer="json")
def destinations(request):
    # request validation
    try:
        req_data = FromRequest(**request.params.mixed())
    except ValidationError as err:
        return Response(json_body={"error": str(err.errors())}, status=400)

    # get destination from db
    with Session() as session:
        stmt = select(
            Destination
        )  # building the query step by step if the url have some parameters
        if req_data.country is not None:
            stmt = stmt.where(Destination.country == req_data.country)
        if req_data.name is not None:
            stmt = stmt.where(Destination.name == req_data.name)

        try:
            result = (
                session.execute(stmt).scalars().all()
            )  # agar kembalikan semua, atau tidak sama sekali (imo gitu sih, cmiiw)
            return [
                serialization_data(dest) for dest in result
            ]  # serialisasikan semua destinasi yang ada dari .all()
        except Exception as e:
            print(e)
            return Response(json_body={"error": "Internal Server Error"}, status=500)


@view_config(route_name="destination_detail", request_method="GET", renderer="json")
def destination_detail(request):
    dest_id = request.matchdict.get("id")
    with Session() as session:
        stmt = select(Destination).where(Destination.id == dest_id)
        try:
            result = session.execute(stmt).scalars().one()  # tampilkan 1 data
            return serialization_data(result)  # serialisasikan
        except NoResultFound:
            return Response(json_body={"error": "Destination not founfd"}, status=404)
        except Exception as e:
            return Response(json_body={"error": "Invalid ID or server error"}, status=400)


@view_config(route_name="destinations", request_method="POST", renderer="json")
@jwt_validate
def create_destination(request):
    # Create storage directory if it doesn't exist
    storage_dir = Path("storage/destinations")
    storage_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Get form data
        name = request.POST.get("name")
        description = request.POST.get("description")
        country = request.POST.get("country")
        photo_file = request.POST.get("photo")
        
        # Validate required fields
        if not name or not description or not country:
            return Response(json_body={"error": "Missing required fields: name, description, country"}, status=400)
        
        if photo_file is None:
            return Response(json_body={"error": "Photo file is required"}, status=400)
        
        # Handle file upload
        try:
            filename = photo_file.filename
            if not filename or filename == '':
                return Response(json_body={"error": "Photo file is required"}, status=400)
            
            # Validate file extension
            allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
            file_ext = Path(filename).suffix.lower()
            
            if file_ext not in allowed_extensions:
                return Response(json_body={"error": f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"}, status=400)
            
            # Check file size (max 5MB)
            file_content = photo_file.file.read()
            if len(file_content) > 5 * 1024 * 1024:
                return Response(json_body={"error": "File size exceeds 5MB limit"}, status=400)
            
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = storage_dir / unique_filename
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            photo_url = f"/destinations/{unique_filename}"
        except AttributeError as e:
            return Response(json_body={"error": f"Invalid file upload: {str(e)}"}, status=400)
        
        # Save destination to database
        with Session() as session:
            new_destination = Destination(
                name=name,
                description=description,
                photo_url=photo_url,
                country=country
            )
            try:
                session.add(new_destination)
                session.commit()
                dest_id = new_destination.id
                
                return {
                    "message": "Destination created successfully",
                    "destination": {
                        "id": str(dest_id),
                        "name": name,
                        "description": description,
                        "photoUrl": photo_url,
                        "country": country
                    }
                }
            except IntegrityError as err:
                session.rollback()
                return Response(json_body={"error": "Destination with this name already exists"}, status=409)
            except Exception as err:
                session.rollback()
                return Response(json_body={"error": str(err)}, status=500)
                
    except Exception as e:
        print(f"Error creating destination: {e}")
        return Response(json_body={"error": "Internal server error"}, status=500)
        return Response(json_body={"error": "Internal server error"}, status=500)
