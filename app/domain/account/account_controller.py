from flask_restplus import Resource, Namespace, fields
from flask import request, current_app
from app.domain.account.account_db import AccountDb

api = Namespace('Account', description='Account Manager')
model = api.model('AccountModel', {
    'active_card': fields.Boolean,
    'available_limit': fields.Integer
})
@api.route('/')
class AccountController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account_db = AccountDb(current_app.config.get('DB_PARAMS'))

    @api.response(200, "Found with success")
    def get(self):
        response = self.account_db.get_accounts()
        return response, 200
    
    @api.expect(model)
    @api.param('active_card','if the card is active',)
    @api.param('available_limit','available limit')
    def post(self):
        data = request.get_json()
        if data:
            if 'active_card' not in data or 'available_limit' not in data:
                error_response = {
                    "errorCode": 'ToDo',
                    "message": 'Bad Request - Missing required fields'
                }
                return error_response, 400
            else:
                account = self.account_db.create_account(data["active_card"], data["available_limit"])
                response = {
                    "account": account.__dict__
                }
                return response, 201
        error_response = {
                "errorCode": 'ToDo',
                "message": 'Bad Request'
            }
        return error_response, 400



@api.route('/<id>')
class AccountIdController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account_db = AccountDb(current_app.config.get('DB_PARAMS'))

    @api.response(200, "Request success")
    def get(self, id):
        account = self.account_db.get_account(id)
        if account:
            return account, 200
        else:
            error_response = {
                "errorCode": 'ToDo',
                "message": f'id {id} não encontrado'
            }
            return error_response, 404

    @api.response(200, "Request success")
    @api.expect(model)
    def put(self, id):
        data = request.json
        if not any(item in data for item in ['active_card', 'available_limit']):
            error_response = {
                "errorCode": 'ToDo', 
                "message": 'Bad Request - Missing required fields'
            }
            return error_response, 400
        else:
            return self.account_db.change_account(id, data), 201

    def delete(self, id):
        rows_affected = self.account_db.remove_account(id)
        if rows_affected > 0:
            return "", 204
        else:
            error_response = {
                "errorCode": 'ToDo',
                "message": f'id {id} não encontrado'
            }
            return error_response, 404
