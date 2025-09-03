from PySide6.QtWidgets import QApplication
from widget import Widget
import os
import sys

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")
    
app = QApplication(sys.argv)

with open(
    os.path.join(base_path, "styles", "diffnes.qss"),
    "r",
) as file:
    qss_content = file.read()

app.setStyleSheet(qss_content)

widget = Widget()
widget.show()

app.exec()