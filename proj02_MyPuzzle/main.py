import sys
import os
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox,
                             QLabel, QPushButton, QWidget, QSpinBox, QFrame, QFileDialog, QComboBox, QSizePolicy,
                             QDialog)
from PyQt6.QtGui import QPixmap, QImage, QResizeEvent
from PyQt6.QtCore import Qt, QRect, QSize, QTimer, QPoint


# 查看原图的对话框
class ViewOriginalDialog(QDialog):
    def __init__(self, parent=None, pixmap=None):
        super().__init__(parent)
        self.setWindowTitle("原图")
        self.originalPixmap = pixmap
        self.aspectRatio = pixmap.width() / pixmap.height()

        # 设置初始大小
        initial_width = 300
        initial_height = int(initial_width / self.aspectRatio)
        self.resize(initial_width, initial_height)

        layout = QVBoxLayout(self)
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.imageLabel)

        self.setLayout(layout)
        self.updateImage()

    def resizeEvent(self, event: QResizeEvent):
        # 保持宽高比
        new_size = event.size()
        new_width = new_size.width()
        new_height = int(new_width / self.aspectRatio)
        self.resize(new_width, new_height)
        self.updateImage()

    def updateImage(self):
        if self.originalPixmap:
            scaled_pixmap = self.originalPixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.imageLabel.setPixmap(scaled_pixmap)

    def sizeHint(self):
        return QSize(600, int(600 / self.aspectRatio))


class PuzzlePiece(QLabel):
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col


class PuzzleGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.imageList = self.loadImageList('./images')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)
        self.timeLeft = 0

    def initUI(self):
        self.setWindowTitle('myPuzzle')
        self.resize(800, 600)  # 设置初始大小，但允许调整

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.gridSideNumber = 3  # 默认 3x3 拼图

        self.puzzleContainer = QFrame(centralWidget)
        self.puzzleContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.puzzleLayout = QGridLayout(self.puzzleContainer)
        self.puzzleLayout.setSpacing(0)
        self.puzzleContainer.setLayout(self.puzzleLayout)

        self.controlPanel = QVBoxLayout()
        self.controlPanel.setSpacing(10)
        self.gridLayout = QHBoxLayout()

        spinBoxLabel = QLabel("图片切割数量 (单位边):")
        self.gridSpinBox = QSpinBox()
        self.gridSpinBox.setMinimum(2)
        self.gridSpinBox.setMaximum(10)
        self.gridSpinBox.setValue(self.gridSideNumber)
        self.gridSpinBox.valueChanged.connect(self.updateGridSize)

        self.gridLayout.addWidget(spinBoxLabel)
        self.gridLayout.addWidget(self.gridSpinBox)

        self.controlPanel.addLayout(self.gridLayout)

        self.viewOriginalButton = QPushButton("查看原图")
        self.viewOriginalButton.clicked.connect(self.viewOriginalImage)

        self.shuffleButton = QPushButton("试玩新图")
        self.shuffleButton.clicked.connect(self.shufflePuzzle)

        self.changeImageButton = QPushButton("切换图片")
        self.changeImageButton.clicked.connect(self.changeImage)

        self.solvePuzzleButton = QPushButton("图片重排")
        self.solvePuzzleButton.clicked.connect(self.solvePuzzle)

        self.randomImageButton = QPushButton("随机图片")
        self.randomImageButton.clicked.connect(self.randomImage)

        self.difficultyLabel = QLabel("难度:")
        self.difficultyComboBox = QComboBox()
        self.difficultyComboBox.addItems(["容易", "中等", "困难"])
        self.difficultyComboBox.currentTextChanged.connect(self.setDifficulty)

        self.challengeButton = QPushButton("开始挑战")
        self.challengeButton.clicked.connect(self.startChallenge)

        self.timerLabel = QLabel("时间: 0", self)

        self.controlPanel.addWidget(self.viewOriginalButton)
        self.controlPanel.addWidget(self.shuffleButton)
        self.controlPanel.addWidget(self.changeImageButton)
        self.controlPanel.addWidget(self.solvePuzzleButton)
        self.controlPanel.addWidget(self.randomImageButton)
        self.controlPanel.addWidget(self.difficultyLabel)
        self.controlPanel.addWidget(self.difficultyComboBox)
        self.controlPanel.addWidget(self.challengeButton)
        self.controlPanel.addWidget(self.timerLabel)

        mainLayout = QHBoxLayout(centralWidget)
        mainLayout.addWidget(self.puzzleContainer, 4)  # 拼图区域占4份
        mainLayout.addLayout(self.controlPanel, 1)  # 控制面板占1份

        self.loadImage('example_image.jpg')
        self.createPuzzle(self.gridSideNumber)

    def loadImageList(self, folder):
        return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.bmp'))]

    def randomImage(self):
        if self.imageList:
            randomImagePath = random.choice(self.imageList)
            self.loadImage(randomImagePath)
            self.createPuzzle(self.gridSideNumber)

    def loadImage(self, imagePath):
        self.img = QImage(imagePath)
        self.originalPixmap = QPixmap.fromImage(self.img)
        self.puzzlePieces = []
        self.piecePositions = []
        self.emptyPosition = (self.gridSideNumber - 1, self.gridSideNumber - 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updatePuzzleSize()

    def updatePuzzleSize(self):
        if hasattr(self, 'originalPixmap'):
            self.createPuzzle(self.gridSideNumber)

    def createPuzzle(self, gridSize):
        self.gridSideNumber = gridSize
        self.puzzleLayout.setSpacing(0)
        self.clearLayout(self.puzzleLayout)

        # 计算每个拼图块的大小
        pieceWidth = self.puzzleContainer.width() // self.gridSideNumber
        pieceHeight = self.puzzleContainer.height() // self.gridSideNumber

        # 初始化拼图块和位置数组
        self.puzzlePieces = [[None for _ in range(gridSize)] for _ in range(gridSize)]
        self.piecePositions = [[None for _ in range(gridSize)] for _ in range(gridSize)]

        # 设置空白位置为右下角
        self.emptyPosition = (gridSize - 1, gridSize - 1)

        for row in range(gridSize):
            for col in range(gridSize):
                piece = PuzzlePiece(row, col)
                piece.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                piece.setMinimumSize(1, 1)  # 允许缩小到最小1x1像素

                if (row, col) != self.emptyPosition:
                    # 计算原图中对应的区域
                    x = col * (self.originalPixmap.width() // gridSize)
                    y = row * (self.originalPixmap.height() // gridSize)
                    piecePixmap = self.originalPixmap.copy(
                        QRect(x, y, self.originalPixmap.width() // gridSize, self.originalPixmap.height() // gridSize))
                    piece.setPixmap(piecePixmap.scaled(pieceWidth, pieceHeight, Qt.AspectRatioMode.KeepAspectRatio,
                                                       Qt.TransformationMode.SmoothTransformation))
                else:
                    piece.setStyleSheet("background-color: white;")

                piece.setScaledContents(True)
                piece.mousePressEvent = lambda event, p=piece: self.movePiece(p.row, p.col)

                self.puzzleLayout.addWidget(piece, row, col)
                self.puzzlePieces[row][col] = piece
                self.piecePositions[row][col] = (row, col)

        # 打乱拼图
        self.shufflePuzzle()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def updateGridSize(self):
        newSize = self.gridSpinBox.value()
        self.createPuzzle(newSize)

    def viewOriginalImage(self):
        dialog = ViewOriginalDialog(self, self.originalPixmap)
        dialog.setMinimumSize(100, int(100 / dialog.aspectRatio))

        # 计算对话框应该显示的位置
        main_window_center = self.geometry().center()
        dialog_size = dialog.size()
        dialog_position = QPoint(
            main_window_center.x() - dialog_size.width() // 2,
            main_window_center.y() - dialog_size.height() // 2
        )
        dialog.move(dialog_position)

        dialog.exec()

    def shufflePuzzle(self):
        # 创建所有位置的列表，除了空白位置
        positions = [(r, c) for r in range(self.gridSideNumber) for c in range(self.gridSideNumber) if
                     (r, c) != self.emptyPosition]

        # 随机打乱非空白位置
        random.shuffle(positions)

        # 将空白位置添加到列表末尾
        positions.append(self.emptyPosition)

        # 创建一个新的puzzlePieces数组来存储重新排列后的拼图块
        new_puzzlePieces = [[None for _ in range(self.gridSideNumber)] for _ in range(self.gridSideNumber)]

        for new_pos, old_pos in enumerate(positions):
            new_row, new_col = divmod(new_pos, self.gridSideNumber)
            old_row, old_col = old_pos

            piece = self.puzzlePieces[old_row][old_col]
            new_puzzlePieces[new_row][new_col] = piece

            if piece is not None:
                piece.row, piece.col = new_row, new_col
                self.puzzleLayout.addWidget(piece, new_row, new_col)

            self.piecePositions[new_row][new_col] = old_pos

            if old_pos == self.emptyPosition:
                self.emptyPosition = (new_row, new_col)

        # 更新puzzlePieces
        self.puzzlePieces = new_puzzlePieces

    def movePiece(self, row, col):
        emptyRow, emptyCol = self.emptyPosition
        if self.isAdjacent(row, col, emptyRow, emptyCol):
            # 交换拼图块
            pieceA = self.puzzlePieces[row][col]
            pieceB = self.puzzlePieces[emptyRow][emptyCol]
            self.puzzlePieces[row][col], self.puzzlePieces[emptyRow][emptyCol] = pieceB, pieceA

            # 更新布局
            self.puzzleLayout.addWidget(pieceA, emptyRow, emptyCol)
            self.puzzleLayout.addWidget(pieceB, row, col)

            # 更新位置信息
            pieceA.row, pieceA.col = emptyRow, emptyCol
            pieceB.row, pieceB.col = row, col

            # 更新 piecePositions
            self.piecePositions[row][col], self.piecePositions[emptyRow][emptyCol] = \
                self.piecePositions[emptyRow][emptyCol], self.piecePositions[row][col]

            # 更新空白位置
            self.emptyPosition = (row, col)

            # 检查是否完成拼图
            if self.isSolved():
                if self.timer.isActive():
                    self.timer.stop()
                    QMessageBox.information(self, '恭喜', f'拼图完成! 用时: {60 - self.timeLeft} 秒')
                    self.challengeButton.setEnabled(True)
                else:
                    QMessageBox.information(self, '恭喜', '拼图完成!')

    def isAdjacent(self, row1, col1, row2, col2):
        if row1 == row2 and abs(col1 - col2) == 1:
            return True
        if col1 == col2 and abs(row1 - row2) == 1:
            return True
        return False

    def changeImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择图片", "",
                                                  "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if fileName:
            self.loadImage(fileName)
            self.createPuzzle(self.gridSideNumber)

    def solvePuzzle(self):
        self.createPuzzle(self.gridSideNumber)

    def isSolved(self):
        for row in range(self.gridSideNumber):
            for col in range(self.gridSideNumber):
                if self.piecePositions[row][col] != (row, col):
                    return False
        return True

    def setDifficulty(self, difficulty):
        if difficulty == "容易":
            self.gridSideNumber = 3
        elif difficulty == "中等":
            self.gridSideNumber = 4
        elif difficulty == "困难":
            self.gridSideNumber = 5
        else:
            self.gridSideNumber = int(difficulty)

        self.gridSpinBox.setValue(self.gridSideNumber)
        self.createPuzzle(self.gridSideNumber)

    def startChallenge(self):
        self.timeLeft = 60  # 设置挑战时间（秒）
        self.timer.start(1000)  # 每秒更新一次
        self.shufflePuzzle()
        self.challengeButton.setEnabled(False)

    def updateTimer(self):
        self.timeLeft -= 1
        self.timerLabel.setText(f"时间: {self.timeLeft}")
        if self.timeLeft <= 0:
            self.timer.stop()
            QMessageBox.information(self, '挑战失败', '时间到！')
            self.challengeButton.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PuzzleGame()
    ex.show()
    sys.exit(app.exec())
