
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QComboBox, QTableWidget, QTableWidgetItem, QHeaderView)
import sample_data 
from styles import set_role

def create_page(data=None):
    data = sample_data.get_sample_data()
    # If no data is given, use the sample data
    if data is None:
        data = sample_data.get_sample_data()

    page = QWidget()
    layout = QVBoxLayout(page)
    title = QLabel("Knowledge Management")
    set_role(title, "title")
    layout.addWidget(title)

    # Build the interface here

    return page
