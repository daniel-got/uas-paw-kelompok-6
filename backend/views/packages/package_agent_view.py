from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import select, desc
from db import Session
from models.package_model import Package
from . import serialization_data
import uuid


@view_config(route_name="package_agent", request_method="GET", renderer="json")
def get_package_by_agent(request):
    agent_id = request.matchdict.get("agentId")

    with Session() as session:
        #filter id agent 
        try:
            uuid.UUID(agent_id)
        except ValueError:
            return Response(json_body={"error": "Invalid Agent ID format"}, status=400)
        
        #filter package by agent_id 
        stmt = (
            select(Package)
            .where(Package.agent_id == agent_id)
            .order_by(desc(Package.created_at))
        )
        
        #filtered package by agent
        try:
            results = session.execute(stmt).scalars().all()
            return [serialization_data(pkg) for pkg in results]
        except Exception as e:
            print(f"Error fetching agent packages: {e}")
            return Response(json_body={"error": "Internal Server Error"}, status=500)
