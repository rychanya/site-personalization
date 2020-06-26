from django.db import models


class Player(models.Model):
    def __str__(self):
        return f'<Player {self.id}>'
    


class Game(models.Model):
    number = models.IntegerField()
    is_solve = models.BooleanField(default=False)
    creater = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='creater')
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='winner', blank=True, null=True)

    def __str__(self):
        return f'<Game {self.id} - number {self.number}>'
    


class PlayerGameInfo(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    attempts_count = models.IntegerField(default=0)
    
    
