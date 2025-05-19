import chess

class Board:
    def __init__(self):
        self.board = chess.Board()

    def get_legal_moves(self):
        # return the list of legal moves (UCI format)
        return list(self.board.legal_moves)

    def push_move(self, move_uci):
        # identify the moves (form UCI)
        from_sq = chess.parse_square(move_uci[0:2])
        to_sq = chess.parse_square(move_uci[2:4])
        piece = self.board.piece_at(from_sq)
        
        # Kiểm tra trường hợp tốt di chuyển đến hàng cuối (phong cấp)
        is_promotion = False
        if piece and piece.piece_type == chess.PAWN:
            # Tốt trắng đến hàng 8
            if piece.color == chess.WHITE and chess.square_rank(to_sq) == 7:
                is_promotion = True
            # Tốt đen đến hàng 1
            elif piece.color == chess.BLACK and chess.square_rank(to_sq) == 0:
                is_promotion = True
        
        if is_promotion:
            # Tự động phong hậu
            move = chess.Move(from_sq, to_sq, promotion=chess.QUEEN)
        else:
            move = chess.Move(from_sq, to_sq)
            
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False

    def is_check(self):
        return self.board.is_check()

    def is_checkmate(self):
        return self.board.is_checkmate()

    def is_stalemate(self):
        return self.board.is_stalemate()

    def fen(self):
        return self.board.fen()

    def reset(self):
        self.board.reset()

    def turn(self):
        return self.board.turn  # True if white, False if black

    def result(self):
        return self.board.result()

    def is_game_over(self):
        return self.board.is_game_over()

    def legal_moves_squares(self):
        # Trả về danh sách nước đi hợp lệ dạng (from_square, to_square)
        return [(move.from_square, move.to_square) for move in self.board.legal_moves]

    def get_piece_at(self, square):
        # Lấy quân cờ tại ô (0-63)
        return self.board.piece_at(square)

    def pop(self):
        return self.board.pop()
