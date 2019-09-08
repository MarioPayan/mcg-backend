from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .controller import Controller


class GameConsumer(WebsocketConsumer):
    controller = Controller()

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        if(command == 'join_game'):
            player_id = self.save_player(text_data_json['player_name'])
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'broadcast_new_player',
                    'player_id': player_id
                }
            )
            if(self.controller.games_dic[self.room_name]['game_ready']):
                self.start_game(
                    self.controller.games_dic[self.room_name]['current_turn'])
        if(command == 'make_movement'):
            movement = text_data_json['movement']
            result = self.make_movement(movement)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'broadcast_make_movement',
                    'movement': result
                }
            )
            if self.controller.play_with_ia:
                ia_suggested_move = self.controller.ia_move(self.room_name)
                result = self.make_movement(ia_suggested_move)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'broadcast_make_movement',
                        'movement': result
                    }
                )
        if(command == 'close_connection'):
            code = text_data_json['code']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'disconnect',
                    'code': code
                }
            )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'broadcast_lost_player'
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def start_game(self, turn_number):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'broadcast_game_ready',
                'turn_number': turn_number
            }
        )

    def save_player(self, player_name):
        return self.controller.add_player(player_name, self.room_name)

    def make_movement(self, movement):
        after_move = self.controller.make_movement(
            self.room_name,
            movement['player_id'],
            movement['row'],
            movement['side']
        )
        if (after_move == -1):
            return after_move
        (movement['x'], movement['y']), movement['winner'] = after_move
        movement['next_turn'] = self.controller.next_turn(self.room_name)
        return movement

    def broadcast_new_player(self, event):
        self.send(text_data=json.dumps({
            'command': 'new_player',
            'player_id': event['player_id'],
        }))

    def broadcast_make_movement(self, event):
        self.send(text_data=json.dumps({
            'command': 'new_movement',
            'movement': event['movement']
        }))

    def broadcast_game_ready(self, event):
        self.send(text_data=json.dumps({
            'command': 'game_ready',
            'turn_number': event['turn_number'],
        }))

    def broadcast_lost_player(self, event):
        self.send(text_data=json.dumps({
            'command': 'game_error',
        }))
