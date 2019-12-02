import json
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core import serializers
from django.forms.models import model_to_dict

from game.models import Game
from game.controller import GameController, ValidationError

class CreateGame(View):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        try:
            new_game_data = json.loads(request.body)
            GameController(None).validate_create(new_game_data)
            players = new_game_data.pop('players')
            new_game_data['x_player'] = players[0]
            new_game_data['o_player'] = players[1]
            new_game_data['board'] = [[None] * 3] * 3  # Since we don't change the board, 
            # we can use lists multiplication
            new_game_data['updated_by'] = new_game_data['o_player']

            game = Game.objects.create(**new_game_data)
            return JsonResponse(model_to_dict(game))
        except ValidationError as e:
            return JsonResponse({'errors': e.errors}, status=400)


class UpdateGame(View):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        try:
            game = get_object_or_404(Game, id=kwargs['id'])
            new_game_data = json.loads(request.body)
            controller = GameController(game)
            controller.validate_update(new_game_data)
            game.board = new_game_data['board']
            controller.set_updated_by()
            controller.set_finished()
            game.save()
            return JsonResponse(model_to_dict(game))
        except ValidationError as e:
            return JsonResponse({'errors': e.errors}, status=400)
        except Game.DoesNotExist:
            return JsonResponse({'errors': {'error_code': 'game_not_found'}}, status=404)
