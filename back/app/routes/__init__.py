from . import auth

def api_add_resouces(api):
    api.add_resource(auth.LoginApi, '/api/auth/login')
    api.add_resource(auth.RegisterApi, '/api/auth/register')
