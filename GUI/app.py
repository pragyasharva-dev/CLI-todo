# --------------------- Imports ---------------------------

from storage.json_store import load_tasks, TASK_FILE
from src.task_service import (
    add_task,
    delete_task,
    toggle_priority_command,
    toggle_completion_command,
    update_task_priority,
    undo_task,
    flush_task_list,
    update_task_view
)
from version import CURRENT_VERSION

import sys
import os
import shutil
import requests

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QLineEdit, QPushButton, QLabel,
    QMessageBox, QInputDialog, QFileDialog, QFrame, QGroupBox,
    QGridLayout, QScrollArea, QSizePolicy, QAbstractItemView,
    QComboBox
)
from PyQt6.QtCore import Qt, QSize, QSettings, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap, QBrush, QIcon

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

GUI_DIR = resource_path('GUI')

# ---------------------- Stylesheets -------------------------------------

DARK_THEME = {
    "bg": "#1e1e2e",
    "surface": "#282840",
    "accent": "#7c83ff",
    "accent_hover": "#6a70e0",
    "text": "#e0e0e6",
    "text_dim": "#8888a0",
    "border": "#3a3a52",
    "danger": "#e05565",
    "danger_hover": "#c74555",
    "success": "#50c878",
    "success_hover": "#40b068",
    "list_bg": "#22223a",
    "list_select": "#3b3b5c",
    "completed_text": "#666680",
}

LIGHT_THEME = {
    "bg": "#f4f5f7",
    "surface": "#ffffff",
    "accent": "#5c63e0",
    "accent_hover": "#4a50d0",
    "text": "#1a1a24",
    "text_dim": "#8888a0",
    "border": "#d0d0df",
    "danger": "#d04555",
    "danger_hover": "#b73545",
    "success": "#40b068",
    "success_hover": "#30a058",
    "list_bg": "#ffffff",
    "list_select": "#e0e0f0",
    "completed_text": "#aaaabc",
}

HACKER_THEME = {
    "bg": "#0d0d0d",
    "surface": "#141414",
    "accent": "#00ff00",
    "accent_hover": "#00cc00",
    "text": "#00ff00",
    "text_dim": "#005500",
    "border": "#003300",
    "danger": "#ff0000",
    "danger_hover": "#cc0000",
    "success": "#00ff00",
    "success_hover": "#00cc00",
    "list_bg": "#0a0a0a",
    "list_select": "#003300",
    "completed_text": "#004400",
}

OCEAN_THEME = {
    "bg": "#0f172a",
    "surface": "#1e293b",
    "accent": "#38bdf8",
    "accent_hover": "#0ea5e9",
    "text": "#f8fafc",
    "text_dim": "#64748b",
    "border": "#334155",
    "danger": "#f43f5e",
    "danger_hover": "#e11d48",
    "success": "#10b981",
    "success_hover": "#059669",
    "list_bg": "#1e293b",
    "list_select": "#334155",
    "completed_text": "#475569",
}

SUNSET_THEME = {
    "bg": "#2d1b2e",
    "surface": "#3d263e",
    "accent": "#ff7b54",
    "accent_hover": "#f05a28",
    "text": "#ffeadd",
    "text_dim": "#a27b87",
    "border": "#5c3a5e",
    "danger": "#e63946",
    "danger_hover": "#d90429",
    "success": "#2a9d8f",
    "success_hover": "#21867a",
    "list_bg": "#362237",
    "list_select": "#5c3a5e",
    "completed_text": "#755462",
}

NATURE_THEME = {
    "bg": "#121212",
    "surface": "rgba(30, 30, 30, 0.7)",
    "accent": "#4caf50",
    "accent_hover": "#45a049",
    "text": "#ffffff",
    "text_dim": "#aaaaaa",
    "border": "rgba(255, 255, 255, 0.1)",
    "danger": "#e53935",
    "danger_hover": "#d32f2f",
    "success": "#4caf50",
    "success_hover": "#45a049",
    "list_bg": "rgba(20, 20, 20, 0.6)",
    "list_select": "rgba(255, 255, 255, 0.1)",
    "completed_text": "#777777",
    "bg_image": os.path.join(GUI_DIR, "assets", "theme1.jpg")
}

