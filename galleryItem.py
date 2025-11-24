from PySide6.QtWidgets import QWidget ,QVBoxLayout ,QLabel
from PySide6.QtCore import Qt

class galleryItem(QWidget):
    def __init__(self,repo,parent):
        super().__init__()
        self.repo = repo
        self.p = parent
        self.setFixedSize(150,200)
        self.setStyleSheet("""
            QWidget{
                background-color:White;               
            }
            QLabel{
                background-color:#1f1f1f;    
                qproperty-alignment: AlignCenter;           
            }
""")
        layout = QVBoxLayout(self)
        image= QWidget()
        image.setFixedSize(150,150)
        Title= QLabel()
        Title.setText(repo.name)
        layout.addWidget(image)
        layout.addWidget(Title)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.p.p.open_repo(self.repo)