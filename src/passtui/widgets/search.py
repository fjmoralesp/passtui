from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Input, Static, Label
from passtui.widgets.pass_list import PassList
from typing import Any


class Search(Static):
    _id: str
    _input: Input

    BORDER_TITLE = "/"

    BINDINGS = [
        Binding("enter", "search", "Search", priority=True),
        Binding("escape", "cancel", "Cancel"),
    ]

    DEFAULT_CSS = """
        Search {
            column-span: 2;
            layout: horizontal;
            border: solid $primary-muted;
            height: 100%;
            padding: 0 2;
        }
        Search Label {
            margin: 0 1 0 0;
        }
    """

    def __init__(self, data: list[str], id: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self.results = data
        self._id = id

    def action_search(self) -> None:
        self.screen.focus_next(PassList)

    def action_cancel(self) -> None:
        self._input.clear()
        self.screen.focus_next(PassList)

    def compose(self) -> ComposeResult:
        self._input = Input(placeholder="Type to search", id=self._id, compact=True)
        yield Label("Search:")
        yield self._input

    def set_focus(self) -> None:
        self._input.focus()

    def apply_filter(self, value: str) -> None:
        if value:
            self.results = [
                entry for entry in self.data if value.lower() in entry.lower()
            ]
        else:
            self.results = self.data

    def get_value(self) -> str:
        return self._input.value

    def refresh_filter(self) -> None:
        self.apply_filter(self.get_value())

    @on(Input.Changed)
    async def on_changed(self, event: Input.Changed) -> None:
        self.apply_filter(event.value)
