from random import randint
from .models import Game, Movement
from .game_logic import GameLogic, ArtificialIntelligence


class Controller():
    games_dic = {}
    play_with_ia = False
    ia = ArtificialIntelligence()

    def create_game(self, game_id):
        self.games_dic[game_id]['game_logic'] = GameLogic()
        self.games_dic[game_id]['game_logic'].create_board()
        self.games_dic[game_id]['board_db'] = Game.objects.create(
            player_1=self.games_dic[game_id]['players'][0],
            player_2=self.games_dic[game_id]['players'][1],
            room_name=game_id
        )

    def make_movement(self, game_id, player_id, row, side):
        result = self.games_dic[game_id]['game_logic'].action_on_board(
            player_id, row, side)
        if (result != -1):
            Movement.objects.create(
                game=self.games_dic[game_id]['board_db'],
                player_id=player_id,
                row=row,
                side=side,
                winner=result[1]
            )
            return result

    def next_turn(self, game_id):
        if self.play_with_ia:
            self.games_dic[game_id]['current_turn'] = 2
        else:
            player_len = len(self.games_dic[game_id]['players'])
            self.games_dic[game_id]['current_turn'] = (
                self.games_dic[game_id]['current_turn'] % player_len) + 1
        return self.games_dic[game_id]['current_turn']

    def add_player(self, player_name, game_id):
        if game_id not in self.games_dic:
            self.create_game_instance(game_id)
        if self.play_with_ia:
            self.games_dic[game_id]['players'].append("IA")
        self.games_dic[game_id]['players'].append(player_name)
        needed_players = self.games_dic[game_id]['needed_players']
        if (len(self.games_dic[game_id]['players']) == needed_players):
            self.create_game(game_id)
            self.games_dic[game_id]['game_ready'] = True
            self.games_dic[game_id]['current_turn'] = randint(
                1, len(self.games_dic[game_id]['players']))
        return len(self.games_dic[game_id]['players'])

    def create_game_instance(self, game_id):
        self.games_dic[game_id] = {
            "game_logic": None,
            "board_db": None,
            "game_ready": False,
            "current_turn": 0,
            "players": [],
            "needed_players": 2
        }

    def ia_move(self, game_id):
        (row, side) = self.ia.take_decision(
            self.games_dic[game_id]['board_db'])
        return {
            "player_id": 1,
            "row": row,
            "side": side
        }

    def build_game(self, game_room_name):
        try:
            game_db = Game.objects.get(room_name=game_room_name)
        except Game.DoesNotExist:
            print("This game doesn't exists")
            return None
        movements_db = list(Movement.objects.filter(game=game_db))
        game = GameLogic()
        game.create_board()
        for move in movements_db:
            game.action_on_board(
                move.player_id,
                move.row,
                move.side
            )
        for row in game.board:
            print(row)
        game.print_board()
        print("Player 1: " + game_db.player_1)
        print("Player 2: " + game_db.player_2)
        print("Winner: " + str(movements_db[-1].winner))
