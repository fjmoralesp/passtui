from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label, Button
from typing import Any


class ConfirmModalScreen(ModalScreen[bool]):
    BINDINGS = [
        Binding("enter", "confirm", "Confirm", priority=True),
        Binding("escape", "cancel", "Cancel"),
    ]

    DEFAULT_CSS = """
    ConfirmModalScreen {
        align: center middle;
    }
    ConfirmModalScreen Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 1 2;
        width: 84;
        height: 11;
        border: tall $warning;
        border-title-color: $warning;
        border-title-align: center;
        background: $surface;
    }
    ConfirmModalScreen Label {
        column-span: 2;
        width: 1fr;
        content-align: center middle;
        color: $text;
        padding: 0 1;
    }
    ConfirmModalScreen Button {
        width: 1fr;
        height: 1fr;
    }
    """

    def __init__(
        self,
        message: str = "Are you sure?",
        title: str = "Confirm",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._message = message
        self._title = title

    def compose(self) -> ComposeResult:
        with Grid(id="modal-grid"):
            yield Label(self._message)
            yield Button("(Enter) Confirm", variant="warning", id="confirm")
            yield Button("(Esc) Cancel", variant="error", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#modal-grid").border_title = f" {self._title} "

    @on(Button.Pressed, "#confirm")
    async def handle_button_confirm(self) -> None:
        self.action_confirm()

    @on(Button.Pressed, "#cancel")
    async def handle_button_cancel(self) -> None:
        self.action_cancel()

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)
