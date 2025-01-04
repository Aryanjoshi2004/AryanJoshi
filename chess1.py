import tkinter as tk
from PIL import Image, ImageTk
import os

class ChessPiece:
    def __init__(self, color, piece_type):
        self.color = color
        self.piece_type = piece_type
        self.has_moved = False

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.root.configure(bg='#2c2c2c')
        
        # Game state
        self.selected_piece = None
        self.current_player = 'white'
        self.valid_moves = []
        
        # Create the board
        self.board_frame = tk.Frame(root, bg='#2c2c2c', padx=20, pady=20)
        self.board_frame.pack(expand=True)
        
        # Initialize the board state
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        
        # Status label
        self.status_label = tk.Label(
            root,
            text="White's turn",
            bg='#2c2c2c',
            fg='#ffffff',
            font=('Arial', 14)
        )
        self.status_label.pack(pady=10)

    def setup_board(self):
        # Initialize pieces
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        
        for col in range(8):
            # Set up pawns
            self.board[1][col] = ChessPiece('black', 'pawn')
            self.board[6][col] = ChessPiece('white', 'pawn')
            
            # Set up other pieces
            self.board[0][col] = ChessPiece('black', piece_order[col])
            self.board[7][col] = ChessPiece('white', piece_order[col])
        
        # Create the visual board
        for row in range(8):
            for col in range(8):
                # Alternate colors for squares
                color = '#b58863' if (row + col) % 2 == 0 else '#f0d9b5'
                
                square = tk.Label(
                    self.board_frame,
                    width=8,
                    height=4,
                    bg=color,
                    relief='flat'
                )
                square.grid(row=row, column=col)
                square.bind('<Button-1>', lambda e, r=row, c=col: self.square_clicked(r, c))
                self.squares[row][col] = square
                
                # Place pieces
                piece = self.board[row][col]
                if piece:
                    self.update_square_display(row, col)

    def update_square_display(self, row, col):
        piece = self.board[row][col]
        square = self.squares[row][col]
        
        # Clear existing text
        square.configure(text='')
        
        if piece:
            # Use Unicode chess symbols
            symbols = {
                'white': {
                    'king': '♔', 'queen': '♕', 'rook': '♖',
                    'bishop': '♗', 'knight': '♘', 'pawn': '♙'
                },
                'black': {
                    'king': '♚', 'queen': '♛', 'rook': '♜',
                    'bishop': '♝', 'knight': '♞', 'pawn': '♟'
                }
            }
            symbol = symbols[piece.color][piece.piece_type]
            square.configure(
                text=symbol,
                font=('Arial', 24),
                fg='#000000' if piece.color == 'white' else '#2c2c2c'
            )

    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []
        
        valid_moves = []
        
        if piece.piece_type == 'pawn':
            direction = -1 if piece.color == 'white' else 1
            
            # Forward move
            if 0 <= row + direction < 8 and not self.board[row + direction][col]:
                valid_moves.append((row + direction, col))
                
                # Initial two-square move
                if not piece.has_moved and 0 <= row + 2*direction < 8 and not self.board[row + 2*direction][col]:
                    valid_moves.append((row + 2*direction, col))
            
            # Captures
            for c in [col - 1, col + 1]:
                if 0 <= c < 8 and 0 <= row + direction < 8:
                    target = self.board[row + direction][c]
                    if target and target.color != piece.color:
                        valid_moves.append((row + direction, c))
        
        elif piece.piece_type == 'rook':
            # Horizontal and vertical moves
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                r, c = row + direction[0], col + direction[1]
                while 0 <= r < 8 and 0 <= c < 8:
                    target = self.board[r][c]
                    if not target:
                        valid_moves.append((r, c))
                    elif target.color != piece.color:
                        valid_moves.append((r, c))
                        break
                    else:
                        break
                    r += direction[0]
                    c += direction[1]
        
        elif piece.piece_type == 'knight':
            moves = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ]
            for move in moves:
                r, c = row + move[0], col + move[1]
                if 0 <= r < 8 and 0 <= c < 8:
                    target = self.board[r][c]
                    if not target or target.color != piece.color:
                        valid_moves.append((r, c))
        
        elif piece.piece_type == 'bishop':
            # Diagonal moves
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                r, c = row + direction[0], col + direction[1]
                while 0 <= r < 8 and 0 <= c < 8:
                    target = self.board[r][c]
                    if not target:
                        valid_moves.append((r, c))
                    elif target.color != piece.color:
                        valid_moves.append((r, c))
                        break
                    else:
                        break
                    r += direction[0]
                    c += direction[1]
        
        elif piece.piece_type == 'queen':
            # Combine rook and bishop moves
            directions = [
                (0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)
            ]
            for direction in directions:
                r, c = row + direction[0], col + direction[1]
                while 0 <= r < 8 and 0 <= c < 8:
                    target = self.board[r][c]
                    if not target:
                        valid_moves.append((r, c))
                    elif target.color != piece.color:
                        valid_moves.append((r, c))
                        break
                    else:
                        break
                    r += direction[0]
                    c += direction[1]
        
        elif piece.piece_type == 'king':
            # All adjacent squares
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    r, c = row + i, col + j
                    if 0 <= r < 8 and 0 <= c < 8:
                        target = self.board[r][c]
                        if not target or target.color != piece.color:
                            valid_moves.append((r, c))
        
        return valid_moves

    def highlight_squares(self, moves, color):
        for row, col in moves:
            self.squares[row][col].configure(bg=color)

    def reset_colors(self):
        for row in range(8):
            for col in range(8):
                color = '#b58863' if (row + col) % 2 == 0 else '#f0d9b5'
                self.squares[row][col].configure(bg=color)

    def square_clicked(self, row, col):
        piece = self.board[row][col]
        
        # If no piece is selected
        if not self.selected_piece:
            if piece and piece.color == self.current_player:
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(row, col)
                self.reset_colors()
                self.highlight_squares([(row, col)], '#7b61ff')  # Selected piece
                self.highlight_squares(self.valid_moves, '#90EE90')  # Valid moves
        
        # If a piece is already selected
        else:
            selected_row, selected_col = self.selected_piece
            
            # If clicked square is a valid move
            if (row, col) in self.valid_moves:
                # Move the piece
                self.board[row][col] = self.board[selected_row][selected_col]
                self.board[selected_row][selected_col] = None
                self.board[row][col].has_moved = True
                
                # Update display
                self.update_square_display(row, col)
                self.update_square_display(selected_row, selected_col)
                
                # Switch players
                self.current_player = 'black' if self.current_player == 'white' else 'white'
                self.status_label.configure(text=f"{self.current_player.capitalize()}'s turn")
            
            # Reset selection
            self.selected_piece = None
            self.valid_moves = []
            self.reset_colors()

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()