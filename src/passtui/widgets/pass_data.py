from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import TextArea, Static
from passtui.models.pass_store import PassModel
from passtui.security import passcli
from passtui.screens.input_modal import InputModalScreen
from passtui.utils.clipboard import (
    copy_password_to_clipboard,
    copy_username_to_clipboard,
    copy_line_to_clipboard,
)

DEFAULT_MESSAGE = "GPG locked. 🔐"


class PassData(Static):
    text_area: TextArea

    _is_dirty = False
    _pass_model: PassModel | None = None
    _pass_path: str | None = None

    BORDER_TITLE = "E"

    # priority=True to override TextArea Bindings
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", priority=True),
        Binding("i", "insert", "Insert"),
        Binding("c", "copy_password", "Copy password"),
        Binding("b", "copy_username", "Copy username"),
        Binding("y", "copy_current_line", "Copy current line"),
        Binding("j", "cursor_down", "Cursor Down"),
        Binding("k", "cursor_up", "Cursor Up"),
        Binding("h", "cursor_left", "Cursor left"),
        Binding("l", "cursor_right", "Cursor right"),
        Binding("ctrl+s", "save", "Save"),
    ]

    DEFAULT_CSS = """
    PassData {
        border: solid $primary-muted;
    }
    PassData TextArea {
        width: 1fr;
        height: 1fr;
        background: $background;
    }
    """

    def compose(self) -> ComposeResult:
        self.text_area = TextArea.code_editor(
            DEFAULT_MESSAGE,
            language="markdown",
            read_only=True,
            show_line_numbers=False,
            theme="css",
            compact=True,
        )

        yield self.text_area

    def add_new_password(self) -> None:
        pass_model, template = PassModel.get_new_entry_template()
        success = self._set_text(template)
        if not success:
            return

        self._pass_model = pass_model
        self._pass_path = None
        self.action_insert()

    def set_password(self, pass_model: PassModel, pass_path: str) -> None:
        success = self._set_text(str(pass_model))
        if not success:
            return

        self._pass_model = pass_model
        self._pass_path = pass_path
        self._set_read_only_mode()

    def set_focus(self) -> None:
        self.text_area.focus()

    def action_cancel(self) -> None:
        self._set_read_only_mode()

    def action_insert(self) -> None:
        if not self._pass_model:
            self.notify("Emptiness is read-only. 😄", severity="error")
            return

        self._is_dirty = True
        self._set_edit_mode()

    def _set_text(self, text: str) -> bool:
        if self._is_dirty:
            self.notify("You have pending changes to save", severity="warning")
            return False

        self.text_area.text = text
        return True

    def _set_edit_mode(self) -> None:
        self.text_area.read_only = False
        self.text_area.show_line_numbers = True
        self._focus_workaround_for_textual_bindings()

    def _set_read_only_mode(self) -> None:
        self.text_area.read_only = True
        self.text_area.show_line_numbers = True
        self._focus_workaround_for_textual_bindings()

    def _focus_workaround_for_textual_bindings(self) -> None:
        # Textual shows Bindings only when parent widget is focused first
        self.focus()
        self.text_area.focus()

    def action_copy_password(self) -> None:
        sucess = copy_password_to_clipboard(self._pass_model)
        if not sucess:
            self.notify("Failed to copy password", severity="error")
            return

        self.notify("Password copied to clipboard")

    def action_copy_username(self) -> None:
        sucess = copy_username_to_clipboard(self._pass_model)
        if not sucess:
            self.notify("Failed to copy Username", severity="error")
            return

        self.notify("Username copied to clipboard")

    def action_copy_current_line(self) -> None:
        cursor_location = self.text_area.cursor_location
        line_number = cursor_location[0]
        line = self.text_area.get_line(line_number)
        success = copy_line_to_clipboard(line)

        if not success:
            self.notify("Failed to copy line", severity="error")
            return

        self.notify("Line copied to clipboard")

    def action_cursor_down(self) -> None:
        self.text_area.action_cursor_down()

    def action_cursor_up(self) -> None:
        self.text_area.action_cursor_up()

    def action_cursor_left(self) -> None:
        self.text_area.action_cursor_left()

    def action_cursor_right(self) -> None:
        self.text_area.action_cursor_right()

    def action_save(self) -> None:
        self._save()

    @work
    async def _save(self) -> None:
        if not self._pass_model or not self._is_dirty:
            self.notify("Nothing to save", severity="warning")
            return

        if not self._pass_path:
            self._pass_path = await self.app.push_screen_wait(
                InputModalScreen(
                    label="Enter the password path",
                    placeholder="(e.g., my-passwords/emails/gmail)",
                )
            )
            if not self._pass_path:
                self.notify("No valid path provided", severity="error")
                return

        try:
            pass_data = self.text_area.text
            self._pass_model = PassModel(pass_data)
            passcli.save_store_key(self._pass_path, self._pass_model)
            self.notify("Saved!")
            self._is_dirty = False
        except Exception as e:
            self.notify(f"Failed to save: {e}", severity="error")
