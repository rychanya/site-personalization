from django.shortcuts import render, redirect
from game.models import Player, Game, PlayerGameInfo
from django.core.exceptions import ObjectDoesNotExist
from random import choice
from .forms import NumberForm

def reset(request):
    if 'message' in request.session:
        del request.session['message']
    if 'win_number' in request.session:
        del request.session['win_number']
    if 'game_id' in request.session:
        del request.session['game_id']
    return redirect('/')
    

def show_home(request):
    message = request.session.get('message')
    win_number = request.session.get('win_number')
    if 'message' in request.session:
        del request.session['message']
    if 'win_number' in request.session:
        del request.session['win_number']
    if message and win_number:
        return render(
            request,
            'home.html',
            {
                'number': win_number,
                'message': message
            }
        )
    
    try:
        player_id = int(request.session.get('player_id'))
        player = Player.objects.get(pk=player_id)
    except (TypeError, ObjectDoesNotExist):
        player = Player.objects.create()
        request.session['player_id'] = player.id

    try:
        game_id = int(request.session.get('game_id'))
        game = Game.objects.get(pk=game_id)
    except (TypeError, ObjectDoesNotExist):
        game = Game.objects.filter(is_solve=False).first()
        if not game:
            game = Game.objects.create(creater=player, number=choice(range(100)))
            request.session['game_id'] = game.id

    if request.method == 'POST':
        form = NumberForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            try:
                info = PlayerGameInfo.objects.get(game=game, player=player)
            except ObjectDoesNotExist:
                info = PlayerGameInfo.objects.create(game=game, player=player)
            info.attempts_count += 1
            info.save()
            if number == game.number:
                game.winner = player
                game.is_solve = True
                game.save()
                request.session['win_number'] = game.number
                message = 'Вы угадали загаданное число!'
            elif number < game.number:
                message = 'Введенное число меньше угадываемого.'
            else:
                message = 'Введенное число больше угадываемого.'
            request.session['message'] = message
            return redirect('/')
    else:
        form = NumberForm()

    if game.creater == player:
        info = PlayerGameInfo.objects.filter(game=game).order_by('attempts_count').first()
        context = {
            'number': game.number,
            # 'message': message
            'counter': info.attempts_count if info else None,
            'is_solve': game.is_solve
        }
    else:
        context = {
            'form': form,
            'message': message
        }


    return render(
        request,
        'home.html',
        context=context
    )
