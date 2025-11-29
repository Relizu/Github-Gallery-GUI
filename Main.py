from PySide6.QtWidgets import QApplication
from package.mainwindow import mainWindow
import sys

app = QApplication(sys.argv)
window = mainWindow()

window.show()
sys.exit(app.exec())