import argparse
from copy import deepcopy
import os
import random
import sys
import time

# helpful: https://www.linuxdoc.org/HOWTO/Bash-Prompt-HOWTO-6.html
green_ansi_code = '[32m'
reset_ansi_code = '[0m'

ansi_map = {0: reset_ansi_code, 1: green_ansi_code}
char_map = {0: ' ', 1: '*'}

num_rows = 50
num_cols = 50
board = [[random.randint(0, 1) for _ in range(num_cols)] for _ in range(num_rows)]

def print_board(board):
  for row in board:
    print(' '.join(map(lambda x: str(f"\033{ansi_map[x]}{char_map[x]}\033{reset_ansi_code}"), row)))


# for each iteration of game
#   if dead cell has 3 neighbors, it becomes alive
#   if a live cell has 1 or less neighbors, it dies
#   if a live cell has 4 or more neighbors, it dies
#   otherwise lives on without change (if live with 2 or 3 live neighbors)

def check_neighbors(board, row_i, col_i):
  # 1, 0
  live_neighbors = 0

  num_rows = len(board)
  num_cols = len(board[1])  # assume cols are same for each row

  for i in range(row_i - 1, row_i + 2): # 0,1,2
    for j in range(col_i - 1, col_i + 2): # -1,0,1
      if row_i == i and col_i == j:
        continue
      if i < 0 or i > num_rows - 1:
        continue
      if j < 0 or j > num_cols - 1:
        continue
      live_neighbors += is_alive(board[i][j])

  return live_neighbors


def is_alive(cell):
  return cell == 1


def run_iteration(board):
  # i think we need a new board since iterating over old board
  # yesss
  new_board = deepcopy(board)

  for row_i, row in enumerate(board):
    for col_i, cell in enumerate(row):
      # check if cell is alive
      # check num neighbors
      # modify state of cell if needed
      num_live_neighbors = check_neighbors(board, row_i, col_i)

      # print("hihi", row_i, col_i, num_live_neighbors)

      if num_live_neighbors > 3 and is_alive(cell):
        # if overpopulated and cell is live, kill cell
        new_board[row_i][col_i] = 0

      if num_live_neighbors < 2 and is_alive(cell):
        # underpopulated and cell is alive, kill cell
        new_board[row_i][col_i] = 0

      if num_live_neighbors == 3 and not is_alive(cell):  # lol tyty! np i'm great at this lol <3
        # dead cell comes back!!
        new_board[row_i][col_i] = 1

      # else:
        # print("hehe", new_board[row_i][col_i])

    # omg at this demo lol
    # have you seen that sad titanic flute meme
    # nope looking up now lol
  return new_board


# do you want to jump back on and finish? i feeel like we're pretty close maybeee
# ya let's do it! i guess we grab a virtual room..?
# https://us06web.zoom.us/j/[redacted]
# I'm in pairing room 2! ty! messaged you on zulip!!

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='conway\'s game of life')
  parser.add_argument('-u', '--user-input', action='store_true', help='prompt for user input before next iteration')
  args = parser.parse_args()

  try:
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
      board = run_iteration(board)
      print_board(board)
      sys.stdout.flush()

      if args.user_input:
        input()
      else:
        time.sleep(1)

      os.system('cls' if os.name == 'nt' else 'clear')
  except KeyboardInterrupt:
    sys.exit(0)
