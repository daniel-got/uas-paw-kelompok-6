from .auth_routes import include_auth_routes
from .package_routes import include_packages_routes
from .destination_routes import include_destinations_routes
from .qris_routes import include_qris_routes
from .payment_routes import include_payments_routes
from .booking_routes import include_bookings_routes
from .review_routes import include_review_routes
from .analytics_routes import include_analytics_routes
from .assignment_routes import include_assignment_routes


def include_routes(config):
    include_auth_routes(config)
    include_packages_routes(config)
    include_destinations_routes(config)
    include_qris_routes(config)
    include_payments_routes(config)
    include_bookings_routes(config)
    include_review_routes(config)
    include_analytics_routes(config)
    include_assignment_routes(config)
