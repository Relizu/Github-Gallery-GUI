from PySide6.QtWidgets import QStackedWidget ,QLabel
from loginPage import loginPage
from GalleryPage import galleryPage
class mainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("متصفح جيت هب")
        self.resize(600,600)
        self.setStyleSheet("""
            background-color:#1f1f1f;
            color: white;
        """)
        self.addWidget(loginPage())
        self.addWidget(galleryPage())
        self.setCurrentIndex(1)

        