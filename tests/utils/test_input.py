from textual.widgets import Input
from passtui.utils.input import get_input_validation


def test_get_input_validation_valid():
    validation_result = type(
        "obj", (object,), {"is_valid": True, "failure_descriptions": []}
    )()

    event = Input.Submitted(None, "test")
    event.validation_result = validation_result

    is_valid, failures = get_input_validation(event)
    assert is_valid == True
    assert failures == []


def test_get_input_validation_invalid():
    validation_result = type(
        "obj",
        (object,),
        {"is_valid": False, "failure_descriptions": ["Validation failed"]},
    )()

    event = Input.Submitted(None, "test")
    event.validation_result = validation_result

    is_valid, failures = get_input_validation(event)
    assert is_valid == False
    assert failures == ["Validation failed"]


def test_get_input_validation_none_result():
    event = Input.Submitted(None, "test")
    event.validation_result = None

    is_valid, failures = get_input_validation(event)
    assert is_valid == False
    assert failures == []
