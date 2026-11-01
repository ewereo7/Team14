# Main application entry point
from dashboard import create_page as dashboard_page
from gantt import create_page as gantt_page
from tasks import create_page as tasks_page
from knowledge import create_page as knowledge_page


import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QDialog
)
from PySide6.QtCore import Qt

#From the styles.py module
from styles import apply_theme, set_role, make_card
import sample_data

# login screen
from auth_app import LoginWindow

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Make-It-All Productivity & Knowledge System")
        self.resize(1280, 800)

        #Gets the user from login
        self.user = user
        #Used when the window closes
        self.logged_out = False 

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
        
        #Our logo image to put in the sidebar
        pixmap = QPixmap("logo.png") 
        
        #Scale the image to fit the sidebar nicely
        scaled_pixmap = pixmap.scaled(160, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        
        self.sidebar_layout.addWidget(self.logo_label)

        # Current user (Employee, Team Leader, Manager)
        self.role_label = QLabel("Logged in as:")
        set_role(self.role_label, "caption")
        self.sidebar_layout.addWidget(self.role_label)

        name=self.user["name"]
        role = self.user["role"]
        self.user_label = QLabel(f"{name} ({role})")
        self.user_label.setWordWrap(True)
        self.sidebar_layout.addWidget(self.user_label)

        self.sidebar_layout.addSpacing(20)

        #Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", 0),
            ("To-Do Lists && Tasks", 1),
            ("Gantt Chart", 2),
            ("Knowledge Management", 3)
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

        #log out button
        self.logout_button = QPushButton("Log out")
        self.logout_button.clicked.connect(self.log_out)
        self.sidebar_layout.addWidget(self.logout_button)

        self.main_layout.addWidget(self.sidebar)

        #Makes sure one screen is avaliable at one time
        self.stack = QStackedWidget()
        self.stack.setObjectName("Page")
        
        # Dashboard Screen
        self.page_dashboard_card = dashboard_page()

        # link to Tasks Screen 
        self.page_tasks = tasks_page()  
        
        # link to Gantt Chart Screen
        self.page_gantt = gantt_page()  
        
        # link to Knowledge Management Screen
        self.page_knowledge = knowledge_page()

        # Add screens to stack
        self.stack.addWidget(self.page_dashboard_card) # Index 0
        self.stack.addWidget(self.page_tasks)          # Index 1
        self.stack.addWidget(self.page_gantt)          # Index 2
        self.stack.addWidget(self.page_knowledge)      # Index 3

        self.main_layout.addWidget(self.stack, stretch=1)

        #Sets default view and runs a permission check
        self.nav_buttons[0].setChecked(True)
        self.switch_page(0)
        self.update_permissions()

    def switch_page(self, index):
        #picks the correct screen
        self.stack.setCurrentIndex(index)

    def log_out(self):
        #Back to login after closing
        self.logged_out = True
        self.close()

    def update_permissions(self):
        #Picks what can been seen depending on the role
        role_key = self.user["role"]
        
        #Enforces role based restrictions 
        if role_key == "Employee":
            #Hides Dashboard button completely as employees should not have access to these features
            self.nav_buttons[0].hide()  
            
            if self.stack.currentIndex() in [0]:
                self.nav_buttons[1].setChecked(True)
                self.switch_page(1)
        else:
            #Show Dashboard and Team Workload buttons for managers/team leaders
            self.nav_buttons[0].show()  

        print(f"Switched active user view to role: {role_key}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    #Gets the right style sheet
    apply_theme(app)
    
    # Login Screen
    while True:
        login_window = LoginWindow()
        login_result=login_window.exec()
        if login_result != QDialog.Accepted: #User closed the login window
            break

        #Main window
        user = login_window.user
        window = MainWindow(user)
        window.show()
        app.exec()

        #Finishes unless they logged out
        if not window.logged_out:
            break

    sys.exit(0)
