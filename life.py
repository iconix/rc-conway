import argparse
from copy import deepcopy
from dataclasses import dataclass
import os
import random
import sys
import time
from typing import Dict, List

# ansi color codes for cell aging viz
# helpful: https://www.linuxdoc.org/HOWTO/Bash-Prompt-HOWTO-6.html
COLOR_CODES: Dict[int, str] = {
  1: '[32m',  # green - youngin'
  2: '[33m',  # yellow - adultin'
  3: '[34m',  # blue - maturin'
  4: '[31m',  # red - elder
}

RESET_CODE: str = '[0m'
CELL_CHAR: str = '*'
SPACE_CHAR: str = ' '

DEFAULT_ROWS: int = 50
DEFAULT_COLS: int = 100
DEFAULT_DELAY: float = 0.1

Game = List[List[int]]

@dataclass
class GameConfig:
  rows: int
  cols: int
  user_input: bool = False
  delay: float = DEFAULT_DELAY

def create_game(rows: int, cols: int, random_seed: int = None) -> Game:
  """Initialize random game."""
  if random_seed is not None:
    random.seed(random_seed)
  return [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]

def print_cell(cell: int) -> str:
  """Print an appropriately colored cell based on its age."""
  return str(f"\033{COLOR_CODES.get(cell, RESET_CODE)}{'*' if cell in COLOR_CODES else SPACE_CHAR}\033{RESET_CODE}")

def print_game(game: Game) -> str:
  """Print current state of the game."""
  for row in game:
    print(' '.join(map(print_cell, row)))

# for each iteration of game
#   if dead cell has 3 neighbors, it becomes alive
#   if a live cell has 1 or less neighbors, it dies
#   if a live cell has 4 or more neighbors, it dies
#   otherwise lives on without change (if live with 2 or 3 live neighbors)

def is_alive(cell: int) -> bool:
  """Check if cell is alive or dead."""
  return cell > 0

def check_live_neighbors(game: Game, row: int, col: int) -> int:
  """Count live neighbors for a cell."""
  num_rows, num_cols = len(game), len(game[0])

  live_neighbors = 0
  for i in range(-1, 2):
    for j in range(-1, 2):
      if i == 0 and j == 0:
        continue

      # wrap around game boundaries
      neighbor_row = (row + i) % num_rows
      neighbor_col = (col + j) % num_cols
      live_neighbors += 1 if is_alive(game[neighbor_row][neighbor_col]) else 0

  return live_neighbors

def update_cell(cell: int, num_live_neighbors: int) -> int:
  """Determine new cell state based on Conway's rules."""
  if is_alive(cell):
    if num_live_neighbors > 3:
      # cell dies - overpopulated
      return 0
    elif num_live_neighbors < 2:
      # cell dies - underpopulated
      return 0
    else:
      # cell lives on
      return min(cell + 1, 4)

  if num_live_neighbors == 3:  # lol tyty! np i'm great at this lol <3
    # new cell is born!!
    return 1

  # cell stays dead ok
  return 0

def next_generation(game: Game) -> Game:
  """Calculate the next generation of the game."""
  # i think we need a new board since iterating over old board
  # yesss
  new_game = deepcopy(game)
  num_rows, num_cols = len(game), len(game[0])

  for row in range(num_rows):
    for col in range(num_cols):
      # check if cell is alive
      # check num neighbors
      # modify state of cell if needed
      num_live_neighbors = check_live_neighbors(game, row, col)
      new_game[row][col] = update_cell(game[row][col], num_live_neighbors)

  # omg at this demo lol
  # have you seen that sad titanic flute meme
  # nope looking up now lol
  return new_game

def render_frame(game: Game, config: GameConfig):
  """Render a single frame of the game."""
  print_game(game)
  sys.stdout.flush()

  if config.user_input:
    input()
  else:
    time.sleep(config.delay)

  os.system('cls' if os.name == 'nt' else 'clear')

def parse_arguments() -> GameConfig:
  """Parse command line arguments."""
  parser = argparse.ArgumentParser(description="conway's game of life with aging cells")
  parser.add_argument('-r', '--rows', type=int, default=DEFAULT_ROWS,
                    help='number of rows in the grid')
  parser.add_argument('-c', '--cols', type=int, default=DEFAULT_COLS,
                    help='number of columns in the grid')
  parser.add_argument('-u', '--user-input', action='store_true',
                    help='prompt for user input before next generation')
  parser.add_argument('-d', '--delay', type=float, default=DEFAULT_DELAY,
                    help='delay between generations in seconds')
  parser.add_argument('-s', '--seed', type=int,
                    help='random seed for game initialization')

  args = parser.parse_args()
  return GameConfig(args.rows, args.cols, args.user_input, args.delay)

def main():
  """Main game loop."""
  config = parse_arguments()

  try:
    game = create_game(config.rows, config.cols)
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
      render_frame(game, config)
      game = next_generation(game)
  except KeyboardInterrupt:
    sys.exit(0)

# do you want to jump back on and finish? i feeel like we're pretty close maybeee
# ya let's do it! i guess we grab a virtual room..?
# https://us06web.zoom.us/j/[redacted]
# I'm in pairing room 2! ty! messaged you on zulip!!

if __name__ == '__main__':
  main()
