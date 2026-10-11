class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class CourseRecommendationError(AppException):
    """Raised when there is an issue generating recommendations."""

    def __init__(self, message: str):
        super().__init__(message, status_code=500)
