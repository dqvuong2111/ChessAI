import chess
import random

class ChessAI:
    def __init__(self, color):
        self.color = color
        self.calculations = 0
        self.calculations_alpha_beta = 0

        # Piece-Square Tables (Evaluation Matrices)
        self.pawn_eval_white = [
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
            [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
            [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
            [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
            [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
            [0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5],
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ]
        
        self.pawn_eval_black = self._reverse_array(self.pawn_eval_white)
        
        self.knight_eval_white = [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
            [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
            [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
            [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
            [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
            [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
        ]
        
        self.knight_eval_black = self._reverse_array(self.knight_eval_white)
        
        self.bishop_eval_white = [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
            [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
            [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
            [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
            [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        ]
        
        self.bishop_eval_black = self._reverse_array(self.bishop_eval_white)
        
        self.rook_eval_white = [
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
        ]
        
        self.rook_eval_black = self._reverse_array(self.rook_eval_white)
        
        self.queen_eval_white = [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ]
        
        self.queen_eval_black = self._reverse_array(self.queen_eval_white)
        
        self.king_eval_white = [
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
            [2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]
        ]
        
        self.king_eval_black = self._reverse_array(self.king_eval_white)

    def _reverse_array(self, array):
        """Reverse the evaluation matrix for black pieces."""
        return array[::-1]

    def _get_piece_value(self, piece):
        """Assign base value to different pieces."""
        values = {
            chess.PAWN: 10.0,
            chess.KNIGHT: 30.0,
            chess.BISHOP: 30.0,
            chess.ROOK: 50.0,
            chess.QUEEN: 90.0,
            chess.KING: 900.0
        }
        return values.get(piece, 0.0)

    def _get_piece_square_value(self, piece, square, color):
        """Get positional value for a piece based on its square."""
        row, col = chess.square_rank(square), chess.square_file(square)
        
        # Adjust row/col based on color
        if color == chess.BLACK:
            row = 7 - row
        
        # Select appropriate evaluation matrix
        if piece == chess.PAWN:
            eval_matrix = self.pawn_eval_white if color == chess.WHITE else self.pawn_eval_black
        elif piece == chess.KNIGHT:
            eval_matrix = self.knight_eval_white if color == chess.WHITE else self.knight_eval_black
        elif piece == chess.BISHOP:
            eval_matrix = self.bishop_eval_white if color == chess.WHITE else self.bishop_eval_black
        elif piece == chess.ROOK:
            eval_matrix = self.rook_eval_white if color == chess.WHITE else self.rook_eval_black
        elif piece == chess.QUEEN:
            eval_matrix = self.queen_eval_white if color == chess.WHITE else self.queen_eval_black
        elif piece == chess.KING:
            eval_matrix = self.king_eval_white if color == chess.WHITE else self.king_eval_black
        else:
            return 0.0
        
        return eval_matrix[row][col]

    def evaluate_board(self, board):
        """Evaluate the current board state."""
        if board.is_checkmate():
            return float('-inf') if board.turn == self.color else float('inf')
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0.0
        
        total_evaluation = 0.0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                # Determine sign based on piece color
                sign = 1 if piece.color == self.color else -1
                
                # Calculate piece value
                piece_value = self._get_piece_value(piece.piece_type)
                piece_square_value = self._get_piece_square_value(piece.piece_type, square, piece.color)
                
                total_evaluation += sign * (piece_value + piece_square_value)
        
        return total_evaluation

    def minimax(self, board, depth, maximizing_player):
        """Minimax algorithm."""
        self.calculations += 1

        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)       
        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, False)
                board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, True)
                board.pop()
                min_eval = min(min_eval, eval)
            return min_eval
    
    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning."""
        self.calculations_alpha_beta += 1  # Count every node evaluated

        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def get_best_move(self, board, depth=3, use_alpha_beta=True):
        """Find the best move using minimax with or without alpha-beta pruning."""
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        self.calculations = 0
        self.calculations_alpha_beta = 0

        # Evaluate all legal moves
        for move in board.legal_moves:
            board.push(move)
            # Check for immediate checkmate
            if board.is_checkmate():
                board.pop()
                return move, self.calculations, self.calculations_alpha_beta

            # Evaluate the move using the selected algorithm
            if use_alpha_beta:
                move_eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            else:
                move_eval = self.minimax(board, depth - 1, False)
            
            board.pop()

            # Update best move
            if best_move is None or move_eval > max_eval:
                max_eval = move_eval
                best_move = move

            if use_alpha_beta:
                alpha = max(alpha, move_eval)

        # Return best move or first legal move if none found, along with calculation statistics
        return best_move if best_move else next(board.legal_moves, None), self.calculations, self.calculations_alpha_beta

    def choose_move(self, board, use_alpha_beta=True, depth=3):
        """Choose a move for the AI."""
        move, calculations, calculations_alpha_beta = self.get_best_move(board, depth=depth, use_alpha_beta=use_alpha_beta)
        return move, calculations, calculations_alpha_beta