CUTE_THEME = {
    "bg": "#fef6fb",
    "surface": "rgba(255, 255, 255, 0.85)",
    "accent": "#ff9ece",
    "accent_hover": "#ff7bb7",
    "text": "#6b5b63",
    "text_dim": "#a38d97",
    "border": "rgba(255, 182, 217, 0.3)",
    "danger": "#ff8c94",
    "danger_hover": "#ffaaaf",
    "success": "#a8e6cf",
    "success_hover": "#94d2ba",
    "list_bg": "rgba(255, 245, 250, 0.7)",
    "list_select": "rgba(255, 214, 234, 0.4)",
    "completed_text": "#c5b8be",
    "bg_image": os.path.join(GUI_DIR, "assets", "cute_theme.jpg")
}
THEMES = {
    "Dark": DARK_THEME,
    "Light": LIGHT_THEME,
    "Hacker": HACKER_THEME,
    "Ocean": OCEAN_THEME,
    "Sunset": SUNSET_THEME,
    "Nature": NATURE_THEME,
    "Cute" : CUTE_THEME
}


def build_stylesheet(t):
    """Generates the full QSS stylesheet from a theme dict."""
    
    # If a background image is used, the main window and central widget
    # must be completely transparent so the paintEvent can draw beneath everything.
    base_bg = "transparent" if t.get('bg_image') else t['bg']
    
    return f"""
        QMainWindow, QWidget#central {{
            background-color: {base_bg};
        }}
        QScrollArea {{
            background-color: transparent;
            border: none;
        }}
        QScrollArea > QWidget > QWidget {{
            background-color: transparent;
        }}
        QWidget#scrollContent {{
            background-color: transparent;
        }}

        /* Header */
        QLabel#title {{
            color: {t['text']};
            font-size: 18pt;
            font-weight: bold;
            font-family: 'Segoe UI';
        }}
        QLabel#stats {{
            color: {t['text_dim']};
            font-size: 9pt;
            font-family: 'Segoe UI';
        }}

        /* Icon buttons (theme, bg) */
        QPushButton#iconBtn {{
            background-color: transparent;
            border: none;
            color: {t['text']};
            font-size: 12pt;
            padding: 4px;
            border-radius: 6px;
        }}
        QPushButton#iconBtn:hover {{
            background-color: {t['border']};
        }}

        /* Divider */
        QFrame#divider {{
            background-color: {t['border']};
            max-height: 1px;
            min-height: 1px;
        }}

        /* Task list */
        QListWidget {{
            background-color: {t['list_bg']};
            border: 1px solid {t['border']};
            border-radius: 6px;
            color: {t['text']};
            font-family: 'Consolas';
            font-size: 10pt;
            padding: 4px;
            outline: none;
        }}
        QListWidget::item {{
            padding: 6px 8px;
            border-radius: 4px;
        }}
        QListWidget::item:selected {{
            background-color: {t['list_select']};
            color: {t['text']};
        }}
        QListWidget::item:hover {{
            background-color: {t['list_select']};
        }}

        /* Input row */
        QFrame#inputFrame {{
            background-color: {t['surface']};
            border: 1px solid {t['border']};
            border-radius: 8px;
        }}
        QLineEdit#taskInput {{
            background-color: transparent;
            border: none;
            color: {t['text']};
            font-size: 10pt;
            font-family: 'Segoe UI';
            padding: 8px;
        }}
        QPushButton#addBtn {{
            background-color: {t['accent']};
            color: #ffffff;
            border: none;
            border-radius: 6px;
            font-size: 14pt;
            font-weight: bold;
            font-family: 'Segoe UI';
            min-width: 34px;
            max-width: 34px;
            min-height: 34px;
            max-height: 34px;
        }}
        QPushButton#addBtn:hover {{
            background-color: {t['accent_hover']};
        }}

        /* Section headers */
        QLabel#sectionLabel {{
            color: {t['text_dim']};
            font-size: 8pt;
            font-weight: bold;
            font-family: 'Segoe UI';
            padding-top: 4px;
        }}

        /* Action buttons — accent */
        QPushButton#accentBtn {{
            background-color: {t['accent']};
            color: #ffffff;
            border: none;
            border-radius: 8px;
            font-size: 10pt;
            font-family: 'Segoe UI';
            padding: 8px 0px;
        }}
        QPushButton#accentBtn:hover {{
            background-color: {t['accent_hover']};
        }}

        /* Action buttons — success */
        QPushButton#successBtn {{
            background-color: {t['success']};
            color: #ffffff;
            border: none;
            border-radius: 8px;
            font-size: 10pt;
            font-family: 'Segoe UI';
            padding: 8px 0px;
        }}
        QPushButton#successBtn:hover {{
            background-color: {t['success_hover']};
        }}

        /* Action buttons — danger */
        QPushButton#dangerBtn {{
            background-color: {t['danger']};
            color: #ffffff;
            border: none;
            border-radius: 8px;
            font-size: 10pt;
            font-family: 'Segoe UI';
            padding: 8px 0px;
        }}
        QPushButton#dangerBtn:hover {{
            background-color: {t['danger_hover']};
        }}

        /* Footer */
        QLabel#footer {{
            color: {t['text_dim']};
            font-size: 8pt;
            font-family: 'Segoe UI';
        }}

        /* Scrollbar */
        QScrollBar:vertical {{
            background: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {t['border']};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {t['accent']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: transparent;
        }}
        /* Combobox (Theme Selector) */
        QComboBox {{
            background-color: transparent;
            color: {t['text']};
            border: 1px solid {t['border']};
            border-radius: 6px;
            padding: 4px 10px;
            font-family: 'Segoe UI';
            font-size: 9pt;
            font-weight: bold;
        }}
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {t['surface']};
            color: {t['text']};
            selection-background-color: {t['list_select']};
            border: 1px solid {t['border']};
            border-radius: 4px;
        }}
    """

