from rest_framework_mongoengine import serializers
from .models import GroupSession, QueueItem, Member

class QueueItemSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = QueueItem
        fields = '__all__'

class MemberSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class GroupSessionSerializer(serializers.DocumentSerializer):
    queue = QueueItemSerializer(many=True)
    members = MemberSerializer(many=True)
    
    class Meta:
        model = GroupSession
        fields = '__all__'
        read_only_fields = ('created_at', 'ended_at')
        
    def create(self, validated_data):
        queue_data = validated_data.pop("queue", [])  
        members_data = validated_data.pop("members", [])  

        group_session = GroupSession(**validated_data)  
        group_session.queue = [QueueItem(**item) for item in queue_data]   
        group_session.members = [Member(**item) for item in members_data] 
        group_session.save()

        return group_session
