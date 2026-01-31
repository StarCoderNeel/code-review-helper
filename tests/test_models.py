import pytest
import models
import re

@pytest.fixture
def user():
    return models.User(username='testuser', email='test@example.com', password='securepassword123')

@pytest.fixture
def invalid_user():
    return models.User(username='invaliduser', email='invalid-email', password='short')

def test_user_initialization_valid(user):
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.password == 'securepassword123'

def test_user_initialization_missing_username():
    with pytest.raises(ValueError):
        models.User(email='test@example.com', password='securepassword123')

def test_user_initialization_missing_email():
    with pytest,raises(ValueError):
        models.User(username='testuser', password='securepassword123')

def test_user_validate_valid_email(user):
    assert user.validate()

def test_user_validate_invalid_email(invalid_user):
    with pytest.raises(ValueError):
        invalid_user.validate()

@pytest.mark.parametrize("email, expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("user@domain.co.uk", True),
    ("user@domain", False),
    ("user@domain.com.", False),
    ("user.name@domain.com", True),
    ("user@domain.com", True),
    ("user@domain.com with space", False)
])
def test_validate_email_format(email, expected):
    user = models.User(username='testuser', email=email, password='securepassword123')
    if expected:
        assert user.validate()
    else:
        with pytest.raises(ValueError):
            user.validate()

def test_create_user_duplicate_username():
    models.create_user(username='dupuser', email='dup@example.com', password='securepassword123')
    with pytest.raises(ValueError):
        models.create_user(username='dupuser', email='dup2@example.com', password='securepassword123')

def test_create_user_invalid_password_length():
    with pytest.raises(ValueError):
        models.create_user(username='testuser', email='test@example.com', password='123')

def test_create_user_missing_required_fields():
    with pytest.raises(ValueError):
        models.create_user(username='testuser', email='test@example.com')  # Missing password

def test_user_password_hashing():
    user = models.User(username='hashuser', email='hash@example.com', password='securepassword123')
    assert user.password != 'securepassword123'  # Ensure password is not stored in plaintext