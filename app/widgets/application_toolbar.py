from PySide6.QtCore import Signal
from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QLineEdit, QPushButton, QWidget


class ApplicationToolbar(QWidget):
    """Toolbar widget containing search field and status filter toggle buttons."""

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
        self.filter_all_btn = QPushButton()
        self.filter_configured_btn = QPushButton()
        self.filter_unconfigured_btn = QPushButton()
        self.filter_group = QButtonGroup(self)

    def _configure_widgets(self) -> None:
        self.search_bar.setPlaceholderText("🔍 Search installed applications...")

        self.filter_all_btn.setText("All Apps")
        self.filter_all_btn.setObjectName("FilterButton")
        self.filter_all_btn.setCheckable(True)
        self.filter_all_btn.setChecked(True)

        self.filter_configured_btn.setText("With Gesture")
        self.filter_configured_btn.setObjectName("FilterButton")
        self.filter_configured_btn.setCheckable(True)

        self.filter_unconfigured_btn.setText("Without Gesture")
        self.filter_unconfigured_btn.setObjectName("FilterButton")
        self.filter_unconfigured_btn.setCheckable(True)

        self.filter_group.addButton(self.filter_all_btn)
        self.filter_group.addButton(self.filter_configured_btn)
        self.filter_group.addButton(self.filter_unconfigured_btn)
        self.filter_group.setExclusive(True)

    def _create_layouts(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        filter_box = QHBoxLayout()
        filter_box.setSpacing(6)
        filter_box.addWidget(self.filter_all_btn)
        filter_box.addWidget(self.filter_configured_btn)
        filter_box.addWidget(self.filter_unconfigured_btn)

        layout.addWidget(self.search_bar, 1)
        layout.addLayout(filter_box)

    def _create_connections(self) -> None:
        self.search_bar.textChanged.connect(self.searchChanged.emit)
        self.filter_all_btn.clicked.connect(lambda: self.filterChanged.emit("All"))
        self.filter_configured_btn.clicked.connect(lambda: self.filterChanged.emit("Gesture Created"))
        self.filter_unconfigured_btn.clicked.connect(lambda: self.filterChanged.emit("Gesture Not Created"))

    def _load_data(self) -> None:
        pass
