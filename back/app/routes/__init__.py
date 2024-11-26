from . import user_room
from . import auth
from . import user

def api_add_resouces(api):
    # 登陆接口
    api.add_resource(auth.LoginApi, '/api/auth/login')
    # 用户接口
    api.add_resource(user.UsersApi, '/api/user')
    api.add_resource(user.UserApi, '/api/user/<id>')
    # 房间用户映射关系
    api.add_resource(user_room.UserRoomsApi, '/api/user-room')
    api.add_resource(user_room.UserRoomApi, '/api/user-room/<room_id>/<user_id>')
