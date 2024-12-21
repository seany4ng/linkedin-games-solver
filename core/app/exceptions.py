# General API Exception
class APIException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# Specific API Exceptions
class TangoBoardInsufficientException(APIException):
    def __init__(self):
        super().__init__(
            message="Provided Tango board state is insufficient",
            status_code=400,
        )


class TangoBoardSolvedIncorrectlyException(APIException):
    def __init__(self):
        super().__init__(
            message="Tango board was solved incorrectly",
            status_code=400,
        )
