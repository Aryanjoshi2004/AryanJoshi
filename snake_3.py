import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Snake Game")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        
        # Game settings
        self.cell_size = 20
        self.width = 30
        self.height = 20
        self.speed = 100  # milliseconds between moves
        self.difficulty = "Normal"
        
        # Game state
        self.direction = "Right"
        self.next_direction = "Right"
        self.snake = [(15, 10), (14, 10), (13, 10)]
        self.food = None
        self.special_food = None
        self.score = 0
        self.high_score = 0
        self.game_running = False
        self.paused = False
        
        # Colors
        self.colors = {
            "background": "#1a1a1a",
            "snake": "#00ff00",
            "snake_head": "#00cc00",
            "food": "#ff0000",
            "special_food": "#ffd700",
            "grid": "#2d2d2d"
        }
        
        self.create_widgets()
        self.create_bindings()
        
    def create_widgets(self):
        # Create main container
        self.container = ttk.Frame(self.window)
        self.container.pack(expand=True, fill="both")
        
        # Create left panel for controls
        self.left_panel = ttk.Frame(self.container, padding="10")
        self.left_panel.pack(side="left", fill="y")
        
        # Create game canvas
        self.canvas = tk.Canvas(
            self.container,
            width=self.width * self.cell_size,
            height=self.height * self.cell_size,
            bg=self.colors["background"],
            highlightthickness=0
        )
        self.canvas.pack(side="right", padx=10, pady=10)
        
        # Score display
        self.score_var = tk.StringVar(value="Score: 0")
        self.high_score_var = tk.StringVar(value="High Score: 0")
        
        ttk.Label(self.left_panel, textvariable=self.score_var, font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(self.left_panel, textvariable=self.high_score_var, font=("Arial", 12)).pack(pady=5)
        
        # Difficulty selector
        ttk.Label(self.left_panel, text="Difficulty:").pack(pady=5)
        self.difficulty_var = tk.StringVar(value="Normal")
        difficulty_menu = ttk.OptionMenu(
            self.left_panel,
            self.difficulty_var,
            "Normal",
            "Easy",
            "Normal",
            "Hard",
            command=self.change_difficulty
        )
        difficulty_menu.pack(pady=5)
        
        # Control buttons
        ttk.Button(self.left_panel, text="New Game", command=self.new_game).pack(pady=10, fill="x")
        self.pause_button = ttk.Button(self.left_panel, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(pady=5, fill="x")
        ttk.Button(self.left_panel, text="Quit", command=self.window.quit).pack(pady=10, fill="x")
        
        # Controls help
        controls_frame = ttk.LabelFrame(self.left_panel, text="Controls", padding="10")
        controls_frame.pack(pady=20, fill="x")
        
        controls_text = """
        Arrow Keys: Move Snake
        P: Pause/Resume
        Space: Quick Start
        Esc: Quit Game
        """
        ttk.Label(controls_frame, text=controls_text).pack()
        
        # Draw initial grid
        self.draw_grid()
        
    def create_bindings(self):
        # Keyboard bindings
        self.window.bind("<Up>", lambda e: self.change_direction("Up"))
        self.window.bind("<Down>", lambda e: self.change_direction("Down"))
        self.window.bind("<Left>", lambda e: self.change_direction("Left"))
        self.window.bind("<Right>", lambda e: self.change_direction("Right"))
        self.window.bind("<space>", lambda e: self.new_game())
        self.window.bind("<p>", lambda e: self.toggle_pause())
        self.window.bind("<Escape>", lambda e: self.window.quit())
        
    def draw_grid(self):
        # Draw vertical lines
        for i in range(self.width):
            x = i * self.cell_size
            self.canvas.create_line(
                x, 0, x, self.height * self.cell_size,
                fill=self.colors["grid"]
            )
        
        # Draw horizontal lines
        for i in range(self.height):
            y = i * self.cell_size
            self.canvas.create_line(
                0, y, self.width * self.cell_size, y,
                fill=self.colors["grid"]
            )
            
    def draw_cell(self, x, y, color):
        self.canvas.create_rectangle(
            x * self.cell_size,
            y * self.cell_size,
            (x + 1) * self.cell_size,
            (y + 1) * self.cell_size,
            fill=color,
            outline=""
        )
        
    def draw_snake(self):
        # Draw snake body
        for segment in self.snake[1:]:
            self.draw_cell(segment[0], segment[1], self.colors["snake"])
        
        # Draw snake head
        head = self.snake[0]
        self.draw_cell(head[0], head[1], self.colors["snake_head"])
        
    def spawn_food(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                self.draw_cell(x, y, self.colors["food"])
                break
                
    def spawn_special_food(self):
        if random.random() < 0.2:  # 20% chance to spawn special food
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if (x, y) not in self.snake and (x, y) != self.food:
                    self.special_food = (x, y)
                    self.draw_cell(x, y, self.colors["special_food"])
                    break
                    
    def change_direction(self, new_direction):
        opposites = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }
        
        if new_direction != opposites.get(self.direction):
            self.next_direction = new_direction
            
    def move_snake(self):
        if not self.game_running or self.paused:
            return
            
        # Update direction
        self.direction = self.next_direction
        
        # Get current head position
        head = self.snake[0]
        
        # Calculate new head position
        if self.direction == "Up":
            new_head = (head[0], head[1] - 1)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 1)
        elif self.direction == "Left":
            new_head = (head[0] - 1, head[1])
        else:  # Right
            new_head = (head[0] + 1, head[1])
            
        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake):
            self.game_over()
            return
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check for food
        if new_head == self.food:
            self.score += 10
            self.food = None
            self.spawn_food()
            self.spawn_special_food()
        elif new_head == self.special_food:
            self.score += 50
            self.special_food = None
        else:
            # Remove tail
            self.snake.pop()
            
        # Update score display
        self.score_var.set(f"Score: {self.score}")
        
        # Redraw game
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_snake()
        if self.food:
            self.draw_cell(self.food[0], self.food[1], self.colors["food"])
        if self.special_food:
            self.draw_cell(self.special_food[0], self.special_food[1], self.colors["special_food"])
            
        # Schedule next move
        self.window.after(self.speed, self.move_snake)
        
    def change_difficulty(self, _=None):
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            self.speed = 150
        elif difficulty == "Normal":
            self.speed = 100
        else:  # Hard
            self.speed = 50
            
    def toggle_pause(self):
        if self.game_running:
            self.paused = not self.paused
            self.pause_button.configure(text="Resume" if self.paused else "Pause")
            if not self.paused:
                self.move_snake()
                
    def new_game(self):
        # Reset game state
        self.snake = [(15, 10), (14, 10), (13, 10)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.food = None
        self.special_food = None
        self.game_running = True
        self.paused = False
        
        # Update display
        self.score_var.set("Score: 0")
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_snake()
        self.spawn_food()
        
        # Start game
        self.move_snake()
        
    def game_over(self):
        self.game_running = False
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_var.set(f"High Score: {self.high_score}")
            
        messagebox.showinfo("Game Over", f"Final Score: {self.score}\nHigh Score: {self.high_score}")
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()