from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, pyqtSignal


class PuzzlePiece(QLabel):
    clicked = pyqtSignal(int)

    def __init__(self, pixmap, index):
        super().__init__()
        self.setPixmap(pixmap)
        self.index = index
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.index)
