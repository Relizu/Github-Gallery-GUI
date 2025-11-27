from PySide6.QtWidgets import QWidget ,QVBoxLayout ,QLabel ,QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import matplotlib.pyplot as plt
from io import BytesIO

class galleryItem(QWidget):
    def __init__(self,repo,parent):
        super().__init__()
        self.repo = repo
        self.p = parent
        self.setFixedSize(160,200)
        self.setStyleSheet("""
            QLabel{
                background-color:#1f1f1f;    
                qproperty-alignment: AlignCenter;           
            }
""")

        layout = QVBoxLayout(self)

        chart_buf = self.languages_pie_chart(repo.get_languages())
        pixmap =QPixmap()
        pixmap.loadFromData(chart_buf.getvalue())

        image= QLabel()
        image.setStyleSheet("background-color:#2A2A2A; border-radius:20px")

        pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image.setPixmap(pixmap)
        image.setFixedSize(150,150)

        Title= QLabel()
        Title.setText(repo.name)

        layout.addWidget(image)
        layout.addWidget(Title)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.p.p.open_repo(self.repo)
    
    def languages_pie_chart(self,languages):
        labels = list(languages.keys())
        sizes = list(languages.values())

        fig, ax = plt.subplots(figsize=(2, 2), dpi=100)
        ax.pie(sizes, labels=labels, autopct='%1.0f%%')
        ax.axis('equal')

        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        plt.close(fig)
        buf.seek(0)
        return buf
    
