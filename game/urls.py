# Import the necessary modules for defining Django URLs and including views
from django.urls import path
 
# Import the viewsets for the game related views
from .views import GameHistoryView, RecordMoveView, StartGameSessionView

# Define the urlpatterns for the game endpoints
urlpatterns = [
    # endpoint to start a game session
    path('start-game-session/', StartGameSessionView.as_view()),
    # endpoint to record a game 
    path('record-player-move/<uuid:session_id>/', RecordMoveView.as_view()),
    # endpoint to fech user history
    path('user-game-history/', GameHistoryView.as_view()),
]