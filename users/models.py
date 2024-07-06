# Import necessary modules
from django.db import models
 
# Define the User model class
class User(models.Model):
    # User's full name, limited to 30 characters
    fullName = models.CharField(max_length=30)
    username = models.CharField(max_length=30,unique=True)
   
    # User's email address, must be unique
    email = models.EmailField(unique=True)
   
    # User's password, stored as a text field, can be null
    password = models.TextField(max_length=200, null=True, default='')


    def is_authenticated(self):
        # Return True if the user is authenticated, False otherwise
        return True 