from PySide6.QtWidgets import QWidget ,QVBoxLayout ,QLabel ,QPushButton ,QScrollArea ,QSpacerItem, QSizePolicy

class repoPage(QWidget):
    def __init__(self,repo,parent):
        super().__init__()
        self.p = parent
        self.repo = repo
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

        layout.addWidget(backButton)
        layout.addWidget(name)
        layout.addWidget(description)
        for i in repo.get_contents(""):
            layout.addWidget(QLabel(i.name))
        
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))