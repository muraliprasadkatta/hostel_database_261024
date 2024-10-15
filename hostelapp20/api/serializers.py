
from rest_framework import serializers
from hostelapp20.models import AddProperty

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddProperty
        fields = '__all__'  # Expose all fields of the AddProperty model
