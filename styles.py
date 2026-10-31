
"""Visual theme for the Make-It-All prototype.

Owner: Person 6 (Design / Data / QA).  Everyone else imports from here and
never hard-codes a colour or font size in their own file.

    from ui.styles import apply_theme, PALETTE, status_colour, set_role

    apply_theme(app)                                  # once, in main.py
    title = QLabel("Dashboard"); set_role(title, "title")
    card = QFrame(); card.setObjectName("Card")       # white rounded card
    colour = status_colour(task["status"])            # hex string for Gantt bars
"""

PALETTE = {
    "bg":          "#E5E7EB",   # window background
    "surface":     "#FFFFFF",   # cards, tables
    "sidebar":     "#FFD400",   # navigation panel
    "sidebar_hi":  "#E6BF00",   # hovered / selected nav button
    "primary":     "#FFD400",   # buttons, links, selection
    "primary_dk":  "#E6BF00",   # button hover
    "text":        "#111827",
    "text_muted":  "#667085",
    "border":      "#D1D5DB",
    "grid":        "#EDF0F6",   # Gantt grid lines
    "success":     "#2E9D6B",
    "warning":     "#E8A317",
    "danger":      "#D64545",
    "info":        "#2F6FED",
    "button":      "#858585",
    "button_hover": "#6B6B6B",
}

# One colour per task status. Gantt bars, chips and dashboard cards all use these.
STATUS_COLOURS = {
    "Completed":   PALETTE["success"],
    "In Progress": PALETTE["primary"],
    "Scheduled":   "#9AA5B8",
    "At Risk":     PALETTE["danger"],
}

FONT_FAMILY = '"Segoe UI", "Helvetica Neue", Arial, sans-serif'
FONT_SIZES = {"caption": 11, "body": 13, "subtitle": 15, "title": 22, "metric": 28}

# Standard sizes so every page lines up
SPACING = {"page": 24, "card": 16, "gap": 12}
RADIUS = 10
SIDEBAR_WIDTH = 220
WINDOW_SIZE = (1280, 800)        # design and screenshot at this size


def status_colour(status):
    """Hex colour for a task status (grey if the status is unknown)."""
    return STATUS_COLOURS.get(status, PALETTE["text_muted"])


def status_chip_qss(status):
    """Inline stylesheet for a small coloured status label."""
    c = status_colour(status)
    return (f"background:{c}; color:white; border-radius:9px; "
            f"padding:2px 10px; font-size:{FONT_SIZES['caption']}px; font-weight:600;")


