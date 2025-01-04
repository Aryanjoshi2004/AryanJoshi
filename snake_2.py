import tkinter as tk
from tkinter import messagebox
import random

class SnakeAndLadder:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake and Ladder")
        self.window.geometry("800x600")
        
        # Define snakes and ladders
        self.snakes = {
            16: 6,
            47: 26,
            49: 11,
            56: 53,
            62: 19,
            64: 60,
            87: 24,
            93: 73,
            95: 75,
            98: 78
        }
        
        self.ladders = {
            1: 38,
            4: 14,
            9: 31,
            21: 42,
            28: 84,
            36: 44,
            51: 67,
            71: 91,
            80: 100
        }
        
        # Initialize players
        self.player1_pos = 0
        self.player2_pos = 0
        self.current_player = 1
        
        self.create_board()
        self.create_controls()
        
    def create_board(self):
        # Create main board frame
        self.board_frame = tk.Frame(self.window)
        self.board_frame.pack(pady=20)
        
        # Create 10x10 grid of cells
        self.cells = {}
        for i in range(10):
            for j in range(10):
                # Calculate the number for this cell
                if i % 2 == 0:
                    number = (10 - i) * 10 - j
                else:
                    number = (10 - i - 1) * 10 + j + 1
                
                # Create cell frame
                cell = tk.Frame(
                    self.board_frame,
                    width=50,
                    height=50,
                    relief="solid",
                    borderwidth=1
                )
                cell.grid(row=i, column=j)
                cell.pack_propagate(False)
                
                # Add number label
                label = tk.Label(cell, text=str(number))
                label.pack(expand=True)
                
                # Store cell reference
                self.cells[number] = cell
                
                # Color special cells
                if number in self.snakes:
                    cell.configure(bg='pink')
                    tk.Label(cell, text=f"→{self.snakes[number]}", fg='red').pack()
                elif number in self.ladders:
                    cell.configure(bg='lightgreen')
                    tk.Label(cell, text=f"→{self.ladders[number]}", fg='green').pack()
    
    def create_controls(self):
        # Control frame
        control_frame = tk.Frame(self.window)
        control_frame.pack(pady=20)
        
        # Dice roll button
        self.roll_button = tk.Button(
            control_frame,
            text="Roll Dice",
            command=self.roll_dice,
            width=20,
            height=2
        )
        self.roll_button.pack()
        
        # Status label
        self.status_label = tk.Label(
            control_frame,
            text="Player 1's turn",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=10)
        
        # Player positions label
        self.positions_label = tk.Label(
            control_frame,
            text="Player 1: 0 | Player 2: 0",
            font=("Arial", 12)
        )
        self.positions_label.pack(pady=5)
        
        # New game button
        self.new_game_button = tk.Button(
            control_frame,
            text="New Game",
            command=self.new_game,
            width=20
        )
        self.new_game_button.pack(pady=10)
    
    def roll_dice(self):
        # Roll dice
        roll = random.randint(1, 6)
        
        # Update position based on current player
        if self.current_player == 1:
            self.move_player(1, roll)
        else:
            self.move_player(2, roll)
        
        # Update labels
        self.update_labels()
        
        # Switch player
        self.current_player = 3 - self.current_player  # Switches between 1 and 2
        
    def move_player(self, player, roll):
        # Get current position
        current_pos = self.player1_pos if player == 1 else self.player2_pos
        
        # Calculate new position
        new_pos = current_pos + roll
        
        # Check if player won
        if new_pos >= 100:
            if new_pos == 100:
                self.game_won(player)
            return
        
        # Check for snakes and ladders
        if new_pos in self.snakes:
            new_pos = self.snakes[new_pos]
        elif new_pos in self.ladders:
            new_pos = self.ladders[new_pos]
        
        # Update position
        if player == 1:
            self.player1_pos = new_pos
        else:
            self.player2_pos = new_pos
        
        # Update cell colors
        self.update_board()
    
    def update_board(self):
        # Reset all cell colors (except snakes and ladders)
        for num, cell in self.cells.items():
            if num not in self.snakes and num not in self.ladders:
                cell.configure(bg='white')
        
        # Color player positions
        if self.player1_pos > 0:
            self.cells[self.player1_pos].configure(bg='lightblue')
        if self.player2_pos > 0:
            self.cells[self.player2_pos].configure(bg='yellow')
        
        # If players are on same position
        if self.player1_pos == self.player2_pos and self.player1_pos > 0:
            self.cells[self.player1_pos].configure(bg='purple')
    
    def update_labels(self):
        self.status_label.configure(text=f"Player {self.current_player}'s turn")
        self.positions_label.configure(
            text=f"Player 1: {self.player1_pos} | Player 2: {self.player2_pos}"
        )
    
    def game_won(self, player):
        messagebox.showinfo("Game Over", f"Player {player} wins!")
        self.new_game()
    
    def new_game(self):
        # Reset positions
        self.player1_pos = 0
        self.player2_pos = 0
        self.current_player = 1
        
        # Reset board colors
        self.update_board()
        
        # Reset labels
        self.update_labels()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = SnakeAndLadder()
    game.run()