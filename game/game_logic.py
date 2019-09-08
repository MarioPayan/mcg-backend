class GameLogic():
    x_size = 7
    y_size = 7
    connect = 4
    max_moves = None
    current_moves = 0
    board = [[]]

    def create_board(self):
        self.board = [[0] * self.x_size for j in range(self.y_size)]
        self.max_moves = self.x_size * self.y_size

    def action_on_board(self, player, y, side):
        line = self.board[y]
        if side == "R":
            line.reverse()
        for i, position in enumerate(line):
            if(position == 0):
                line[i] = player
                x = self.x_size - i - 1 if side == "R" else i
                break
            if(i == len(line) - 1):
                return -1
        if side == "R":
            line.reverse()
        self.board[y] = line
        self.current_moves = self.current_moves + 1
        return ((x, y), self.check_for_winner(x, y))

    def validate_pos(self, x, y):
        if (x >= 0 and x < self.x_size and y >= 0 and y < self.y_size):
            return self.board[y][x]
        else:
            return -1

    def check_for_winner(self, last_x, last_y):
        if (self.current_moves == self.max_moves):
            return 100
        scope = (self.connect * 2) - 1
        shift = self.connect - 1
        horizontal = [
            self.validate_pos(
                last_x + i - shift,
                last_y
            ) for i in range(scope)]
        vertical = [
            self.validate_pos(
                last_x,
                last_y + i - shift
            ) for i in range(scope)]
        positive_diagonal = [
            self.validate_pos(
                last_x + i - shift,
                last_y - i + shift
            ) for i in range(scope)]
        negative_diagonal = [
            self.validate_pos(
                last_x + i - shift,
                last_y + i - shift
            ) for i in range(scope)]
        directions = [
            horizontal,
            vertical,
            positive_diagonal,
            negative_diagonal]
        for direction in directions:
            for i in range(self.connect):
                if (len(set(direction[i:i + self.connect])) == 1):
                    return self.board[last_y][last_x]
        return 0


class ArtificialIntelligence():
    def take_decision(self, board):
        return (0, "L")
