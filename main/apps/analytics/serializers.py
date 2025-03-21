# from rest_framework_mongoengine import serializers
# from .models import UserStream, Location

# class LocationSerializer(serializers.EmbeddedDocumentSerializer):
#     class Meta:
#         model = Location
#         fields = '__all__'

# class UserStreamSerializer(serializers.DocumentSerializer):
#     location = LocationSerializer()
    
#     class Meta:
#         model = UserStream
#         fields = '__all__'