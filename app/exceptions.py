class ApiError(Exception):
    pass


class DataSourceException(ApiError):
    pass


class PlayerNotFoundException(ApiError):
    pass


class NoPersonasException(ApiError):
    pass


class TooManyPersonasException(ApiError):
    pass
