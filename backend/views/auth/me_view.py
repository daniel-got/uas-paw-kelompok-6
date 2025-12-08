import jwt
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from db import Session
from models.user_model import User


@view_config(route_name="me", request_method="GET", renderer="json")
def me(request):
    # get header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return Response(json_body={"error": "Missing Token"}, status=401)
    try:
        token_type, token = auth_header.split(" ", 1)
        if token_type != "Bearer":
            raise ValueError("Invalid token type")
    except ValueError:
        return Response(
            json_body={"error": "Invalid Authorization header format"}, status=401
        )

    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return Response(json_body={"error": "Token expired"}, status=401)
    except:
        return Response(json_body={"error": "Invalid token"}, status=401)

    with Session() as session:
        stmt = select(User).where(User.email == payload["email"])
        try:
            result = session.execute(stmt).scalars().one()
        except NoResultFound:
            return Response(json_body={"message": "User tidak ditemukan"}, status=401)
        except Exception as e:
            print(e)
            return Response(json_body={"error": "Internal Server Error"}, status=500)

    return {
        "id": str(result.id),
        "name": result.name,
        "email": result.email,
        "role": result.role,
    }
