from PySide6.QtWidgets import QWidget ,QVBoxLayout ,QHBoxLayout , QScrollArea ,QPushButton
from PySide6.QtCore import Qt
from galleryItem import galleryItem

class galleryPage(QWidget):
    def __init__(self):
        super().__init__()
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
        AddButton = QPushButton("+")
        AddButton.setStyleSheet("""border: 1px solid white;border-radius:10px; font-size:40px;""")
        AddButton.setFixedSize(50,50)
        topperLayout.addWidget(AddButton)
        galleryArea= QScrollArea()
        galleryArea.setFrameShape(QScrollArea.NoFrame)
        layout.addWidget(topper)
        layout.addWidget(galleryArea)
        
        layout.addWidget(galleryItem("111"))
        layout.addWidget(galleryItem("222"))