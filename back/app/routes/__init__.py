from . import auth
from . import user

def api_add_resouces(api):
    api.add_resource(auth.LoginApi, '/api/auth/login')
    # api.add_resource(auth.RegisterApi, '/api/auth/register')
    api.add_resource(user.UsersApi, '/api/user')
    api.add_resource(user.UserApi, '/api/user/<id>')
