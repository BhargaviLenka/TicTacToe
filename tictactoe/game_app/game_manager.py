import random
from .constants import ResultConstants, PlayerConstants, Levels
from .models import Player, Game, Leaderboard


class GameManager:
    @staticmethod
    def create_leaderboard(request, player):
        board = request.POST.get('board')
        move = int(request.POST.get('move'))
        level = request.POST.get('level')
        board = board[:move] + PlayerConstants.PLAYER_X + board[move + 1:]
        result, winning_board_indices = GameManager.check_winner(board)
        if result == PlayerConstants.PLAYER_X:
            result = ResultConstants.WIN
        elif result == ResultConstants.DRAW:
            result = ResultConstants.DRAW
        else:
            ai_index = GameManager.ai_move(board, level)
            if ai_index is not None:
                board = board[:ai_index] + PlayerConstants.PLAYER_O + board[ai_index + 1:]

            result, winning_board_indices = GameManager.check_winner(board)
            if result == PlayerConstants.PLAYER_O:
                result = ResultConstants.LOSS
            elif result == ResultConstants.DRAW:
                result = ResultConstants.DRAW
            else:
                result = ResultConstants.ONGOING

        cells = [{'index': i, 'value': board[i]} for i in range(9)]
        rows = [cells[i * 3:(i + 1) * 3] for i in range(3)]

        context = {
            'player': player,
            'result': result,
            'board': board,
            'rows': rows,
            'level': level,
            'range': range(3),
            'is_game_ongoing': result,
            'winning_board_indices': winning_board_indices
        }
        return context, result, board, level, winning_board_indices

    @staticmethod
    def update_leaderboard(player, result):
        leaderboard_obj, created = Leaderboard.objects.get_or_create(player=player)
        if result == ResultConstants.WIN:
            leaderboard_obj.wins += 1
        elif result == ResultConstants.LOSS:
            leaderboard_obj.losses += 1
        elif result == ResultConstants.DRAW:
            leaderboard_obj.draws += 1
        leaderboard_obj.save()

    @staticmethod
    def check_winner(board):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        winning_board_indices = []
        for a, b, c in win_conditions:
            if board[a] == board[b] == board[c] and board[a] != " ":
                winning_board_indices.extend([a, b, c])
                return board[a], winning_board_indices
        if " " not in board:
            return ResultConstants.DRAW, []
        return ResultConstants.ONGOING, []

    @staticmethod
    def minimax(board, is_maximizing):
        winner, winning_board_indices = GameManager.check_winner(board)
        if winner == PlayerConstants.PLAYER_X:
            return -10
        elif winner == PlayerConstants.PLAYER_O:
            return 10
        elif winner == ResultConstants.DRAW:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board = board[:i] + PlayerConstants.PLAYER_O + board[i+1:]
                    score = GameManager.minimax(board, False)
                    board = board[:i] + " " + board[i+1:]
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board = board[:i] + PlayerConstants.PLAYER_X + board[i+1:]
                    score = GameManager.minimax(board, True)
                    board = board[:i] + " " + board[i+1:]
                    best_score = min(score, best_score)
            return best_score

    @staticmethod
    def best_move(board):
        best_score = -float('inf')
        move = -1
        for i in range(9):
            if board[i] == " ":
                board = board[:i] + PlayerConstants.PLAYER_O + board[i+1:]
                score = GameManager.minimax(board, False)
                board = board[:i] + " " + board[i+1:]
                if score > best_score:
                    best_score = score
                    move = i
        return move

    @staticmethod
    def ai_move(board, level, optimal_percentage=0.6):
        if level == Levels.EASY:
            return GameManager.random_move(board)
        elif level == Levels.MEDIUM:
            val = random.random()
            if val < optimal_percentage:
                return GameManager.best_move(board)
            else:
                return GameManager.random_move(board)
        else:
            return GameManager.best_move(board)

    @staticmethod
    def random_move(board):
        available_moves = [i for i in range(9) if board[i] == " "]
        return random.choice(available_moves) if available_moves else None

