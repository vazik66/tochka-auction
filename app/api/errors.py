from fastapi_jsonrpc import BaseError


class TODOError(BaseError):
    CODE = 0000
    MESSAGE = "TODO ERROR"


class PasswordsDoNotMatch(BaseError):
    CODE = -32001
    MESSAGE = "Passwords do not match"


class EmailAlreadyInUse(BaseError):
    CODE = -32002
    MESSAGE = "Email already in use"


class IncorrectEmailOrPassword(BaseError):
    CODE = -32003
    MESSAGE = "Incorrect email or password"


class NotEnoughPrivileges(BaseError):
    CODE = -32004
    MESSAGE = "Not enough privileges"


class UserNotFound(BaseError):
    CODE = -32005
    MESSAGE = "User not found"


class BadCredentials(BaseError):
    CODE = -32006
    MESSAGE = "Could not validate credentials"


class ItemNotFound(BaseError):
    CODE = -32007
    MESSAGE = "Item Not Found"


class EmailNotValid(BaseError):
    CODE = -32008
    MESSAGE = "Email is invalid"


class InvalidAmount(BaseError):
    CODE = -32009
    MESSAGE = "New bid should be greater than previous bid"


class CantPlaceBid(BaseError):
    CODE = -32010
    MESSAGE = "You can't place bid on this item"


class AuctionHasEnded(BaseError):
    CODE = -32011
    MESSAGE = "Auction has ended"


class OwnerCanNotBid(BaseError):
    CODE = -32012
    MESSAGE = "Owner can't bid on his item"


class BidIsSmallerThanMinBidStep(BaseError):
    CODE = -32013
    MESSAGE = "Bid is smaller than minimum bid step"


class EndDateMustBeBigger(BaseError):
    CODE = -32014
    MESSAGE = "End date must be bigger"


class CanNotDeleteWhenWinnerIsChosen(BaseError):
    CODE = -32015
    MESSAGE = "Can't delete item when winner is chosen"
