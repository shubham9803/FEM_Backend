from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = "__all__"
        read_only_fields = ['family', 'added_by', 'created_at']

    def validate(self, data):
        user = self.context['request'].user

        if not user.family:
            raise serializers.ValidationError(
                "You must join a family before adding expenses."
            )

        return data

    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['family'] = user.family
        validated_data['added_by'] = user

        return super().create(validated_data)