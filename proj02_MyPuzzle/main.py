import sys
import os
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox,
                             QLabel, QPushButton, QWidget, QSpinBox, QFrame, QFileDialog, QComboBox, QScrollArea)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QRect, QSize, QTimer


class PuzzleGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.imageList = self.loadImageList('./images')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)
        self.timeLeft = 0

    def initUI(self):
        self.setWindowTitle('My Puzzle')
        self.setFixedSize(800, 600)  # 固定主窗口大小

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.gridSideNumber = 3  # 默认 3x3 拼图

        # 使用 QScrollArea 来容纳拼图
        self.scrollArea = QScrollArea(centralWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedSize(600, 600)  # 固定滚动区域大小

        self.puzzleContainer = QFrame()
        self.puzzleContainer.setFixedSize(580, 580)  # 固定拼图容器大小
        self.puzzleLayout = QGridLayout(self.puzzleContainer)
        self.puzzleLayout.setSpacing(0)
        self.puzzleContainer.setLayout(self.puzzleLayout)

        self.controlPanel = QVBoxLayout()
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
        mainLayout.addWidget(self.puzzleContainer)
        mainLayout.addLayout(self.controlPanel)

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
        self.originalPixmap = QPixmap.fromImage(self.img).scaled(
            self.puzzleContainer.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.puzzlePieces = []
        self.piecePositions = []
        self.emptyPosition = (self.gridSideNumber - 1, self.gridSideNumber - 1)  # 初始空白块位置

    def createPuzzle(self, gridSize):
        self.gridSideNumber = gridSize
        self.puzzleLayout.setSpacing(0)
        self.clearLayout(self.puzzleLayout)
        pieceWidth = self.puzzleContainer.width() // self.gridSideNumber
        pieceHeight = self.puzzleContainer.height() // self.gridSideNumber
        self.puzzlePieces = []
        self.piecePositions = []
        self.emptyPosition = (gridSize - 1, gridSize - 1)

        for row in range(gridSize):
            rowItems = []
            for col in range(gridSize):
                piece = QLabel(self.puzzleContainer)
                piece.setFixedSize(pieceWidth, pieceHeight)
                if not (row == gridSize - 1 and col == gridSize - 1):  # Skip bottom-right corner
                    x = col * pieceWidth
                    y = row * pieceHeight
                    piece.setPixmap(self.originalPixmap.copy(QRect(x, y, pieceWidth, pieceHeight)))
                else:
                    piece.setStyleSheet("background-color: white;")
                piece.setScaledContents(True)
                # 将鼠标事件传递给 movePiece 方法并附上块的位置
                piece.mousePressEvent = self.createMousePressEvent(row, col)
                self.puzzleLayout.addWidget(piece, row, col)
                rowItems.append(piece)
                self.piecePositions.append((row, col))
            self.puzzlePieces.append(rowItems)

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
        if not hasattr(self, 'originalImageLabel'):
            self.originalImageLabel = QLabel(self)
            self.originalImageLabel.setFixedSize(200, 200)
            self.originalImageLabel.move(10, self.height() - 210)
            self.originalImageLabel.setScaledContents(True)

        self.originalImageLabel.setPixmap(self.originalPixmap)
        self.originalImageLabel.show()

    def shufflePuzzle(self):
        positions = self.piecePositions[:-1]
        random.shuffle(positions)  # 随机打乱拼图块
        positions.append(self.emptyPosition)

        for idx, position in enumerate(positions):
            row, col = divmod(idx, self.gridSideNumber)
            piece = self.puzzlePieces[position[0]][position[1]]
            self.puzzleLayout.addWidget(piece, row, col)

        self.piecePositions = positions

    def createMousePressEvent(self, row, col):
        print("click", row, col)
        return lambda event: self.movePiece(row, col)

    def movePiece(self, row, col):
        emptyRow, emptyCol = self.emptyPosition
        if (row == emptyRow and abs(col - emptyCol) == 1) or (col == emptyCol and abs(row - emptyRow) == 1):
            emptyPiece = self.puzzlePieces[emptyRow][emptyCol]
            piece = self.puzzlePieces[row][col]
            self.puzzleLayout.addWidget(piece, emptyRow, emptyCol)
            self.puzzleLayout.addWidget(emptyPiece, row, col)
            self.piecePositions[self.piecePositions.index((row, col))] = (emptyRow, emptyCol)
            self.piecePositions[-1] = (row, col)
            self.emptyPosition = (row, col)

            if self.isSolved():
                if self.timer.isActive():
                    self.timer.stop()
                    QMessageBox.information(self, '恭喜', f'拼图完成! 用时: {60 - self.timeLeft} 秒')
                    self.challengeButton.setEnabled(True)
                else:
                    QMessageBox.information(self, '恭喜', '拼图完成!')

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
        for i, pos in enumerate(self.piecePositions):
            expected_pos = divmod(i, self.gridSideNumber)
            if pos != expected_pos:
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
