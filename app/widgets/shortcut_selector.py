from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class ShortcutSelector(QWidget):
    """Reusable widget for capturing and selecting global key shortcuts."""

    shortcutChanged = Signal(str)

    def __init__(self, current_shortcut: str = "Super+Shift+G", parent: QWidget = None) -> None:
        super().__init__(parent)
        self._current_shortcut = current_shortcut
        self._recording = False

        self._create_widgets()
        self._configure_widgets()
        self._create_layouts()
        self._create_connections()
        self._load_data()

    def _create_widgets(self) -> None:
        self.display_label = QLabel()
        self.record_button = QPushButton()

    def _configure_widgets(self) -> None:
        self.display_label.setObjectName("SectionTitle")
        self.record_button.setText("Change Shortcut")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _create_layouts(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(self.display_label)
        layout.addWidget(self.record_button)

    def _create_connections(self) -> None:
        self.record_button.clicked.connect(self._toggle_recording)

    def _load_data(self) -> None:
        self.display_label.setText(self._current_shortcut)

    def set_shortcut(self, shortcut: str) -> None:
        self._current_shortcut = shortcut
        self.display_label.setText(shortcut)

    def get_shortcut(self) -> str:
        return self._current_shortcut

    def _toggle_recording(self) -> None:
        if not self._recording:
            self._recording = True
            self.record_button.setText("Press key combination...")
            self.record_button.setObjectName("PrimaryButton")
            self.record_button.setStyle(self.record_button.style())
            self.setFocus()
        else:
            self._stop_recording()

    def _stop_recording(self) -> None:
        self._recording = False
        self.record_button.setText("Change Shortcut")
        self.record_button.setObjectName("")
        self.record_button.setStyle(self.record_button.style())

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self._recording:
            super().keyPressEvent(event)
            return

        key = event.key()
        if key in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            return

        modifiers = []
        mod_flags = event.modifiers()
        if mod_flags & Qt.KeyboardModifier.MetaModifier or mod_flags & Qt.KeyboardModifier.GroupSwitchModifier:
            modifiers.append("Super")
        if mod_flags & Qt.KeyboardModifier.ControlModifier:
            modifiers.append("Ctrl")
        if mod_flags & Qt.KeyboardModifier.AltModifier:
            modifiers.append("Alt")
        if mod_flags & Qt.KeyboardModifier.ShiftModifier:
            modifiers.append("Shift")

        key_name = event.text().upper() if event.text() else str(key)
        if key == Qt.Key.Key_Space:
            key_name = "Space"

        shortcut_str = "+".join(modifiers + [key_name])
        self.set_shortcut(shortcut_str)
        self.shortcutChanged.emit(shortcut_str)
        self._stop_recording()
