from typing import Optional

from app.api.api_v1.users import rpc

from fastapi import Depends

from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps, errors
from pydantic import parse_obj_as


@rpc.method()
def create_item(
    item_in: schemas.ItemCreate,
    db: Session = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
) -> schemas.Item:
    """
    {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "create_item",
      "params": {
         "item_in": {
          "title": "string",
          "description": "string",
          "price": 0
        }
      }
    }
    """
    item = crud.crud_item.create(db, item_in, user)
    return schemas.Item.from_orm(item)


@rpc.method()
def get_multi_by_owner(
    skip: Optional[int],
    limit: Optional[int],
    db: Session = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
) -> list[schemas.Item]:
    """
    {
      "jsonrpc": "2.0",
      "id": 0,
      "method": "get_multi_by_owner",
      "params": {
        "skip": 0,
        "limit": 100
      }
    }
    """
    items = crud.get_multi_by_owner(db=db, owner_id=user.id, skip=skip, limit=limit)
    return parse_obj_as(list[schemas.Item], items)


@rpc.method()
def get_items(
    skip: Optional[int], limit: Optional[int], db: Session = Depends(deps.get_db)
) -> list[schemas.Item]:
    """
    {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "get_items",
      "params": {
        "skip": 0,
        "limit": 100
      }
    }
    """
    return crud.crud_item.get_multi(db, skip, limit)


@rpc.method()
def delete_item(
    item_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> str:
    """
    {
      "jsonrpc": "2.0",
      "id": 0,
      "method": "delete_item",
      "params": {
        "item_id": "string"
      }
    }
    """
    item = crud.crud_item.get_by_id(db, item_id)
    if not item:
        raise errors.ItemNotFound
    if current_user.id != item.owner_id or not current_user.is_superuser:
        raise errors.NotEnoughPrivileges

    crud.crud_item.delete(db, item_id)
    return "Success"


@rpc.method()
def set_moderation(
    item_id: str,
    db: Session = Depends(deps.get_db),
    _: models.User = Depends(deps.get_current_superuser),
) -> schemas.Item:
    """
    {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "set_moderation",
      "params": {
          "item_id": "string"
      }
    }
    """
    item = crud.crud_item.get_by_id(db, item_id)
    if not item:
        raise errors.ItemNotFound
    item = crud.crud_item.set_moderate(db, item.id)
    return item


@rpc.method()
def remove_moderation(
    item_id: str,
    db: Session = Depends(deps.get_db),
    _: models.User = Depends(deps.get_current_superuser),
) -> schemas.Item:
    """
    {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "remove_moderation",
      "params": {
          "item_id": "string"
      }
    }
    """
    item = crud.crud_item.get_by_id(db, item_id)
    if not item:
        raise errors.ItemNotFound
    item = crud.crud_item.remove_moderate(db, item.id)
    return item


@rpc.method()
def archive(
    item_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Item:
    """
    {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "archive",
      "params": {
          "item_id": "string"
      }
    }
    """
    item = crud.crud_item.get_by_id(db, item_id)
    if not item:
        raise errors.ItemNotFound
    if current_user.id != item.owner_id or not current_user.is_superuser:
        raise errors.NotEnoughPrivileges
    item = crud.crud_item.set_archive(db, item.id)
    return item


@rpc.method()
def remove_archive(
    item_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Item:
    """
    {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "remove_archive",
      "params": {
          "item_id": "string"
      }
    }
    """
    item = crud.crud_item.get_by_id(db, item_id)
    if not item:
        raise errors.ItemNotFound
    if current_user.id != item.owner_id or not current_user.is_superuser:
        raise errors.NotEnoughPrivileges
    item = crud.crud_item.remove_archive(db, item.id)
    return item
