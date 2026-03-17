from textual.widgets import Input

type InputEvent = Input.Changed | Input.Submitted


def get_input_validation(event: InputEvent) -> tuple[bool, list[str]]:
    result = event.validation_result
    is_valid = False if result is None else result.is_valid
    failure_descriptions = [] if result is None else result.failure_descriptions

    return is_valid, failure_descriptions
