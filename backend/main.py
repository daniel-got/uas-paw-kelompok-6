import hupper
from waitress import serve
from pyramid.config import Configurator


def main():
    with Configurator() as config:
        # route
        ## auth
        config.add_route("register", "/api/auth/register")
        config.add_route("login", "/api/auth/login")
        config.add_route("me", "/api/auth/me")

        config.scan("views")
        app = config.make_wsgi_app()

    print("Server running on http://0.0.0.0:6543 (Hot Reload Active)")
    serve(app, host="0.0.0.0", port=6543)


if __name__ == "__main__":
    hupper.start_reloader("main.main")
    main()
