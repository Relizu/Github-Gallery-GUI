from PySide6.QtWidgets import QWidget ,QVBoxLayout ,QLabel

class galleryItem(QWidget):
    def __init__(self,text):
        super().__init__()
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
        Title.setText(text)
        layout.addWidget(image)
        layout.addWidget(Title)