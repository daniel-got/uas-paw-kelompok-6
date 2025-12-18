"""Update user profile"""
import bcrypt
from pyramid.response import Response
from pyramid.view import view_config
from pydantic import BaseModel, ValidationError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from models.user_model import User
from helpers.jwt_validate_helper import jwt_validate


class UpdateProfileRequest(BaseModel):
    name: str | None = None
    email: str | None = None


class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str


@view_config(route_name="update_profile", request_method="PUT", renderer="json")
@jwt_validate
def update_profile(request):
    try:
        try:
            req_data = UpdateProfileRequest(**request.json_body)
        except ValidationError as err:
            return Response(json_body={"error": str(err.errors())}, status=400)
        
        user_id = request.jwt_claims.get("sub")
        db_session = request.dbsession
        
        # Get current user
        stmt = select(User).where(User.id == user_id)
        try:
            user = db_session.execute(stmt).scalars().one()
        except NoResultFound:
            return Response(json_body={"error": "User not found"}, status=404)
        
        # Check if email already exists (if changing email)
        if req_data.email and req_data.email != user.email:
            existing_user_stmt = select(User).where(User.email == req_data.email)
            existing_user = db_session.execute(existing_user_stmt).scalars().first()
            if existing_user:
                return Response(json_body={"error": "Email already in use"}, status=400)
            user.email = req_data.email
        
        # Update name if provided
        if req_data.name:
            user.name = req_data.name
        
        db_session.commit()
        db_session.refresh(user)
        
        return {
            "message": "Profile updated successfully",
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
        }
        
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}


@view_config(route_name="change_password", request_method="POST", renderer="json")
@jwt_validate
def change_password(request):
    try:
        # Parse request body
        try:
            req_data = ChangePasswordRequest(**request.json_body)
        except ValidationError as err:
            return Response(json_body={"error": str(err.errors())}, status=400)
        
        user_id = request.jwt_claims.get("sub")
        db_session = request.dbsession
        
        # Get current user
        stmt = select(User).where(User.id == user_id)
        try:
            user = db_session.execute(stmt).scalars().one()
        except NoResultFound:
            return Response(json_body={"error": "User not found"}, status=404)
        
        # Verify current password
        current_password_bytes = req_data.currentPassword.encode("utf-8")
        is_valid = bcrypt.checkpw(current_password_bytes, user.password_hash.encode("utf-8"))
        
        if not is_valid:
            return Response(json_body={"error": "Current password is incorrect"}, status=400)
        
        # Validate new password length
        if len(req_data.newPassword) < 6:
            return Response(json_body={"error": "New password must be at least 6 characters"}, status=400)
        
        # Hash new password
        new_password_bytes = req_data.newPassword.encode("utf-8")
        salt = bcrypt.gensalt()
        new_password_hash = bcrypt.hashpw(new_password_bytes, salt).decode("utf-8")
        
        # Update password
        user.password_hash = new_password_hash
        db_session.commit()
        
        return {"message": "Password changed successfully"}
        
    except Exception as e:
        request.response.status = 500
        return {"error": f"Internal server error: {str(e)}"}
