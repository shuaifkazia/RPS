# Import necessary modules and classes
from users.helpers import Authentication
from .serializer import userSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from django.contrib.auth.hashers import make_password, check_password
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
 
 
class userViewset(APIView):
    # Handle POST request to create a new user
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "fullName":openapi.Schema(type=openapi.TYPE_STRING),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }))
    def post(self, request, format=None):
        try:  
            user=User.objects.get(email=request.data['email'])
            if user:
               return Response("User with this email already exist",409)
        except Exception:
            pass
 
     
        
       
        request.data['password'] = make_password(request.data["password"])
        current_user = User.objects.create(
            fullName=request.data["fullName"],
            username=request.data["username"],
            email=request.data["email"],
            password=make_password(request.data["password"])
        )
    
        return Response("User added Sucessfully", 201)
   
 
class loginViewset(APIView):
   
    # Handle POST request to perform user login and issue a JWT token
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }))
    def post(self, request, format=None):
        try:
            try:
                # Retrieve the current user by their username
                current_user = User.objects.get(username=request.data["username"])
                
                # Check if the provided password matches the stored hashed password
               
                if check_password(request.data["password"], current_user.password):
                    # Serialize the user data
                    serialized = userSerializer(
                        current_user, many=False
                    )
                    # Create a JWT token for the user
                    try:
                        encoded_token = jwt.encode(
                            {"user": serialized.data}, "QZTD", algorithm="HS256"
                        )
                    except Exception as e:
                        print(e)
                    # Return the JWT token as a response with status code 201 (Created)
                   
                    return Response(
                        {
                            'fullName':serialized.data['fullName'],
                            "token": encoded_token,
                            "userId":serialized.data['id']
                        },
                        201,
                    )
                else:
                    return Response("Invlaid Credentials!", 401)
            except User.DoesNotExist:
                return Response("Invlaid Credentials!", 404)
        except Exception:
            return Response("Wrong Attempt", 401) 
 
class ResetPassword(APIView):
    authentication_classes = [Authentication]

    @swagger_auto_schema(manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer Token',
                required=True,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password']
        ) # Add Bearer token security schema here
    )
    def post(self, request, format=None):
        try:  
            user = User.objects.get(username=request.data["username"].lower())
            if user:
                user.password = make_password(request.data["password"])
                user.save()
                return Response("Password Changed Successfully", 200)
            else:
                return Response("Invalid", 409)
        except Exception:
            return Response("Something Went Wrong",500)
        
 
 
