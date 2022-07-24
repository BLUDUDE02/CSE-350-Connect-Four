import numpy as np
import sqlite3

con = sqlite3.connect("savelog.db")
con.execute("DROP TABLE IF EXISTS game")
con.execute("""CREATE TABLE game(
                 turn INTEGER NOT NULL UNIQUE,
                 player INTEGER NOT NULL,
                 row INTEGER NOT NULL,
                 col INTEGER NOT NULL,
                 board TEXT NOT NULL
                 )
                 """)
con.row_factory = sqlite3.Row

def record_move(board, turn, player, row, column, con):
    try:
        with con:
            con.execute("""INSERT INTO
                        game(turn, player, row, col, board) VALUES (?,?,?,?,?)""",
                        (turn, player, row, column, board))
                        
    except sqlite3.IntegrityError as e:
        print(e)
        print("could not record turn", turn)
        
    return