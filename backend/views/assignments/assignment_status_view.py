from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import select
from db import Session
from models.tour_guide_assignment_model import TourGuideAssignment
from helpers.jwt_validate_helper import jwt_validate
from pydantic import BaseModel, ValidationError
from typing import Literal

class StatusUpdateRequest(BaseModel):
    status: Literal["assigned", "on_duty", "completed"]

@view_config(route_name="assignment_status", request_method="PATCH", renderer="json")
@jwt_validate
def assignment_status_update(request):
    try:
        assignment_id = request.matchdict.get("id")
        user_id = request.jwt_claims.get("sub")
        
        if request.jwt_claims.get("role") != "guide":
            return Response(json_body={"error": "Hanya guide yang dapat memperbarui status"}, status=403)

        try:
            data = StatusUpdateRequest(**request.json_body)
        except ValidationError:
            return Response(json_body={"error": "Status tidak valid"}, status=400)

        with Session() as session:
            stmt = select(TourGuideAssignment).where(TourGuideAssignment.id == assignment_id)
            assignment = session.execute(stmt).scalar_one_or_none()

            if not assignment:
                return Response(json_body={"error": "Penugasan tidak ditemukan"}, status=404)

            if str(assignment.guide_id) != user_id:
                return Response(json_body={"error": "Anda tidak berwenang atas tugas ini"}, status=403)

            assignment.status = data.status
            session.commit()
            return {"message": f"Status diperbarui menjadi {data.status}", "id": str(assignment.id)}
            
    except Exception as e:
        return Response(json_body={"error": "Internal Server Error"}, status=500)
