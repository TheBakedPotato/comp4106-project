#!/usr/bin/python3

from textui import TextUI
from checkersboard import CheckersBoard

ui = TextUI()
board = CheckersBoard(8)
textBoard = ui.drawBoard(board)

print(textBoard.draw())