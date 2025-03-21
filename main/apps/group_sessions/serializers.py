# from rest_framework_mongoengine import serializers
# from .models import GroupSession, QueueItem, SessionMember

# class QueueItemSerializer(serializers.EmbeddedDocumentSerializer):
#     class Meta:
#         model = QueueItem
#         fields = '__all__'

# class SessionMemberSerializer(serializers.EmbeddedDocumentSerializer):
#     class Meta:
#         model = SessionMember
#         fields = '__all__'

# class GroupSessionSerializer(serializers.DocumentSerializer):
#     queue = QueueItemSerializer(many=True)
#     members = SessionMemberSerializer(many=True)
    
#     class Meta:
#         model = GroupSession
#         fields = '__all__'