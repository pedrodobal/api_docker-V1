from flask import Flask, Blueprint
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restplus import Api

from app.domain.account.account_controller import api as account
from app.domain.transaction.transaction_controller import api as transaction

def create_app(db_params):
    app = Flask(__name__)
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['DB_PARAMS'] = db_params
    app.wsgi_app = ProxyFix(app.wsgi_app)
    blueprint = Blueprint('api', __name__)
    app.register_blueprint(blueprint)

    api = Api(app, title='Transactions', version='1.0',prefix='/api')

    api.add_namespace(account, path='/account')
    api.add_namespace(transaction, path='/transaction')

    return app