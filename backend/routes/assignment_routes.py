#assignment routes
def include_assignment_routes(config):
    config.add_route("assignment_create", "/api/assignments")
    config.add_route("assignment_list", "/api/assignments")
    config.add_route("assignment_status", "/api/assignments/{id}/status")
