import pytest
import utils
from datetime import datetime

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")
    return file_path

def test_safe_divide_normal_case():
    assert utils.safe_divide(10, 2) == 5

def test_safe_divide_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        utils.safe_divide(10, 0)

def test_safe_divide_non_numeric():
    with pytest.raises(TypeError):
        utils.safe_divide("a", 2)

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (6, 3, 2),
    (0, 5, 0),
    (None, 5, None),
    (10, 0, None),
    ("100", 2, 50),
    (None, None, None),
])
def test_safe_divide_params(a, b, expected):
    result = utils.safe_divide(a, b)
    assert result == expected

def test_parse_int_valid():
    assert utils.parse_int("123") == 123
    assert utils.parse_int("-456") == -456
    assert utils.parse_int("0") == 0

def test_parse_int_invalid():
    with pytest.raises(ValueError):
        utils.parse_int("abc")
    with pytest.raises(TypeError):
        utils.parse_int(None)

@pytest.mark.parametrize("s, expected", [
    ("123", 123),
    ("-456", -456),
    ("0", 0),
    ("abc", None),
    (None, None),
    ("", None),
])
def test_parse_int_params(s, expected):
    assert utils.parse_int(s) == expected

@pytest.mark.parametrize("email, expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("user@domain", False),
    ("user@domain.co.uk", True),
    (None, False),
    ("", False),
    ("test@.com", False),
    ("test@domain..com", False),
])
def test_is_valid_email_params(email, expected):
    assert utils.is_valid_email(email) == expected

def test_format_date_valid():
    date_obj = datetime(2023, 10, 5)
    assert utils.format_date(date_obj, "%Y-%m-%d") == "2023-10-05"

def test_format_date_invalid_format():
    with pytest.raises(ValueError):
        utils.format_date(datetime(2023, 10, 5), "InvalidFormat")

def test_format_date_none():
    assert utils.format_date(None, "%Y-%m-%d") is None

def test_read_file_valid(temp_file):
    content = utils.read_file(temp_file)
    assert content == "test content"

def test_read_file_not_found():
    with pytest.raises(FileNotFoundError):
        utils.read_file("nonexistent.txt")

def test_read_file_empty():
    empty_file = temp_file.parent / "empty.txt"
    empty_file.touch()
    assert utils.read_file(empty_file) == ""

def test_merge_dicts_normal():
    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 3, "c": 4}
    result = utils.merge_dicts(dict1, dict2)
    assert result == {"a": 1, "b": 3, "c": 4}

def test_merge_dicts_overwrite():
    dict1 = {"a": 1}
    dict2 = {"a": 2}
    result = utils.merge_dicts(dict1, dict2)
    assert result == {"a": 2}

def test_merge_dicts_none():
    assert utils.merge_dicts(None, {"a": 1}) == {"a": 1}
    assert utils.merge_dicts({"a": 1}, None) == {"a": 1}

def test_generate_uuid():
    uuid = utils.generate_uuid()
    assert uuid is not None
    assert isinstance(uuid, str)
    assert len(uuid) == 36

def test_validate_password_valid():
    assert utils.validate_password("Password1!") is True
    assert utils.validate_password("Pass1!") is True
    assert utils.validate_password("p@ssw0rd") is True

def test_validate_password_invalid():
    assert utils.validate_password("password") is False
    assert utils.validate_password("PASSWORD1!") is False
    assert utils.validate_password("Pass1") is False
    assert utils.validate_password("") is False
    assert utils.validate_password(None) is False
    assert utils.validate_password("123456") is False
    assert utils.validate_password("Pass123") is False