from PySide6.QtWidgets import QWidget ,QVBoxLayout ,QHBoxLayout , QScrollArea ,QPushButton, QLabel, QDialog, QLineEdit, QRadioButton, QCheckBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter

from galleryItem import galleryItem
from github import Github
import requests

class galleryPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.p = parent
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
        
        profile = QLabel()
        profile.setStyleSheet("border:0;")
        profile.setFixedSize(50, 50)

        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(self.g.get_user().avatar_url).content)
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        mask = QPixmap(50, 50)
        mask.fill(Qt.transparent)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 50, 50)
        painter.end()

        pixmap.setMask(mask.createMaskFromColor(Qt.transparent))

        profile.setPixmap(pixmap)


        AddButton = QPushButton("+")
        AddButton.setStyleSheet("""border: 1px solid white;border-radius:10px; font-size:40px;""")
        AddButton.setFixedSize(50,50)
        AddButton.clicked.connect(self.add_repo)

        topperLayout.addWidget(profile)
        topperLayout.addWidget(AddButton)

        galleryArea= QScrollArea()
        galleryArea.setWidgetResizable(True)
        galleryArea.setFrameShape(QScrollArea.NoFrame)
        layout.addWidget(topper)
        layout.addWidget(galleryArea)
        contentwidget= QWidget()
        self.contentlayout = QHBoxLayout(contentwidget)
        galleryArea.setWidget(contentwidget)

        for repo in self.g.get_user().get_repos():
            self.contentlayout.addWidget(galleryItem(repo,parent=self))
    
    def update(self):
        while self.contentlayout.count():
            item = self.contentlayout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        for repo in self.g.get_user().get_repos():
            self.contentlayout.addWidget(galleryItem(repo,parent=self))

    def add_repo(self):
        msg = QDialog()
        msg.setWindowTitle("اضافه ريبو")

        main_layout = QVBoxLayout()

        main_layout.addWidget(QLabel("العنوان"))
        title_input = QLineEdit()
        main_layout.addWidget(title_input)

        main_layout.addWidget(QLabel("الوصف"))
        description_input = QLineEdit()
        main_layout.addWidget(description_input)

        publicbtn =QRadioButton("عام")
        main_layout.addWidget(publicbtn)

        privatebtn =QRadioButton("خاص")
        main_layout.addWidget(privatebtn)

        publicbtn.setChecked(True)

        main_layout.addWidget(QLabel("اضافه ملف اقرأني(README.md)"))
        readmebtn =QCheckBox()
        main_layout.addWidget(readmebtn)

        button_layout = QHBoxLayout()
        submit_btn = QPushButton("اضافة")
        cancel_btn = QPushButton("الغاء")
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(cancel_btn)
        main_layout.addLayout(button_layout)

        submit_btn.clicked.connect(msg.accept)
        cancel_btn.clicked.connect(msg.reject)

        msg.setLayout(main_layout)
        print(self.g.get_user())
        if msg.exec() == QDialog.Accepted:
            self.g.get_user().create_repo(
                name=title_input.text().strip().replace(" ", "-"),
                description=description_input.text(),
                private=privatebtn.isChecked(),  
                auto_init=readmebtn.isChecked()  
            )
            self.update()
        else:
            return None