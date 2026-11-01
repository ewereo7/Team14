# Login and registration screens
#Accounts stay in memory for the prototype, new ones are lost when the app closes
from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

#From the styles.py module
from styles import set_role
import sample_data

STAFF_DOMAIN="@make-it-all.co.uk"
MIN_PASSWORD_LENGTH = 12
COMMON_PASSWORDS = ["password1234", "password123!", "qwerty123456", "123456789012", "letmein12345"]

#demo password
DEMO_PASSWORD = "Make-It-All-2026"

# Temporary staff
AUTHORISED_TEMP_STAFF = [
    {"name": "Sam Carter", "email": "sam.carter@make-it-all.co.uk", "role": "Employee", "team": "Web"},
]

#Adds the temporary staff as well
STAFF_LIST = sample_data.EMPLOYEES + AUTHORISED_TEMP_STAFF

# Accounts already made
accounts = {
    "amira.hussain@make-it-all.co.uk": DEMO_PASSWORD,
    "noah.okafor@make-it-all.co.uk": DEMO_PASSWORD,
    "james.shah@make-it-all.co.uk": DEMO_PASSWORD,
}

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Make-It-All Login")
        self.setFixedSize(420, 560)

        self.user = None #main.py gets the user from here

        #main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(32, 24, 32, 24)

        #app logo image
        self.logo_label = QLabel()

        pixmap = QPixmap("logo.png")

        #Scale the image to fit the window
        scaled_pixmap = pixmap.scaled(240, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.logo_label)

        #Makes sure one form is shown at a time
        self.stack = QStackedWidget()

        # Login Screen
        self.login_page=QWidget()
        self.login_layout = QVBoxLayout(self.login_page)
        login_title = QLabel("Log in")
        set_role(login_title, "title")
        self.login_layout.addWidget(login_title)

        #Wrong login details
        self.login_error = QLabel("Invalid email or password.")
        set_role(self.login_error, "danger")
        self.login_error.hide()
        self.login_layout.addWidget(self.login_error)

        self.login_notice = QLabel("Account created. You can now log in.")
        set_role(self.login_notice, "warning")
        self.login_notice.hide()
        self.login_layout.addWidget(self.login_notice)

        # email input
        self.login_layout.addWidget(QLabel("Staff email"))
        self.login_email = QLineEdit()
        self.login_layout.addWidget(self.login_email)

        self.login_layout.addWidget(QLabel("Password"))
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password) #Hides the password
        #Enter also logs in
        self.login_password.returnPressed.connect(self.login_clicked)
        self.login_layout.addWidget(self.login_password)

        self.login_button = QPushButton("Log in")
        self.login_button.clicked.connect(self.login_clicked)
        self.login_layout.addWidget(self.login_button)

        # link to Register Screen
        self.open_register_button = QPushButton("Register a new account")
        self.open_register_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.login_layout.addWidget(self.open_register_button)

        self.login_layout.addStretch()


        # Register Screen
        self.register_page = QWidget()
        self.register_layout = QVBoxLayout(self.register_page)

        register_title = QLabel("Register")
        set_role(register_title, "title")
        self.register_layout.addWidget(register_title)

        self.register_error = QLabel() #error message goes here
        self.register_error.setWordWrap(True)
        set_role(self.register_error, "danger")
        self.register_error.hide()
        self.register_layout.addWidget(self.register_error)

        #New account details
        self.register_layout.addWidget(QLabel("Staff email"))
        self.register_email = QLineEdit()
        self.register_layout.addWidget(self.register_email)

        self.register_layout.addWidget(QLabel("Password"))
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_layout.addWidget(self.register_password)

        #confirm password
        self.register_layout.addWidget(QLabel("Confirm password"))
        self.register_confirm = QLineEdit()
        self.register_confirm.setEchoMode(QLineEdit.Password)
        self.register_layout.addWidget(self.register_confirm)

        #Password requirements
        hint = QLabel(f"At least {MIN_PASSWORD_LENGTH} characters, with an uppercase letter, "
                      "a lowercase letter, a number and a symbol.")
        hint.setWordWrap(True)
        set_role(hint, "caption")
        self.register_layout.addWidget(hint)

        self.register_button=QPushButton("Create account")
        self.register_button.clicked.connect(self.register_clicked)
        self.register_layout.addWidget(self.register_button)

        #back to login
        self.back_button = QPushButton("Back to log in")
        self.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.register_layout.addWidget(self.back_button)

        self.register_layout.addStretch()

        # Add screens to stack
        self.stack.addWidget(self.login_page) # Index 0
        self.stack.addWidget(self.register_page)    # Index 1
        self.main_layout.addWidget(self.stack)

    def login_clicked(self):
        email=self.login_email.text().strip().lower()
        password = self.login_password.text()

        #Checks the saved password first
        if email in accounts and accounts[email] == password:
            for person in STAFF_LIST:
                if person["email"] == email:
                    self.user = person #Name and role for the main window
                    self.accept()
                    return

        #try again
        self.login_notice.hide()
        self.login_error.show()
        self.login_password.clear()

    def register_clicked(self):
        email = self.register_email.text().strip().lower()
        password = self.register_password.text()
        confirm_password=self.register_confirm.text()

        #Checks that the email is a company one
        if not email.endswith(STAFF_DOMAIN):
            self.register_error.setText(f"You must use your staff email address ({STAFF_DOMAIN}).")
            self.register_error.show()
            return

        #Find the staff member
        staff_member = None
        for person in STAFF_LIST:
            if person["email"] == email:
                staff_member = person
                break

        if staff_member is None:
            self.register_error.setText("This email is not authorised. Please contact your manager.")
            self.register_error.show()
            return

        #already registered
        if email in accounts:
            self.register_error.setText("An account already exists for this email.")
            self.register_error.show()
            return

        #Password checks
        if len(password) < MIN_PASSWORD_LENGTH:
            self.register_error.setText(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.")
            self.register_error.show()
            return

        if password.lower() in COMMON_PASSWORDS:
            self.register_error.setText("That password is too common.")
            self.register_error.show()
            return

        has_upper = False
        has_lower = False
        has_number=False
        has_symbol = False
        for character in password:
            if character.isupper():
                has_upper = True
            elif character.islower():
                has_lower = True
            elif character.isdigit():
                has_number = True
            elif not character.isalnum() and not character.isspace():
                has_symbol = True

        if not (has_upper and has_lower and has_number and has_symbol):
            self.register_error.setText("Password needs an uppercase letter, a lowercase letter, a number and a symbol.")
            self.register_error.show()
            return

        #Check they match
        if password != confirm_password:
            self.register_error.setText("The passwords do not match.")
            self.register_error.show()
            return

        accounts[email] = password
        #Back to login
        self.login_email.setText(email)
        self.login_error.hide()
        self.login_notice.show()
        self.register_error.hide()

        #Clear the boxes for next time
        self.register_email.clear()
        self.register_password.clear()
        self.register_confirm.clear()
        self.stack.setCurrentIndex(0)
