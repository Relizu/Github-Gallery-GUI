from PySide6.QtWidgets import QWidget ,QVBoxLayout ,QLabel ,QPushButton ,QScrollArea ,QSpacerItem, QSizePolicy, QTextBrowser
import markdown
import base64
import requests

class repoPage(QWidget):
    def __init__(self,repo,parent):
        super().__init__()
        self.p = parent
        self.repo = repo
        self.currentdir=""
        main_layout = QVBoxLayout(self)

        content = QScrollArea()
        content.setWidgetResizable(True)  
        main_layout.addWidget(content)

        contentWidget = QWidget()
        content.setWidget(contentWidget)
        layout = QVBoxLayout(contentWidget)
        
        backButton= QPushButton("<<")
        backButton.clicked.connect(self.p.back_to_gallery)

        name =QLabel(repo.name)
        name.setStyleSheet("font-size:30px")

        description =QLabel(repo.description)
        description.setStyleSheet("font-size:10px")

        downloadButton= QPushButton("تنزيل")
        downloadButton.clicked.connect(self.downloadrepo)

        self.dirLayout= QVBoxLayout()

        layout.addWidget(backButton)
        layout.addWidget(name)
        layout.addWidget(description)
        layout.addWidget(downloadButton)
        layout.addLayout(self.dirLayout)
        try:
            for i in repo.get_contents(self.currentdir):
                if i.type =="dir":
                    tempLabelbtn=QPushButton("📁"+i.name)
                    tempLabelbtn.clicked.connect(lambda checked=False, b=tempLabelbtn: self.updateDir(b))
                    self.dirLayout.addWidget(tempLabelbtn)
                else:
                    tempLabelbtn=QPushButton("📄"+i.name)
                    
                    self.dirLayout.addWidget(tempLabelbtn)
        except:
            print("empty probably")
        viewer = QTextBrowser()
        try:
            if repo.get_contents(self.currentdir+"README.md"):
                viewer.setHtml(markdown.markdown(base64.b64decode(repo.get_contents(self.currentdir+"README.md").content).decode("utf-8"), extensions=["fenced_code"]))
        except:
            print("no readme")
        viewer.setOpenExternalLinks(True) 
        layout.addWidget(viewer)

    
    def updateDir(self, sender):
        while self.dirLayout.count():
            item = self.dirLayout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        self.currentdir +="/"+sender.text()[1:]
        for i in self.repo.get_contents(self.currentdir):
            if i.type =="dir":
                tempLabelbtn=QPushButton("📁"+i.name)
                tempLabelbtn.clicked.connect(lambda checked=False, b=tempLabelbtn: self.updateDir(b))
                self.dirLayout.addWidget(tempLabelbtn)
            else:
                tempLabelbtn=QPushButton("📄"+i.name)
                tempLabelbtn.clicked.connect(lambda checked=False, b=tempLabelbtn: self.updateDir(b))
                self.dirLayout.addWidget(tempLabelbtn)
    
    def downloadrepo(self):
        zip_url = self.repo.get_archive_link(archive_format="zipball", ref="main") 

        response = requests.get(zip_url)
        with open("downloads/"+self.repo.name+".zip", "wb") as f:
            f.write(response.content)