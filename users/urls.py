# Import the necessary modules for defining Django URLs and including views
from django.urls import path
 
# Import the viewsets for the user and authentication related views
from .views import ResetPassword, loginViewset, userViewset
# Define the urlpatterns for the authentication and user-related endpoints
urlpatterns = [
    # URL for creating user-related data using userViewset
    path(
        "register/",  # The URL path for user-related data
        userViewset.as_view(),    # The view handling POST (create) requests
    ),
    # URL for user authentication and login using loginViewset
    path(
        "login/",  # The URL path for user authentication and login
        loginViewset.as_view(),   # The view handling the login process
    ),
    # URL for user password reset
    path(
        "resetpassword/",  
        ResetPassword.as_view(),   
    ),
 
]