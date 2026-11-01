import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QStackedWidget

from PySide6.QtGui import QPixmap
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChart
from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QLineSeries
from PySide6.QtCharts import QValueAxis

from PySide6.QtGui import QColor
from PySide6.QtGui import QPen

from PySide6.QtWidgets import QTreeWidget
from PySide6.QtWidgets import QTreeWidgetItem

# Example data for the static prototype
activeTasks = 18
completedTasks = 12
atRiskTasks = 8
overdueTasks = 4

# Total number of tasks
totalTasks = activeTasks + completedTasks

# Cumulative completed tasks at the end of each week
weeklyCompleted = [2, 4, 7, 10, 12, 15]

# https://github.com/JiyaMehta-6/Pyside6/blob/main/Template%20-%20Dashboard/template_Dashboard.py?
# Using This Github as a reference i created manager dashboard cards to show active tasks, completed tasks, at risk tasks and overdue tasks. I also created a static line chart to show the completion of tasks over a 6 week period. The data is not dynamic and does not reflect real-time updates. The manager will be able to flick through numerous line charts of projects.
def createCard(mainHeading, number, colour):
    projectCard = QFrame()
    projectCard.setObjectName("statCard")
    projectCard.setStyleSheet("""QFrame#statCard {background-color: white;border: 1px solid #dddddd;border-radius: 7px;} """)
    cardLayout = QVBoxLayout(projectCard)
    cardLayout.setContentsMargins(18, 14, 18, 14)
    label = QLabel(mainHeading)
    label.setStyleSheet("font-size: 14px; color: #555555;")
    value = QLabel(str(number))
    value.setStyleSheet("font-size: 32px; font-weight: bold; color: black;")
    cardLayout.addWidget(label)
    cardLayout.addWidget(value)

    return projectCard


