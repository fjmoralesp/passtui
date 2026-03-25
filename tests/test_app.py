import pytest
from passtui.app import PassTUI
from textual.app import ComposeResult
from textual.widgets import Static


class MinimalPassTUI(PassTUI):
    def __init__(self):
        self.keys = []
        from textual.app import App

        App.__init__(self)
        self.CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Static("test")


@pytest.mark.asyncio
async def test_apptui_initialization():
    app = MinimalPassTUI()
    assert app.keys == []


@pytest.mark.asyncio
async def test_apptui_compose():
    app = MinimalPassTUI()
    async with app.run_test() as pilot:
        static = app.query_one(Static)
        assert static is not None


def test_apptui_bindings():
    app = MinimalPassTUI()
    binding_keys = [binding.key for binding in app.BINDINGS]
    expected_keys = ["/", "n", "e", "t", "s", "g", "x", "z"]
    assert binding_keys == expected_keys


def test_apptui_action_search_password():
    app = MinimalPassTUI()
    assert hasattr(app, "action_search_password")


def test_apptui_action_focus_editor():
    app = MinimalPassTUI()
    assert hasattr(app, "action_focus_editor")


def test_apptui_action_focus_explorer():
    app = MinimalPassTUI()
    assert hasattr(app, "action_focus_explorer")


def test_apptui_on_mount():
    app = MinimalPassTUI()
    app.on_mount()
    assert app.theme == "rose-pine-moon"
