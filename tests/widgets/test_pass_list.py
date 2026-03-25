import pytest
from passtui.widgets.pass_list import PassList
from passtui.models.pass_store import PassModel
from passtui.security import passcli
from textual.app import App, ComposeResult
from textual.widgets import Static


class AppHelper(App):
    def compose(self) -> ComposeResult:
        yield PassList(items=["item1", "item2"], id="pass_list")


def test_passlist_init():
    items = ["item1", "item2"]
    pass_list = PassList(items=items)
    assert pass_list.items == items
    assert pass_list.is_filter == False


def test_passlist_watch_items():
    pass_list = PassList(items=[])
    pass_list.items = ["item1", "item2"]
    assert pass_list.items == ["item1", "item2"]


@pytest.mark.asyncio
async def test_passlist_get_highlighted_node_data():
    app = AppHelper()
    async with app.run_test() as pilot:
        pass_list = app.query_one("#pass_list", PassList)
        pass_list._current_node = type("obj", (object,), {"data": None})()
        assert pass_list._get_highlighted_node_data() is None


@pytest.mark.asyncio
async def test_passlist_action_copy_password():
    app = AppHelper()
    async with app.run_test() as pilot:
        pass_list = app.query_one("#pass_list", PassList)
        pass_list.action_copy_password()


@pytest.mark.asyncio
async def test_passlist_action_copy_username():
    app = AppHelper()
    async with app.run_test() as pilot:
        pass_list = app.query_one("#pass_list", PassList)
        pass_list.action_copy_username()
