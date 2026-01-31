import pytest
from your_module.services import UserService, validate_email

@pytest.fixture
def db():
    return {}

@pytest.fixture
def user_service(db):
    return UserService(db)

def test_create_user_valid_data(user_service):
    user_data = {"name": "Alice", "email": "alice@example.com"}
    user_id = user_service.create_user(user_data)
    assert user_id in user_service.db
    assert user_service.db[user_id]["name"] == "Alice"
    assert user_service.db[user_id]["email"] == "alice@example.com"

def test_create_user_invalid_data(user_service):
    with pytest.raises(ValueError):
        user_service.create_user({"name": "", "email": "invalid"})

def test_get_user_existing_user(user_service):
    user_service.create_user({"name": "Bob", "email": "bob@example.com"})
    user = user_service.get_user("user123")
    assert user["name"] == "Bob"
    assert user["email"] == "bob@example.com"

def test_get_user_non_existent_user(user_service):
    with pytest.raises(KeyError):
        user_service.get_user("nonexistent")

def test_update_user_valid_data(user_service):
    user_service.create_user({"name": "Charlie", "email": "charlie@example.com"})
    user_service.update_user("user456", {"name": "Charlie Updated"})
    user = user_service.get_user("user456")
    assert user["name"] == "Charlie Updated"

def test_update_user_invalid_user(user_service):
    with pytest.raises(KeyError):
        user_service.update_user("nonexistent", {})

def test_delete_user_valid(user_service):
    user_service.create_user({"name": "Dave", "email": "dave@example.com"})
    user_service.delete_user("user789")
    with pytest.raises(KeyError):
        user_service.get_user("user789")

def test_delete_user_invalid(user_service):
    with pytest.raises(KeyError):
        user_service.delete_user("nonexistent")

@pytest.mark.parametrize("email, expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("user@domain.co.uk", True),
    ("user.name@domain.com", True),
    ("user@domain", False),
    ("user@domain.c", False),
    ("", False),
])
def test_validate_email_valid_cases(email, expected):
    assert validate_email(email) == expected

@pytest.mark.parametrize("email", [
    None,
])
def test_validate_email_invalid_input(email):
    with pytest.raises(TypeError):
        validate_email(email)