# ===================== Drag-and-Drop List =================================

class DragDropListWidget(QListWidget):
    """QListWidget with internal drag-and-drop that emits reorder signals."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self._drag_source_row = -1

    def startDrag(self, supportedActions):
        self._drag_source_row = self.currentRow()
        super().startDrag(supportedActions)

    def dropEvent(self, event):
        old_row = self._drag_source_row
        super().dropEvent(event)
        new_row = self.currentRow()

        if old_row >= 0 and new_row >= 0 and old_row != new_row:
            window = self.window()
            if hasattr(window, '_on_task_reordered'):
                window._on_task_reordered(old_row, new_row)

    def mousePressEvent(self, event):
        """Intercept clicks to see if they clicked the star (far left) or checkbox."""
        x_pos = event.pos().x()
        
        # The star is roughly in the first 30 pixels
        if x_pos < 30:
            item = self.itemAt(event.pos())
            if item is not None:
                row = self.row(item)
                window = self.window()
                if hasattr(window, '_on_star_clicked'):
                    window._on_star_clicked(row)
                    return  # Eat the event so it doesn't select/drag the row
                    
        # The checkbox is roughly between 30 and 60 pixels
        elif 30 <= x_pos < 60:
            item = self.itemAt(event.pos())
            if item is not None:
                row = self.row(item)
                window = self.window()
                if hasattr(window, '_on_checkbox_clicked'):
                    window._on_checkbox_clicked(row)
                    return  # Eat the event so it doesn't select/drag the row
                    
        super().mousePressEvent(event)


# ===================== Background Widget ==================================

class BackgroundWidget(QWidget):
    """A central widget that handles painting the background image."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._bg_pixmap = None

    def set_background(self, pixmap):
        self._bg_pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._bg_pixmap:
            from PyQt6.QtGui import QPainter
            painter = QPainter(self)
            scaled = self._bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
            painter.end()


# ===================== Update Checker =====================================

class UpdateCheckerThread(QThread):
    update_available = pyqtSignal(str)

    def run(self):
        try:
            from version import check_for_updates
            has_update, latest_ver = check_for_updates()
            if has_update:
                self.update_available.emit(latest_ver)
        except Exception as e:
            print(f"Update checker thread failed: {e}")


