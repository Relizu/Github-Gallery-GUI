from PySide6.QtWidgets import QWidget ,QLabel ,QPushButton ,QVBoxLayout ,QSpacerItem ,QSizePolicy
from PySide6.QtCore import Qt

class loginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QPushButton{
                width:20px;
                border: 1px solid white;
                padding: 20px 10px;
                border-radius: 10px;
            }
            QPushButton:hover{
                background-color:white;
                color:#1f1f1f;
            }
            QLabel{
                font-size: 70px;
                qproperty-alignment: AlignCenter;
            }
        """)
        layout = QVBoxLayout(self)
        ll = QLabel()
        ll.setText("مرحبا...")
        
        LoginButton = QPushButton("تسجيل دخول باستخدام جيت هب",self)
        LoginButton.setFixedSize(200,60)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(ll)
        layout.addWidget(LoginButton,alignment=Qt.AlignCenter)        
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))