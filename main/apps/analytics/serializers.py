from rest_framework_mongoengine import serializers
from .models import UserStream, Location

class LocationSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class UserStreamSerializer(serializers.DocumentSerializer):
    location = LocationSerializer()
    
    class Meta:
        model = UserStream
        fields = '__all__'
        read_only_fields = ('timestamp',)
        
    def create(self, validated_data):
        location_data = validated_data.pop("location", {})
        user_stream = UserStream(**validated_data)
        user_stream.location = Location(**location_data)
        user_stream.save()
        return user_stream