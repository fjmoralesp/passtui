import pytest
from passtui.utils.clipboard import (
    copy_password_to_clipboard,
    copy_username_to_clipboard,
    copy_line_to_clipboard,
)
from passtui.models.pass_store import PassModel


def test_copy_password_to_clipboard():
    pass_model = PassModel("mypassword\nUsername: testuser")

    result = copy_password_to_clipboard(pass_model)
    assert isinstance(result, bool)


def test_copy_username_to_clipboard():
    pass_model = PassModel("mypassword\nUsername: testuser")

    result = copy_username_to_clipboard(pass_model)
    assert isinstance(result, bool)


def test_copy_line_to_clipboard():
    result = copy_line_to_clipboard("test line")
    assert isinstance(result, bool)

    result = copy_line_to_clipboard("")
    assert isinstance(result, bool)
