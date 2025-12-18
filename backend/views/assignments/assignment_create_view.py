from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import select, and_
from db import Session
from models.tour_guide_assignment_model import TourGuideAssignment
from models.booking_model import Booking
from models.user_model import User
from helpers.jwt_validate_helper import jwt_validate
from pydantic import BaseModel, ValidationError
import uuid

class AssignmentRequest(BaseModel):
    bookingId: str
    guideId: str

@view_config(route_name="assignment_create", request_method="POST", renderer="json")
@jwt_validate
def assignment_create(request):
    try:
        user_id = request.jwt_claims.get("sub")
        user_role = request.jwt_claims.get("role")
        
        if user_role != "agent":
            return Response(json_body={"error": "Hanya agent yang dapat menugaskan guide"}, status=403)

        try:
            data = AssignmentRequest(**request.json_body)
            booking_uuid = uuid.UUID(data.bookingId)
            guide_uuid = uuid.UUID(data.guideId)
        except (ValidationError, ValueError):
            return Response(json_body={"error": "Format ID tidak valid"}, status=400)

        with Session() as session:
            booking = session.execute(
                select(Booking).where(Booking.id == booking_uuid)
            ).scalar_one_or_none()

            if not booking or booking.status != "confirmed":
                return Response(json_body={"error": "Booking tidak ditemukan atau belum dikonfirmasi"}, status=404)

            if str(booking.package.agent_id) != user_id:
                return Response(json_body={"error": "Anda tidak memiliki akses ke booking ini"}, status=403)
            
            #validasi guide 
            guide = session.execute(
                select(User).where(User.id == guide_uuid, User.role == "guide")
            ).scalar_one_or_none()

            if not guide:
                return Response(json_body={"error": "Guide tidak ditemukan atau role tidak valid"}, status=400)

            # Mencari apakah guide sudah punya tugas pada travel_date yang sama
            clash_query = select(TourGuideAssignment).join(Booking).where(
                and_(
                    TourGuideAssignment.guide_id == guide_uuid,
                    Booking.travel_date == booking.travel_date,
                    TourGuideAssignment.status.in_(["assigned", "on_duty"])
                )
            )
            clash_exists = session.execute(clash_query).scalar_one_or_none()

            if clash_exists:
                return Response(json_body={
                    "error": f"Guide {guide.name} sudah memiliki tugas lain pada tanggal {booking.travel_date}"
                }, status=409)

            #create assignment
            new_assignment = TourGuideAssignment(
                booking_id=booking_uuid,
                guide_id=guide_uuid,
                status="assigned"
            )

            session.add(new_assignment)
            session.commit()
            
            return {
                "message": "Guide berhasil ditugaskan",
                "assignmentId": str(new_assignment.id),
                "travelDate": str(booking.travel_date),
                "guideName": guide.name
            }
                
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return Response(json_body={"error": "Internal Server Error"}, status=500)
