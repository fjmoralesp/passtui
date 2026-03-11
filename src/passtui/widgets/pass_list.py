from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import ListItem, ListView, Label


class PassList(Container):
    items = reactive(list, recompose=True)
    selected = reactive("")

    def compose(self) -> ComposeResult:
        list_items = [ListItem(Label(item)) for item in self.items]
        yield ListView(*list_items)

    @on(ListView.Selected)
    def on_selected(self, event: ListView.Selected) -> None:
        self.selected = self.items[event.index]
