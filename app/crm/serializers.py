from rest_framework import serializers
from .models import Company, Storage

class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Company
        fields = ['id', 'name', 'owner']

    def create(self, validated_data):
        user = self.context['request'].user
        if Company.objects.filter(owner=user).exists():
            raise serializers.ValidationError("У вас уже есть созданная компания.")
        return Company.objects.create(owner=user, **validated_data)

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['id', 'name', 'company']
        read_only_fields = ['company']
