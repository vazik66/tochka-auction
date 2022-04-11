from sqlalchemy.orm import Session
from app.crud import crud_item
from app.schemas.item import ItemCreate, ItemUpdate
from app.tests.utils import utils


def test_create_item(db: Session, user_for_test) -> None:
    randomItemData = utils.Random_Item()
    item = ItemCreate(
        title=randomItemData.title,
        description=randomItemData.description,
        price=randomItemData.price,
    )
    item = crud_item.create(db, item, user_for_test)
    assert item.title == randomItemData.title
    assert item.is_moderating is True
    assert item.owner_id == user_for_test.id


def test_get_multi_by_owner(db: Session, user_for_test) -> None:
    items = crud_item.get_multi_by_owner(db, owner_id=user_for_test.id)
    assert len(items) > 0


def test_get_multy_default(db: Session) -> None:
    items = crud_item.get_multi(db)
    assert len(items) == 0


def test_update(db: Session, user_for_test):
    item = crud_item.get_multi_by_owner(db, owner_id=user_for_test.id)[0]
    item_update = ItemUpdate(title="Updated Title")

    item = crud_item.update(db, item=item, item_update=item_update)

    assert item.title == "Updated Title"


def test_get_by_id(db: Session, user_for_test):
    item = crud_item.get_multi_by_owner(db, owner_id=user_for_test.id)[0]

    item2 = crud_item.get_by_id(db, item.id)

    assert item == item2
