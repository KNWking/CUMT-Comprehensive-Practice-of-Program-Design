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
    # 略


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
        # 略

    def randomImage(self):
        # 略

    def loadImage(self, imagePath):
        # 略

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
        pieceWidth = self.puzzleContainer.width() // self.gridSideNumber
        pieceHeight = self.puzzleContainer.height() // self.gridSideNumber
        self.puzzlePieces = [[None for _ in range(gridSize)] for _ in range(gridSize)]
        self.piecePositions = []
        self.emptyPosition = (gridSize - 1, gridSize - 1)

        for row in range(gridSize):
            for col in range(gridSize):
                piece = QLabel()
                piece.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                piece.setMinimumSize(1, 1)  # 允许缩小到最小1x1像素
                if not (row == gridSize - 1 and col == gridSize - 1):  # Skip bottom-right corner
                    x = col * (self.originalPixmap.width() // gridSize)
                    y = row * (self.originalPixmap.height() // gridSize)
                    piecePixmap = self.originalPixmap.copy(
                        QRect(x, y, self.originalPixmap.width() // gridSize, self.originalPixmap.height() // gridSize))
                    piece.setPixmap(piecePixmap.scaled(pieceWidth, pieceHeight, Qt.AspectRatioMode.KeepAspectRatio,
                                                       Qt.TransformationMode.SmoothTransformation))
                else:
                    piece.setStyleSheet("background-color: white;")
                piece.setScaledContents(True)
                piece.mousePressEvent = lambda event, r=row, c=col: self.movePiece(r, c)
                self.puzzleLayout.addWidget(piece, row, col)
                self.puzzlePieces[row][col] = piece
                self.piecePositions.append((row, col))

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
        # 略

    def shufflePuzzle(self):
        positions = [(r, c) for r in range(self.gridSideNumber) for c in range(self.gridSideNumber)]
        positions.remove(self.emptyPosition)
        random.shuffle(positions)  # 随机打乱拼图块
        positions.append(self.emptyPosition)

        for idx, (row, col) in enumerate(positions):
            newRow, newCol = divmod(idx, self.gridSideNumber)
            piece = self.puzzlePieces[row][col]
            self.puzzleLayout.addWidget(piece, newRow, newCol)
            if (row, col) == self.emptyPosition:
                self.emptyPosition = (newRow, newCol)

        self.piecePositions = positions

    def movePiece(self, row, col):
        emptyRow, emptyCol = self.emptyPosition
        if self.isAdjacent(row, col, emptyRow, emptyCol):
            # 交换拼图块
            self.puzzlePieces[row][col], self.puzzlePieces[emptyRow][emptyCol] \
                = self.puzzlePieces[emptyRow][emptyCol], self.puzzlePieces[row][col]

            # 更新布局
            self.puzzleLayout.addWidget(self.puzzlePieces[emptyRow][emptyCol], emptyRow, emptyCol)
            self.puzzleLayout.addWidget(self.puzzlePieces[row][col], row, col)

            # 更新位置信息
            clickedPieceIndex = self.piecePositions.index((row, col))
            self.piecePositions[clickedPieceIndex] = (emptyRow, emptyCol)
            self.piecePositions[-1] = (row, col)
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
        # 检查行列差的绝对值
        row_diff = abs(row1 - row2)
        col_diff = abs(col1 - col2)
        # 如果行列差的绝对值都不超过1，则表示元素相邻
        return row_diff <= 1 and col_diff <= 1 and (row_diff != 0 or col_diff != 0)

    def changeImage(self):
        # 略

    def solvePuzzle(self):
        self.createPuzzle(self.gridSideNumber)

    def isSolved(self):
        for i, pos in enumerate(self.piecePositions):
            expected_pos = divmod(i, self.gridSideNumber)
            if pos != expected_pos:
                return False
        return True

    def setDifficulty(self, difficulty):
        # 略

    def startChallenge(self):
        # 略

    def updateTimer(self):
        # 略


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PuzzleGame()
    ex.show()
    sys.exit(app.exec())
