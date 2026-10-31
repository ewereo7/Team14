# To-do lists and Project Tasks Page
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QComboBox, QTableWidget, QTableWidgetItem, QHeaderView)
import sample_data 
from styles import set_role, status_chip_qss


COLUMNS = ["Task", "Project", "Assigned to", "Start", "Due", "Status", "Progress"]


def create_page(data=None):
    data = sample_data.get_sample_data()
    # If no data is given then use the sample data
    if data is None:
        data = sample_data.get_sample_data()

    # Turns a project id into its name
    project_names = {p["id"]: p["name"] for p in data["projects"]}

    page = QWidget()
    layout = QVBoxLayout(page)
    title = QLabel("To-Do Lists & Tasks")
    set_role(title, "title")
    layout.addWidget(title)

    # Filter dropdowns
    filters = QHBoxLayout()

    # Person Dropdown
    person_box = QComboBox()
    person_box.addItem("Everyone", None)
    for e in data["employees"]:
        person_box.addItem(e["name"], e["name"])

    # Project Dropdown
    project_box = QComboBox()
    project_box.addItem("All projects", None)
    for p in data["projects"]:
        project_box.addItem(p["name"], p["id"])

    # Add labels and dropdowns to the row
    filters.addWidget(QLabel("Person:"))
    filters.addWidget(person_box)
    filters.addWidget(QLabel("Project:"))
    filters.addWidget(project_box)
    filters.addStretch() # Keeps them on the left
    layout.addLayout(filters)

    # Task table
    table = QTableWidget(0, len(COLUMNS))
    table.setHorizontalHeaderLabels(COLUMNS)
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    table.verticalHeader().setVisible(False)
    layout.addWidget(table)

    # Refills the table based on the dropdowns
    def fill_table():
        tasks = sample_data.tasks_for(data, person=person_box.currentData(),
                                      project_id=project_box.currentData())
        table.setRowCount(len(tasks))

        for row, t in enumerate(tasks):
            # Status left as None, it gets a coloured label instead
            values = [t["title"], project_names[t["project_id"]], t["assigned_to"],
                      t["start_date"], t["end_date"], None, f'{t["progress"]}%']
            for col, v in enumerate(values):
                if v is not None:
                    table.setItem(row, col, QTableWidgetItem(v))

            chip = QLabel(t["status"])
            chip.setStyleSheet(status_chip_qss(t["status"]))
            table.setCellWidget(row, 5, chip)

    person_box.currentIndexChanged.connect(fill_table)
    project_box.currentIndexChanged.connect(fill_table)
    fill_table()
    return page
