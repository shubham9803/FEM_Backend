from rest_framework import serializers
from .models import User,Family

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'fname', 'lname', 'mobile', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ['id', 'name', 'code', 'created_by']
        read_only_fields = ['code', 'created_by']


class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fname', 'lname', 'mobile', 'email']        