# ===================== Main Window ========================================

class TodoApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo")
        self.setWindowIcon(QIcon(os.path.join(GUI_DIR, "assets", "icon.ico")))
        self.setFixedSize(440, 680)
        # Specifically disable the maximize button while keeping all other standard window behaviors (like movement and snapping)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)

        self.settings = QSettings("CLI-todo", "GUI")
        saved_theme = self.settings.value("theme", "Dark")
        self.current_theme_name = saved_theme if saved_theme in THEMES else "Dark"

        # Central widget
        central = BackgroundWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        # Outer layout — holds the scroll area
        outer_layout = QVBoxLayout(central)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        outer_layout.addWidget(self.scroll_area)

        # Scroll content
        scroll_content = QWidget()
        scroll_content.setObjectName("scrollContent")
        self.scroll_area.setWidget(scroll_content)

        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(24, 24, 24, 16)
        layout.setSpacing(0)

        # --- Header ---
        header = QHBoxLayout()
        header.setSpacing(8)

        self.title_label = QLabel("Todo")
        self.title_label.setObjectName("title")
        header.addWidget(self.title_label)

        header.addStretch()
        
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(list(THEMES.keys()))
        self.theme_selector.setCurrentText(self.current_theme_name)
        self.theme_selector.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        header.addWidget(self.theme_selector)

        self.undo_btn = QPushButton("↩️")
        self.undo_btn.setObjectName("iconBtn")
        self.undo_btn.setFixedSize(32, 32)
        self.undo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.undo_btn.clicked.connect(self.undo_task_gui)
        header.addWidget(self.undo_btn)

        self.stats_label = QLabel("0 Total")
        self.stats_label.setObjectName("stats")
        header.addWidget(self.stats_label)

        layout.addLayout(header)
        layout.addSpacing(16)

        # --- Task list ---
        self.task_list = DragDropListWidget()
        self.task_list.setMinimumHeight(200)
        self.task_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.task_list, stretch=1)
        layout.addSpacing(16)

        # --- Input row ---
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_frame.setFixedHeight(44)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(4, 4, 4, 4)
        input_layout.setSpacing(4)

        self.task_input = QLineEdit()
        self.task_input.setObjectName("taskInput")
        self.task_input.setPlaceholderText("What needs to be done?")
        self.task_input.returnPressed.connect(self.add_task_gui)
        input_layout.addWidget(self.task_input)

        self.add_btn = QPushButton("+")
        self.add_btn.setObjectName("addBtn")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_task_gui)
        input_layout.addWidget(self.add_btn)

        layout.addWidget(input_frame)
        layout.addSpacing(20)

        # --- Button groups ---
        # Group 1: Task Actions (Now handled by clicks/drag-and-drop)
        # layout.addWidget(self._section_label("TASK ACTIONS"))
        # layout.addSpacing(4)
        # row1 = QHBoxLayout()
        # row1.setSpacing(6)
        # row1.addWidget(self._action_btn("↕ Move", "accentBtn", self.update_priority_gui))
        # layout.addLayout(row1)
        # layout.addSpacing(16)

        # Group 3: Danger Zone
        layout.addWidget(self._section_label("DANGER ZONE"))
        layout.addSpacing(4)
        row3 = QHBoxLayout()
        row3.setSpacing(6)
        row3.addWidget(self._action_btn("✕ Delete", "dangerBtn", self.delete_task_gui))
        row3.addWidget(self._action_btn("⟳ Clear All", "dangerBtn", self.flush_task_gui))
        layout.addLayout(row3)
        layout.addSpacing(12)

        # --- Footer ---
        footer = QLabel(f"ToDoApp  •  v{CURRENT_VERSION}")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

        # --- Apply theme & load data ---
        self.apply_theme()
        self.load_bg_image()
        self.refresh_tasks()

        # Check for updates in background
        self._update_thread = UpdateCheckerThread()
        self._update_thread.update_available.connect(self.prompt_update)
        self._update_thread.start()

    # -----------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------

    @staticmethod
    def strike(text):
        """Returns text with unicode strikethrough."""
        return "".join(c + "\u0336" for c in text)

    def _section_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("sectionLabel")
        return lbl

    def _action_btn(self, text, style_id, slot):
        btn = QPushButton(text)
        btn.setObjectName(style_id)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn.clicked.connect(slot)
        return btn

    # -----------------------------------------------------------------
    # Theme
    # -----------------------------------------------------------------

    def apply_theme(self):
        theme = THEMES[self.current_theme_name]
        self.setStyleSheet(build_stylesheet(theme))
        self._current_theme = theme

    def change_theme(self, theme_name):
        self.current_theme_name = theme_name
        self.settings.setValue("theme", theme_name)
        self.apply_theme()
        self.load_bg_image()
        self.refresh_tasks()

    # -----------------------------------------------------------------
    # Background image
    # -----------------------------------------------------------------

    def load_bg_image(self):
        bg_img = self._current_theme.get("bg_image")
        pixmap = None
        if bg_img and os.path.exists(bg_img):
            pixmap = QPixmap(bg_img)
        
        # Pass it to the central widget to paint
        if isinstance(self.centralWidget(), BackgroundWidget):
            self.centralWidget().set_background(pixmap)

    # -----------------------------------------------------------------
    # Task operations
    # -----------------------------------------------------------------

    def refresh_tasks(self):
        self.task_list.clear()
        update_task_view()       
        tasks = load_tasks(TASK_FILE)
        t = self._current_theme

        completed_count = 0
        priority_count = 0

        for task in tasks:
            if task.completed:
                status = "✓"
                completed_count += 1
                name = self.strike(task.name)
            else:
                status = "☐"
                name = task.name

            star = "★" if task.priority else "☆"
            if task.priority:
                priority_count += 1

            item = QListWidgetItem(f" {star}   {status}   {name}")

            if task.completed:
                item.setForeground(QColor(t["completed_text"]))
            else:
                item.setForeground(QColor(t["text"]))

            self.task_list.addItem(item)

        self.stats_label.setText(
            f"{len(tasks)} Total  •  {completed_count} Done  •  {priority_count} Priority"
        )

    def _on_task_reordered(self, old_row, new_row):
        """Called by DragDropListWidget after a successful drag-and-drop."""
        # update_task_priority uses 1-based indices
        update_task_priority(old_row + 1, new_row + 1)
        self.refresh_tasks()

    def get_selected_index(self):
        row = self.task_list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Select a task first.")
            return None
        return row

    def add_task_gui(self):
        text = self.task_input.text().strip()
        if not text:
            return
        add_task(text)
        self.task_input.clear()
        self.refresh_tasks()

    def delete_task_gui(self):
        index = self.get_selected_index()
        if index is None:
            return
            
        reply = QMessageBox.question(
            self, "Delete Task",
            "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
            
        delete_task(index)
        self.refresh_tasks()

    def update_priority_gui(self):
        index = self.get_selected_index()
        if index is None:
            return
        desired, ok = QInputDialog.getInt(self, "Move Task", "Enter new position:", min=1)
        if not ok:
            return
        update_task_priority(index + 1, desired)
        self.refresh_tasks()

    def undo_task_gui(self):
        undo_task()
        self.refresh_tasks()

    def flush_task_gui(self):
        reply = QMessageBox.question(
            self, "Clear All Tasks",
            "This will remove every task.\nAre you sure?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        flush_task_list()
        self.refresh_tasks()

    def _on_checkbox_clicked(self, row):
        """Called by DragDropListWidget when the checkbox is clicked."""
        toggle_completion_command(row)
        self.refresh_tasks()



    def _on_star_clicked(self, row):
        """Called by DragDropListWidget when the priority star is clicked."""
        task = load_tasks(TASK_FILE)[row]
        if task.completed:
            return  # Do not allow toggling priority on completed tasks
            
        toggle_priority_command(row)
        self.refresh_tasks()

    def prompt_update(self, latest_ver):
        reply = QMessageBox.question(
            self, "Update Available",
            f"A new version ({latest_ver}) is available.\nWould you like to download and install it now?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            import subprocess
            import sys

            if hasattr(sys, '_MEIPASS'):
                # Running as a frozen .exe — use batch script approach
                try:
                    self._do_exe_update()
                except Exception as e:
                    QMessageBox.warning(self, "Update Failed", f"Could not start update:\n{e}")
                    return
            else:
                # Running from source — use updater.py directly
                updater_path = os.path.join(os.path.dirname(GUI_DIR), "updater", "updater.py")
                if os.path.exists(updater_path):
                    subprocess.Popen([sys.executable, updater_path])
                else:
                    QMessageBox.warning(self, "Error", "Updater script not found.")
                    return

            QApplication.quit()

    def _do_exe_update(self):
        """Download the new exe and launch a batch script to swap files.

        This avoids the Windows file-lock problem: the batch script runs
        outside of any Python process, so the .exe is not held open during
        the rename.
        """
        import subprocess
        import sys
        from version import latest

        current_exe = os.path.abspath(sys.executable)
        exe_dir = os.path.dirname(current_exe)
        exe_name = os.path.basename(current_exe)
        new_exe = os.path.join(exe_dir, "TodoApp_new.exe")
        old_exe = os.path.join(exe_dir, "TodoApp_old.exe")
        bat_path = os.path.join(exe_dir, "_update.bat")

        # 1. Fetch the download URL from GitHub releases
        response = requests.get(latest, timeout=15)
        release = response.json()
        assets = release.get("assets")
        if not assets:
            raise Exception("No release assets found on GitHub.")
        download_url = assets[0]["browser_download_url"]

        # 2. Download the new executable
        r = requests.get(download_url, stream=True, timeout=60)
        if r.status_code != 200:
            raise Exception(f"Download failed with status {r.status_code}")
        with open(new_exe, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        # 3. Write a batch script that waits, swaps, and relaunches
        #    - Uses 'tasklist' polling to wait for our PID to disappear
        #    - Retries the rename in a loop in case the OS is slow to release
        bat_content = f"""@echo off
setlocal EnableDelayedExpansion
set "LOG={os.path.join(exe_dir, '_update_log.txt')}"

echo [%DATE% %TIME%] Update script started > "%LOG%"

REM Wait for the app to exit (5 seconds)
echo [%DATE% %TIME%] Waiting 5s for app to exit... >> "%LOG%"
ping -n 6 127.0.0.1 >NUL

REM Retry moving old exe out of the way, up to 30 attempts (~60s)
set RETRIES=0
:RENAME
set /a RETRIES+=1
echo [%DATE% %TIME%] Move attempt !RETRIES! >> "%LOG%"

if exist "{old_exe}" (
    del /f "{old_exe}" >NUL 2>&1
)

move /Y "{current_exe}" "{old_exe}" >NUL 2>&1
if errorlevel 1 (
    if !RETRIES! GEQ 30 (
        echo [%DATE% %TIME%] FAILED after 30 attempts >> "%LOG%"
        goto DONE
    )
    ping -n 3 127.0.0.1 >NUL
    goto RENAME
)

echo [%DATE% %TIME%] Old exe moved OK >> "%LOG%"

move /Y "{new_exe}" "{current_exe}" >NUL 2>&1
if errorlevel 1 (
    echo [%DATE% %TIME%] FAILED: could not move new exe >> "%LOG%"
    move /Y "{old_exe}" "{current_exe}" >NUL 2>&1
    goto DONE
)

echo [%DATE% %TIME%] Update complete. Launching... >> "%LOG%"
start "" "{current_exe}"

:DONE
echo [%DATE% %TIME%] Script finished. >> "%LOG%"
"""
        with open(bat_path, "w") as f:
            f.write(bat_content)

        # 4. Launch the batch script hidden and detached
        subprocess.Popen(
            bat_path,
            shell=True,
            creationflags=0x08000000,  # CREATE_NO_WINDOW
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


# -------------------------------- Entry point ----------------------------------


def main():
    import sys
    import os

    # Clean up leftover update files when the app starts normally
    if hasattr(sys, '_MEIPASS'):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        for leftover in ["TodoApp_old.exe", "TodoApp_new.exe", "_update.bat", "_update_log.txt"]:
            try:
                path = os.path.join(exe_dir, leftover)
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass

    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()