import pygame
import chess
from board import Board
from config import Config
from ai import ChessAI
import os

class Game:
    def __init__(self, ai_enabled=False):
        pygame.mixer.init()  # Initialize sound mixer
        
        # Load sound effects
        base_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sounds')
        self.move_sound = pygame.mixer.Sound(os.path.join(base_path, 'move.wav'))
        self.capture_sound = pygame.mixer.Sound(os.path.join(base_path, 'capture.wav'))
        
        self.board = Board()
        self.config = Config()
        self.selected_square = None
        self.legal_moves = self.board.get_legal_moves()
        self.ai_enabled = ai_enabled
        self.ai = ChessAI(chess.BLACK) if ai_enabled else None
        self.ai_turn = False

    def show_bg(self, surface):
        theme = self.config.theme
        last_move = getattr(self, 'last_move', None)
        
        for row in range(8):
            for col in range(8):
                # Default color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                
                # Highlight last moved squares
                current_square = (7 - row) * 8 + col
                if last_move and current_square in last_move.get('squares', []):
                    # Use consistent highlight color for all moves
                    color = (200, 230, 100)  # Light yellow-green
                
                rect = (col * 80, row * 80, 80, 80)
                pygame.draw.rect(surface, color, rect)
        
        # Render coordinate notation
        font = pygame.font.Font(None, 24)
        
        # Column letters (A-H)
        for col in range(8):
            letter = chr(ord('A') + col)
            text = font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(center=(col * 80 + 40, 8 * 80 + 40))
            surface.blit(text, text_rect)
        
        # Row numbers (1-8)
        for row in range(8):
            number = str(8 - row)
            text = font.render(number, True, (0, 0, 0))
            text_rect = text.get_rect(center=(8 * 80 + 40, row * 80 + 40))
            surface.blit(text, text_rect)

    def show_pieces(self, surface):
        for square in chess.SQUARES:
            piece = self.board.get_piece_at(square)
            if piece:
                row = 7 - (square // 8)
                col = square % 8
                piece_symbol = piece.symbol().lower()
                piece_name = {
                    'r': 'rook',
                    'n': 'knight',
                    'b': 'bishop',
                    'q': 'queen',
                    'k': 'king',
                    'p': 'pawn'
                }[piece_symbol]
                img_path = f'assets/images/imgs-80px/{"white" if piece.color else "black"}_{piece_name}.png'
                img = pygame.image.load(img_path)
                img_center = col * 80 + 40, row * 80 + 40
                img_rect = img.get_rect(center=img_center)
                surface.blit(img, img_rect)

    def show_captures(self, surface, from_square):
        """Draw red squares for pieces that can be captured"""
        for move in self.board.board.legal_moves:
            if move.from_square == from_square:
                to_square = move.to_square
                row = 7 - (to_square // 8)
                col = to_square % 8
                
                # Check if there is an opponent's piece at the destination square
                target_piece = self.board.get_piece_at(to_square)
                
                # If there is an opponent's piece, fill the entire square with red
                if target_piece is not None and target_piece.color != self.board.board.turn:
                    rect = pygame.Rect(col * 80, row * 80, 80, 80)
                    pygame.draw.rect(surface, (255, 150, 150), rect)  # Fill the entire square with light red
                    
    def show_move_dots(self, surface, from_square):
        """Draw yellow dots for squares that can be moved to"""
        for move in self.board.board.legal_moves:
            if move.from_square == from_square:
                to_square = move.to_square
                row = 7 - (to_square // 8)
                col = to_square % 8
                
                # Draw yellow dot
                center_x = col * 80 + 40
                center_y = row * 80 + 40
                pygame.draw.circle(surface, (255, 255, 0), (center_x, center_y), 15)  # Yellow dot
                
    def show_moves(self, surface, from_square):
        """Combined function (kept to avoid modifying main.py if not needed)"""
        self.show_captures(surface, from_square)
        self.show_move_dots(surface, from_square)

    def play_move(self, move_uci):
        # Check if the move is a capture
        from_sq = chess.parse_square(move_uci[0:2])
        to_sq = chess.parse_square(move_uci[2:4])
        
        # Check if there's a piece at the destination square (capture)
        if self.board.get_piece_at(to_sq):
            self.capture_sound.play()
        else:
            self.move_sound.play()
        
        return self.board.push_move(move_uci)

    def is_check(self):
        return self.board.is_check()

    def is_checkmate(self):
        return self.board.is_checkmate()

    def is_stalemate(self):
        return self.board.is_stalemate()

    def reset(self):
        self.board.reset()
        self.selected_square = None
        self.legal_moves = self.board.get_legal_moves()

    def result(self):
        # Return the result of the game
        return self.board.board.result()