from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QRect


class ImageProcessor:
    @staticmethod
    def resize_image(image_path, target_size):
        image = QImage(image_path)
        return image.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

    @staticmethod
    def split_image(image, rows, cols):
        pieces = []
        w, h = image.width() // cols, image.height() // rows
        for i in range(rows):
            for j in range(cols):
                piece = image.copy(QRect(j * w, i * h, w, h))
                pieces.append(piece)
        return pieces
