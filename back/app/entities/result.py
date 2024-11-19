class Result:
    def __init__(self, code=0, msg=None, data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def set_code(self, code):
        self.code = code

    def set_msg(self, msg):
        self.msg = msg

    def set_data(self, data):
        self.data = data

    def to_dict(self):
        data = { 'code': self.code, }
        if self.msg is not None:
            data['msg'] = self.msg
        if self.data is not None:
            data['data'] = self.data

        return data
