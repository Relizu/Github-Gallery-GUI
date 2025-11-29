from PySide6.QtWidgets import QWidget ,QVBoxLayout ,QLabel ,QPushButton ,QScrollArea ,QSpacerItem, QSizePolicy, QTextBrowser, QFileDialog ,QDialog ,QLineEdit, QHBoxLayout, QStackedWidget
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QPlainTextEdit
import markdown
import base64
import requests
import os

class repoPage(QWidget):
    def __init__(self,repo,parent):
        super().__init__()
        self.p = parent
        self.repo = repo
        self.currentdir=""
        self.setStyleSheet("""
        border: 0;
        """)

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

        uploadfileButton= QPushButton("رفع ملف")
        uploadfileButton.clicked.connect(self.uploadfile)



        self.dirLayout= QVBoxLayout()

        layout.addWidget(backButton)
        layout.addWidget(name)
        layout.addWidget(description)
        layout.addWidget(downloadButton)
        layout.addWidget(uploadfileButton)
        dircontainer =QWidget()
        dircontainer.setStyleSheet("background-color:#2A2A2A; border:1px solid white;")
        dircontainer.setLayout(self.dirLayout)
        layout.addWidget(dircontainer)
        try:
            self.update()
        except:
            print("empty probably")
        fileLayout =QVBoxLayout()

        StackedContent=QStackedWidget()

        self.viewer = QTextBrowser()
        self.viewer.setStyleSheet("border:1px solid white;")

        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet("border:1px solid white;")

        try:
            if repo.get_contents(self.currentdir+"README.md"):
                self.currentfilelabel =QLabel("README.md")
                self.viewer.setHtml(markdown.markdown(base64.b64decode(repo.get_contents(self.currentdir+"README.md").content).decode("utf-8"), extensions=["fenced_code"]))
                self.editor.setPlainText(base64.b64decode(repo.get_contents(self.currentdir+"README.md").content).decode("utf-8"))
        except:
            self.currentfilelabel =QLabel("")
            print("no readme")
        self.viewer.setOpenExternalLinks(True) 
        
        layout.addWidget(self.currentfilelabel)
        layout.addWidget(self.viewer)

    def update(self):
        while self.dirLayout.count():
            item = self.dirLayout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        for i in self.repo.get_contents(self.currentdir):
            fileLayout=QHBoxLayout()

            removefilebtn=QPushButton("x")
            removefilebtn.setFixedWidth(30)
            removefilebtn.clicked.connect(lambda checked=False, b=removefilebtn: self.deleteFile(b))

            editfilebtn=QPushButton("🖊️")
            editfilebtn.setFixedWidth(30)
            editfilebtn.clicked.connect(lambda checked=False, b=editfilebtn: self.editfile(b))

            if i.type =="dir":
                tempLabelbtn=QPushButton("📁"+i.name)
                tempLabelbtn.clicked.connect(lambda checked=False, b=tempLabelbtn: self.updateDir(b))
            else:
                tempLabelbtn=QPushButton("📄"+i.name)
                tempLabelbtn.clicked.connect(lambda checked=False, b=tempLabelbtn: self.openfile(b))
            tempLabelbtn.setStyleSheet("border-top:1px solid white;")
            
            removefilebtn.file=tempLabelbtn
            editfilebtn.file = tempLabelbtn

            fileLayout.addWidget(tempLabelbtn)
            fileLayout.addWidget(editfilebtn)
            fileLayout.addWidget(removefilebtn)

            self.dirLayout.addLayout(fileLayout)

    def updateDir(self, sender):
        self.currentdir +="/"+sender.text()[1:]
        self.update()
    
    def openfile(self, sender):
        self.currentfilelabel.setText(sender.text()[1:])
        if sender.text()[-3:] == ".md":
            if self.currentdir=="":
                self.viewer.setHtml(markdown.markdown(base64.b64decode(self.repo.get_contents(sender.text()[1:]).content).decode("utf-8"), extensions=["fenced_code"]))
            else:
                self.viewer.setHtml(markdown.markdown(base64.b64decode(self.repo.get_contents(self.currentdir+"/"+sender.text()[1:]).content).decode("utf-8"), extensions=["fenced_code"]))
        else:
            self.viewer.setHtml("")

    def downloadrepo(self):
        zip_url = self.repo.get_archive_link(archive_format="zipball", ref="main") 

        response = requests.get(zip_url)
        downloads_path = os.path.join(os.getcwd(), "downloads", self.repo.name + ".zip")
        with open(downloads_path, "wb") as f:
            f.write(response.content)
    
    def uploadfile(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "All Files (*)")
        info =QFileInfo(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        msg = QDialog()
        msg.setWindowTitle("اضافه رساله")
        main_layout = QVBoxLayout()

        main_layout.addWidget(QLabel("الرساله"))
        commit_input = QLineEdit()
        main_layout.addWidget(commit_input)

        button_layout = QHBoxLayout()
        submit_btn = QPushButton("اضافة")
        cancel_btn = QPushButton("الغاء")
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(cancel_btn)
        main_layout.addLayout(button_layout)
        submit_btn.clicked.connect(msg.accept)
        cancel_btn.clicked.connect(msg.reject)

        msg.setLayout(main_layout)
        if msg.exec() == QDialog.Accepted:
            if self.currentdir=="":
                self.repo.create_file(info.fileName(),commit_input.text(),content)
            else:
                self.repo.create_file(self.currentdir+"/"+info.fileName(),commit_input.text(),content)
            
            self.update()
        else:
            return None
        
    def deleteFile(self, sender):
        msg = QDialog()
        msg.setWindowTitle("حذف الملف")
        main_layout = QVBoxLayout()

        main_layout.addWidget(QLabel("الرساله"))
        commit_input = QLineEdit()
        main_layout.addWidget(commit_input)

        main_layout.addWidget(QLabel("هل متأكد انك تريد حذف الملف؟"))

        button_layout = QHBoxLayout()
        submit_btn = QPushButton("حذف")
        cancel_btn = QPushButton("الغاء")
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(cancel_btn)
        main_layout.addLayout(button_layout)
        submit_btn.clicked.connect(msg.accept)
        cancel_btn.clicked.connect(msg.reject)

        msg.setLayout(main_layout)
        if msg.exec() == QDialog.Accepted:
            if self.currentdir=="":
                filec =self.repo.get_contents(sender.file.text()[1:])
            else:
                filec =self.repo.get_contents(self.currentdir+"/"+sender.file.text()[1:])

            self.repo.delete_file(filec.path,commit_input.text(),filec.sha)

            self.update()
        else:
            return None
    
    def editfile(self, sender):
        msg = QDialog()
        msg.setWindowTitle("تحرير الملف")
        main_layout = QVBoxLayout()

        main_layout.addWidget(QLabel("محتوى الملف"))
        content_input = QPlainTextEdit()
        if self.currentdir=="":
            content_input.setPlainText(base64.b64decode(self.repo.get_contents(sender.file.text()[1:]).content).decode("utf-8"))
        else:
            content_input.setPlainText(base64.b64decode(self.repo.get_contents(self.currentdir+"/"+sender.file.text()[1:]).content).decode("utf-8"))
        main_layout.addWidget(content_input)

        main_layout.addWidget(QLabel("الرساله"))
        commit_input = QLineEdit()
        main_layout.addWidget(commit_input)

        main_layout.addWidget(QLabel("هل متأكد انك تريد تعديل محتوى الملف؟"))

        button_layout = QHBoxLayout()
        submit_btn = QPushButton("تعديل")
        cancel_btn = QPushButton("الغاء")
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(cancel_btn)
        main_layout.addLayout(button_layout)
        submit_btn.clicked.connect(msg.accept)
        cancel_btn.clicked.connect(msg.reject)

        msg.setLayout(main_layout)
        if msg.exec() == QDialog.Accepted:
            if self.currentdir=="":
                filec =self.repo.get_contents(sender.file.text()[1:])
            else:
                filec =self.repo.get_contents(self.currentdir+"/"+sender.file.text()[1:])

            self.repo.update_file(
                path=sender.file.text()[1:],
                message=commit_input.text(),
                content=content_input.toPlainText(),
                sha=filec.sha
            )

            self.update()
        else:
            return None