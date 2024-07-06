import random
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseBadRequest

from users.helpers import Authentication
from .models import gameSessionModel, playerMoveModel
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class StartGameSessionView(APIView):
    authentication_classes = [Authentication]
    
    @swagger_auto_schema(manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer Token',
                required=True,
            ),
        ])
    def post(self, request):
        gameSession = gameSessionModel.objects.create(user=request.user)
        return JsonResponse({'sessionId': str(gameSession.sessionId), 'startTime': gameSession.sessionStartTime})

class RecordMoveView(APIView):


    authentication_classes = [Authentication]

    def Result(self,playerMove, computerMove):
        if playerMove == computerMove:
            return "It's a tie!"
        elif (playerMove == 'ROCK' and computerMove == 'SCISSORS') or \
             (playerMove == 'PAPER' and computerMove == 'ROCK') or \
             (playerMove == 'SCISSORS' and computerMove == 'PAPER'):
            return "Player wins"
        else:
            return "Computer wins"

    @swagger_auto_schema(manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer Token',
                required=True,
            ),
    ],request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        
        properties={
            "playerMove":openapi.Schema(type=openapi.TYPE_STRING,enum=["ROCK", "PAPER", "SCISSORS"])
        }))
    def post(self, request, session_id):
        gameSession = get_object_or_404(gameSessionModel, sessionId=session_id, user=request.user)
        playerMove = request.data['playerMove']

        if playerMove not in ['ROCK', 'PAPER', 'SCISSORS']:
            return HttpResponseBadRequest("Player Entered an Invalid Move")

        computerMove = random.choice(['ROCK', 'PAPER', 'SCISSORS'])
        gameResult = self.Result(playerMove, computerMove)

        if not playerMove or not computerMove or not gameResult:
            return HttpResponseBadRequest("Missing required fields")

        playerMoveObject = playerMoveModel.objects.create(
            gameSessionId=gameSession,
            playerMove=playerMove,
            computerMove=computerMove,
            gameResult=gameResult
        )

        return JsonResponse({
            'playerMove': playerMoveObject.playerMove,
            'computerMove': playerMoveObject.computerMove,
            'gameResult': playerMoveObject.gameResult,
            'moveRecordTime': playerMoveObject.moveRecordTime
        })

class GameHistoryView(APIView):
    authentication_classes = [Authentication]

    @swagger_auto_schema(manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer Token',
                required=True,
            ),
        ])
    def get(self, request):
        gameSession = gameSessionModel.objects.filter(user=request.user)
        history = []
        for session in gameSession:
            moves = playerMoveModel.objects.filter(gameSessionId=session)
            session_data = {
                'sessionId': str(session.sessionId),
                'startTime': session.sessionStartTime,
                'endTime': session.sessionendTime,
                'game': [{
                    'playerMove': move.playerMove,
                    'computerMove': move.computerMove,
                    'gameResult': move.gameResult,
                    'moveRecordTime': move.moveRecordTime
                } for move in moves]
            }
            history.append(session_data)
        return JsonResponse({'history': history})
