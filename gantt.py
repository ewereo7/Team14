# Gantt chart
# Import necessary libraries
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from sample_data import get_sample_data, parse_date
from styles import PALETTE, set_role, status_colour
from datetime import date


def create_page():
    page = QWidget()
    page.setObjectName("Page")
    data = get_sample_data()
    project = data["projects"][0]

    project_tasks = [
    task
    for task in data["tasks"]
    if task["project_id"] == project["id"]
]
    print(project["name"])
    print(len(project_tasks))

    layout = QVBoxLayout(page)
    title = QLabel("Project Gantt Chart")

    set_role(title, "title")
    project_selector = QComboBox()
    for project in data["projects"]:
        project_selector.addItem(project["name"], project["id"])

    layout.addWidget(title)
    layout.addWidget(project_selector)
    figure = Figure(
    figsize=(10, 6),
    facecolor=PALETTE["surface"]
)

    canvas = FigureCanvasQTAgg(figure)

    layout.addWidget(canvas)
    
    ax = figure.add_subplot(111)
    
    def update_chart():
        project_id = project_selector.currentData()

        selected_tasks = [
            task
            for task in data["tasks"]
            if task["project_id"] == project_id
        ]

        draw_gantt(ax, selected_tasks)

        figure.tight_layout()

        canvas.draw()
    
    project_selector.currentIndexChanged.connect(update_chart)
    update_chart()


    return page

def draw_gantt(ax, tasks):

    ax.clear()

    for index, task in enumerate(tasks):

        start = parse_date(task["start_date"])
        end = parse_date(task["end_date"])

        start_num = mdates.date2num(start)

        duration = (end - start).days + 1

        colour = status_colour(task["status"])

        ax.barh(
            y=index,
            width=duration,
            left=start_num,
            color=colour,
            height=0.6
        )
        ax.text(
            x=start_num + duration + 0.3,
            y=index,
            s=f"{task['progress']}%",
            va="center",
            fontsize=9,
            color=PALETTE["text"]
        )

    if tasks:
        latest_end = max(
            parse_date(task["end_date"])
            for task in tasks
        )

        ax.set_xlim(
            right=mdates.date2num(latest_end) + 5
        )

    statuses = [
    "Completed",
    "In Progress",
    "Scheduled",
    "At Risk"
    ]

    legend_items = [
        Patch(
            facecolor=status_colour(status),
            label=status
        )
        for status in statuses
    ]

    ax.legend(
        handles=legend_items,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.12),
        ncol=4,
        frameon=False
    )
    today = mdates.date2num(date.today())

    ax.axvline(
        x=today,
        color=PALETTE["danger"],
        linestyle="--",
        linewidth=1.5,
        alpha=0.8,
        label="Today"
    )
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([task["title"] for task in tasks])

    ax.invert_yaxis()

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))

    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)


if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    from styles import apply_theme
    apply_theme(app)

    window = create_page()
    window.resize(1100, 700)
    window.show()

    sys.exit(app.exec())