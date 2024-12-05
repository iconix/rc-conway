import argparse
from copy import deepcopy
import os
import random
import sys
import time

# helpful: https://www.linuxdoc.org/HOWTO/Bash-Prompt-HOWTO-6.html
aging_ansi_codes = {
    1: '[32m',  # green
    2: '[33m',  # yellow
    3: '[34m',  # blue
    4: '[31m',  # red
}
reset_ansi_code = '[0m'

ansi_map = {0: reset_ansi_code}
ansi_map.update(aging_ansi_codes)
char_map = {0: ' ', 1: '*', 2: '*', 3: '*', 4: '*'}

num_rows = 50
num_cols = 100

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
  num_cols = len(board[0])  # assume cols are same for each row

  for i in range(row_i - 1, row_i + 2):
    for j in range(col_i - 1, col_i + 2):
      if row_i == i and col_i == j:
        continue
      if i < 0 or i > num_rows - 1:
        continue
      if j < 0 or j > num_cols - 1:
        continue
      live_neighbors += 1 if is_alive(board[i][j]) else 0

  return live_neighbors


def is_alive(cell):
  return cell > 0

def render_frame(board, user_input=False, delay=0):
  print_board(board)
  sys.stdout.flush()

  if user_input:
    input()
  else:
    time.sleep(delay)

  os.system('cls' if os.name == 'nt' else 'clear')

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

      if num_live_neighbors > 3 and is_alive(cell):
        # kill cell if overpopulated
        new_board[row_i][col_i] = 0
      elif num_live_neighbors < 2 and is_alive(cell):
        # kill cell if underpopulated
        new_board[row_i][col_i] = 0
      elif is_alive(cell):
        # cell lives on
        new_board[row_i][col_i] = min(cell + 1, 4)
      elif num_live_neighbors == 3 and not is_alive(cell):  # lol tyty! np i'm great at this lol <3
        # new cell is born!!
        new_board[row_i][col_i] = 1

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
  parser.add_argument('-d', '--delay', type=float, default=0.1, help='delay between frames in seconds')
  args = parser.parse_args()

  try:
    board = [[random.randint(0, 1) for _ in range(num_cols)] for _ in range(num_rows)]

    os.system('cls' if os.name == 'nt' else 'clear')
    render_frame(board, user_input=args.user_input, delay=args.delay)

    while True:
      board = run_iteration(board)
      render_frame(board, user_input=args.user_input, delay=args.delay)
  except KeyboardInterrupt:
    sys.exit(0)
