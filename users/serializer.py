from rest_framework import serializers

from users.models import User

class userSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','fullName','username', 'email', 'password')
