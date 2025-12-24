from rest_framework import serializers
from .models import Manager

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'email', 'password']
        
    def create(self, validated_data):
        manager = Manager.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        manager.set_password(validated_data['password'])
        manager.save()
        
        return manager

