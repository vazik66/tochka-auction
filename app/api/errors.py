from fastapi_jsonrpc import BaseError


class TODOError(BaseError):
    CODE = 0000
    MESSAGE = "TODO ERROR"


class PasswordsDoNotMatch(BaseError):
    CODE = 0000
    MESSAGE = "Passwords do not match"


class EmailAlreadyInUse(BaseError):
    CODE = 0000
    MESSAGE = "Email already in use"


class IncorrectEmailOrPassword(BaseError):
    CODE = 0000
    MESSAGE = "Incorrect email or password"


class NotEnoughPrivileges(BaseError):
    CODE = 0000
    MESSAGE = "Not enough privileges"


class UserNotFound(BaseError):
    CODE = 0000
    MESSAGE = "User not found"


class BadCredentials(BaseError):
    CODE = 0000
    MESSAGE = "Could not validate credentials"


class ItemNotFound(BaseError):
    CODE = 0000
    MESSAGE = "Item Not Found"


class EmailNotValid(BaseError):
    CODE = 0000
    MESSAGE = "Email is invalid"
