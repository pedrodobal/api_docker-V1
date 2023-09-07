import app
from os import environ

if __name__ == '__main__':
    db_params = {
            "dbname": "infnet",
            "user": "postgres",
            "password": "aquelasenha",
            "host": "192.168.1.107",
            "port": "5432"
        }
    SERVER_HOST = environ.get('SERVER_HOST', 'localhost')
    api_app = app.create_app(db_params)
    api_app.run(host=SERVER_HOST, port=5500, debug=(not environ.get('ENV') == 'PRODUCTION'), threaded=True)