from db import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from typing import Optional
from pyramid.view import view_config
from pydantic import BaseModel, ValidationError
from pyramid.response import Response
from models.destination_model import Destination
from . import serialization_data
from helpers.jwt_validate_helper import jwt_validate


class DestinationRequest(BaseModel):
    country: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None


@view_config(route_name="destinations", request_method="GET", renderer="json")
def destinations(request):
    # request validation
    try:
        req_data = DestinationRequest(**request.params.mixed())
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
            print(e)
            return Response(
                json_body={"error": "Invalid ID or server error"}, status=400
            )


@view_config(route_name="destinations", request_method="POST", renderer="json")
@jwt_validate
def create_destinations(request):
    if request.jwt_claims["role"] != "agent":
        return Response(
            json_body={"error": "Forbidden : Only agent can access"}, status=403
        )

    try:
        req_data = DestinationRequest(**request.json_body)
    except ValidationError as err:
        return Response(json_body={"error": str(err.errors())}, status=400)

    with Session() as session:
        new_destination = Destination(
            name = req_data.name,
            description= req_data.description,
            photo_url= req_data.photo_url,
            country = req_data.country,
        )

        try:
            session.add(new_destination)
            session.commit()
            session.refresh(new_destination)
            return serialization_data(new_destination)
        except IntegrityError as err:
            session.rollback()
            return Response(json_body={"error": str(err.orig)}, status=409)
        except Exception as e:
            session.rollback()
            print(f"CRITICAL ERROR: {e}")
            return Response(
                json_body={"error": f"Internal Server Error: {str(e)}"}, status=500
            )
