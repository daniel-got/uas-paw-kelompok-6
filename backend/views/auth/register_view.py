import bcrypt
from pyramid.response import Response
from pyramid.view import view_config
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import IntegrityError
from db import Session
from enum import Enum
from models.user_model import User


class UserRole(str, Enum):
    agent = "agent"
    tourist = "tourist"
    guide = "guide"


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole


@view_config(route_name="register", request_method="POST", renderer="json")
def register(request):
    # request validation
    try:
        req_data = RegisterRequest(**request.json_body)
    except ValidationError as err:
        return Response(json_body={"error": str(err.errors())}, status=400)

    # hash the password
    bytes = req_data.password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt).decode("utf-8")

    user_id = None
    with Session() as session:
        new_user = User(
            name=req_data.name,
            email=req_data.email,
            password_hash=hash,
            role=req_data.role,
        )
        try:
            session.add(new_user)
            session.commit()
            user_id = new_user.id
        except IntegrityError as err:
            session.rollback()
            return Response(json_body={"error": str(err.orig)}, status=409)

    return {
        "message": "User registered",
        "user": {
            "id": str(user_id),
            "name": req_data.name,
            "email": req_data.email,
            "role": req_data.role,
        },
    }
