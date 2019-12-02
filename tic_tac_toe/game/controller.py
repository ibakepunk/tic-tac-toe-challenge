from game.models import Game

class ValidationError(Exception):
    def __init__(self, errors: list):
        super().__init__('Validation failed')
        self.errors = errors

class GameController(object):
    def __init__(self, game: Game):
        self.game = game

    def compute_board_changes(self, new_board):
        changes = []
        for i in range(3):
            for j in range(3):
                if self.game.board[i][j] != new_board[i][j]:
                    changes.append((i, j))

        return changes

    def validate_update(self, new_data):
        errors = []

        updated_by = new_data.get('updated_by')
        if not updated_by:
            errors.append({'field': 'updated_by', 'error_code': 'required'})
        elif self.game.updated_by == updated_by:
            errors.append({'field': 'updated_by', 'error_code': 'not_your_turn'})

        new_board = new_data.get('board')
        board_valid = True
        if not new_board:
            errors.append({'field': 'board', 'error_code': 'required'})
            board_valid = False
        else:
            if len(self.game.board) != 3 or not all(len(line) == 3 for line in self.game.board):
                errors.append({'field': 'board', 'error_code': 'board_dimensions_invalid'})
                board_valid = False
        
        if board_valid:
            changes = self.compute_board_changes(new_data.get('board'))
            if len(changes) > 1:
                errors.append({'field': 'board', 'error_code': 'too_much_turns'})
            
            i, j = changes[0]
            if self.game.board[i][j] is not None:
                errors.append({'field': 'board', 'error_code': 'cant_update_filled_cell'})

            next_turn = 'x' if self.game.updated_by == self.game.o_player else 'o'
            if new_board[i][j] != next_turn:
                errors.append({'field': 'updated_by', 'error_code': 'not_your_symbol'})

        if errors:
            raise ValidationError(errors)

    def validate_create(self, new_data: dict) -> None:
        errors = []
        players = new_data.get('players')
        if not players:
            errors.append({'field': 'players', 'error_code': 'required'})

        if len(players) != 2 or players[0] == players[1]:
            errors.append({'field': 'players', 'error_code': 'two_distinct_players_required'})
        
        if len(new_data) > 2:
            errors.append({'field': '__all__', 'error_code': 'additional_fields_not_allowed'})

        if errors:
            raise ValidationError(errors)

    def set_updated_by(self):
        if self.game.updated_by == self.game.o_player:
            self.game.updated_by = self.game.x_player
        else:
            self.game.updated_by = self.game.o_player

    def get_winning_lines(self):
        diagonals = [
            [self.game.board[i][i] for i in range(3)], 
            [self.game.board[i][j] for i, j in zip(range(3), range(2, -1, -1))],
        ]
        return [
            self.game.board,
            zip(*self.game.board),
            diagonals,
        ]

    def get_winner(self):
        for lines in self.get_winning_lines():
            for line in lines:
                if len(set(line)) == 1 and line[0] is not None:
                    return line[0]

        return None
    
    def check_draw(self):
        for lines in self.get_winning_lines():
            for line in lines:
                # It's draw if all the lines are filled with both Xs and Os
                if len(set(c for c in line if c is not None)) != 2:
                    return False
        return True


    def set_finished(self):
        winner = self.get_winner()
        if winner or self.check_draw():
            self.game.finished = True
