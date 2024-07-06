import uuid
from django.db import models

from users.models import User

class gameSessionModel(models.Model):
    sessionId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sessionStartTime = models.DateTimeField(auto_now_add=True)
    sessionendTime = models.DateTimeField(null=True, blank=True)


class playerMoveModel(models.Model):
    gameSessionId = models.ForeignKey(gameSessionModel, on_delete=models.CASCADE)
    playerMove = models.CharField(max_length=100)
    computerMove = models.CharField(max_length=100)
    gameResult = models.CharField(max_length=100)  # e.g., "win", "lose", "draw"
    moveRecordTime = models.DateTimeField(auto_now_add=True)