class WNSException(Exception):
    def __init__(self, code: int, title: str, message: str):
        self.code = code
        self.title = title
        self.message = message