def create_page():

    # Main window
    managerWindow = QWidget()
    managerWindow.setWindowTitle("Make-It-All")
    managerWindow.resize(1150, 750)

    #https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QVBoxLayout.html
    #helps with layout of the page
    mainLayout = QVBoxLayout(managerWindow)
    mainLayout.setContentsMargins(0, 0, 0, 0)   #make sure the layout is taking up the whole window and not leaving any space around the edges
    mainLayout.setSpacing(0)


    #Used to make the navigation bar colours were chosen to match comapny logo
    #https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html#PySide6.QtWidgets.QWidget.setLayout

    navbarWidget = QWidget()  #creates a widget to hold the navigation bar
    navbarWidget.setStyleSheet("background-color: #FFD700;")  # yellow colour to match company logo
    navbar = QHBoxLayout()   #creates a horizontal layout for the navigation bar
    navbar.setContentsMargins(18, 8, 18, 8)   #18 pixels before logo and last button and 8 pixels above and below the logo and buttons
    navbar.setSpacing(10)  #allows spacing between things in the navigation bar

    navbarWidget.setLayout(navbar) #assigns horizontal layout to navigtion bar widget
    # Making sure company logo is on the top left
    # https://www.pythonguis.com/faq/adding-images-to-pyside6-applications/?

    companyLogo = QLabel()

    pixmap = QPixmap("logo.png")  # i need to change "makeItAll.png" later to match the image file's name in the github
    pixmap = pixmap.scaledToHeight(55, Qt.TransformationMode.SmoothTransformation)
    companyLogo.setPixmap(pixmap)
    navbar.addWidget(companyLogo)
    navbar.addStretch()



    # buttons for my navigation bar

    overviewButton = QPushButton("Overview")
    employeesButton = QPushButton("View Employee's Workloads")
    projectsButton = QPushButton("View All Projects")
    tasksButton = QPushButton("Assign Tasks")

    #https://doc.qt.io/qt-6/stylesheet-examples.html?utm_source=chatgpt.com#customizing-a-qpushbutton-using-the-box-model

    buttonStyle = """
        QPushButton {
            background-color: #808080;
            color: white;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: #666666;
            font: bold 14px;
            min-width: 6em;
            padding: 6px;
        }

        QPushButton:pressed {
            background-color: #505050;
            border-style: inset;
        }
    """

    #https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html#PySide6.QtWidgets.QWidget.setLayout
    #https://doc.qt.io/qtforpython-6/overviews/qtwidgets-stylesheet-syntax.html?

    # Apply styling to the navigation buttons
    overviewButton.setStyleSheet(buttonStyle)
    employeesButton.setStyleSheet(buttonStyle)
    projectsButton.setStyleSheet(buttonStyle)
    tasksButton.setStyleSheet(buttonStyle)

    # Add navigation buttons to the horizontal layout
    navbar.addWidget(overviewButton)
    navbar.addWidget(employeesButton)
    navbar.addWidget(projectsButton)
    navbar.addWidget(tasksButton)

    # Add the navbar container to the main window layout
    mainLayout.addWidget(navbarWidget)


    # CONTAINER FOR ALL PAGES

    pages = QStackedWidget()


    # OVERVIEW PAGE
    # OVERVIEW PAGE

    overviewPage = QWidget()
    overviewPage.setObjectName("overviewPage")

    overviewPage.setStyleSheet("""
        QWidget#overviewPage {
            background-color: #E5E7EB;
        }
    """)

    #Overview page layout - references used to help with layout
    # https://www.pythonguis.com/tutorials/pyside6-layouts/?#qvboxlayout-vertically-arranged-widgets
    # https://www.pythonguis.com/tutorials/pyside6-layouts/?#nesting-layouts-in-pyside6



    # OVERVIEW PAGE

    overviewLayout = QVBoxLayout()
    overviewLayout.setContentsMargins(25, 25, 25, 25)
    overviewLayout.setSpacing(20)

    overviewPage.setLayout(overviewLayout)

    title = QLabel("You have successfully logged in to the Manager Dashboard")
    title.setStyleSheet("font-size: 28px; font-weight: bold; color: black;")

    subtitle = QLabel("This will provide an overview of Make-It-All project completion.")
    subtitle.setStyleSheet("font-size: 15px; color: #666666;")

    overviewLayout.addWidget(title)
    overviewLayout.addWidget(subtitle)



    # My manager dashboard cards that use earlier function createCard to show active tasks, completed tasks, at risk tasks and overdue tasks. The cards are static and do not reflect real-time updates. The manager will be able to flick through numerous line charts of projects.

    cardsLayout = QHBoxLayout()
    cardsLayout.setSpacing(15)

    cardsLayout.addWidget(createCard("Current Projects", 18 , "#2563eb"))
    cardsLayout.addWidget(createCard("Completed Projects", 12 , "#16a34a"))
    cardsLayout.addWidget(createCard("Projects at risk", 8 , "#d97706"))
    cardsLayout.addWidget(createCard("Overdue Projects", 4 , "#dc2626"))

    overviewLayout.addLayout(cardsLayout)


    # WEEKLY PROGRESS LINE CHART
    # i will have each point to represent a week of the project
    # the below resource was used to help with creating line chart and adding points
    # https://doc.qt.io/qtforpython-6/examples/example_charts_linechart.html?
    series = QLineSeries()
    series.setName("Completed tasks")
    series.setPointsVisible(True)
    series.setPen(QPen(QColor("#FFD700"), 3))

    for week, completed in enumerate(weeklyCompleted, start=1):
        percentage = (completed / totalTasks) * 100
        series.append(week, percentage)

    # Create the chart
    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Weekly Task Completion")
    chart.legend().hide()

    #https://doc.qt.io/qtforpython-6/examples/example_charts_lineandbar.html?


    # X-axis: Week numbers
    axisX = QValueAxis()
    axisX.setRange(1, 6)
    axisX.setTickCount(6)
    axisX.setLabelFormat("Week %.0f")

    # Y-axis: Completion percentage
    axisY = QValueAxis()
    axisY.setRange(0, 100)
    axisY.setTickCount(6)
    axisY.setLabelFormat("%.0f%%")

    chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
    chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)

    series.attachAxis(axisX)
    series.attachAxis(axisY)

    # Display chart inside the overview page
    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
    chartView.setMinimumHeight(350)

    overviewLayout.addWidget(chartView)

    # Static chart navigation arrows
    chartNavigation = QHBoxLayout()

    leftArrow = QLabel("<")
    rightArrow = QLabel(">")
    chartNumber = QLabel("Chart 1 of 10")

    # Style the arrows - this resource was used to help useQLabel, setAlignment() and setStyleSheet() to customise the appearance of labels.
    #https://doc.qt.io/qtforpython-6.8/tutorials/basictutorial/widgetstyling.html?

    # Style the left arrow
    leftArrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html?#PySide6.QtWidgets.QWidget.setFixedSize
    # used to make sure size doesnt change
    leftArrow.setFixedSize(40, 30)
    leftArrow.setStyleSheet("""
        background-color: #808080;
        color: white;
        border-radius: 5px;
        font-size: 20px;
    """)

    # Style the right arrow
    # https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html?#PySide6.QtWidgets.QWidget.setFixedSize
    # used to make sure size is same
    rightArrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
    rightArrow.setFixedSize(40, 30)
    rightArrow.setStyleSheet("""
        background-color: #808080;
        color: white;
        border-radius: 5px;
        font-size: 20px;
    """)

    chartNumber.setStyleSheet("color: black; font-size: 14px;")   #makes text chart 1 of 10 black and 14px in size

    # Centre the arrows underneath the chart
    chartNavigation.addStretch()  #Creates flexible empty space on the left of the navigation controls.
    chartNavigation.addWidget(leftArrow)
    chartNavigation.addWidget(chartNumber)     #all of this is used to make labels follow right order
    chartNavigation.addWidget(rightArrow)
    chartNavigation.addStretch()

    overviewLayout.addLayout(chartNavigation)

    # Explanation underneath the chart
    chart_note = QLabel(
        "The line chart shows a static example of an example of a visual project completion over a 6-week period. The data is not dynamic and does not reflect real-time updates the manager will be able to flick through numerous line charts of projects."
    )
    chart_note.setStyleSheet("color: #666666; font-size: 12px;")
    chart_note.setWordWrap(True)

    overviewLayout.addWidget(chart_note)

    pages.addWidget(overviewPage)


    #https://learnmodernpython.com/pyqt-pyside-mastering-qstackedwidget-for-tabbed-interfaces/?#using-custom-buttons


    # For employees page

    
    # For view employees workload page
    # https://doc.qt.io/qtforpython-6/tutorials/basictutorial/treewidget.html
    # using this resource i used the QTreeWidget tutorial to display employees and their assigned tasks
    # the tutorial uses Qtreewidget and QTreeWidgetItem to create a tree structure to display data in a heirachry manner where clicking an arrow next to parent item reveals item underneath.
    # the tutorial uses a dictoinary of folders and files whereas i will use a dictionary of employees and their assigned tasks. The tutorial uses a static example of folders and files whereas i will use a static example of employees and their assigned tasks
    employeesPage = QWidget()
    employeesLayout = QVBoxLayout(employeesPage)

    employeesTitle = QLabel("Employee Workloads")
    employeesTitle.setStyleSheet("font-size: 28px; font-weight: bold;")

    employeesLayout.addWidget(employeesTitle)

    # copied the static employee task data from the team's Tasks page
    employeeTasks = {
        "Amira Hussain": [("Wireframes", "Completed", "100%"),("UI design", "In Progress", "55%")],

        "Ben Johnson": [
            ("Front-end build", "In Progress", "20%"),

            ("Browser and device testing", "At Risk", "0%"),

            ("Write printing paper guide", "Scheduled", "0%"),

            ("Update footer and legal pages", "In Progress", "40%"),

            ("SEO checks", "Scheduled", "0%"),

            ("Fix navigation bugs", "In Progress", "10%")
        ],

        "Chloe Nguyen": [("Content migration", "In Progress", "30%"),("Accessibility review", "Scheduled", "0%")],

        "Erin Wallace": [("Task list screens", "In Progress", "15%"),("Reporting dashboard", "Scheduled", "0%"),("Order and install printers", "Scheduled", "0%")],

        "Hannah Reid": [("Requirements workshop", "Completed", "100%"),("User acceptance testing", "Scheduled", "0%")],

        "Kash Patel": [("Data model", "In Progress", "60%"),("Login and permissions", "At Risk", "25%"),("Compare printer suppliers", "In Progress", "70%")],

        "Noah Okafor": [("Stakeholder interviews", "Completed", "100%"),("Launch", "Scheduled", "0%")]
    }

    #Create the tree widget
    employeesHeirarchy = QTreeWidget()
    employeesHeirarchy.setColumnCount(3)
    employeesHeirarchy.setHeaderLabels([
        "Employee / Task", "Status", "Progress"
    ])

    employeesHeirarchy.setColumnWidth(0, 330)
    employeesHeirarchy.setColumnWidth(1, 130)

    # Add each employee and their tasks
    heirarchy = []

    for employee, tasks in employeeTasks.items():
        employeeItem = QTreeWidgetItem([employee])

        for task, status, progress in tasks:
            taskItem = QTreeWidgetItem([
                task, status, progress
            ])
            employeeItem.addChild(taskItem)

        heirarchy.append(employeeItem)

    employeesHeirarchy.insertTopLevelItems(0, heirarchy)

    employeesLayout.addWidget(employeesHeirarchy)

    pages.addWidget(employeesPage)



    #For projects page

    
    #For projects page
    # https://doc.qt.io/qtforpython-6/tutorials/basictutorial/treewidget.html
    # I followed the same approach as the employees page to create a projects page that displays projects and their associated tasks in a tree structure


    projectsPage = QWidget()
    projectsLayout = QVBoxLayout(projectsPage)

    projectsTitle = QLabel("Project Progress")
    projectsTitle.setStyleSheet(
        "font-size: 28px; font-weight: bold;"
    )

    projectsLayout.addWidget(projectsTitle)

    # Static project task data
    projectTasks = {
        "Website Redesign": [
            ("Stakeholder interviews", "Noah Okafor", "Completed", "100%"),

            ("Wireframes", "Amira Hussain", "Completed", "100%"),

            ("UI design", "Amira Hussain", "In Progress", "55%"),

            ("Content migration", "Chloe Nguyen", "In Progress", "30%"),

            ("Front-end build", "Ben Johnson", "In Progress", "20%"),

            ("Accessibility review", "Chloe Nguyen", "Scheduled", "0%"),
            ("Browser and device testing", "Ben Johnson", "At Risk", "0%"),
            ("Launch", "Noah Okafor", "Scheduled", "0%"),
            ("Update footer and legal pages", "Ben Johnson", "In Progress", "40%"),
            ("SEO checks", "Ben Johnson", "Scheduled", "0%"),

            ("Fix navigation bugs", "Ben Johnson", "In Progress", "10%")
        ],

        "Customer Portal": [
            ("Requirements workshop", "Hannah Reid", "Completed", "100%"),
            ("Data model", "Kash Patel", "In Progress", "60%"),
            ("Login and permissions", "Kash Patel", "At Risk", "25%"),
            ("Task list screens", "Erin Wallace", "In Progress", "15%"),
            ("Reporting dashboard", "Erin Wallace", "Scheduled", "0%"),
            ("User acceptance testing", "Hannah Reid", "Scheduled", "0%")
        ],

        "Office Printing": [
            ("Compare printer suppliers", "Kash Patel", "In Progress", "70%"),
            ("Order and install printers", "Erin Wallace", "Scheduled", "0%"),
            ("Write printing paper guide", "Ben Johnson", "Scheduled", "0%")
        ]
    }

    # Create the tree widget
    projectsHeirarchy = QTreeWidget()
    projectsHeirarchy.setColumnCount(4)
    projectsHeirarchy.setHeaderLabels(["Project / Task", "Assigned to", "Status", "Progress"])

    projectsHeirarchy.setColumnWidth(0, 330)
    projectsHeirarchy.setColumnWidth(1, 160)
    projectsHeirarchy.setColumnWidth(2, 130)

    #  we then addd the projects and their tasks here
    heirarchyTwo = []

    for project, tasks in projectTasks.items():
        projectItem = QTreeWidgetItem([project])

        for task, employee, status, progress in tasks:
            taskItem = QTreeWidgetItem([
                task, employee, status, progress
            ])
            projectItem.addChild(taskItem)

        heirarchyTwo.append(projectItem)

    projectsHeirarchy.insertTopLevelItems(0, heirarchyTwo)

    projectsLayout.addWidget(projectsHeirarchy)

    pages.addWidget(projectsPage)



    # For tasks page

    tasksPage = QWidget()
    tasksLayout = QVBoxLayout(tasksPage)

    tasksTitle = QLabel("In final solution we will be able to assign tasks to employees here")
    tasksTitle.setStyleSheet(
        "font-size: 28px; font-weight: bold;"
    )

    tasksLayout.addWidget(tasksTitle)
    tasksLayout.addStretch()

    pages.addWidget(tasksPage)


    # ADD PAGES BELOW NAVBAR

    mainLayout.addWidget(pages)


    # To connect the navigation bar

    overviewButton.clicked.connect(
        lambda: pages.setCurrentIndex(0)
    )

    employeesButton.clicked.connect(
        lambda: pages.setCurrentIndex(1)
    )

    projectsButton.clicked.connect(
        lambda: pages.setCurrentIndex(2)
    )

    tasksButton.clicked.connect(
        lambda: pages.setCurrentIndex(3)
    )




    return managerWindow #used to run the application

