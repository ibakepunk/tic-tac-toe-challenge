from django.db import models
from django.contrib.postgres.fields import JSONField


class Game(models.Model):
    IN_PROGRESS = 'in_progress'
    DRAW = 'draw'
    X_WON = 'x'
    O_WON = 'o'
    STATUSES = (
        (IN_PROGRESS, 'Still playing'), 
        (DRAW, 'Finished as a draw'), 
        (X_WON, 'Player X won'), 
        (O_WON, 'Player O won'),
    )

    finished = models.BooleanField(default=False)
    status = models.CharField(choices=STATUSES, max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=140)
    x_player = models.CharField(max_length=140)
    o_player = models.CharField(max_length=140)
    board = JSONField()

    class Meta:
        app_label = 'game'
