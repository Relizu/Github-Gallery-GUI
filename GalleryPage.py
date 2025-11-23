from PySide6.QtWidgets import QWidget ,QVBoxLayout ,QHBoxLayout , QScrollArea ,QPushButton ,QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from galleryItem import galleryItem
from github import Github
import requests

class galleryPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.user_token = parent.token
        self.g = Github(self.user_token)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        topper = QWidget()
        topper.setStyleSheet("""
            border-top: 0px;
            border-left: 0px;
            border-right: 0px;
            border-bottom: 1px solid white;
        """)
        topper.setFixedHeight(70)
        topperLayout =QHBoxLayout(topper)
        
        profile=QLabel()
        profile.setFixedWidth(50)
        profile.setStyleSheet("border: 0px")
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(self.g.get_user().avatar_url).content)
        pixmap =  pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        profile.setPixmap(pixmap)

        AddButton = QPushButton("+")
        AddButton.setStyleSheet("""border: 1px solid white;border-radius:10px; font-size:40px;""")
        AddButton.setFixedSize(50,50)

        topperLayout.addWidget(profile)
        topperLayout.addWidget(AddButton)

        galleryArea= QScrollArea()
        galleryArea.setWidgetResizable(True)
        galleryArea.setFrameShape(QScrollArea.NoFrame)
        layout.addWidget(topper)
        layout.addWidget(galleryArea)
        contentwidget= QWidget()
        contentlayout = QHBoxLayout(contentwidget)
        galleryArea.setWidget(contentwidget)

        for repo in self.g.get_user().get_repos():
            contentlayout.addWidget(galleryItem(repo.name))
        