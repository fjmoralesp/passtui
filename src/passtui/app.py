from textual import work
from textual.app import App

from passtui.screens.auth import AuthScreen


class PassTUI(App):
    @work()
    async def on_mount(self) -> None:
        if await self.push_screen_wait(AuthScreen()):
            pass
