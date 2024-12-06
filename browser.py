import asyncio
from js import document
from pyodide.ffi import create_proxy

from life import CELL_CHAR, COLOR_CODES, SPACE_CHAR, create_game, next_generation

class BrowserRunner:
    def __init__(self):
        self.running = False
        self.step_mode = False
        self.current_game = None

    def toggle_game(self, *args):
        """Toggle the game's running state between playing and paused."""
        if self.step_mode:
            if self.current_game is None:
                self.reset_game()
            return

        self.running = not self.running
        if self.current_game is None:
            self.reset_game()

    def toggle_step_mode(self, *args):
        """Toggle step-by-step mode and update UI."""
        self.step_mode = document.getElementById('user-input').checked
        next_step_btn = document.getElementById('next-step-btn')

        if self.step_mode:
            next_step_btn.classList.add('visible')
            self.running = False  # pause the game when entering step mode
        else:
            next_step_btn.classList.remove('visible')

    def next_step(self, *args):
        """Advance the game by one generation."""
        if self.current_game is not None and not self.running:
            self.current_game = next_generation(self.current_game)
            self.render_frame(self.current_game)

    def reset_game(self, *args):
        """Reset the game with current configuration."""
        rows = int(document.getElementById('rows').value)
        cols = int(document.getElementById('cols').value)
        self.current_game = create_game(rows, cols)
        self.render_frame(self.current_game)

    def render_frame(self, game):
        """Render the current frame to the HTML container."""
        output = []
        for row in game:
            row_chars = []
            for cell in row:
                char = CELL_CHAR if cell in COLOR_CODES else SPACE_CHAR
                cell_class = f'cell-{cell}'
                row_chars.append(f'<span class="{cell_class}">{char}</span>')
            output.append(''.join(row_chars))

        game_container = document.getElementById('game-container')
        game_container.innerHTML = '<br>'.join(output)

    async def game_loop(self):
        """Main game loop that updates and renders the board state."""
        while True:
            delay = int(document.getElementById('delay').value) / 1000  # convert to seconds
            if self.running and self.current_game is not None and not self.step_mode:
                self.current_game = next_generation(self.current_game)
                self.render_frame(self.current_game)
                await asyncio.sleep(delay)
            else:
                await asyncio.sleep(delay)

    def start(self):
        """Initialize and start the game."""
        # hide loading indicator and show game ui when python is ready
        loading_div = document.getElementById('loading')
        game_ui = document.getElementById('game-ui')
        loading_div.style.display = 'none'
        game_ui.style.display = 'block'

        # start the game loop
        asyncio.ensure_future(self.game_loop())

def setup_events():
    """Set up event listeners for all game control buttons and inputs."""
    start_btn = document.getElementById('start-btn')
    next_btn = document.getElementById('next-step-btn')
    reset_btn = document.getElementById('reset-btn')
    step_mode = document.getElementById('user-input')

    start_btn.addEventListener('click', create_proxy(runner.toggle_game))
    next_btn.addEventListener('click', create_proxy(runner.next_step))
    reset_btn.addEventListener('click', create_proxy(runner.reset_game))
    step_mode.addEventListener('change', create_proxy(runner.toggle_step_mode))


# start the game and set up events
runner = BrowserRunner()
runner.start()
setup_events()
