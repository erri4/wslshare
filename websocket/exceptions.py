class UnrelatedException(Exception):
    def __init__(self, errcode: int = 0) -> None:
        errcodes = [0, 1, 2]
        errdic = ['user must be logged out to do this', 'user must be inside a room to do this', 'user can\'t be connected twice']
        self.errcode = 0
        if errcode in errcodes:
            self.errcode = errcode
        self.errtxt = errdic[errcode]
        super().__init__('unhandled unrelated exception')
