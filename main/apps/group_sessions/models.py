from mongoengine import Document, EmbeddedDocument, fields
from django.conf import settings
import datetime

class QueueItem(EmbeddedDocument):
    """Embedded document for music in the queue"""
    track_id = fields.StringField(required=True)
    track_name = fields.StringField(required=True)
    artist = fields.StringField(required=True)
    thumbnail = fields.StringField()  # URL to thumbnail

class Member(EmbeddedDocument):
    """Embedded document for session members"""
    user_id = fields.StringField(required=True)

class GroupSession(Document):
    """Group listening session document"""
    host_user_id = fields.StringField(required=True)
    session_code = fields.StringField(unique=True, max_length=10)
    status = fields.StringField(choices=('active', 'ended'), default='active')
    is_active = fields.BooleanField(default=True)
    queue = fields.EmbeddedDocumentListField(QueueItem, default=[])
    members = fields.EmbeddedDocumentListField(Member, default=[])
    created_at = fields.DateTimeField(default=datetime.datetime.now)
    ended_at = fields.DateTimeField()
    
    meta = {
        'collection': 'group_sessions',
        'indexes': [
            'host_user_id',
            'session_code',
            {'fields': ['created_at'], 'expireAfterSeconds': 86400}  # Optional: auto-expire after 24h
        ]
    }