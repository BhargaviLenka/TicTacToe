from django.shortcuts import render, redirect
from .models import Player, Game, Leaderboard
from .game_manager import GameManager
from .constants import ResultConstants
import random


def index(request):
    request.session.flush()
    if request.method == "POST":
        name = request.POST.get('name').strip().lower().title()
        player, created = Player.objects.get_or_create(name=name)
        request.session['username'] = name
        request.session['player_id'] = player.id
        return redirect('play', player_id=player.id)
    return render(request, 'index.html')


def play(request, player_id):
    try:
        player = Player.objects.get(id=player_id)
    except Exception as error:
        print(str(error))
        return redirect('index')
    level = result = None
    if (player and player.id != request.session.get('player_id')) or not player:
        request.session.flush()
        return redirect('index')
    winning_board_indices = []
    if request.method == "POST":
        context, result, board, level, winning_board_indices = GameManager.create_leaderboard(request, player)
        if result != ResultConstants.ONGOING:
            Game.objects.create(player=player, board=board, status=result)
            GameManager.update_leaderboard(player, result)
            return render(request, 'board.html', context)
    else:
        board = " " * 9

    cells = [{'index': i, 'value': board[i]} for i in range(9)]
    rows = [cells[i * 3:(i + 1) * 3] for i in range(3)]
    context = {
        'player': player,
        'board': board,
        'rows': rows,
        'level': level,
        'is_game_ongoing': result,
        'result': result,
        'winning_board_indices': winning_board_indices,
    }
    return render(request, 'board.html', context)


def leaderboard(request, player_id=None):
    if player_id and player_id != request.session.get('player_id'):
        return redirect('leaderboard')
    leaders = Leaderboard.objects.all().order_by('-wins')[:10]
    return render(request, 'leaderboard.html', {'leaders': leaders, 'player_id': player_id})

