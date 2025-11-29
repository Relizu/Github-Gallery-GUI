from PySide6.QtWidgets import QWidget ,QLabel ,QPushButton ,QVBoxLayout ,QSpacerItem ,QSizePolicy ,QDialog ,QHBoxLayout
from PySide6.QtCore import Qt ,QObject, QThread, Signal
from PySide6.QtGui import QGuiApplication
import requests
import time
import keyring
from github import Github

class PollWorker(QObject):
    finished = Signal(str)   
    error = Signal(str)

    def __init__(self, client_id, device_code, interval):
        super().__init__()
        self.client_id = client_id
        self.device_code = device_code
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            time.sleep(self.interval)

            resp = requests.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": self.client_id,
                    "device_code": self.device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                },
                headers={"Accept": "application/json"},
            )

            data = resp.json()

            if "access_token" in data:
                token = data["access_token"]
                self.finished.emit(token)
                return

            if data.get("error") == "expired_token":
                self.error.emit("Device code expired")
                return


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
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(ll)
        if keyring.get_password("githubgallery", "github_access_token"):
            loginAs= QPushButton("دخول ك"+Github(keyring.get_password("githubgallery", "github_access_token")).get_user().name)
            loginAs.setFixedSize(200,60)
            loginAs.clicked.connect(self.login_As)
            layout.addWidget(loginAs,alignment=Qt.AlignCenter)

        LoginButton = QPushButton("تسجيل دخول باستخدام جيت هب",self)
        LoginButton.setFixedSize(200,60)
        LoginButton.clicked.connect(self.start_login)

        
        layout.addWidget(LoginButton,alignment=Qt.AlignCenter)        
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def start_login(self):
        resp = requests.post(
            "https://github.com/login/device/code",
            data={"client_id": self.CLIENT_ID, "scope": "repo read:user"},
            headers={"Accept": "application/json"}
        )

        data = resp.json()
        self.user_code = data["user_code"]
        self.device_code = data["device_code"]
        self.interval = data["interval"]

        print("code:", self.user_code)

        self.thread = QThread()
        self.worker = PollWorker(self.CLIENT_ID, self.device_code, self.interval)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.login_success)
        self.worker.error.connect(self.login_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        msg = QDialog()
        msg.setWindowTitle("تسجيل الدخول")
        main_layout = QVBoxLayout()

        main_layout.addWidget(QLabel("قم بالدخول الي الرابط ثم قم بادخال الكود"))

        main_layout.addWidget(QLabel("الرابط:"))
        linklayout =QHBoxLayout()
        linklayout.addWidget(QLabel("https://github.com/login/device/"))
        linkcopy =QPushButton("نسخ")
        linkcopy.clicked.connect(lambda checked=False, b="https://github.com/login/device/": self.copytext(b))
        linklayout.addWidget(linkcopy)
        main_layout.addLayout(linklayout)
        
        main_layout.addWidget(QLabel("الكود:"))
        codelayout =QHBoxLayout()
        codelayout.addWidget(QLabel(self.user_code))
        codecopy =QPushButton("نسخ")
        codecopy.clicked.connect(lambda checked=False, b=self.user_code: self.copytext(b))
        codelayout.addWidget(codecopy)
        main_layout.addLayout(codelayout)

        button_layout = QHBoxLayout()
        submit_btn = QPushButton("حسنا")
        cancel_btn = QPushButton("الغاء")
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(cancel_btn)
        main_layout.addLayout(button_layout)
        submit_btn.clicked.connect(msg.accept)
        cancel_btn.clicked.connect(msg.reject)

        msg.setLayout(main_layout)
        if msg.exec() == QDialog.Accepted:
            return None
        else:
            return None

    def login_success(self, token):
        print("Token received:", token)

        keyring.set_password("githubgallery", "github_access_token", token)
        self.p.token = token
        self.p.goto_gallery()

    def login_error(self, msg):
        print("Error:", msg)

    def copytext(self,text):
        clipboard =QGuiApplication.clipboard()
        clipboard.setText(text)
    
    def login_As(self):
        self.p.token = keyring.get_password("githubgallery", "github_access_token")
        self.p.goto_gallery()