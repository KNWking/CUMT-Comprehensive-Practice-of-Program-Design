import random
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, Qt
from image_processor import ImageProcessor
from puzzle_board import PuzzleBoard


class GameController(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = "resources/images/img01.jpg"
        self.rows = 3
        self.cols = 3
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 控制按钮
        control_layout = QHBoxLayout()
        self.start_button = QPushButton("开始游戏")
        self.start_button.clicked.connect(self.start_game)
        control_layout.addWidget(self.start_button)

        self.view_original_button = QPushButton("查看原图")
        self.view_original_button.clicked.connect(self.toggle_original_image)
        control_layout.addWidget(self.view_original_button)

        main_layout.addLayout(control_layout)

        # 游戏板
        self.game_layout = QHBoxLayout()
        main_layout.addLayout(self.game_layout)

        # 原图显示
        self.original_image_label = QLabel()
        self.original_image_label.setFixedSize(200, 200)
        self.original_image_label.setScaledContents(True)
        self.original_image_label.hide()

        self.setLayout(main_layout)

    def start_game(self):
        image = ImageProcessor.resize_image(self.image_path, (300, 300))
        pieces = ImageProcessor.split_image(image, self.rows, self.cols)
        random.shuffle(pieces)

        if hasattr(self, 'puzzle_board'):
            self.game_layout.removeWidget(self.puzzle_board)
            self.puzzle_board.deleteLater()

        self.puzzle_board = PuzzleBoard([QPixmap.fromImage(piece) for piece in pieces], self.rows, self.cols)
        self.game_layout.addWidget(self.puzzle_board)

        # 设置原图
        self.original_image_label.setPixmap(QPixmap.fromImage(image))

    def toggle_original_image(self):
        if self.original_image_label.isHidden():
            self.original_image_label.show()
            self.game_layout.addWidget(self.original_image_label)
        else:
            self.original_image_label.hide()
            self.game_layout.removeWidget(self.original_image_label)
