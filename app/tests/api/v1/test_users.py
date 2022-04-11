from app.tests.utils.user import *

API_V1_STR = "/api/v1/jsonrpc"


def test_signup(client: TestClient, db: Session) -> None:
    identity = random_identity()
    params = {
        "form_data": {
            "email": identity.email,
            "password": identity.password,
            "full_name": identity.name,
            "password_confirm": identity.password,
        }
    }

    r = client.post(API_V1_STR, data=wrap_to_jsonrpc(params, "signup"))
    result = r.json()["result"]
    user = crud.crud_user.get_by_email(db, email=identity.email)

    assert user
    assert user.email == result["email"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    identity = random_identity()

    user_in = UserCreate(
        full_name=identity.name,
        email=EmailStr(identity.email),
        password=identity.password,
        password_confirm=identity.password,
    )

    user = crud.crud_user.create(db, user_in)

    params = {"user_id": str(user.id)}

    r = client.post(
        API_V1_STR,
        headers=superuser_token_headers,
        data=wrap_to_jsonrpc(params, method="get_user_by_id"),
    )

    result = r.json()["result"]
    existing_user = crud.crud_user.get_by_email(db, email=identity.email)

    assert existing_user
    assert existing_user.email == result["email"]


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    identity = random_identity()

    user_in = UserCreate(
        full_name=identity.name,
        email=EmailStr(identity.email),
        password=identity.password,
        password_confirm=identity.password,
    )
    crud.crud_user.create(db, user_in)

    params = {
        "form_data": {
            "email": identity.email,
            "password": identity.password,
            "full_name": identity.name,
            "password_confirm": identity.password,
        }
    }

    r = client.post(API_V1_STR, data=wrap_to_jsonrpc(params, method="signup"))
    created_user = r.json()

    assert "error" in created_user


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    identity = random_identity()
    user_in = UserCreate(
        full_name=identity.name,
        email=EmailStr(identity.email),
        password=identity.password,
        password_confirm=identity.password,
    )
    crud.crud_user.create(db, user_in)

    identity2 = random_identity()
    user_in2 = UserCreate(
        full_name=identity2.name,
        email=EmailStr(identity2.email),
        password=identity2.password,
        password_confirm=identity2.password,
    )
    crud.crud_user.create(db, user_in2)

    params = {"skip": 0, "limit": 100}

    r = client.post(
        API_V1_STR,
        headers=superuser_token_headers,
        data=wrap_to_jsonrpc(params, "get_users"),
    )
    result = r.json()["result"]

    assert len(result) > 1
    for user in result:
        assert "email" in user
