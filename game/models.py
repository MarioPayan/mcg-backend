from django.db import models


class Game(models.Model):
    player_1 = models.CharField(
        max_length=80,
        null=False,
        blank=False
    )
    player_2 = models.CharField(
        max_length=80,
        null=False,
        blank=False
    )
    room_name = models.CharField(
        max_length=80,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.room_name


class Movement(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT
    )
    player_id = models.IntegerField()
    row = models.IntegerField()
    side = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )
    winner = models.IntegerField()

    class Meta:
        unique_together = ('id', 'game')

    def __str__(self):
        return f'{self.game}: ({self.player_id},{self.row},{self.side})'
