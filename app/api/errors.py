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


class InvalidAmount(BaseError):
    CODE = 0000
    MESSAGE = "New bid should be greater than previous bid"


class CantPlaceBid(BaseError):
    CODE = 0000
    MESSAGE = "You can't place bid on this item"


class AuctionHasEnded(BaseError):
    CODE = 0000
    MESSAGE = "Auction has ended"


class OwnerCanNotBid(BaseError):
    CODE = 0000
    MESSAGE = "Owner can't bid on his item"


class BidIsSmallerThanMinBidStep(BaseError):
    CODE = 0000
    MESSAGE = "Bid is smaller than minimum bid step"


class EndDateMustBeBigger(BaseError):
    CODE = 0000
    MESSAGE = "End date must be bigger"


class CanNotDeleteWhenWinnerIsChosen(BaseError):
    CODE = 0000
    MESSAGE= "Can't delete item when winner is chosen"