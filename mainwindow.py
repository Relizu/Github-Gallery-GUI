from PySide6.QtWidgets import QStackedWidget ,QLabel
from loginPage import loginPage
from GalleryPage import galleryPage
from repo_page import repoPage

class mainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.token=""
        self.setWindowTitle("متصفح جيت هب")
        self.resize(600,600)
        self.setStyleSheet("""
            background-color:#1f1f1f;
            color: white;
            border-radius:30px;
        """)
        self.addWidget(loginPage(parent=self))
        
        self.setCurrentIndex(0)
        
    def goto_gallery(self):
        self.gallery = galleryPage(parent=self)
        self.addWidget(self.gallery)
        self.setCurrentIndex(1)
    def open_repo(self,repo):
        self.addWidget(repoPage(repo,parent=self))
        self.setCurrentIndex(2)
    def back_to_gallery(self):
        w = self.currentWidget()
        self.removeWidget(w)
        self.setCurrentIndex(1)
        w.deleteLater()