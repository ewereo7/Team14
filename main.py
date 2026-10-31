# Main application entry point
from dashboard import create_page as dashboard_page
from gantt import create_page as gantt_page
from tasks import create_page as tasks_page
from knowledge import create_page as knowledge_page
from team import create_page as team_page
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QComboBox
)
from PySide6.QtCore import Qt

#From the styles.py module
from styles import apply_theme, set_role, make_card
import sample_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Make-It-All Productivity & Knowledge System")
        self.resize(1280, 800)

        #Load shared sample data just in case
        self.data = sample_data.get_sample_data()

        #Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(16)

        #sidebar navigation
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(12, 16, 12, 16)

        #app logo image
        from PySide6.QtGui import QPixmap
        self.logo_label = QLabel()
        
        # Change "logo.png" to match your actual image file's name in your project folder
        pixmap = QPixmap("logo.png") 
        
        # Scale the image to fit the sidebar nicely
        scaled_pixmap = pixmap.scaled(160, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        
        self.sidebar_layout.addWidget(self.logo_label)

        # Choose roels (Employee, Team Leader, Manager)
        self.role_label = QLabel("Current Role / User:")
        set_role(self.role_label, "caption")
        self.sidebar_layout.addWidget(self.role_label)
        
        self.role_combo = QComboBox()
        #Gets the users from the data
        for role, name in self.data["role_users"].items():
            self.role_combo.addItem(f"{role} ({name})", role)
        #To get responsiveness from the system   
        self.role_combo.currentIndexChanged.connect(self.update_permissions)
        self.sidebar_layout.addWidget(self.role_combo)

        self.sidebar_layout.addSpacing(20)

        #Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", 0),
            ("To-Do Lists && Tasks", 1),
            ("Team Workload", 2),
            ("Gantt Chart", 3),
            ("Knowledge Management", 4)
        ]

        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setCheckable(True)
            #higlights the button pressed
            btn.setAutoExclusive(True)
            btn.clicked.connect(lambda checked, idx=index: self.switch_page(idx))
            self.sidebar_layout.addWidget(btn)
            self.nav_buttons[index] = btn

        self.sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

        #Makes sure one screen is avaliable at one time
        self.stack = QStackedWidget()
        self.stack.setObjectName("Page")
        
        #Dashboard Screen (Card Container Example)
        self.page_dashboard_card = make_card()
        dash_layout = QVBoxLayout(self.page_dashboard_card)
        dash_title = QLabel("Manager Dashboard")
        set_role(dash_title, "title")
        dash_layout.addWidget(dash_title)
        dash_layout.addWidget(QLabel("dashboard.py content goes here (uses self.data)"))
        dash_layout.addStretch()

        # 2. Tasks Screen Placeholder
        self.page_tasks = tasks_page()  # This will call the create_page function from tasks.py
        
        # 3. Team Workload Screen Placeholder (can leverage sample_data.workload(self.data))
        self.page_team = QLabel("Team Workload Management Screen (team.py)")
        
        # 4. Gantt Chart Placeholder
        self.page_gantt = gantt_page()  # This will call the create_page function from gantt.py
        
        # 5. Knowledge Management Placeholder
        self.page_knowledge = QLabel("Knowledge Management Topics & Posts (knowledge.py)")

        # Add screens to stack
        self.stack.addWidget(self.page_dashboard_card) # Index 0
        self.stack.addWidget(self.page_tasks)          # Index 1
        self.stack.addWidget(self.page_team)           # Index 2
        self.stack.addWidget(self.page_gantt)          # Index 3
        self.stack.addWidget(self.page_knowledge)      # Index 4

        self.main_layout.addWidget(self.stack, stretch=1)

        # Set default view and run initial permission check
        self.nav_buttons[0].setChecked(True)
        self.switch_page(0)
        self.update_permissions()

    def switch_page(self, index):
        #picks the correct screen
        self.stack.setCurrentIndex(index)

    def update_permissions(self):
        #Picks what can been seen depending on the role
        role_key = self.role_combo.currentData()
        
        # Enforce role restrictions based on stakeholder requirements
        if role_key == "Employee":
            # Hide Dashboard (Index 0) and Team Workload (Index 2) buttons completely
            self.nav_buttons[0].hide()  
            self.nav_buttons[2].hide()  
            
            if self.stack.currentIndex() in [0, 2]:
                self.nav_buttons[1].setChecked(True)
                self.switch_page(1)
        else:
            # Show Dashboard and Team Workload buttons for managers/team leaders
            self.nav_buttons[0].show()  
            self.nav_buttons[2].show()  

        print(f"Switched active user view to role: {role_key}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    #Gets the right style sheet
    apply_theme(app)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
