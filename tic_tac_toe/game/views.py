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

class GameCollection(View):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        return JsonResponse({'objects': [model_to_dict(game) for game in games], 'count': len(games)})

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


class GameView(View):
    def get(self, request, *args, **kwargs):
        try:
            game = Game.objects.get(id=kwargs['id'])
            return JsonResponse(model_to_dict(game))
        except Game.DoesNotExist:
            return JsonResponse({'errors': {'error_code': 'game_not_found'}}, status=404)
            
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        try:
            game = Game.objects.get(id=kwargs['id'], status=Game.IN_PROGRESS)
            new_game_data = json.loads(request.body)
            controller = GameController(game)
            controller.validate_update(new_game_data)
            controller.game.board = new_game_data['board']
            controller.set_updated_by()
            controller.set_status()
            controller.game.save()
            return JsonResponse(model_to_dict(game))
        except ValidationError as e:
            return JsonResponse({'errors': e.errors}, status=400)
        except Game.DoesNotExist:
            return JsonResponse({'errors': {'error_code': 'game_not_found'}}, status=404)
        