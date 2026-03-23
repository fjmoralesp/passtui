from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button
from typing import Any


class InputModalScreen(ModalScreen[str | None]):
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    DEFAULT_CSS = """
    InputModalScreen {
        align: center middle;
    }
    InputModalScreen Grid {
        column-span: 2;
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 2;
        width: 80;
        height: 9;
        border: thick $background 80%;
        background: $surface;
    }
    InputModalScreen Horizontal {
        column-span: 2;
        border: solid $primary-muted;
    }
    InputModalScreen Horizontal Label {
        margin: 0 1 0 0;
    }
    InputModalScreen Button {
        width: 1fr;
        height: 1fr;
    }
    """

    def __init__(
        self,
        label: str = "Input",
        placeholder: str = "Enter value",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._label = label
        self._placeholder = placeholder

    def compose(self) -> ComposeResult:
        with Grid():
            with Horizontal():
                yield Label(self._label + ":")
                yield Input(placeholder=self._placeholder, compact=True)
            yield Button("(Enter) Submit", variant="primary", id="submit")
            yield Button("(Esc) Cancel", variant="error", id="cancel")

    @on(Button.Pressed, "#submit")
    async def handle_button_submit(self) -> None:
        value = self.query_one(Input).value
        self.submit(value)

    @on(Button.Pressed, "#cancel")
    async def handle_button_cancel(self) -> None:
        self.action_cancel()

    @on(Input.Submitted)
    async def on_submit(self, event: Input.Submitted) -> None:
        self.submit(event.value)

    def submit(self, value: str | None) -> None:
        self.dismiss(value if value else None)

    def action_cancel(self) -> None:
        self.dismiss(None)
