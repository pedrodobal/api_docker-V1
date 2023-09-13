import app
from os import environ

def main():
    SERVER_HOST = environ.get('SERVER_HOST', 'localhost')
    application = create_application()
    application.run(host=SERVER_HOST, port=5500, debug=(not environ.get('ENV') == 'PRODUCTION'), threaded=True)

def create_application():
    db_params = {
        "dbname": environ.get('DB_NAME', 'default_dbname'),
        "user": environ.get('DB_USER', 'default_user'),
        "password": environ.get('DB_PASSWORD', 'default_password'),
        "host": environ.get('DB_HOST', 'default_host'),
        "port": environ.get('DB_PORT', 'default_port')
    }
    return app.create_app(db_params)

if __name__ == '__main__':
    main()
