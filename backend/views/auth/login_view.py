import bcrypt
import jwt
import datetime
from pyramid.response import Response
from pyramid.view import view_config
from pydantic import BaseModel, ValidationError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from db import Session
from models.user_model import User


class FromRequest(BaseModel):
    email: str
    password: str


@view_config(route_name="login", request_method="POST", renderer="json")
def login(request):
    # request validation
    try:
        req_data = FromRequest(**request.json_body)
    except ValidationError as err:
        return Response(json_body={"error": str(err.errors())}, status=400)

    with Session() as session:
        stmt = select(User).where(User.email == req_data.email)
        try:
            result = session.execute(stmt).scalars().one()
        except NoResultFound:
            return Response(json_body={"message": "User tidak ditemukan"}, status=401)
        except Exception as e:
            print(e)
            return Response(json_body={"error": "Internal Server Error"}, status=500)

    # check the password with the hash in the db
    bytes = req_data.password.encode("utf-8")
    is_valid = bcrypt.checkpw(bytes, result.password_hash.encode("utf-8"))

    if is_valid == True:
        # making jwt token
        encoded = jwt.encode(
            {
                "sub": str(result.id),
                "email": result.email,
                "role": result.role,
                "exp": datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(minutes=30),
                "iat": datetime.datetime.now(datetime.timezone.utc),
            },
            "secret",
            algorithm="HS256",
        )
        return {
            "message": "User login",
            "user": {
                "id": str(result.id),
                "name": result.name,
                "email": result.email,
                "role": result.role,
            },
            "token": encoded,
        }

    return {"message": "Password salah"}
