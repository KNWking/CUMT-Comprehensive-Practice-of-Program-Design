import sys
import os
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox,
                             QLabel, QPushButton, QWidget, QSpinBox, QFrame, QFileDialog, QComboBox, QSizePolicy,
                             QDialog)
from PyQt6.QtGui import QPixmap, QImage, QResizeEvent, QIcon
from PyQt6.QtCore import Qt, QRect, QSize, QTimer, QPoint
from qfluentwidgets import (FluentWindow, PushButton, ComboBox, FluentIcon,
                            PrimaryPushButton, setFont, FluentIcon, NavigationItemPosition,
                            MessageBox, MessageBoxBase, SubtitleLabel, TitleLabel, BodyLabel, CompactSpinBox)


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
        self.original_image_dialog = None
        self.challengeTime = 0
        self.EASY_TIME = 30
        self.MEDIUM_TIME = 90
        self.HARD_TIME = 360
        self.EASY_GRID_SIDE_NUMBER = 2
        self.MEDIUM_GRID_SIDE_NUMBER = 3
        self.HARD_GRID_SIDE_NUMBER = 4

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

        spinBoxLabel = BodyLabel("图片切割数量 (单位边):", self)
        self.gridSpinBox = CompactSpinBox()
        self.gridSpinBox.setRange(2, 10)
        self.gridSpinBox.setValue(self.gridSideNumber)
        self.gridSpinBox.valueChanged.connect(self.updateGridSize)

        self.gridLayout.addWidget(spinBoxLabel)
        self.gridLayout.addWidget(self.gridSpinBox)

        self.controlPanel.addLayout(self.gridLayout)

        self.viewOriginalButton = PushButton(FluentIcon.VIEW, "查看原图", self)
        self.viewOriginalButton.clicked.connect(self.viewOriginalImage)
        self.controlPanel.addWidget(self.viewOriginalButton)

        self.changeImageButton = PushButton(FluentIcon.PHOTO, "切换图片", self)
        self.changeImageButton.clicked.connect(self.changeImage)
        self.controlPanel.addWidget(self.changeImageButton)

        self.solvePuzzleButton = PushButton(FluentIcon.SYNC, "图片重排", self)
        self.solvePuzzleButton.clicked.connect(self.solvePuzzle)
        self.controlPanel.addWidget(self.solvePuzzleButton)

        self.randomImageButton = PushButton(FluentIcon.QUESTION, "随机图片", self)
        self.randomImageButton.clicked.connect(self.randomImage)
        self.controlPanel.addWidget(self.randomImageButton)

        self.controlPanel.addSpacing(40)  # 在难度选择之前添加间距

        # 创建一个水平布局来放置难度标签和选择框
        difficultyLayout = QHBoxLayout()

        self.difficultyLabel = BodyLabel("难度:")
        self.difficultyComboBox = ComboBox()
        self.difficultyComboBox.addItems(["容易", "中等", "困难"])
        self.difficultyComboBox.currentTextChanged.connect(self.setDifficulty)
        difficultyLayout.addWidget(self.difficultyLabel)
        difficultyLayout.addWidget(self.difficultyComboBox)
        self.controlPanel.addLayout(difficultyLayout)

        # 创建一个水平布局来放置挑战按钮
        challengeLayout = QHBoxLayout()
        self.challengeButton = PrimaryPushButton("开始挑战", self)
        self.challengeButton.clicked.connect(self.startChallenge)
        self.stopChallengeButton = PushButton("停止挑战")
        self.stopChallengeButton.clicked.connect(self.stopChallenge)
        self.stopChallengeButton.setEnabled(False)
        challengeLayout.addWidget(self.challengeButton)
        challengeLayout.addWidget(self.stopChallengeButton)
        self.controlPanel.addLayout(challengeLayout)

        self.timerLabel = BodyLabel("剩余时间: 0", self)
        self.controlPanel.addWidget(self.timerLabel)

        # 可以添加一些空白来调整其他控件的间距
        self.controlPanel.addStretch(1)

        mainLayout = QHBoxLayout(centralWidget)
        mainLayout.addWidget(self.puzzleContainer, 4)  # 拼图区域占4份
        mainLayout.addLayout(self.controlPanel, 1)  # 控制面板占1份

        self.loadImage('example_image.jpg')
        QTimer.singleShot(0, lambda: self.createPuzzle(self.gridSideNumber))

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
                piece.setMinimumSize(1, 1)

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
        # 如果原图框已经打开，关闭。
        if self.original_image_dialog is not None and self.original_image_dialog.isVisible():
            self.original_image_dialog.close()

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

        # 将 exec() 改为 show()
        dialog.show()

        # 保持对话框的引用，防止被垃圾回收
        self.original_image_dialog = dialog

    def shufflePuzzle(self):
        n = self.gridSideNumber
        puzzle = list(range(n * n))
        attempts = 0
        while True:
            attempts += 1
            random.shuffle(puzzle)
            inversions = self.countInversions(puzzle)
            blank_index = puzzle.index(0)
            blank_row = blank_index // n
            blank_col = blank_index % n

            # debug 用
            print(f"尝试 {attempts}:")
            print(f"拼图: {puzzle}")
            print(f"逆序数: {inversions}")
            print(f"空白方格位置: 行 {blank_row}, 列 {blank_col}")

            if n % 2 == 1:
                is_solvable = inversions % 2 == 0
            else:
                is_solvable = (inversions + blank_row) % 2 == 0

            print(f"是否可解: {is_solvable}")

            if is_solvable:
                break

            if attempts > 1000:
                print("超出最大尝试次数，尝试强制生成可解题目")
                if n % 2 == 1:
                    while inversions % 2 != 0:
                        random.shuffle(puzzle)
                        inversions = self.countInversions(puzzle)
                else:
                    while (inversions + blank_row) % 2 != 0:  # 这里也改成了 != 0
                        random.shuffle(puzzle)
                        inversions = self.countInversions(puzzle)
                        blank_index = puzzle.index(0)
                        blank_row = blank_index // n
                break

        print(f"最终拼图: {puzzle}")
        print(f"最终逆序数: {inversions}")
        print(f"最终空白块位置: row {blank_row}, col {blank_col}")
        self.updatePuzzleFromList(puzzle)

    def countInversions(self, puzzle):
        inversions = 0
        for i in range(len(puzzle) - 1):
            for j in range(i + 1, len(puzzle)):
                if puzzle[i] > puzzle[j] and puzzle[i] != 0 and puzzle[j] != 0:
                    inversions += 1
        return inversions

    def updatePuzzleFromList(self, puzzle):
        n = self.gridSideNumber
        for i in range(n * n):
            row, col = divmod(i, n)
            value = puzzle[i]
            original_row, original_col = divmod(value, n)  # 移到这里，对所有块都计算

            piece = self.puzzlePieces[row][col]
            if value == 0:
                self.emptyPosition = (row, col)
                piece.clear()
                piece.setStyleSheet("background-color: white;")
            else:
                x = original_col * (self.originalPixmap.width() // n)
                y = original_row * (self.originalPixmap.height() // n)
                piecePixmap = self.originalPixmap.copy(
                    QRect(x, y, self.originalPixmap.width() // n, self.originalPixmap.height() // n))
                piece.setPixmap(piecePixmap.scaled(piece.width(), piece.height(), Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation))

            self.puzzlePieces[row][col] = piece
            self.piecePositions[row][col] = (original_row, original_col)
            piece.row, piece.col = row, col
            self.puzzleLayout.addWidget(piece, row, col)

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
                    self.challengeButton.setEnabled(True)
                    self.stopChallengeButton.setEnabled(False)
                    QMessageBox.information(self, '恭喜', f'拼图完成! 用时: {self.challengeTime - self.timeLeft} 秒')
                else:
                    QMessageBox.information(self, '恭喜', '拼图完成!')

    def isAdjacent(self, row1, col1, row2, col2):
        if row1 == row2 and abs(col1 - col2) == 1:
            return True
        if col1 == col2 and abs(row1 - row2) == 1:
            return True
        return False

    def changeImage(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "选择图片", "",
                                                  "Images (*.png *.jpg *.bmp);;All Files (*)")
        if fileName:
            try:
                # 尝试加载新图片
                new_image = QImage(fileName)
                if new_image.isNull():
                    raise Exception("无法加载图片")

                # 如果成功加载，更新当前图片
                self.img = new_image
                self.originalPixmap = QPixmap.fromImage(self.img)

                # 重新创建拼图
                self.createPuzzle(self.gridSideNumber)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载图片时出错: {str(e)}")
        else:
            # 用户取消了选择，不做任何操作
            pass

    def solvePuzzle(self):
        self.createPuzzle(self.gridSideNumber)

    def isSolved(self):
        for row in range(self.gridSideNumber):
            for col in range(self.gridSideNumber):
                if self.piecePositions[row][col] != (row, col):
                    return False
        return True

    def setDifficulty(self):
        difficulty = self.difficultyComboBox.currentText()
        if difficulty == "容易":
            self.gridSideNumber = self.EASY_GRID_SIDE_NUMBER
        elif difficulty == "中等":
            self.gridSideNumber = self.MEDIUM_GRID_SIDE_NUMBER
        elif difficulty == "困难":
            self.gridSideNumber = self.HARD_GRID_SIDE_NUMBER
        else:
            # 如果难度不是预设的三个选项，就假设它是一个数字
            try:
                self.gridSideNumber = int(difficulty)
            except ValueError:
                # 如果转换失败，使用默认值
                self.gridSideNumber = 3

    def startChallenge(self):
        self.setDifficulty()
        self.gridSpinBox.setValue(self.gridSideNumber)
        self.createPuzzle(self.gridSideNumber)
        difficulty = self.difficultyComboBox.currentText()
        if difficulty == "容易":
            self.timeLeft = self.EASY_TIME
            self.challengeTime = self.EASY_TIME
        elif difficulty == "中等":
            self.timeLeft = self.MEDIUM_TIME
            self.challengeTime = self.MEDIUM_TIME
        elif difficulty == "困难":
            self.timeLeft = self.HARD_TIME
            self.challengeTime = self.HARD_TIME
        else:
            # 默认时间
            self.timeLeft = self.MEDIUM_TIME
            self.challengeTime = self.MEDIUM_TIME

        self.timer.start(1000)  # 每秒更新一次
        self.createPuzzle(self.gridSideNumber)
        self.challengeButton.setEnabled(False)
        self.stopChallengeButton.setEnabled(True)
        self.timerLabel.setText(f"时间: {self.timeLeft}")

    def stopChallenge(self):
        self.timer.stop()
        self.challengeButton.setEnabled(True)
        self.stopChallengeButton.setEnabled(False)
        self.timerLabel.setText("时间: 0")
        QMessageBox.information(self, '挑战结束', '挑战已停止')

    def updateTimer(self):
        self.timeLeft -= 1
        self.timerLabel.setText(f"时间: {self.timeLeft}")
        if self.timeLeft <= 0:
            self.timer.stop()
            self.challengeButton.setEnabled(True)
            self.stopChallengeButton.setEnabled(False)
            QMessageBox.information(self, '挑战失败', '时间到！')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PuzzleGame()
    ex.show()
    sys.exit(app.exec())
