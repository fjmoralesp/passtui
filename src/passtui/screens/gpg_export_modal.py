from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button


class GpgExportData:
    __slots__ = ("passphrase", "output_path")

    def __init__(self, passphrase: bytearray, output_path: str | None) -> None:
        self.passphrase = passphrase
        self.output_path = output_path

    def zero(self) -> None:
        for i in range(len(self.passphrase)):
            self.passphrase[i] = 0


class GpgExportModalScreen(ModalScreen[GpgExportData | None]):
    BINDINGS = [
        Binding("enter", "submit", "Submit", priority=True),
        Binding("escape", "cancel", "Cancel"),
    ]

    DEFAULT_CSS = """
    GpgExportModalScreen {
        align: center middle;
    }
    GpgExportModalScreen Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        padding: 1 2;
        width: 84;
        height: 15;
        border: tall $primary;
        border-title-color: $primary;
        border-title-align: center;
        background: $surface;
    }
    GpgExportModalScreen Horizontal {
        column-span: 2;
        border: tall $surface-lighten-2;
        padding: 0 1;
    }
    GpgExportModalScreen Horizontal Label {
        margin: 0 1 0 0;
        color: $text-muted;
    }
    GpgExportModalScreen Button {
        width: 1fr;
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        with Grid(id="modal-grid"):
            with Horizontal():
                yield Label("Enter GPG key passphrase:")
                yield Input(
                    placeholder="(e.g., password)",
                    id="passphrase",
                    password=True,
                    compact=True,
                )
            with Horizontal():
                yield Label("Output file path (optional):")
                yield Input(
                    placeholder="(defaults: ~/passtui/gpg-export.asc)",
                    id="output",
                    compact=True,
                )
            yield Button("(Enter) Submit", variant="primary", id="submit")
            yield Button("(Esc) Cancel", variant="error", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#modal-grid").border_title = " Export GPG Key "

    @on(Button.Pressed, "#submit")
    async def handle_button_submit(self) -> None:
        self.action_submit()

    @on(Button.Pressed, "#cancel")
    async def handle_button_cancel(self) -> None:
        self.action_cancel()

    def action_submit(self) -> None:
        passphrase_str = self.query_one("#passphrase", Input).value
        output = self.query_one("#output", Input).value
        if passphrase_str:
            self.dismiss(
                GpgExportData(
                    passphrase=bytearray(passphrase_str.encode("utf-8")),
                    output_path=output if output else None,
                )
            )
        else:
            self.notify("Passphrase is required", severity="error")

    def action_cancel(self) -> None:
        self.dismiss(None)
