from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from app.models.application import Application
from app.widgets.application_card import ApplicationCard


class ApplicationGrid(QWidget):
    """Container widget displaying a responsive grid of ApplicationCards."""

    appClicked = Signal(str)  # Emits app_id

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._create_widgets()
        self._configure_widgets()
        self._create_layouts()
        self._create_connections()
        self._load_data()

    def _create_widgets(self) -> None:
        self.scroll_area = QScrollArea()
        self.container = QWidget()
        self.grid_layout = QGridLayout(self.container)
        self.empty_label = QLabel()

    def _configure_widgets(self) -> None:
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("AppScrollArea")

        self.container.setStyleSheet("background: transparent;")
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(12)

        self.empty_label.setText("No applications found matching your criteria.")
        self.empty_label.setObjectName("Subtitle")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.hide()

    def _create_layouts(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area.setWidget(self.container)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.empty_label)

    def _create_connections(self) -> None:
        pass

    def _load_data(self) -> None:
        pass

    def populate(self, apps: List[Application]) -> None:
        """Clears existing cards and populates with new application cards."""
        self.clear()

        if not apps:
            self.scroll_area.hide()
            self.empty_label.show()
            return

        self.empty_label.hide()
        self.scroll_area.show()

        columns = 2  # 2 column responsive grid
        for index, app in enumerate(apps):
            row = index // columns
            col = index % columns
            card = ApplicationCard(app)
            card.clicked.connect(self.appClicked.emit)
            self.grid_layout.addWidget(card, row, col)

    def clear(self) -> None:
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
