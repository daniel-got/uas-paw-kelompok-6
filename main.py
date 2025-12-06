from waitress import serve
from pyramid.config import Configurator
from sqlalchemy import create_engine
import hupper

def main():
    engine = create_engine("sqlite://", echo=True)
    with Configurator() as config:
        # Route
        config.add_route('home', '/api')
        config.add_route('chatai', '/api/chatai')

        config.include('views')
        config.scan()
        app = config.make_wsgi_app()
    
    print("Server running on http://0.0.0.0:6543 (Hot Reload Active)")
    serve(app, host='0.0.0.0', port=6543)

if __name__ == '__main__':
    hupper.start_reloader('main.main')
    
    main()
