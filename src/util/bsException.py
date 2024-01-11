class BSException(Exception):
    def __init__(self, error: str, statusCode: int = 400):
        self.error = error
        self.statusCode = statusCode
        super().__init__(error)
