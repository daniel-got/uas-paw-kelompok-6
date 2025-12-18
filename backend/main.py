import hupper
import json
from waitress import serve
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response
from pyramid.renderers import JSON
from db import Session


class DBRequest(Request):
    @property
    def dbsession(self):
        session = Session()
        def cleanup(request):
            session.close()
        self.add_finished_callback(cleanup)
        return session


# Intercept all request from client and change the response header to allow cors, not the best practice imo but it is what it is
def cors_tween_factory(handler, registry):
    def cors_tween(request):
        # Handle preflight OPTIONS request
        if request.method == 'OPTIONS':
            response = Response(status=200)
        else:
            response = handler(request)
        
        # Add CORS headers to ALL responses
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization, X-Requested-With'
        response.headers['Access-Control-Max-Age'] = '3600'
        
        return response
    
    return cors_tween


def main():
    with Configurator() as config:
        # Intercept all request
        config.add_tween('main.cors_tween_factory')
        
        # Set custom request factory
        config.set_request_factory(DBRequest)
        
        # Setup pretty JSON renderer
        json_renderer = JSON()
        json_renderer.serializer = lambda obj, **kwargs: json.dumps(
            obj, 
            indent=2, 
            ensure_ascii=False,
            default=str
        )
        config.add_renderer('json', json_renderer)
        
        # route
        ## auth
        config.add_route("register", "/api/auth/register")
        config.add_route("login", "/api/auth/login")
        config.add_route("me", "/api/auth/me")
        config.add_route("update_profile", "/api/auth/profile")
        config.add_route("change_password", "/api/auth/change-password")

        ## packages
        config.add_route("packages", "/api/packages")
        config.add_route("package_detail", "/api/packages/{id}")
        config.add_route("package_agent", "/api/packages/agent/{agentId}")

        ## destinations
        config.add_route("destinations", "/api/destinations")
        config.add_route("destination_detail", "/api/destinations/{id}")

        ## qris
        config.add_route("qris", "/api/qris")
        config.add_route("qris_detail", "/api/qris/{id}")
        config.add_route("qris_preview", "/api/qris/preview")
        
        ## payment
        config.add_route("payment_generate", "/api/payment/generate")
        
        ## bookings
        config.add_route("bookings", "/api/bookings")
        config.add_route("booking_detail", "/api/bookings/{id}")
        config.add_route("booking_status", "/api/bookings/{id}/status")
        config.add_route("booking_payment_upload", "/api/bookings/{id}/payment-proof")
        config.add_route("booking_payment_verify", "/api/bookings/{id}/payment-verify")
        config.add_route("booking_payment_reject", "/api/bookings/{id}/payment-reject")
        config.add_route("booking_by_tourist", "/api/bookings/tourist/{touristId}")
        config.add_route("booking_by_package", "/api/bookings/package/{packageId}")
        config.add_route("booking_payment_pending", "/api/bookings/payment/pending")
        
        ## reviews
        config.add_route("reviews", "/api/reviews")
        config.add_route("review_by_package", "/api/reviews/package/{packageId}")
        config.add_route("review_by_tourist", "/api/reviews/tourist/{touristId}")
        
        ## analytics
        config.add_route("analytics_agent_stats", "/api/analytics/agent/stats")
        config.add_route("analytics_agent_package_performance", "/api/analytics/agent/package-performance")
        config.add_route("analytics_tourist_stats", "/api/analytics/tourist/stats")
        
        # Static file serving untuk QRIS storage dan payment proofs
        config.add_static_view(name='qris', path='storage/qris', cache_max_age=3600)
        config.add_static_view(name='payment_proofs', path='storage/payment_proofs', cache_max_age=3600)
        config.add_static_view(name='destinations', path='storage/destinations', cache_max_age=3600)
        config.add_static_view(name='packages', path='storage/packages', cache_max_age=3600)

        #assignment_routes
        config.add_route("assignment_create", "/api/assignments")
        config.add_route("assignment_list", "/api/assignments")
        config.add_route("assignment_status", "/api/assignments/{id}/status")


        config.scan("views")
        config.scan("views.assignments")
        app = config.make_wsgi_app()

    print("Server running on http://0.0.0.0:6543 (Hot Reload Active)")
    serve(app, host="0.0.0.0", port=6543)


if __name__ == "__main__":
    hupper.start_reloader("main.main")
    main()
