from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit, QWidget


class ApplicationToolbar(QWidget):
    """Toolbar widget containing search field and status filter dropdown."""

    searchChanged = Signal(str)
    filterChanged = Signal(str)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._create_widgets()
        self._configure_widgets()
        self._create_layouts()
        self._create_connections()
        self._load_data()

    def _create_widgets(self) -> None:
        self.search_bar = QLineEdit()
        self.filter_combo = QComboBox()

    def _configure_widgets(self) -> None:
        self.search_bar.setPlaceholderText("🔍 Search installed applications...")

        self.filter_combo.addItem("All Apps", "All")
        self.filter_combo.addItem("With Gesture", "Gesture Created")
        self.filter_combo.addItem("Without Gesture", "Gesture Not Created")

    def _create_layouts(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        layout.addWidget(self.search_bar, 1)
        layout.addWidget(self.filter_combo)

    def _create_connections(self) -> None:
        self.search_bar.textChanged.connect(self.searchChanged.emit)
        self.filter_combo.currentIndexChanged.connect(self._on_combo_index_changed)

    def _on_combo_index_changed(self, index: int) -> None:
        filter_value = self.filter_combo.itemData(index)
        if filter_value:
            self.filterChanged.emit(filter_value)

    def _load_data(self) -> None:
        pass

