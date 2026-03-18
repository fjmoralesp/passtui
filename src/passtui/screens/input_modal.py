from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Input
from typing import Any


class InputModalScreen(Screen[str | None]):
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(
        self, placeholder: str = "Enter value", *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self._placeholder = placeholder

    def compose(self) -> ComposeResult:
        yield Input(placeholder=self._placeholder)

    @on(Input.Submitted)
    async def on_submit(self, event: Input.Submitted) -> None:
        value = event.value
        self.dismiss(value if value else None)

    def action_cancel(self) -> None:
        self.dismiss(None)
