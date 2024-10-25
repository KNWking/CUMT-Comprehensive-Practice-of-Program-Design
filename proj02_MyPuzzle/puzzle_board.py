from PyQt6.QtWidgets import QGridLayout, QWidget
from puzzle_piece import PuzzlePiece


class PuzzleBoard(QWidget):
    def __init__(self, image_pieces, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.pieces = []
        self.empty_index = rows * cols - 1

        layout = QGridLayout()
        for i, piece in enumerate(image_pieces):
            puzzle_piece = PuzzlePiece(piece, i)
            puzzle_piece.clicked.connect(self.try_move)
            self.pieces.append(puzzle_piece)
            layout.addWidget(puzzle_piece, i // cols, i % cols)

        self.setLayout(layout)

    def try_move(self, index):
        if self.is_adjacent(index, self.empty_index):
            self.swap_pieces(index, self.empty_index)
            self.empty_index = index

    def is_adjacent(self, index1, index2):
        row1, col1 = divmod(index1, self.cols)
        row2, col2 = divmod(index2, self.cols)
        return abs(row1 - row2) + abs(col1 - col2) == 1

    def swap_pieces(self, index1, index2):
        layout = self.layout()
        item1 = layout.itemAtPosition(index1 // self.cols, index1 % self.cols)
        item2 = layout.itemAtPosition(index2 // self.cols, index2 % self.cols)
        layout.removeItem(item1)
        layout.removeItem(item2)
        layout.addWidget(item1.widget(), index2 // self.cols, index2 % self.cols)
        layout.addWidget(item2.widget(), index1 // self.cols, index1 % self.cols)
