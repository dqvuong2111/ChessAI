import pygame
import chess
from theme import Theme
from board import Board
from game import Game
import sys
import time


WIDTH, HEIGHT = 640, 640
SQSIZE = 80

class Main:
    def __init__(self, ai_mode=True, ai_depth=3, use_alpha_beta=True):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game(ai_enabled=ai_mode)
        self.selected_square = None  # Store selected square (index 0-63)
        self.running = True
        self.ai_mode = ai_mode
        self.last_player_move_time = pygame.time.get_ticks()
        self.ai_depth = ai_depth  # Default depth of AI
        self.use_alpha_beta = use_alpha_beta  # Default value for Alpha-Beta algorithm
        self.ai_calculation_time = 0  # Time taken for AI to calculate its move


    def _show_game_end_screen(self, result):
        # Draw the final board state first
        self.game.show_bg(self.screen)
        self.game.show_pieces(self.screen)
        
        # Create a very light transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 32))  # Very transparent black (alpha=32)
        self.screen.blit(overlay, (0, 0))
        
        # Prepare text with background
        font_large = pygame.font.SysFont('Arial', 36)
        font_small = pygame.font.SysFont('Arial', 20)
        
        # Create background for text
        bg_height = 80
        bg = pygame.Surface((WIDTH, bg_height), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 160))  # Semi-transparent black background for text
        self.screen.blit(bg, (0, HEIGHT - bg_height))  # Place at bottom
        
        # Determine text based on result
        if result == '1-0':
            title = font_large.render('White Wins!', True, (255, 255, 255))
            subtitle = font_small.render('Checkmate', True, (200, 200, 200))
        elif result == '0-1':
            title = font_large.render('Black Wins!', True, (255, 255, 255))
            subtitle = font_small.render('Checkmate', True, (200, 200, 200))
        else:  # Draw
            title = font_large.render('Draw', True, (255, 255, 255))
            subtitle = font_small.render('Stalemate', True, (200, 200, 200))
        
        # Add instructions
        instructions = font_small.render('Press R to restart or ESC to quit', True, (200, 200, 200))
        
        # Position text at bottom of screen with background
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT - 60))
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, HEIGHT - 40))
        instructions_rect = instructions.get_rect(center=(WIDTH//2, HEIGHT - 20))
        
        # Render text
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        self.screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        
        # Wait for user to close or restart
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart on 'R'
                        self.game.reset()
                        self.selected_square = None
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:  # Exit on ESC
                        pygame.quit()
                        sys.exit()

    def mainloop(self):
        while self.running:
            current_time = pygame.time.get_ticks()
            self.screen.fill((0, 0, 0))
            self.game.show_bg(self.screen)
            
            # Check for game over conditions
            if self.game.is_checkmate():
                result = self.game.result()
                self._show_game_end_screen(result)
                continue
            elif self.game.is_stalemate():
                result = self.game.result()
                self._show_game_end_screen(result)
                continue
            
            # AI's turn in AI mode
            if (self.ai_mode and 
                self.game.board.board.turn == chess.BLACK and 
                self.selected_square is None and 
                current_time - self.last_player_move_time > 1000):  # Wait 1 second after player move
                
                # Start timing AI calculation
                ai_start_time = time.time()
                
                ai_move, calculations, calculations_alpha_beta = self.game.ai.choose_move(
                    self.game.board.board, 
                    use_alpha_beta=self.use_alpha_beta,
                    depth=self.ai_depth  # Use current depth
                )
                
                # End timing and store calculation time
                self.ai_calculation_time = time.time() - ai_start_time
                
                if ai_move:
                    # Get piece and destination information
                    from_square = chess.square_name(ai_move.from_square)
                    to_square = chess.square_name(ai_move.to_square)
                    piece = self.game.board.get_piece_at(ai_move.from_square)
                    captured = self.game.board.get_piece_at(ai_move.to_square)
                    
                    # Check if the move is a capture
                    if captured:
                        self.game.capture_sound.play()
                    else:
                        self.game.move_sound.play()
                    
                    # Print AI's move details
                    move_info = f"AI Move: {self._get_piece_full_name(piece)} from {from_square} to {to_square}"
                    if captured:
                        move_info += f" captures {self._get_piece_full_name(captured)}"
                    print(move_info)
                    
                    # Print calculation information
                    if self.use_alpha_beta:
                        print(f"Calculation: {calculations_alpha_beta} (Alpha-Beta)")
                        print(f"Calculation time: {self.ai_calculation_time:.3f} seconds")
                    else:
                        print(f"Calculation: {calculations} (Standard Minimax)")
                        print(f"Calculation time: {self.ai_calculation_time:.3f} seconds")
                    
                    # Print comparison if both algorithms were used
                    if calculations > 0 and calculations_alpha_beta > 0:
                        reduction = (1 - calculations_alpha_beta / calculations) * 100 if calculations > 0 else 0
                        print(f"Comparison: Alpha-Beta reduces calculations by {reduction:.2f}%")
                    
                    self.game.board.board.push(ai_move)
                    # Track AI move for highlighting
                    self.last_move = [ai_move.from_square, ai_move.to_square]
                    self.game.last_move = {
                        'squares': self.last_move,
                        'color': 'black'
                    }
                    pygame.time.delay(500)  # Slight delay to show AI's thinking
            
            # Draw red squares for opponent's pieces that can be captured
            if self.selected_square is not None:
                self.game.show_captures(self.screen, self.selected_square)
            
            # Draw pieces to prevent them from being covered
            self.game.show_pieces(self.screen)
            
            # Draw yellow dots for squares that can be moved to
            if self.selected_square is not None:
                self.game.show_move_dots(self.screen, self.selected_square)
            
            # Display player turn only
            font = pygame.font.SysFont('Arial', 20)
            turn_text = "Turn: " + ("White (Player 1)" if self.game.board.board.turn == chess.WHITE else "Black (Player 2)")
            turn_render = font.render(turn_text, True, (255, 255, 255))
            self.screen.blit(turn_render, (10, 10))
            
            # Display AI depth
            font = pygame.font.SysFont('Arial', 20)
            ai_depth_text = f"AI Depth: {self.ai_depth}"
            ai_depth_render = font.render(ai_depth_text, True, (255, 255, 255))
            self.screen.blit(ai_depth_render, (10, 40))
            
            # Display AI calculation time
            ai_time_text = f"AI Calculation Time: {self.ai_calculation_time:.3f} seconds"
            ai_time_render = font.render(ai_time_text, True, (255, 255, 255))
            self.screen.blit(ai_time_render, (10, 70))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // SQSIZE
                    row = 7 - (y // SQSIZE)  # Python-chess coordinate system: a1 = 0, h8 = 63
                    clicked_square = row * 8 + col
                    piece = self.game.board.get_piece_at(clicked_square)
                    if self.selected_square is None:
                        # Select player's own piece
                        if piece and piece.color == self.game.board.board.turn:
                            self.selected_square = clicked_square
                    else:
                        # Check that source and destination squares are different
                        if self.selected_square != clicked_square:
                            # Try to make a move
                            move_uci = self._get_uci(self.selected_square, clicked_square)
                            # Get piece information before making the move
                            piece = self.game.board.get_piece_at(self.selected_square)
                            captured = self.game.board.get_piece_at(clicked_square)
                            from_square = chess.square_name(self.selected_square)
                            to_square = chess.square_name(clicked_square)
                            
                            if self.game.play_move(move_uci):
                                # Print user's move details
                                move_info = f"\nUser Move: {self._get_piece_full_name(piece)} from {from_square} to {to_square}"
                                if captured:
                                    move_info += f" captures {self._get_piece_full_name(captured)}"
                                print(move_info)
                                # Track the last move squares for highlighting
                                from_sq = chess.parse_square(move_uci[0:2])
                                to_sq = chess.parse_square(move_uci[2:4])
                                self.last_move = [from_sq, to_sq]
                                self.game.last_move = {
                                    'squares': self.last_move,
                                    'color': 'white' if self.game.board.board.turn == chess.BLACK else 'black'
                                }
                                self.selected_square = None
                                self.last_player_move_time = pygame.time.get_ticks()  # Update last move time
                            else:
                                # If invalid, reselect
                                if piece and piece.color == self.game.board.board.turn:
                                    self.selected_square = clicked_square
                                else:
                                    self.selected_square = None
                        else:
                            # Deselect if clicked on the same square twice
                            self.selected_square = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game.reset()
                        self.selected_square = None
                    
                    # Tăng độ sâu AI với phím +
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                        if self.ai_depth < 5:
                            self.ai_depth += 1
                        print(f"\nAI depth increased to {self.ai_depth}")
                    
                    # Giảm độ sâu AI với phím -
                    if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        if self.ai_depth > 1:  # Không cho phép độ sâu nhỏ hơn 1
                            self.ai_depth -= 1
                            print(f"\nAI depth decreased to {self.ai_depth}")
                    
                    # Chuyển đổi giữa Alpha-Beta và Minimax thông thường với phím a
                    if event.key == pygame.K_a:
                        self.use_alpha_beta = not self.use_alpha_beta
                        algorithm = "Alpha-Beta Pruning" if self.use_alpha_beta else "Standard Minimax"
                        print(f"\nSwitched to {algorithm} algorithm")

            pygame.display.flip()

    def _get_uci(self, from_square, to_square):
        # Convert index 0-63 to UCI string, example: 12, 28 -> 'e2e4'
        from_file = chr((from_square % 8) + ord('a'))
        from_rank = str((from_square // 8) + 1)
        to_file = chr((to_square % 8) + ord('a'))
        to_rank = str((to_square // 8) + 1)
        return f"{from_file}{from_rank}{to_file}{to_rank}"
    
    def _get_piece_full_name(self, piece):
        """Get the full name of a chess piece without color."""
        if piece is None:
            return "None"
            
        piece_names = {
            'P': 'Pawn',
            'N': 'Knight',
            'B': 'Bishop',
            'R': 'Rook',
            'Q': 'Queen',
            'K': 'King',
            'p': 'Pawn',
            'n': 'Knight',
            'b': 'Bishop',
            'r': 'Rook',
            'q': 'Queen',
            'k': 'King'
        }
        
        return piece_names.get(piece.symbol(), piece.symbol())
        

if __name__ == "__main__":
    # Configure parameters here
    app = Main(ai_mode=True, ai_depth=3, use_alpha_beta=True)
    app.mainloop()