import sys
from PyQt6.QtWidgets import QApplication
from game_controller import GameController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = GameController()
    game.show()
    sys.exit(app.exec())
