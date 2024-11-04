class UnrelatedException(Exception):
    def __init__(self, errcode = 0):
        errcodes = [0, 1]
        errdic = ['user must be logged out to do this', 'user must be inside a room to leave it']
        self.errcode = 0
        if errcode in errcodes:
            self.errcode = errcode
        self.errtxt = errdic[errcode]
        super().__init__('unhandled unrelated exception')
