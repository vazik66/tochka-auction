import datetime
from typing import Optional

from app.api.api_v1.users import rpc

from fastapi import Depends

from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps, errors


@rpc.method(tags=["Item"])
async def create_item(
    item_in: schemas.ItemCreate,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
    s3=Depends(deps.get_s3_client),
) -> schemas.Item:
    """
    Creates item
    """
    user = crud.crud_user.get_by_id(db, current_user_token.sub)
    end_date = datetime.datetime.utcfromtimestamp(item_in.end_date)
    if end_date < datetime.datetime.utcnow():
        raise errors.EndDateMustBeBigger
    if item_in.min_bid < 0 or item_in.min_bid_step < 0:
        raise errors.TODOError
    item = crud.crud_item.create(db, s3, item_in, user)
    return schemas.Item.from_orm(item)


@rpc.method(tags=["Item"])
async def get_item_by_id(
    item_id: str,
    db: Session = Depends(deps.get_db),
) -> schemas.Item:
    """
    Finds item by item_id
    """
    item = crud.crud_item.get_by_id(db, item_id)
    if not item:
        raise errors.ItemNotFound
    return item


@rpc.method(tags=["Item"])
async def get_multi_by_owner(
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> list[schemas.Item]:
    """
    Finds items by current user id
    """
    items = crud.crud_item.get_multi_by_owner(db=db, owner_id=current_user_token.sub)
    return items


@rpc.method(tags=["Item"])
async def get_items(
    skip: Optional[int], limit: Optional[int], db: Session = Depends(deps.get_db)
) -> list[schemas.Item]:
    """
    Returns items with optional skip, limit params
    """
    return crud.crud_item.get_multi(db, skip, limit)


@rpc.method(tags=["Item"])
async def delete_item(
    item_id: str,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
    s3=Depends(deps.get_s3_client),
) -> str:
    """
    Deletes item by item_id if item_owner is current user or if superuser
    """
    item = crud.crud_item.get_by_id(db, item_id)
    if not item:
        raise errors.ItemNotFound
    if len(item.bids) > 0:
        # Can't delete as there are bids placed
        raise errors.TODOError
    if (
        current_user_token.sub != str(item.owner_id)
        and not current_user_token.is_superuser
    ):
        raise errors.NotEnoughPrivileges

    crud.crud_item.delete(db, s3, item_id)
    return "Success"


@rpc.method(tags=["Item"])
async def archive(
    item_id: str,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> schemas.Item:
    """
    Archives item if item owner is current user or if superuser
    """
    item = crud.crud_item.get_by_id(db, item_id)
    if not item:
        raise errors.ItemNotFound
    if current_user_token.sub != item.owner_id and not current_user_token.is_superuser:
        raise errors.NotEnoughPrivileges
    item = crud.crud_item.set_archive(db, item.id)
    return item


@rpc.method(tags=["Item"])
async def remove_archive(
    item_id: str,
    db: Session = Depends(deps.get_db),
    current_user_token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> schemas.Item:
    """
    Unarchives item if item owner is current user or if superuser
    """
    item = crud.crud_item.get_by_id(db, item_id)
    if not item:
        raise errors.ItemNotFound
    if current_user_token.sub != item.owner_id and not current_user_token.is_superuser:
        raise errors.NotEnoughPrivileges
    item = crud.crud_item.remove_archive(db, item.id)
    return item