def set_role(widget, role):
    """Give a widget a text style: title, subtitle, muted, metric, caption, warning."""
    widget.setProperty("role", role)
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def build_stylesheet():
    p, f, s = PALETTE, FONT_SIZES, SPACING
    return f"""
* {{ font-family: {FONT_FAMILY}; font-size: {f['body']}px; color: {p['text']}; }}
QMainWindow, QDialog, QStackedWidget, #Page {{ background: {p['bg']}; }}

/* ---------- text roles ---------- */
QLabel {{ background: transparent; }}
QLabel[role="title"]    {{ font-size: {f['title']}px; font-weight: 700; }}
QLabel[role="subtitle"] {{ font-size: {f['subtitle']}px; font-weight: 600; }}
QLabel[role="muted"]    {{ color: {p['text_muted']}; }}
QLabel[role="caption"]  {{ color: {p['text_muted']}; font-size: {f['caption']}px; }}
QLabel[role="metric"]   {{ font-size: {f['metric']}px; font-weight: 700; }}
QLabel[role="warning"]  {{ color: #8A5A00; background: #FFF4D6; border: 1px solid #F4D488;
                           border-radius: 8px; padding: 8px 12px; }}
QLabel[role="danger"]   {{ color: #8C1F1F; background: #FDE8E8; border: 1px solid #F3B8B8;
                           border-radius: 8px; padding: 8px 12px; }}

/* ---------- sidebar ---------- */
#Sidebar {{ background: {p['sidebar']}; min-width: {SIDEBAR_WIDTH}px; max-width: {SIDEBAR_WIDTH}px; }}
#Sidebar QLabel {{ color: #222222; }}
#Sidebar QLabel[role="muted"] {{ color: #AAB4CF; }}
#Sidebar QPushButton {{ background: transparent; color: Black; text-align: left;
                        padding: 10px 14px; border: none; border-radius: 8px; }}
#Sidebar QPushButton:hover {{ background: {p['sidebar_hi']}; color: white; }}
#Sidebar QPushButton:checked {{ background: {p['primary']}; color: white; font-weight: 600; }}
#Sidebar QComboBox {{ background: {p['sidebar_hi']}; color: #222222; border: none; }}

/* ---------- cards ---------- */
#Card {{ background: {p['surface']}; border: 1px solid {p['border']}; border-radius: {RADIUS}px; }}
#Card QLabel {{ background: transparent; }}

/* ---------- buttons ---------- */
QPushButton {{
    background: {p['button']};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: 600;
}}

QPushButton:hover {{
    background: {p['button_hover']};
}}

QPushButton:pressed {{
    background: {p['button_hover']};
}}

QPushButton:disabled {{
    background: {p['border']};
    color: {p['text_muted']};
}}
/* ---------- inputs ---------- */
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QDateEdit, QSpinBox {{
    background: {p['surface']}; border: 1px solid {p['border']}; border-radius: 8px;
    padding: 7px 10px; selection-background-color: {p['primary']}; selection-color: white; }}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {{ border: 1px solid {p['primary']}; }}
QComboBox::drop-down {{ border: none; width: 22px; }}
QComboBox {{
    background: {p['surface']};
    color: {p['text']};
    border: 1px solid {p['border']};
    border-radius: 8px;
    padding: 8px 12px;
}}

QComboBox QAbstractItemView {{
    background: {p['surface']};
    color: {p['text']};
    border: 1px solid {p['border']};
    selection-background-color: {p['primary']};
    selection-color: {p['text']};
    outline: none;
}}

/* ---------- lists and tables ---------- */
QTableWidget, QTableView, QListWidget, QTreeWidget {{
    background: {p['surface']}; border: 1px solid {p['border']}; border-radius: {RADIUS}px;
    gridline-color: {p['grid']}; alternate-background-color: #FAFBFD;
    selection-background-color: #DCE8FD; selection-color: {p['text']}; outline: none; }}
QHeaderView::section {{ background: {p['bg']}; color: {p['text_muted']}; font-weight: 600;
    border: none; border-bottom: 1px solid {p['border']}; padding: 8px 10px; }}
QListWidget::item {{ padding: 10px; border-bottom: 1px solid {p['grid']}; }}
QListWidget::item:selected {{ background: #DCE8FD; color: {p['text']}; }}

/* ---------- progress bars ---------- */
QProgressBar {{ background: {p['grid']}; border: none; border-radius: 5px; height: 10px;
                text-align: center; font-size: {f['caption']}px; }}
QProgressBar::chunk {{ background: {p['primary']}; border-radius: 5px; }}
QProgressBar[status="Completed"]::chunk {{ background: {STATUS_COLOURS['Completed']}; }}
QProgressBar[status="At Risk"]::chunk   {{ background: {STATUS_COLOURS['At Risk']}; }}

/* ---------- scrollbars, tooltips, tabs ---------- */
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: #C5CCDA; border-radius: 4px; min-height: 30px; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: #C5CCDA; border-radius: 4px; min-width: 30px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
QToolTip {{ background: {p['sidebar']}; color: white; border: none; padding: 6px 8px; }}
QTabWidget::pane {{ border: 1px solid {p['border']}; border-radius: 8px; background: {p['surface']}; }}
QTabBar::tab {{ padding: 8px 16px; background: transparent; color: {p['text_muted']}; }}
QTabBar::tab:selected {{ color: {p['primary']}; border-bottom: 2px solid {p['primary']}; font-weight: 600; }}
"""


def apply_theme(app):
    """Call once after creating QApplication."""
    from PySide6.QtGui import QFont
    app.setStyle("Fusion")                      # same look on Windows, macOS, Linux
    app.setFont(QFont("Segoe UI", FONT_SIZES["body"] - 3))
    app.setStyleSheet(build_stylesheet())


def make_card(parent=None):
    """A white rounded container. Put your layout inside it."""
    from PySide6.QtWidgets import QFrame
    card = QFrame(parent)
    card.setObjectName("Card")
    return card
