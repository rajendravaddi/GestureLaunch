# Gesture Launcher 🚀

**Gesture Launcher** is a modern desktop application for Ubuntu/Linux that allows users to launch applications using custom drawn gestures. Powered by PySide6 and the $1 Unistroke Gesture Recognition algorithm, Gesture Launcher captures mouse/touchpad gesture paths on a transparent system overlay.

---

## Key Features

- **Transparent Gesture Overlay**: Draw custom unistroke shapes directly anywhere on your screen.
- **GNOME Custom Shortcut Integration**: Zero continuous background CPU/memory footprint. Press `Ctrl + Shift + G` to bring up the drawing overlay instantly.
- **$1 Unistroke Recognition Algorithm**: Fast, accurate, scale- and rotation-invariant shape recognition.
- **Application Studio**: Browse installed desktop applications (`.desktop`), create custom gesture templates, and test recognition accuracy.
- **LibAdwaita Aesthetic UI**: Styled with clean Catppuccin-inspired dark themes, smooth micro-animations, and modern Qt widgets.

---

## Project Structure

```
GestureLaunch/
├── app/
│   ├── models/            # Data models (Application, Gesture, Settings)
│   ├── pages/             # GUI Page views (Settings, Applications, Gesture Studio, Help)
│   ├── repository/        # Persistent JSON storage for apps & gestures
│   ├── resources/         # QSS stylesheets & themes
│   ├── services/          # Business logic services (Application, Gesture)
│   ├── utils/             # Helpers ($1 Matcher, Desktop Parser, GNOME Shortcut Manager, Notifier)
│   ├── widgets/           # Reusable Qt widgets (Canvas, Cards, Overlay, Toggle Switch)
│   ├── main_window.py     # Main application window & navigation frame
│   └── navigation.py      # Stacked widget page navigation controller
├── daemon.py              # On-demand gesture overlay launcher
├── main.py                # Main GUI entry point
├── pyproject.toml         # Project dependencies and configuration
└── README.md
```

---

## Installation & Setup

### Prerequisites

- **OS**: Ubuntu / Linux with GNOME Desktop
- **Python**: Python 3.10+
- **Tooling**: [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

### Step-by-Step Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rajendravaddi/GestureLaunch.git
   cd GestureLaunch
   ```

2. **Sync Dependencies**:
   ```bash
   uv sync
   ```

3. **Run the Application**:
   ```bash
   uv run main.py
   ```

---

## How to Use

1. **Enable Keybinding**:
   - Open Gesture Launcher settings.
   - Toggle **Gesture Launch service** to **ON**.
   - This registers `Ctrl + Shift + G` in GNOME system settings.

2. **Record Application Gestures**:
   - Navigate to **Applications**.
   - Select an application (e.g., Firefox, Terminal, Files).
   - Click **Record Gesture** and draw a single unistroke shape.
   - Click **Save Gesture**.

3. **Launch Apps via Gesture**:
   - Press **`Ctrl + Shift + G`** anywhere on your desktop.
   - Draw your recorded gesture shape on the overlay.
   - The matched application will launch automatically!

---

## Tech Stack

- **GUI Framework**: PySide6 (Qt for Python)
- **Gesture Engine**: Custom $1 Unistroke Recognizer algorithm
- **System Integration**: GNOME `gsettings` custom media keybindings, Linux `notify-send` desktop notifications
- **Package Management**: `uv`
