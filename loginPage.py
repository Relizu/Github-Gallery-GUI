from PySide6.QtWidgets import QWidget ,QLabel ,QPushButton ,QVBoxLayout ,QSpacerItem ,QSizePolicy ,QMessageBox
from PySide6.QtCore import Qt
import requests
import time
import threading

class loginPage(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.p= parent
        self.CLIENT_ID="Ov23liv0NqNDycBUrO0W"
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
        LoginButton.clicked.connect(self.start_login)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(ll)
        layout.addWidget(LoginButton,alignment=Qt.AlignCenter)        
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def start_login(self):
        
        resp = requests.post(
            "https://github.com/login/device/code",
            data={"client_id": self.CLIENT_ID, "scope": "read:user"},
            headers={"Accept": "application/json"}
        )
        data = resp.json()

        self.user_code = data["user_code"]
        self.device_code = data["device_code"]
        self.verify_url = data["verification_uri"]
        self.interval = data["interval"]

        print(self.user_code)

        self.poll_for_token()

    def poll_for_token(self):
        while True:
            time.sleep(self.interval)

            token_resp = requests.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": self.CLIENT_ID,
                    "device_code": self.device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
                },
                headers={"Accept": "application/json"}
            )
            token_data = token_resp.json()

            if "access_token" in token_data:
                access_token = token_data["access_token"]
                self.p.token = access_token
                self.p.goto_gallery()
                print(access_token)
                return
    