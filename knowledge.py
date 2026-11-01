from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QTextBrowser,
    QSplitter, QInputDialog, QMessageBox,
    QAbstractItemView
)
from PySide6.QtCore import Qt

import sample_data
from styles import set_role, PALETTE, SPACING


def create_page(data=None):
    # Use supplied data, falling back to sample data only when necessary.
    if data is None:
        data = sample_data.get_sample_data()

    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(16)

    # --------------------------------------------------
    # PAGE TITLE
    # --------------------------------------------------

    title = QLabel("Knowledge Management")
    set_role(title, "title")
    layout.addWidget(title)

    subtitle = QLabel("Share knowledge, find solutions and contribute to discussions.")
    set_role(subtitle, "subtitle")
    layout.addWidget(subtitle)

    # --------------------------------------------------
    # TOPIC FILTER AND CREATE POST BUTTON
    # --------------------------------------------------

    toolbar = QHBoxLayout()

    topic_label = QLabel("Topic:")
    topic_label.setStyleSheet("font-weight: bold;")

    topic_combo = QComboBox()
    topic_combo.addItem("All Topics", None)

    for topic in data["topics"]:
        topic_combo.addItem(topic["name"], topic["id"])

    topic_combo.setMinimumWidth(220)

    new_post_button = QPushButton("+ New Post")
    new_post_button.setCursor(Qt.PointingHandCursor)
    new_post_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {PALETTE['primary']};
            color: {PALETTE['text']};
            border: none;
            border-radius: 6px;
            padding: 9px 18px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {PALETTE['primary_dk']};
        }}
    """)

    toolbar.addWidget(topic_label)
    toolbar.addWidget(topic_combo)
    toolbar.addStretch()
    toolbar.addWidget(new_post_button)

    layout.addLayout(toolbar)

    # --------------------------------------------------
    # MAIN CONTENT AREA
    # --------------------------------------------------

    splitter = QSplitter(Qt.Horizontal)

    # LEFT SIDE: POSTS DISPLAY
    posts_panel = QWidget()
    posts_layout = QVBoxLayout(posts_panel)
    posts_layout.setContentsMargins(0, 0, 8, 0)

    posts_heading = QLabel("Discussion Posts")
    set_role(posts_heading, "subtitle")
    posts_layout.addWidget(posts_heading)

    posts_table = QTableWidget()
    posts_table.setColumnCount(4)
    posts_table.setHorizontalHeaderLabels([
        "Title", "Author", "Created", "Replies"
    ])

    posts_table.setSelectionBehavior(
        QAbstractItemView.SelectRows
    )
    posts_table.setSelectionMode(
        QAbstractItemView.SingleSelection
    )
    posts_table.setEditTriggers(
        QAbstractItemView.NoEditTriggers
    )
    posts_table.verticalHeader().setVisible(False)
    posts_table.setAlternatingRowColors(True)

    header = posts_table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.Stretch)
    header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

    posts_layout.addWidget(posts_table)

    splitter.addWidget(posts_panel)

    # RIGHT SIDE: POST DETAILS
    details_panel = QWidget()
    details_layout = QVBoxLayout(details_panel)
    details_layout.setContentsMargins(8, 0, 0, 0)

    details_heading = QLabel("Post Details")
    set_role(details_heading, "subtitle")
    details_layout.addWidget(details_heading)

    post_title = QLabel("Select a post to view its details")
    post_title.setWordWrap(True)
    post_title.setStyleSheet("font-size: 17px; font-weight: bold;")

    post_author = QLabel("")
    post_author.setStyleSheet(
        f"color: {PALETTE['text_muted']};"
    )

    post_body = QTextBrowser()
    post_body.setOpenExternalLinks(True)
    post_body.setPlaceholderText("Post content will appear here.")

    replies_heading = QLabel("Replies")
    set_role(replies_heading, "subtitle")

    replies_display = QTextBrowser()
    replies_display.setPlaceholderText("No replies yet.")

    reply_button = QPushButton("Add Reply")
    reply_button.setCursor(Qt.PointingHandCursor)
    reply_button.setEnabled(False)

    reply_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {PALETTE['button']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 9px 18px;
        }}
        QPushButton:hover {{
            background-color: {PALETTE['button_hover']};
        }}
        QPushButton:disabled {{
            background-color: {PALETTE['border']};
            color: {PALETTE['text_muted']};
        }}
    """)

    details_layout.addWidget(post_title)
    details_layout.addWidget(post_author)
    details_layout.addWidget(post_body, 2)
    details_layout.addWidget(replies_heading)
    details_layout.addWidget(replies_display, 2)
    details_layout.addWidget(reply_button)

    splitter.addWidget(details_panel)
    splitter.setSizes([550, 550])

    layout.addWidget(splitter)

    # --------------------------------------------------
    # HELPER FUNCTIONS
    # --------------------------------------------------

    selected_post = {"post": None}

    def current_user():
        # Default to the first employee if no role is available.
        return data["role_users"].get(
            "Employee",
            data["employees"][0]["name"]
        )

    def next_id(items):
        if not items:
            return 1
        return max(item["id"] for item in items) + 1

    def refresh_posts():
        # Refresh the posts table using the selected topic.

        posts_table.setRowCount(0)

        selected_topic = topic_combo.currentData()

        filtered_posts = [
            post for post in data["posts"]
            if selected_topic is None
            or post["topic_id"] == selected_topic
        ]

        for post in filtered_posts:
            row = posts_table.rowCount()
            posts_table.insertRow(row)

            values = [
                post["title"],
                post["author"],
                post["created"],
                str(len(post.get("replies", [])))
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                posts_table.setItem(row, column, item)

            # Store the post ID on the title cell.
            posts_table.item(row, 0).setData(
                Qt.UserRole, post["id"]
            )

        if posts_table.rowCount() > 0:
            posts_table.selectRow(0)
        else:
            selected_post["post"] = None
            post_title.setText("No posts found")
            post_author.setText("")
            post_body.clear()
            replies_display.clear()
            reply_button.setEnabled(False)

    def display_post():
        # Display the currently selected post and its replies.

        row = posts_table.currentRow()

        if row < 0:
            return

        post_id = posts_table.item(row, 0).data(Qt.UserRole)

        post = next(
            (p for p in data["posts"] if p["id"] == post_id),
            None
        )

        if post is None:
            return

        selected_post["post"] = post

        post_title.setText(post["title"])
        post_author.setText(
            f"Posted by {post['author']} | {post['created']}"
        )
        post_body.setPlainText(post["body"])

        replies = post.get("replies", [])

        if not replies:
            replies_display.setPlainText("No replies yet.")
        else:
            reply_text = []

            for reply in replies:
                reply_text.append(
                    f"{reply['author']} ({reply['created']})\n"
                    f"{reply['body']}\n"
                    f"{'-' * 45}"
                )

            replies_display.setPlainText(
                "\n\n".join(reply_text)
            )

        reply_button.setEnabled(True)

    # --------------------------------------------------
    # CREATE POST
    # --------------------------------------------------

    def create_post():
        topic_id = topic_combo.currentData()

        if topic_id is None:
            QMessageBox.warning(
                page,
                "Select a Topic",
                "Please select a specific topic before creating a post."
            )
            return

        post_title_text, ok = QInputDialog.getText(
            page, "New Post", "Post title:"
        )

        if not ok or not post_title_text.strip():
            return

        post_body_text, ok = QInputDialog.getMultiLineText(
            page, "New Post", "Post content:"
        )

        if not ok or not post_body_text.strip():
            return

        new_post = {
            "id": next_id(data["posts"]),
            "topic_id": topic_id,
            "author": current_user(),
            "title": post_title_text.strip(),
            "body": post_body_text.strip(),
            "created": datetime.now().strftime("%d %b %Y %H:%M"),
            "replies": []
        }

        data["posts"].append(new_post)

        refresh_posts()

        # Select the newly created post.
        for row in range(posts_table.rowCount()):
            if posts_table.item(row, 0).data(Qt.UserRole) == new_post["id"]:
                posts_table.selectRow(row)
                break

    # --------------------------------------------------
    # ADD REPLY
    # --------------------------------------------------

    def add_reply():
        post = selected_post["post"]

        if post is None:
            return

        reply_text, ok = QInputDialog.getMultiLineText(
            page,
            "Add Reply",
            "Write your reply:"
        )

        if not ok or not reply_text.strip():
            return

        new_reply = {
            "id": next_id(post.get("replies", [])),
            "author": current_user(),
            "body": reply_text.strip(),
            "created": datetime.now().strftime("%d %b %Y %H:%M")
        }

        post.setdefault("replies", []).append(new_reply)

        refresh_posts()

        # Restore selection to the post being discussed.
        for row in range(posts_table.rowCount()):
            if posts_table.item(row, 0).data(Qt.UserRole) == post["id"]:
                posts_table.selectRow(row)
                break

    # --------------------------------------------------
    # CONNECT SIGNALS
    # --------------------------------------------------

    topic_combo.currentIndexChanged.connect(refresh_posts)
    posts_table.itemSelectionChanged.connect(display_post)
    new_post_button.clicked.connect(create_post)
    reply_button.clicked.connect(add_reply)

    # Initial population
    refresh_posts()

    return page
