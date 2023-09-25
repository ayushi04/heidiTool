
class CustomExceptionBase(Exception):
    """Base class for custom exceptions."""
    pass

class MyCustomException(CustomExceptionBase):
    """Custom exception for a specific error scenario."""
    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)